from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message
from pade.core.agent import Agent, Behaviour
from twisted.internet import reactor
import subprocess

class FarmerAdvisorAgent(Agent):
    def __init__(self, aid, soil_pH, moisture, temperature, rainfall):
        super(FarmerAdvisorAgent, self).__init__(aid=aid)
        self.soil_pH = soil_pH
        self.moisture = moisture
        self.temperature = temperature
        self.rainfall = rainfall
        self.behaviour = AdvisorBehaviour(self)
        self.behaviours.append(self.behaviour)

class AdvisorBehaviour(Behaviour):
    def __init__(self, agent):
        super(AdvisorBehaviour, self).__init__(agent)

    def on_start(self):
        display_message(self.agent.aid.localname, "📡 Farmer Advisor Agent is running...")

        try:
            # 🌱 Prepare inputs
            soil_pH = str(self.agent.soil_pH)
            moisture = str(self.agent.moisture)
            temperature = str(self.agent.temperature)
            rainfall = str(self.agent.rainfall)

            # 🧠 Run subprocesses
            subprocess.run(["python3", "scripts/sql_query.py", soil_pH, moisture, temperature, rainfall], check=True)
            subprocess.run(["python3", "scripts/topsis.py"], check=True)
            subprocess.run(["python3", "scripts/combined_agent.py"], check=True)

            display_message(self.agent.aid.localname, "✅ All scripts executed successfully.")

        except subprocess.CalledProcessError as e:
            display_message(self.agent.aid.localname, f"❌ Error running script: {e}")

        # 🛑 Stop reactor after tasks
        reactor.callLater(0, reactor.stop)
