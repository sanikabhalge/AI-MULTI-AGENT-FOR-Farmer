from pade.acl.aid import AID
from pade.misc.utility import start_loop
from agents.market_research_agent import MarketResearchAgent
from scripts.sql_query import load_csv_to_db

def main():
    load_csv_to_db("data/market_researcher_dataset.csv")
    agent_list = []
    market_agent = MarketResearchAgent(AID(name="market_research_agent@localhost:8000"))
    agent_list.append(market_agent)
    start_loop(agent_list)

if __name__ == "__main__":
    main()