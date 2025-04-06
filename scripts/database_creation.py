import sqlite3
import pandas as pd
import os

# ---------- Common Utility ----------
def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

# ---------- Farmer Advisor DB Setup ----------
def setup_farmer_advisor_db(csv_path="/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/farmer_advisor_dataset.csv",
                             db_path="/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/farmer_advisor.db"):
    df = pd.read_csv(csv_path)
    ensure_dir(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crops (
        Farm_ID INTEGER PRIMARY KEY,
        Soil_pH REAL,
        Soil_Moisture REAL,
        Temperature_C REAL,
        Rainfall_mm REAL,
        Crop_Type TEXT,
        Fertilizer_Usage_kg REAL,
        Pesticide_Usage_kg REAL,
        Crop_Yield_ton REAL,
        Sustainability_Score REAL
    )
    """)

    df.to_sql("crops", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    print("🌾 Farmer Advisor database setup complete.")


# ---------- Market Research DB Setup ----------
def setup_market_research_db(csv_path="/home/sanika/multiagent/AI-MULTI-AGENT-Farmer/data/market_data.csv",
                             db_path="/home/sanika/multiagent/AI-MULTI-AGENT-Farmer/data/crop_data.db"):
    df = pd.read_csv(csv_path)
    ensure_dir(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_data (
        Market_ID INTEGER,
        Product TEXT,
        Market_Price_per_ton REAL,
        Demand_Index REAL,
        Supply_Index REAL,
        Competitor_Price_per_ton REAL,
        Economic_Indicator REAL,
        Weather_Impact_Score REAL,
        Seasonal_Factor TEXT,
        Consumer_Trend_Index REAL
    )
    """)

    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO market_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(row))

    conn.commit()
    conn.close()
    print("📊 Market Research database setup complete.")


# ---------- Optional: Run both ----------
if __name__ == "__main__":
    setup_farmer_advisor_db()
    setup_market_research_db()
