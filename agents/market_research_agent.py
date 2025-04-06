from pade.core.agent import Agent, Behaviour
from pade.misc.utility import display_message
from pade.acl.messages import ACLMessage
from scripts.sql_query import fetch_all_market_data  # Uses the new modular SQL query file
import json


class MarketResearchAgent(Agent):
    def __init__(self, aid):
        super(MarketResearchAgent, self).__init__(aid=aid, debug=False)
        self.name = aid.localname
        self.behaviours.append(MarketResponderBehaviour(self))

    def generate_profitable_crops(self):
        """Fetch data from DB and calculate top 3 profitable crops."""
        try:
            data = fetch_all_market_data()
        except Exception as e:
            display_message(self.name, f"❌ Error fetching market data: {e}")
            return []

        filtered_data = []

        for row in data:
            try:
                market_id, product, price, demand, _, comp_price, _, _, _, trend = row
                if demand > 150 and price > 250 and trend > 100:
                    profit_score = price * (demand / 100) + trend * 0.3 - comp_price * 0.1
                    filtered_data.append({
                        "market_id": market_id,
                        "product": product,
                        "price": price,
                        "demand": demand,
                        "comp_price": comp_price,
                        "trend": trend,
                        "profit_score": round(profit_score, 2)
                    })
            except Exception as row_err:
                display_message(self.name, f"⚠️ Skipped a row due to error: {row_err}")

        sorted_data = sorted(filtered_data, key=lambda x: x["profit_score"], reverse=True)
        return sorted_data[:3]


class MarketResponderBehaviour(Behaviour):
    def __init__(self, agent):
        super(MarketResponderBehaviour, self).__init__(agent)

    def on_start(self):
        display_message(self.agent.name, "🌱 Market Research Agent is running and listening...")

    def action(self):
        message = self.receive(timeout=5)
        if message and message.performative == ACLMessage.REQUEST:
            display_message(self.agent.name, f"📩 Received crop request from {message.sender.name}")

            top_crops = self.agent.generate_profitable_crops()

            reply = message.create_reply()
            reply.set_performative(ACLMessage.INFORM)
            reply.set_content(json.dumps(top_crops))

            self.send(reply)
            display_message(self.agent.name, f"📤 Sent top 3 crops to {message.sender.name}")
