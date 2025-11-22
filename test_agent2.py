"""
Test script for Performance Analyzer Agent (Agent 2)
"""

import pandas as pd
from src.agents.performance_analyzer import PerformanceAnalyzerAgent
import json

def main():
    print("🧪 Testing Performance Analyzer Agent")
    print("=" * 70)

    # Load processed data from agent 1
    print("📥 Loading processed data from Agent 1...")
    processed_data = pd.read_csv('data/processed/campaign_data_processed.csv')
    processed_data['date'] = pd.to_datetime(processed_data['date'])
    print(f"✅ Loaded {len(processed_data)} rows\n")

    # Initialize agent 2
    agent = PerformanceAnalyzerAgent(processed_data=processed_data)

    # Run Analysis
    result = agent.run()

    # Save Analysis
    agent.save_analysis()

    # Display key insights
    print("\n" + "=" * 70)
    print("📋 KEY PERFORMANCE INSIGHTS")
    print("=" * 70)

    print("\n🎯 Platform Performance:")
    for platform, metrics in result['platform_analysis'].items():
        print(f"\n    {platform.upper()}:")
        print(f"      CTR: {metrics['avg_ctr']:.2%}")
        print(f"      CPM: ${metrics['avg_cpm']}")
        print(f"      CPC: ${metrics['cost_per_click']}")
        print(f"      Spend Share: {metrics['spend_percentage']}%")

    print("\📅 Weekly Trends:")
    for week_key in sorted(result['weekly_analysis'].keys()):
        week = result['weekly_analysis'][week_key]

        change_indicator = ""
        if 'ctr_change_pct' in week:
            change = week['ctr_change_pct']
            change_indicator = f" (CTR: {'+' if change > 0 else ''}{change}%)"
        print(f"    Week {week['week_number']}: "
            f"CTR {week['avg_ctr']:.2%}{change_indicator}")
    
    print("\n🎨 Creative Performance (Top 3 by CTR):")
    creative_sorted = sorted(
        result['creative_analysis'].items(),
        key=lambda x: x[1]['avg_ctr'],
        reverse=True
    )[:3]
    for creative_id, metrics in creative_sorted:
        print(f"   {creative_id}: CTR {metrics['avg_ctr']:.2%} "
              f"(Rank #{metrics['rank_by_ctr']} on {metrics['platform']})")
    
    print("\n⚡ Anomalies:")
    if result['anomalies']['high_performance_days']:
        print(f"    {result['anomalies']['summary']['total_high_performance_days']}"
            "high-performance day(s) detected:")
        for anomaly in result['anomalies']['high_performance_days'][:3]:
            print(f"    {anomaly['date']}: {anomaly['metric']} = {anomaly['value']:,}"
            f"{anomaly['times_above_average']} x average")

    print("\n✅ Agent 2 testing complete!")
    print("🎯 Next: Build Agent 3 (Insight Generator)\n")

if __name__ == "__main__":
    main()
