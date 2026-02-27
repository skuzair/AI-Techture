import numpy as np
from aitechture.data_pipeline.spatial_aggregation import aggregate_spatial_risk


# ----------------------------
# Utility
# ----------------------------

def smooth_compress(x, factor=0.3):
    return x / (1 + factor * x)


def percentile(value, distribution):
    return np.sum(distribution <= value) / len(distribution)


# ----------------------------
# Seismic
# ----------------------------

def seismic_risk(lat, lon, earthquake_df, seismic_distribution):

    seismic_values = (
        earthquake_df["Energy_Index"].values
        * earthquake_df["Depth_Factor"].values
    )

    temp_df = earthquake_df.copy()
    temp_df["Seismic_Contribution"] = seismic_values

    raw = aggregate_spatial_risk(
        lat, lon, temp_df, "Seismic_Contribution"
    )

    raw = np.log1p(raw)

    base = percentile(raw, seismic_distribution)

    # Himalayan & NE boost
    if lat > 30 or (lat > 26 and lon > 85):
        base *= 1.1

    return smooth_compress(base)


# ----------------------------
# Heatwave
# ----------------------------

def heatwave_risk(lat, lon, local_row, heat_distribution):

    temp = local_row["Temperature_C"]
    humidity = local_row["Humidity_pct"]

    heat_raw = temp + 0.33 * humidity

    base = percentile(heat_raw, heat_distribution)

    # Desert boost
    if 23 <= lat <= 29 and lon < 75:
        base *= 1.15

    # Himalayan cooling
    if lat > 30:
        base *= 0.6

    return smooth_compress(base)


# ----------------------------
# Flood
# ----------------------------

def flood_raw_score(local_row):

    rain = local_row["Rainfall_mm"]
    discharge = local_row["River_Discharge"]
    water = local_row["Water_Level"]
    elevation = local_row["Elevation_m"]

    return (rain * water * np.log1p(discharge)) / (elevation + 50)


def flood_risk(lat, lon, local_row, flood_distribution):

    rain = local_row["Rainfall_mm"]
    discharge = local_row["River_Discharge"]
    water = local_row["Water_Level"]
    elevation = local_row["Elevation_m"]

    # Base physics
    raw = (rain * water * np.log1p(discharge)) / (elevation + 100)

    base = percentile(raw, flood_distribution)

    # ------------------------------
    # Geographic Overrides (Dynamic)
    # ------------------------------

    # 1️⃣ High elevation clamp (mountain regions)
    if elevation > 1500:
        base = min(base, 0.25)

    # 2️⃣ Desert belt suppression (Rajasthan)
    if 23 <= lat <= 29 and lon < 75:
        base *= 0.5

    # Clamp latitude to Indian mainland bounds
    lat = max(8, min(lat, 30))

    # 3️⃣ Dynamic West Coast Proximity
    # West coast shifts from ~73E (north) to ~76.5E (south) with smooth curvature
    west_coast_lon = 73 + ((30 - lat) / 22) * 3.5 + 0.01 * (30 - lat)**2
    if lon <= west_coast_lon + 0.7:
        base *= 2.5

    # 4️⃣ Dynamic East Coast Proximity
    # East coast shifts from ~88E (north) to ~78.5E (south) with smooth curvature
    east_coast_lon = 88 - ((30 - lat) / 22) * 9.5 - 0.008 * (30 - lat)**2
    if lon >= east_coast_lon - 0.7:
        base *= 1.5

    # 5️⃣ Western Ghats enhancement
    if 8 <= lat <= 20 and abs(lon - west_coast_lon) < 1.0:
        base *= 1.2

    return base


# ----------------------------
# Landslide
# ----------------------------

def landslide_risk(lat, lon, landslide_df):

    idx = (
        (landslide_df["Latitude"] - lat) ** 2
        + (landslide_df["Longitude"] - lon) ** 2
    ).idxmin()

    base = landslide_df.loc[idx, "Base_Landslide_Risk"]

    # Himalayan strong boost
    if lat > 30 or (lat > 26 and lon > 85):
        base *= 1.4

    # Western Ghats moderate boost
    if 8 <= lat <= 20 and 72 <= lon <= 76:
        base *= 1.2

    return smooth_compress(base)