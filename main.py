# from pade.misc.utility import start_loop
# from pade.acl.aid import AID
# from agents.farmer_advisor_agent import FarmerAdvisorAgent

# if __name__ == '__main__':
#     # 🧪 Take user input
#     soil_pH = float(input("Enter Soil pH: "))
#     moisture = float(input("Enter Soil Moisture (%): "))
#     temperature = float(input("Enter Temperature (°C): "))
#     rainfall = float(input("Enter Rainfall (mm): "))

#     # 🎯 Initialize agent with user input
#     farmer_agent = FarmerAdvisorAgent(
#         AID(name='farmer_advisor@localhost:8000'),
#         soil_pH, moisture, temperature, rainfall
#     )

#     # 🟢 Start the agent loop
#     start_loop([farmer_agent])
# main.py
# main.py
# import sys
# from agents.farmer_advisor_agent import FarmerAdvisorAgent
# from pade.misc.utility import start_loop
# from pade.acl.aid import AID

# def start_farmer_agent(ph, moisture, temperature, rainfall):
#     port = 8000
#     farmer_agent = FarmerAdvisorAgent(
#         AID(name=f'farmer_advisor@localhost:{port}'),
#         float(ph), float(moisture), float(temperature), float(rainfall)
#     )
#     start_loop([farmer_agent])

# if __name__ == '__main__':
#     ph, moisture, temp, rain = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
#     start_farmer_agent(ph, moisture, temp, rain)

import sys
from pade.misc.utility import start_loop
from pade.acl.aid import AID
from agents.farmer_advisor_agent import FarmerAdvisorAgent
from agents.market_research_agent import MarketResearchAgent

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python main.py <ph> <moisture> <temperature> <rainfall>")
        sys.exit(1)

    # Get command-line inputs
    ph, moisture, temperature, rainfall = map(float, sys.argv[1:])

    # Create agents with different ports
    farmer_agent = FarmerAdvisorAgent(
        AID(name='farmer_advisor@localhost:8000'),
        ph, moisture, temperature, rainfall
    )

    market_agent = MarketResearchAgent(
        AID(name='market_research_agent@localhost:8001')
    )

    # Start both agents
    start_loop([farmer_agent, market_agent])
