import numpy as np
import pandas as pd

def topsis_ranking(df):
    if df.empty:
        print("No suitable crops found.")
        return None

    # Select criteria
    criteria = ['Crop_Yield_ton', 'Fertilizer_Usage_kg', 'Pesticide_Usage_kg', 'Sustainability_Score']
    data = df[criteria].values.astype(float)

    # Normalize
    norm_data = data / np.sqrt((data**2).sum(axis=0))

    # Define ideal best/worst
    ideal_best = np.array([np.max(norm_data[:, 0]), np.min(norm_data[:, 1]), np.min(norm_data[:, 2]), np.max(norm_data[:, 3])])
    ideal_worst = np.array([np.min(norm_data[:, 0]), np.max(norm_data[:, 1]), np.max(norm_data[:, 2]), np.min(norm_data[:, 3])])

    # Compute distances
    dist_best = np.sqrt(((norm_data - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((norm_data - ideal_worst) ** 2).sum(axis=1))

    # Compute TOPSIS Score
    topsis_score = dist_worst / (dist_best + dist_worst)
    df['TOPSIS_Score'] = topsis_score

    # Rank crops
    df = df.sort_values(by='TOPSIS_Score', ascending=False)
    df.to_csv("ranked_crops_by_topsis.csv", index=False)

    #return df.iloc[0]  # Return best crop

if __name__ == "__main__":
    filtered_crops = pd.read_csv("filtered_crops.csv")
    best_crop = topsis_ranking(filtered_crops)
    
    #print(f"Recommended Crop: {best_crop['Crop_Type']}")
