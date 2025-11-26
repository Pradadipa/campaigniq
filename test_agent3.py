"""
Test script for Insight Generator Agent (Agent 3)
"""

import json
from src.agents.insight_generator import InsightGeneratorAgent

def print_insight_safely(insight, index=None):
    """Safely print insight with fallback for missing keys."""
    prefix = f"{index}. " if index else ""
    
    # Try different possible key names
    insight_text = (
        insight.get('insight') or 
        insight.get('observation') or 
        insight.get('finding') or 
        'No insight text available'
    )
    
    impact_text = (
        insight.get('impact') or 
        insight.get('business_impact') or 
        insight.get('why_it_matters') or 
        'Impact not specified'
    )
    
    recommendation_text = (
        insight.get('recommendation') or 
        insight.get('action') or 
        insight.get('suggested_action') or 
        'No recommendation provided'
    )
    
    priority = insight.get('priority', 'medium')
    
    print(f"\n{prefix}{insight_text}")
    print(f"   Impact: {impact_text}")
    print(f"   Recommendation: {recommendation_text}")
    if index:
        print(f"   Priority: {priority.upper()}")

def main():
    print("🧪 Testing Insight Generator Agent")
    print("=" * 70)
    
    # Load performance analysis from Agent 2
    print("📥 Loading performance analysis from Agent 2...")
    try:
        with open('data/processed/performance_analysis.json', 'r') as f:
            performance_analysis = json.load(f)
        print("✅ Analysis loaded\n")
    except FileNotFoundError:
        print("❌ Error: performance_analysis.json not found!")
        print("   Please run test_agent2.py first.")
        return
    
    # Initialize Agent 3
    agent = InsightGeneratorAgent(performance_analysis=performance_analysis)
    
    # Run insight generation
    print("⏳ This will take 30-60 seconds (making 5 API calls)...\n")
    insights = agent.run()
    
    # Save insights
    agent.save_insights()
    
    # DEBUG: Show raw structure
    print("\n" + "=" * 70)
    print("🔍 DEBUG: Checking insight structure")
    print("=" * 70)
    for category in ['budget_efficiency', 'creative_performance', 'ad_fatigue', 'platform_insights']:
        if insights[category] and len(insights[category]) > 0:
            print(f"\n{category} - Keys: {list(insights[category][0].keys())}")
    
    # Display insights
    print("\n" + "=" * 70)
    print("💡 GENERATED INSIGHTS")
    print("=" * 70)
    
    print("\n💰 BUDGET EFFICIENCY INSIGHTS:")
    if insights['budget_efficiency']:
        for i, insight in enumerate(insights['budget_efficiency'], 1):
            print_insight_safely(insight, i)
    else:
        print("   ⚠️  No budget efficiency insights generated")
    
    print("\n🎨 CREATIVE PERFORMANCE INSIGHTS:")
    if insights['creative_performance']:
        for i, insight in enumerate(insights['creative_performance'], 1):
            print_insight_safely(insight, i)
    else:
        print("   ⚠️  No creative performance insights generated")
    
    print("\n⏱️  AD FATIGUE INSIGHTS:")
    if insights['ad_fatigue']:
        for i, insight in enumerate(insights['ad_fatigue'], 1):
            print_insight_safely(insight, i)
    else:
        print("   ⚠️  No ad fatigue insights generated")
    
    print("\n📱 PLATFORM INSIGHTS:")
    if insights['platform_insights']:
        for i, insight in enumerate(insights['platform_insights'], 1):
            print_insight_safely(insight, i)
    else:
        print("   ⚠️  No platform insights generated")
    
    print("\n" + "=" * 70)
    print("🎯 TOP PRIORITY RECOMMENDATIONS")
    print("=" * 70)
    
    if insights['priority_recommendations']:
        for rec in insights['priority_recommendations']:
            rank = rec.get('rank', '?')
            insight_text = rec.get('insight', rec.get('recommendation', 'N/A'))
            action = rec.get('recommendation', rec.get('action', 'N/A'))
            impact = rec.get('estimated_impact', rec.get('impact', 'N/A'))
            urgency = rec.get('urgency', 'unknown')
            
            print(f"\n#{rank}. {insight_text}")
            print(f"    Action: {action}")
            print(f"    Impact: {impact}")
            print(f"    Urgency: {urgency.upper()}")
    else:
        print("   ⚠️  No priority recommendations generated")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ Agent 3 testing complete!")
    print("=" * 70)
    total_insights = sum([
        len(insights['budget_efficiency']),
        len(insights['creative_performance']),
        len(insights['ad_fatigue']),
        len(insights['platform_insights'])
    ])
    print(f"\n📊 Total insights generated: {total_insights}")
    print(f"🎯 Priority recommendations: {len(insights['priority_recommendations'])}")
    print(f"💾 Insights saved to: data/processed/insights.json")
    print("\n🎯 Next: Build Agents 4-6\n")

if __name__ == "__main__":
    main()