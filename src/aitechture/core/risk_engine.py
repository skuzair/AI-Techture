import numpy as np

from aitechture.data_pipeline.data_loader import *
from aitechture.data_pipeline.preprocessing import *
from aitechture.core.climate_zoning import ClimateZoning
from aitechture.core.hazard_models import *
from aitechture.core.material_optimizer import *
from aitechture.core.design_engine import DesignEngine


class RiskEngine:

    def __init__(self):

        self.compiled = load_compiled()
        self.earthquake = load_earthquake()
        self.landslide = load_landslide()
        self.materials = load_materials()

        
        self.design_engine = DesignEngine()

        # ---- Climate Zoning ----
        zoning_features = build_climate_zoning_features(self.compiled)
        self.zoning = ClimateZoning(n_clusters=5)
        self.zones = self.zoning.fit(zoning_features)

        # --------------------------------------------------
        # Precompute Seismic Distribution
        # --------------------------------------------------

        self.seismic_distribution = []

        seismic_values = (
            self.earthquake["Energy_Index"].values
            * self.earthquake["Depth_Factor"].values
        )

        temp_df = self.earthquake.copy()
        temp_df["Seismic_Contribution"] = seismic_values

        for _, row in self.compiled.iterrows():

            raw = aggregate_spatial_risk(
                row["Latitude"],
                row["Longitude"],
                temp_df,
                "Seismic_Contribution"
            )

            self.seismic_distribution.append(np.log1p(raw))

        self.seismic_distribution = np.array(self.seismic_distribution)

        # --------------------------------------------------
        # Precompute Heat Distribution
        # --------------------------------------------------

        self.heat_distribution = []

        for _, row in self.compiled.iterrows():
            heat_raw = row["Temperature_C"] + 0.33 * row["Humidity_pct"]
            self.heat_distribution.append(heat_raw)

        self.heat_distribution = np.array(self.heat_distribution)

        # --------------------------------------------------
        # Precompute Flood Distribution
        # --------------------------------------------------

        self.flood_distribution = []

        for _, row in self.compiled.iterrows():
            raw = flood_raw_score(row)
            self.flood_distribution.append(raw)

        self.flood_distribution = np.array(self.flood_distribution)

    # ------------------------------------------------------

    def _nearest_row(self, lat, lon):
        idx = (
            (self.compiled["Latitude"] - lat) ** 2
            + (self.compiled["Longitude"] - lon) ** 2
        ).idxmin()
        return self.compiled.loc[idx]

    # ------------------------------------------------------

    def evaluate(self, lat, lon):

        local_row = self._nearest_row(lat, lon)

        # ---- Seismic ----
        s_risk = seismic_risk(
            lat,
            lon,
            self.earthquake,
            self.seismic_distribution
        )

        # ---- Flood ----
        f_risk = flood_risk(
            lat,
            lon,
            local_row,
            self.flood_distribution
        )

        # ---- Heatwave ----
        h_risk = heatwave_risk(
            lat,
            lon,
            local_row,
            self.heat_distribution
        )

        # ---- Landslide ----
        l_risk = landslide_risk(
            lat,
            lon,
            self.landslide
        )

        risk_vector = np.array([
            s_risk,
            f_risk,
            h_risk,
            0.5,
            l_risk
        ])

        ranked = rank_materials(self.materials, risk_vector)

        # ✅ NEW DESIGN ENGINE CALL
        design = self.design_engine.generate_design(
            seismic=s_risk,
            flood=f_risk,
            heatwave=h_risk,
            landslide=l_risk,
            soil_type=local_row["Soil Type"],
            elevation=local_row["Elevation_m"],
            rainfall=local_row["Rainfall_mm"],
            temperature=local_row["Temperature_C"]
        )

        return {
            "Seismic_Risk": float(s_risk),
            "Flood_Risk": float(f_risk),
            "Heatwave_Risk": float(h_risk),
            "Landslide_Risk": float(l_risk),
            "Top_Materials": ranked.head(5),
            "Design_Recommendations": design   # ✅ NEW
        }