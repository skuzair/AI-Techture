import numpy as np


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c


def aggregate_spatial_risk(lat, lon, df, value_column, radius_km=300):

    lat_array = df["Latitude"].values
    lon_array = df["Longitude"].values
    values = df[value_column].values

    distances = haversine_distance(lat, lon, lat_array, lon_array)

    mask = distances <= radius_km

    filtered_distances = distances[mask]
    filtered_values = values[mask]

    if len(filtered_values) == 0:
        return 0.0

    attenuation = 1 / (1 + (filtered_distances / 50) ** 2)

    return np.sum(filtered_values * attenuation)