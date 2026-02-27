import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"


def _load_csv(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df


def load_compiled(path=DATA_DIR / "compiled_clean.csv"):
    df = _load_csv(path)

    numeric_cols = [
        "Latitude",
        "Longitude",
        "Rainfall_mm",
        "Temperature_C",
        "Humidity_pct",
        "River_Discharge",
        "Water_Level",
        "Elevation_m",
        "Population_Density",
        "Infrastructure",
        "Historical_Floods",
        "Flood_Occurred",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()
    return df


def load_earthquake(path=DATA_DIR / "earthquake_clean.csv"):
    df = _load_csv(path)

    numeric_cols = [
        "Latitude",
        "Longitude",
        "Depth",
        "Magnitude",
        "Energy_Index",
        "Depth_Factor",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()
    return df


def load_landslide(path=DATA_DIR / "landslide_clean.csv"):
    df = _load_csv(path)

    numeric_cols = [
        "Latitude",
        "Longitude",
        "Rainfall_Norm",
        "Elevation_Norm",
        "Erosion_Norm",
        "EQ_Freq_Norm",
        "Mining Activity",
        "Historical_Landslide_Norm",
        "Base_Landslide_Risk",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()
    return df


def load_materials(path=DATA_DIR / "materials_clean.csv"):
    df = _load_csv(path)
    return df


def load_climate_rules(path=DATA_DIR / "climate_rules_advanced.csv"):
    return _load_csv(path)


def load_hazard_rules(path=DATA_DIR / "hazard_rules_advanced.csv"):
    return _load_csv(path)


def load_soil_rules(path=DATA_DIR / "soil_rules_advanced.csv"):
    return _load_csv(path)