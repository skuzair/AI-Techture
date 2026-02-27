import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class ClimateZoning:

    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=n_clusters, random_state=42)

    def fit(self, climate_features):
        scaled = self.scaler.fit_transform(climate_features)
        zones = self.model.fit_predict(scaled)
        return zones

    def predict(self, point_features):
        scaled_point = self.scaler.transform([point_features])
        return self.model.predict(scaled_point)[0]