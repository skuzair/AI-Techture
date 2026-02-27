import numpy as np


def rank_materials(material_df, risk_vector):

    hazard_cols = [
        "Res_Earthquake",
        "Res_Flood",
        "Res_Heatwave",
        "Res_Cyclone",
        "Res_Landslide",
    ]

    materials = material_df.copy()

    material_matrix = materials[hazard_cols].values.astype(float)

    scores = material_matrix @ risk_vector

    materials["Suitability_Score"] = scores

    return materials.sort_values("Suitability_Score", ascending=False)