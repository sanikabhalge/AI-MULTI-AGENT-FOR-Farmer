import sqlite3
import pandas as pd

def filter_crops(soil_pH, soil_moisture, temperature, rainfall):
    conn = sqlite3.connect("//home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/farmer_advisor.db")  # Connect to SQLite DB
    query = f"""
    SELECT * FROM crops
    WHERE Soil_pH BETWEEN {soil_pH - 0.5} AND {soil_pH + 0.5}
    AND Soil_Moisture BETWEEN {soil_moisture - 5} AND {soil_moisture + 5}
    AND Temperature_C BETWEEN {temperature - 2} AND {temperature + 2}
    AND Rainfall_mm BETWEEN {rainfall - 20} AND {rainfall + 20}
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    import sys
    # Get input from command line arguments
    soil_pH, soil_moisture, temperature, rainfall = map(float, sys.argv[1:])
    
    filtered_crops = filter_crops(soil_pH, soil_moisture, temperature, rainfall)
    filtered_crops.to_csv("/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/filtered_crops.csv", index=False)  # Save for TOPSIS
