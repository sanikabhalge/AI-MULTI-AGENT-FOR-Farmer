import sqlite3
import os
import pandas as pd
import sys

# === CONFIGURATION ===
FARMER_DB_PATH = "/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/farmer_advisor.db"
MARKET_DB_PATH = "/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/crop_data.db"
FILTERED_CROPS_OUTPUT = "/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/filtered_crops.csv"

# === FARMER DATA UTILS ===

def filter_crops(soil_pH, soil_moisture, temperature, rainfall):
    """Filter crops from SQLite based on environmental conditions."""
    conn = sqlite3.connect(FARMER_DB_PATH)
    query = f"""
    SELECT * FROM crops
    WHERE Soil_pH BETWEEN {abs(soil_pH) } AND {abs(soil_pH) }
    AND Soil_Moisture BETWEEN {soil_moisture - 5} AND {soil_moisture + 5}
    AND Temperature_C BETWEEN {temperature - 5} AND {temperature + 5}
    AND Rainfall_mm BETWEEN {rainfall - 20} AND {rainfall + 20}
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# === MARKET DATA UTILS ===

def create_market_db():
    """Create market_data table in SQLite database."""
    os.makedirs(os.path.dirname(MARKET_DB_PATH), exist_ok=True)
    with sqlite3.connect(MARKET_DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''
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
        ''')
        conn.commit()

def insert_market_row(row):
    """Insert one row of market data."""
    with sqlite3.connect(MARKET_DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO market_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(row))
        conn.commit()

def load_market_csv(csv_path):
    """Load full market CSV into market_data table."""
    df = pd.read_csv(csv_path)
    create_market_db()
    for _, row in df.iterrows():
        insert_market_row(row)
    print("✅ Market data loaded into database.")

def fetch_all_market_data():
    """Fetch all records from market_data table."""
    with sqlite3.connect(MARKET_DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM market_data")
        return cur.fetchall()

# === MAIN EXECUTION ===

if __name__ == "__main__":
    if len(sys.argv) == 5:
        # Run filtering mode
        soil_pH, soil_moisture, temperature, rainfall = map(float, sys.argv[1:])
        filtered_df = filter_crops(soil_pH, soil_moisture, temperature, rainfall)
        filtered_df.to_csv(FILTERED_CROPS_OUTPUT, index=False)
        print(f"✅ Filtered crops saved to {FILTERED_CROPS_OUTPUT}")
    elif len(sys.argv) == 2:
        # Run market data loading mode
        csv_path = sys.argv[1]
        load_market_csv(csv_path)
    else:
        print("Usage:\n  Filter crops: script.py <pH> <moisture> <temp> <rainfall>\n  Load market data: script.py <market_csv_path>")
