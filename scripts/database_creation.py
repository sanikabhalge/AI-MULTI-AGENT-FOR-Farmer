import sqlite3
import pandas as pd

# Load the dataset
csv_file = "/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/farmer_advisor_dataset.csv"
df = pd.read_csv(csv_file)

# Connect to SQLite (creates a database file if not exists)
conn = sqlite3.connect("/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/farmer_advisor.db")
cursor = conn.cursor()

# Create a table for crops
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

# Insert data into the table
df.to_sql("crops", conn, if_exists="replace", index=False)

# Commit and close
conn.commit()
conn.close()

print("Database setup completed. Dataset loaded into SQLite.")
