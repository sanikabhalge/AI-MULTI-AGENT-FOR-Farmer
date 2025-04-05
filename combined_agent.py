import pandas as pd

# Load the datasets
advisor_df = pd.read_csv("/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/ranked_crops_by_topsis.csv")
market_df = pd.read_csv("/home/sanika/multiagent/AI-MULTI-AGENT-FOR-Farmer/profitable_crop_analysis.csv")

# Normalize column names
advisor_df.columns = advisor_df.columns.str.strip()
market_df.columns = market_df.columns.str.strip()

# Normalize key columns for reliable matching
advisor_df['Crop_Type'] = advisor_df['Crop_Type'].str.strip().str.lower()
market_df['Product'] = market_df['Product'].str.strip().str.lower()

# Get top 3 market-preferred crops
top_market_crops = market_df.head(3)['Product'].tolist()

# Match with TOPSIS ranked crops
for index, row in advisor_df.iterrows():
    crop = row['Crop_Type']
    if crop in top_market_crops:
        # Get matching market price
        market_price = market_df[market_df['Product'] == crop].iloc[0]['Market_Price_per_ton']
        
        print("✅ Final Recommendation:")
        print(f"🌱 Crop Type: {crop.title()}")
        print(f"💰 Market Price (per ton): ₹{market_price}")
        break
else:
    print("❌ No suitable crop found that matches both TOPSIS ranking and market preference.")
