from pade.core.agent import Agent
from pade.misc.utility import display_message
from scripts.sql_query import fetch_all_data
import csv

class MarketResearchAgent(Agent):
    def __init__(self, aid):
        super(MarketResearchAgent, self).__init__(aid=aid, debug=False)
        self.name = aid.name
        self.output_file = 'data/profitable_crop_analysis.csv'

    def on_start(self):
        super().on_start()
        display_message(self.name, '🌱 Market Research Agent Started')
        self.export_profitable_crop_analysis()

    def export_profitable_crop_analysis(self):
        data = fetch_all_data()
        filtered_data = []

        for row in data:
            market_id, product, price, demand, _, comp_price, _, _, _, trend = row
            if demand > 150 and price > 250 and trend > 100:
                profit_score = price * (demand / 100) + trend * 0.3 - comp_price * 0.1
                filtered_data.append((market_id, product, price, demand, comp_price, trend, round(profit_score, 2)))

        sorted_data = sorted(filtered_data, key=lambda x: x[-1], reverse=True)

        with open(self.output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Market_ID", "Product", "Market_Price_per_ton", "Demand_Index",
                "Competitor_Price_per_ton", "Consumer_Trend_Index", "Profit_Score"
            ])
            writer.writerows(sorted_data)

        display_message(self.name, f"📊 Saved to {self.output_file}")
