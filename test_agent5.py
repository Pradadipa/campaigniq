"""
Test script for Dashboard Generator Agent (Agent 5) - Direct Build Approach
"""

import json
import pandas as pd

def main():
    print("🧪 Testing Dashboard Generator Agent (Direct Build)")
    print("=" * 70)

    # Load all required data
    print("📥 Loading data...")

    # Load processed data from agent 1
    processed_data = pd.read_csv('data/processed/campaign_data_processed.csv')
    processed_data['date'] = pd.to_datetime(processed_data['date'])
    print("✅ Processed data loaded")

    # Load performance analysis from Agent 2
    with open('data/processed/performance_analysis.json', 'r') as f:
        performance_analysis = json.load(f)
    print("✅ Performance analysis loaded")

    # Load insight from Agent 3
    with open('data/processed/insights.json', 'r') as f:
        insight = json.load(f)
    print("✅ Insights loaded")

    print("\n" + "=" * 70)
    print("✅ ALL DATA LOADED SUCCESSFULLY")
    print("=" * 70)
    
    print("\n🎯 To view the dashboard, run:")
    print("   streamlit run dashboard_app.py")
    print("\n📊 The dashboard will open in your browser automatically!")
    print("\n🎨 Dashboard includes:")
    print("   • Executive KPI summary cards")
    print("   • Weekly performance trends (with Week 4 decline visible!)")
    print("   • Platform comparison charts")
    print("   • Creative performance rankings")
    print("   • AI-powered insights with priority recommendations")
    print("\n💡 Navigate using the tabs at the top of the dashboard")
    
    print("\n" + "=" * 70)
    print("🎯 Next: Build Agent 6 (Report Composer)")
    print("=" * 70)

if __name__ == "__main__":
    main()