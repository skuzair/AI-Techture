from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"

import numpy as np
import pandas as pd


class DesignEngine:

    def __init__(self,
             hazard_rules_path=DATA_DIR / "hazard_rules_advanced.csv",
             soil_rules_path=DATA_DIR / "soil_rules_advanced.csv",
             climate_rules_path=DATA_DIR / "climate_rules_advanced.csv"):

        self.hazard_rules = pd.read_csv(hazard_rules_path)
        self.soil_rules = pd.read_csv(soil_rules_path)
        self.climate_rules = pd.read_csv(climate_rules_path)

    # --------------------------------------------------
    # Helper
    # --------------------------------------------------

    def _normalize_scores(self, scores):
        total = sum(scores.values()) + 1e-8
        return {k: v / total for k, v in scores.items()}

    # --------------------------------------------------
    # Core Design Evaluation
    # --------------------------------------------------

    def generate_design(self,
                    seismic,
                    flood,
                    heatwave,
                    landslide,
                    soil_type,
                    elevation,
                    rainfall,
                    temperature):

        hazard_vector = {
            "Earthquake": seismic,
            "Flood": flood,
            "Heatwave": heatwave,
            "Landslide": landslide,
        }

        structural_score = 0
        foundation_score = 0
        roof_score = 0
        window_score = 0

        structural_votes = {}
        foundation_votes = {}
        roof_votes = {}
        window_votes = {}

        # ---------------------------
        # Hazard Voting (Core Layer)
        # ---------------------------

        for hazard, intensity in hazard_vector.items():

            row = self.hazard_rules[
                self.hazard_rules["Hazard"] == hazard
            ]

            if row.empty:
                continue

            row = row.iloc[0]

            structural_weight = intensity * row["Structural_Weight"]
            foundation_weight = intensity * row["Foundation_Weight"]
            roof_weight = intensity * row["Roof_Weight"]
            window_weight = intensity * row["Window_Weight"]

            structural_score += structural_weight
            foundation_score += foundation_weight
            roof_score += roof_weight
            window_score += window_weight

            structural_votes[row["Structural_Recommendation"]] = \
                structural_votes.get(row["Structural_Recommendation"], 0) + structural_weight

            foundation_votes[row["Foundation_Recommendation"]] = \
                foundation_votes.get(row["Foundation_Recommendation"], 0) + foundation_weight

            roof_votes[row["Roof_Recommendation"]] = \
                roof_votes.get(row["Roof_Recommendation"], 0) + roof_weight

            window_votes[row["Window_Recommendation"]] = \
                window_votes.get(row["Window_Recommendation"], 0) + window_weight

        # Capture hazard-only winners
        hazard_structural = max(structural_votes, key=structural_votes.get)
        hazard_foundation = max(foundation_votes, key=foundation_votes.get)
        hazard_roof = max(roof_votes, key=roof_votes.get)
        hazard_window = max(window_votes, key=window_votes.get)

        # ---------------------------
        # Soil Influence Layer
        # ---------------------------

        soil_adjustments = {}

        soil_row = self.soil_rules[
            self.soil_rules["Soil_Type"] == soil_type
        ]

        if not soil_row.empty:
            soil_row = soil_row.iloc[0]

            structural_score *= soil_row["Structural_Weight"]
            foundation_score *= soil_row["Foundation_Weight"]

            soil_adjustments["Structural"] = soil_row["Structural_Recommendation"]
            soil_adjustments["Foundation"] = soil_row["Foundation_Recommendation"]

            structural_votes[soil_row["Structural_Recommendation"]] = \
                structural_votes.get(soil_row["Structural_Recommendation"], 0) + structural_score * 0.3

            foundation_votes[soil_row["Foundation_Recommendation"]] = \
                foundation_votes.get(soil_row["Foundation_Recommendation"], 0) + foundation_score * 0.3

        # ---------------------------
        # Climate Categorization Layer
        # ---------------------------

        elevation_cat = "High" if elevation > 1500 else \
                        "Mid" if elevation > 500 else "Low"

        rain_cat = "High" if rainfall > 2500 else \
                "Mid" if rainfall > 1000 else "Low"

        weather_cat = "Hot" if temperature > 32 else \
                    "Cold" if temperature < 12 else "Moderate"

        climate_adjustments = {}

        for category, level in [
            ("Elevation", elevation_cat),
            ("Precipitation", rain_cat),
            ("Weather", weather_cat)
        ]:

            row = self.climate_rules[
                (self.climate_rules["Category"] == category) &
                (self.climate_rules["Severity_Level"] == level)
            ]

            if row.empty:
                continue

            row = row.iloc[0]

            climate_factor = 0.35

            structural_score += row["Structural_Weight"] * climate_factor
            foundation_score += row["Foundation_Weight"] * climate_factor
            roof_score += row["Roof_Weight"] * climate_factor
            window_score += row["Window_Weight"] * climate_factor

            climate_adjustments[category] = {
                "Structural": row["Structural_Recommendation"],
                "Foundation": row["Foundation_Recommendation"],
                "Roof": row["Roof_Recommendation"],
                "Window": row["Window_Recommendation"]
            }

            structural_votes[row["Structural_Recommendation"]] = \
                structural_votes.get(row["Structural_Recommendation"], 0) + row["Structural_Weight"] * climate_factor

            foundation_votes[row["Foundation_Recommendation"]] = \
                foundation_votes.get(row["Foundation_Recommendation"], 0) + row["Foundation_Weight"] * climate_factor

            roof_votes[row["Roof_Recommendation"]] = \
                roof_votes.get(row["Roof_Recommendation"], 0) + row["Roof_Weight"] * climate_factor

            window_votes[row["Window_Recommendation"]] = \
                window_votes.get(row["Window_Recommendation"], 0) + row["Window_Weight"] * climate_factor

        # ---------------------------
        # Final Integrated Selection
        # ---------------------------

        structural_choice = max(structural_votes, key=structural_votes.get)
        foundation_choice = max(foundation_votes, key=foundation_votes.get)
        roof_choice = max(roof_votes, key=roof_votes.get)
        window_choice = max(window_votes, key=window_votes.get)

        hazard_dominance = max(hazard_vector, key=hazard_vector.get)

        total_score = np.mean([
            structural_score,
            foundation_score,
            roof_score,
            window_score
        ])

        return {
            "Primary_Hazard_Driver": hazard_dominance,

            "Hazard_Driven_Design": {
                "Structural": hazard_structural,
                "Foundation": hazard_foundation,
                "Roof": hazard_roof,
                "Window": hazard_window
            },

            "Climate_Adjustments": climate_adjustments,
            "Soil_Adjustments": soil_adjustments,

            "Final_Integrated_Design": {
                "Structural": structural_choice,
                "Foundation": foundation_choice,
                "Roof": roof_choice,
                "Window": window_choice
            },

            "Design_Strength_Index": round(float(total_score), 3)
        }