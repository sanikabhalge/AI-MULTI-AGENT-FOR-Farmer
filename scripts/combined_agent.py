import pandas as pd
import json

# Load the datasets
advisor_df = pd.read_csv("/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/ranked_crops_by_topsis.csv")
market_df = pd.read_csv("/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/profitable_crop_analysis.csv")

# Normalize column names
advisor_df.columns = advisor_df.columns.str.strip()
market_df.columns = market_df.columns.str.strip()

# Normalize key columns for reliable matching
advisor_df['Crop_Type'] = advisor_df['Crop_Type'].str.strip().str.lower()
market_df['Product'] = market_df['Product'].str.strip().str.lower()

# Get top 3 market-preferred crops
top_market_crops = market_df.head(3)['Product'].tolist()

recommendation = {}

for index, row in advisor_df.iterrows():
    crop = row['Crop_Type']
    if crop in top_market_crops:
        market_price = market_df[market_df['Product'] == crop].iloc[0]['Market_Price_per_ton']
        
        recommendation["crop"] = crop.title()
        recommendation["price"] = round(market_price, 2)

        # ✅ Save to file
        with open("/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/recommendation.json", "w") as f:
            json.dump(recommendation, f)
        
        break
else:
    recommendation["error"] = "No suitable crop found"
    with open("/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/data/recommendation.json", "w") as f:
        json.dump(recommendation, f)
