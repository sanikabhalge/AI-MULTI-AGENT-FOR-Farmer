from pade.core.agent import Agent, Behaviour
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.misc.utility import display_message
from twisted.internet import reactor
import subprocess
import pandas as pd
import json
import os

class FarmerAdvisorAgent(Agent):
    def __init__(self, aid, soil_pH, moisture, temperature, rainfall):
        super(FarmerAdvisorAgent, self).__init__(aid=aid)
        self.soil_pH = soil_pH
        self.moisture = moisture
        self.temperature = temperature
        self.rainfall = rainfall
        self.behaviour = AdvisorBehaviour(self)
        self.behaviours.append(self.behaviour)
        self.advisor_df = None  # Will hold TOPSIS results in memory

class AdvisorBehaviour(Behaviour):
    def __init__(self, agent):
        super(AdvisorBehaviour, self).__init__(agent)
        self.waiting_for_market = False

    def on_start(self):
        display_message(self.agent.aid.localname, "📡 Farmer Advisor Agent is running...")

        try:
            # 🌱 Run preprocessing scripts with environmental input
            subprocess.run(["python3", "scripts/sql_query.py",
                            str(self.agent.soil_pH), str(self.agent.moisture),
                            str(self.agent.temperature), str(self.agent.rainfall)],
                           check=True)

            subprocess.run(["python3", "scripts/topsis.py"], check=True)

            # 🧠 Load TOPSIS output directly into memory
            topsis_path = "data/ranked_crops_by_topsis.csv"
            if not os.path.exists(topsis_path):
                raise FileNotFoundError(f"Topsis output not found at {topsis_path}")

            self.agent.advisor_df = pd.read_csv(topsis_path)
            self.agent.advisor_df.columns = self.agent.advisor_df.columns.str.strip()
            self.agent.advisor_df['Crop_Type'] = self.agent.advisor_df['Crop_Type'].str.strip().str.lower()

            display_message(self.agent.aid.localname,
                            f"ℹ️ Loaded {len(self.agent.advisor_df)} ranked crops from TOPSIS.")

            # 📨 Request market data
            msg = ACLMessage(ACLMessage.REQUEST)
            msg.set_content("Send top market crops")
            msg.add_receiver(AID(name="market_research_agent@localhost:8000"))
            self.agent.send(msg)

            self.waiting_for_market = True

        except subprocess.CalledProcessError as e:
            display_message(self.agent.aid.localname, f"❌ Error running script: {e}")
            reactor.callLater(0, reactor.stop)

        except Exception as e:
            display_message(self.agent.aid.localname, f"❌ Initialization error: {e}")
            reactor.callLater(0, reactor.stop)

    def action(self):
        if self.waiting_for_market:
            msg = self.receive(timeout=10)
            if msg:
                display_message(self.agent.aid.localname, f"📬 Received market data from {msg.sender.name}")
                try:
                    top_market_data = json.loads(msg.content)

                    # 🔁 Normalize and extract product data
                    top_market_crops = [
                        (row["product"].strip().lower(), float(row["price"]))
                        for row in top_market_data
                    ]

                    # ✅ Match advisor recommendation with market price
                    recommendation = {}
                    for index, row in self.agent.advisor_df.iterrows():
                        crop = row['Crop_Type']
                        for market_crop, market_price in top_market_crops:
                            if crop == market_crop:
                                recommendation = {
                                    "crop": crop.title(),
                                    "price": round(market_price, 2)
                                }
                                break
                        if recommendation:
                            break

                    # ❌ If no crop matched
                    if not recommendation:
                        recommendation = {"error": "No suitable crop found"}

                    # 💾 Save recommendation (optional)
                    with open("data/recommendation.json", "w") as f:
                        json.dump(recommendation, f, indent=4)

                    display_message(self.agent.aid.localname,
                                    f"✅ Final Recommendation: {recommendation}")

                except Exception as e:
                    display_message(self.agent.aid.localname, f"❌ Error processing message: {e}")
                finally:
                    self.waiting_for_market = False
                    reactor.callLater(0, reactor.stop)
