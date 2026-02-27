import numpy as np
import pandas as pd


def build_climate_zoning_features(df):
    return df[
        [
            "Rainfall_mm",
            "Temperature_C",
            "Humidity_pct",
            "Elevation_m",
        ]
    ].copy()


def build_flood_features(df):
    return df[
        [
            "Rainfall_mm",
            "River_Discharge",
            "Water_Level",
            "Elevation_m",
            "Historical_Floods",
        ]
    ].copy()


def build_heatwave_features(df):
    return df[
        [
            "Temperature_C",
            "Humidity_pct",
            "Elevation_m",
        ]
    ].copy()


def percentile(value, distribution):
    return np.sum(distribution <= value) / len(distribution)


def minmax_scale(series):
    return (series - series.min()) / (series.max() - series.min() + 1e-8)