"""
CampaignIQ Interactive Dashboard
Run with: streamlit run dashboard_app.py
"""

import json
import pandas as pd
from src.agents.dashboard_generator import DashboardGeneratorAgent

def main():
    # Load all Data
    processed_data = pd.read_csv('data/processed/campaign_data_processed.csv')
    processed_data['date'] = pd.to_datetime(processed_data['date'])

    with open('data/processed/performance_analysis.json', 'r') as f:
        performance_analysis = json.load(f)
    

    with open('data/processed/insights.json', 'r') as f:
        insight = json.load(f)

    # Initialize and build dashboard
    dashboard = DashboardGeneratorAgent(
        performance_analysis=performance_analysis,
        insights=insight,
        processed_data=processed_data
    )

    dashboard.build_dashboard()

if __name__ == "__main__":
    main()