import sqlite3
import os
import pandas as pd

DB_FILE = "data/crop_data.db"

def create_connection():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    return sqlite3.connect(DB_FILE)

def create_table():
    with create_connection() as conn:
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

def insert_data(row):
    with create_connection() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO market_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(row))
        conn.commit()

def fetch_all_data():
    with create_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM market_data")
        return cur.fetchall()

def load_csv_to_db(csv_path):
    df = pd.read_csv(csv_path)
    create_table()
    for _, row in df.iterrows():
        insert_data(row)
    print("✅ Data loaded into database.")