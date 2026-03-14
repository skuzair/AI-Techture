# 🏗️ AI-Techture

### AI-Driven Multi-Hazard Risk Intelligence & Climate-Adaptive Architecture Engine

**Version:** v1.0.0\
**Project Type:** Hackathon-Grade Applied AI System

------------------------------------------------------------------------

## 📌 Overview

AI-Techture is a hybrid decision-intelligence platform that evaluates
location-specific environmental hazards and generates adaptive
architectural and material recommendations.

The system integrates:

-   🌍 10,000+ geospatial environmental data points\
-   🌋 2,000+ earthquake records (energy + depth modeling)\
-   🌧 3,000+ landslide susceptibility records\
-   🧱 Structured hazard, climate, and soil design rules

Unlike purely statistical ML systems, AI-Techture combines:

-   Physics-informed hazard modeling\
-   Geodesic spatial attenuation\
-   Percentile-based normalization\
-   Multi-hazard weighted decision synthesis\
-   Rule-weighted architectural intelligence

The result is a geographically realistic, engineering-aware climate
adaptation engine.

------------------------------------------------------------------------

## 🧠 System Architecture

AI-Techture consists of three intelligence layers:

### 1️⃣ Hazard Intelligence Engine (Predictive Layer)

Computes normalized risk scores:

-   Seismic Risk (energy × depth modeling)\
-   Flood Risk (hydraulic approximation + terrain scaling)\
-   Heatwave Risk (heat stress modeling)\
-   Landslide Risk (susceptibility blending)

Enhancements include:

-   Himalayan seismic amplification\
-   Western Ghats landslide enhancement\
-   Coastal flood scaling\
-   Desert flood suppression\
-   Elevation-based dampening

All outputs are normalized to: **\[0.0 -- 1.0\]**

------------------------------------------------------------------------

### 2️⃣ Material Optimization Engine

Ranks construction materials using:

-   Multi-hazard resilience vectors\
-   Weighted risk dot-product scoring\
-   Performance-normalized suitability index

------------------------------------------------------------------------

### 3️⃣ Architectural Design Engine (Prescriptive Layer)

Blends:

-   Hazard dominance detection\
-   Soil-type structural influence\
-   Climate severity categorization\
-   Multi-hazard voting & conflict resolution\
-   Design Strength Index computation

Outputs:

-   Structural system recommendation\
-   Foundation system strategy\
-   Roof system\
-   Window / ventilation strategy\
-   Primary hazard driver\
-   Integrated design strength index

------------------------------------------------------------------------

## 📊 Sample Risk Intelligence Report

    Seismic Risk      : 0.763
    Flood Risk        : 0.154
    Heatwave Risk     : 0.331
    Landslide Risk    : 0.526

    Primary Hazard    : Earthquake

    Top Material Recommendations:
    - Recycled Steel
    - Bamboo
    - High Performance Concrete (HPC)
    - Cross-Laminated Timber (CLT)
    - Concrete

    Hazard-Driven Core Design:
    Structural : Flexible reinforced frame with base isolation
    Foundation : Deep pile foundation with seismic joints
    Roof       : Lightweight roofing to reduce mass
    Window     : Shatter-resistant emergency egress windows

------------------------------------------------------------------------

## 🗂️ Folder Structure

    AI-Techture/
    │
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    ├── run.py
    │
    ├── data/
    │   ├── climate_rules_advanced.csv
    │   ├── compiled_clean.csv          (~10,000 rows)
    │   ├── earthquake_clean.csv        (~2,000 rows)
    │   ├── hazard_rules_advanced.csv
    │   ├── landslide_clean.csv         (~3,000 rows)
    │   ├── materials_clean.csv
    │   └── soil_rules_advanced.csv
    │
    └── src/
        └── aitechture/
            ├── api/
            │   └── app.py
            │
            ├── core/
            │   ├── climate_zoning.py
            │   ├── design_engine.py
            │   ├── hazard_models.py
            │   ├── material_optimizer.py
            │   └── risk_engine.py
            │
            └── data_pipeline/
                ├── data_loader.py
                ├── preprocessing.py
                └── spatial_aggregation.py

------------------------------------------------------------------------

## 🚀 Running the Application

### Setup

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

### Run CLI

    python run.py

### Run Web Interface

    python src/aitechture/api/app.py

Then open: http://127.0.0.1:5000

------------------------------------------------------------------------

## 🎯 Key Highlights

-   Multi-hazard unified evaluation framework\
-   Physics-informed flood and seismic modeling\
-   Geodesic spatial attenuation\
-   Soil-aware structural adjustments\
-   Climate-adaptive architecture synthesis\
-   Modular layered architecture

------------------------------------------------------------------------

## 📄 License

MIT License

------------------------------------------------------------------------

## 👨‍💻 Author

Uzair Shaikh\
Computer Science & Engineering\
AI \| Climate Risk Modeling \| Applied Decision Intelligence
