import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from flask import Flask, request
from run import evaluate_location

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Disaster Risk Intelligence</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .card {
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(20px);
                padding: 40px;
                border-radius: 20px;
                width: 400px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.5);
                text-align: center;
            }
            h1 {
                margin-bottom: 30px;
                font-weight: 600;
            }
            input {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border-radius: 10px;
                border: none;
                outline: none;
                font-size: 15px;
            }
            button {
                width: 100%;
                padding: 12px;
                margin-top: 15px;
                border-radius: 10px;
                border: none;
                background: #00c6ff;
                background: linear-gradient(to right, #0072ff, #00c6ff);
                color: white;
                font-size: 16px;
                cursor: pointer;
                transition: 0.3s;
            }
            button:hover {
                transform: scale(1.05);
                box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🌍 Multi-Hazard Risk Engine</h1>
            <form action="/evaluate" method="post">
                <input type="text" name="lat" placeholder="Enter Latitude" required>
                <input type="text" name="lon" placeholder="Enter Longitude" required>
                <button type="submit">Evaluate Risk</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route("/evaluate", methods=["POST"])
def evaluate():
    lat = float(request.form["lat"])
    lon = float(request.form["lon"])

    result = evaluate_location(lat, lon)
    design = result["Design_Recommendations"]
    materials = result["Top_Materials"].head(5)

    hazard_core = design["Hazard_Driven_Design"]
    climate_adj = design["Climate_Adjustments"]
    soil_adj = design["Soil_Adjustments"]
    final_design = design["Final_Integrated_Design"]

    # Build climate HTML dynamically
    climate_html = ""
    for category, values in climate_adj.items():
        climate_html += f"""
        <div class="card">
            <div class="title">{category} Adjustment</div>
            <div><b>Structural:</b> {values['Structural']}</div>
            <div><b>Foundation:</b> {values['Foundation']}</div>
            <div><b>Roof:</b> {values['Roof']}</div>
            <div><b>Window:</b> {values['Window']}</div>
        </div>
        """

    # Build soil HTML dynamically
    soil_html = ""
    for key, value in soil_adj.items():
        soil_html += f"""
        <div class="card">
            <div class="title">{key} (Soil Influence)</div>
            <div>{value}</div>
        </div>
        """
    materials_html = ""
    for _, row in materials.iterrows():
        materials_html += f"""
        <div class="card">
            <div class="title">{row['Material']}</div>
            <div class="value">{row['Suitability_Score']:.3f}</div>
        </div>
        """

    return f"""
    <html>
    <head>
        <title>Risk Report</title>
        <style>
            body {{
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: #0f2027;
                color: white;
                padding: 40px;
            }}
            h1 {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
            }}
            .card {{
                background: rgba(255,255,255,0.05);
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.4);
                transition: 0.3s;
            }}
            .card:hover {{
                transform: translateY(-5px);
            }}
            .title {{
                font-weight: bold;
                margin-bottom: 10px;
                font-size: 18px;
            }}
            .value {{
                font-size: 22px;
                color: #00c6ff;
            }}
            .section {{
                margin-top: 40px;
            }}
            a {{
                color: #00c6ff;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>

        <h1>📊 Risk Intelligence Report</h1>

        <div class="grid">
            <div class="card">
                <div class="title">Seismic Risk</div>
                <div class="value">{result['Seismic_Risk']:.3f}</div>
            </div>
            <div class="card">
                <div class="title">Flood Risk</div>
                <div class="value">{result['Flood_Risk']:.3f}</div>
            </div>
            <div class="card">
                <div class="title">Heatwave Risk</div>
                <div class="value">{result['Heatwave_Risk']:.3f}</div>
            </div>
            <div class="card">
                <div class="title">Landslide Risk</div>
                <div class="value">{result['Landslide_Risk']:.3f}</div>
            </div>
        </div>

        <div class="section">
            <h2>⚠ Primary Hazard</h2>
            <div class="card">
                <div class="value">{design['Primary_Hazard_Driver']}</div>
            </div>
        </div>

        <div class="section">
            <h2>🧱 Top Material Recommendations</h2>
            <div class="grid">
                {materials_html}
            </div>
        </div>

        <div class="section">
            <h2>🏗 Hazard-Driven Core Design</h2>
            <div class="grid">
                <div class="card"><b>Structural:</b><br>{hazard_core['Structural']}</div>
                <div class="card"><b>Foundation:</b><br>{hazard_core['Foundation']}</div>
                <div class="card"><b>Roof:</b><br>{hazard_core['Roof']}</div>
                <div class="card"><b>Window:</b><br>{hazard_core['Window']}</div>
            </div>
        </div>

        <div class="section">
            <h2>🌦 Climate-Based Adjustments</h2>
            <div class="grid">
                {climate_html}
            </div>
        </div>

        <div class="section">
            <h2>🌍 Soil-Based Adjustments</h2>
            <div class="grid">
                {soil_html}
            </div>
        </div>

        

        <br><br>
        <center><a href="/">← Analyze Another Location</a></center>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)