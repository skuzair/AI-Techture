import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "src"))

from aitechture.core.risk_engine import RiskEngine

engine = RiskEngine()

def evaluate_location(lat, lon):
    return engine.evaluate(lat, lon)

if __name__ == "__main__":
    lat = float(input("Enter Latitude: "))
    lon = float(input("Enter Longitude: "))

    result = evaluate_location(lat, lon)

    print("=== Multi-Hazard Risk Assessment ===")
    print(f"Location: ({lat}, {lon})")

    print(f"Seismic Risk     : {result['Seismic_Risk']:.3f}")
    print(f"Flood Risk       : {result['Flood_Risk']:.3f}")
    print(f"Heatwave Risk    : {result['Heatwave_Risk']:.3f}")
    print(f"Landslide Risk   : {result['Landslide_Risk']:.3f}")

    print("\nTop Recommended Materials:")
    print(result["Top_Materials"][["Material", "Suitability_Score"]])

    print("\n=== Architectural Design Recommendations ===")

    design = result["Design_Recommendations"]

    print("Primary Hazard Driver:", design["Primary_Hazard_Driver"])
    print("Design Strength Index:", round(design["Design_Strength_Index"], 3))

    final_design = design["Final_Integrated_Design"]

    print("\nStructural System:")
    print(final_design["Structural"])

    print("\nFoundation System:")
    print(final_design["Foundation"])

    print("\nRoof System:")
    print(final_design["Roof"])

    print("\nWindow System:")
    print(final_design["Window"])