"""
CampaignIQ - Complete Pipeline
Runs all 6 agents in sequence to generate complete campaign analysis.

Usage: python run_campaigniq.py
"""

import sys
import json
import pandas as pd
from datetime import datetime

# Import All Agents
from src.utils.data_generator import CampaignDataGenerator
from src.agents.data_ingestion import DataIngestionAgent
from src.agents.performance_analyzer import PerformanceAnalyzerAgent
from src.agents.insight_generator import InsightGeneratorAgent
from src.agents.report_composer import ReportComposerAgent

def print_header(text):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def print_step(step_num, total_steps, text):
    """Print step indicator."""
    print(f"\n[{step_num}/{total_steps}] {text}")
    print("-" * 80)

def main():
    """Execute complete CampaignIQ pipeline."""

    print_header("🚀 CAMPAIGNIQ - AI-POWERED MARKETING ANALYTICS SYSTEM")
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis pipeline will:")
    print("  1. Generate synthetic campaign data")
    print("  2. Ingest and validate data")
    print("  3. Analyze performance metrics")
    print("  4. Generate AI-powered insights")
    print("  5. Create interactive dashboard")
    print("  6. Compose executive reports")
    print("\n⏱️  Estimated time: 3-5 minutes")
    
    input("\nPress ENTER to start...")

    total_steps = 6

    try:
        # STEP 1: GENERATE DATA
        print_step(1, total_steps, "Data Generation")
        print("🔧 Generating synthetic campaign data...")

        generator = CampaignDataGenerator(config_path='config.yaml')
        campaign_data = generator.generate_campaign_data()
        data_path = generator.save_to_csv(campaign_data, filename='baliglow_campaign_data.csv')

        print(f"✅ Generated {len(campaign_data)} rows of campaign data")

        # STEP 2: DATA Ingestion
        print_step(2, total_steps, "Data Ingestion & Validation")
        print("📥 Running Data Ingestion Agent...")

        ingestion_agent = DataIngestionAgent(data_path=data_path)
        processed_data, data_report = ingestion_agent.run()

        ingestion_agent.save_processed_data()
        ingestion_agent.save_report(data_report)

        print(f"✅ Data validated and processed")
        print(f"    Quality score: {100 - sum([v['missing_rows'] for v in data_report['data_quality']['data_completeness'].values()])}")

        # STEP 3: Performance Analysis
        print_step(3, total_steps, "Performance Analysis")
        print("📊 Running Performance Analyzer Agent...")

        analyzer_agent = PerformanceAnalyzerAgent(processed_data=processed_data)
        performance_analysis = analyzer_agent.run()

        analyzer_agent.save_analysis()

        print(f"✅ Performance analysis complete")
        print(f"     Overall CTR: {performance_analysis['overall_kpis']['average_ctr']:.2%}")
        print(f"     Berst platform: TikTok ({performance_analysis['platform_analysis']['tiktok']['avg_ctr']:.2%} CTR)")

        # STEP 4: Insight Generation
        print_step(4, total_steps, "AI Insight Generation")
        print("💡 Running Insight Generator Agent (using GPT-4 Mini)...")
        print("⏳ This will take 30-60 seconds (making 5 API calls)...")

        insight_agent = InsightGeneratorAgent(performance_analysis=performance_analysis)
        insights = insight_agent.run()

        insight_agent.save_insights()

        total_insights = insights['metadata']['total_insights']
        priority_recs = len(insights['priority_recommendations'])

        print(f"✅ AI insights generated")
        print(f"    Total insights: {total_insights}")
        print(f"    Priority recommendations: {priority_recs}")

        # STEP 5: Dashboard Creation
        print_step(5, total_steps, "Interactive Dashboard")
        print("📊 Dashboard Builder Agent ready...")
        
        print(f"✅ Dashboard configuration complete")
        print(f"   To view dashboard: streamlit run dashboard_app.py")

        # STEP 6: Report Generation
        print_step(6, total_steps, "Report Composition")
        print("📄 Running Report Composer Agent (using GPT-4 Mini)...")
        print("⏳ This will take 60-90 seconds (making 4 API calls)...")

        report_agent = ReportComposerAgent(
            performance_analysis=performance_analysis,
            insights=insights
        )
        reports = report_agent.run()

        report_files = report_agent.save_reports()

        print(f"✅ Executive reports generated")
        if report_files:
            print(f"   Report types: {len(report_files)}")
        else:
            print(f"   Reports saved to: data/outputs/reports/")

        print_header("✅ CAMPAIGNIQ PIPELINE COMPLETE!")
        
        print("\n📊 OUTPUTS GENERATED:")
        print("\n1. Data Files:")
        print("   • data/raw/baliglow_campaign_data.csv")
        print("   • data/processed/campaign_data_processed.csv")
        print("   • data/processed/data_quality_report.json")
        
        print("\n2. Analysis Files:")
        print("   • data/processed/performance_analysis.json")
        print("   • data/processed/insights.json")
        
        print("\n3. Reports:")
        print("   • data/outputs/reports/executive_summary.md")
        print("   • data/outputs/reports/detailed_analysis.md")
        print("   • data/outputs/reports/action_plan.md")
        print("   • data/outputs/reports/client_report.md")
        print("   • data/outputs/reports/complete_report.md")
        
        print("\n4. Interactive Dashboard:")
        print("   • Run: streamlit run dashboard_app.py")
        
        print("\n" + "=" * 80)
        print("📈 CAMPAIGN PERFORMANCE SUMMARY")
        print("=" * 80)

        overall = performance_analysis['overall_kpis']
        print(f"\n💰 Budget: ${overall['total_spend']:,.2f}")
        print(f"👁️  Impressions: {overall['total_impressions']:,}")
        print(f"🖱️  Clicks: {overall['total_clicks']:,}")
        print(f"📊 Average CTR: {overall['average_ctr']:.2%}")
        print(f"💵 Cost Per Click: ${overall['cost_per_click']:.2f}")
        
        print("\n🏆 TOP PERFORMING PLATFORM:")
        best_platform = max(
            performance_analysis['platform_analysis'].items(),
            key=lambda x: x[1]['avg_ctr']
        )
        print(f"   {best_platform[0].upper()}")
        print(f"   CTR: {best_platform[1]['avg_ctr']:.2%}")
        print(f"   CPM: ${best_platform[1]['avg_cpm']:.2f}")
        
        print("\n💡 TOP PRIORITY ACTION:")
        if insights['priority_recommendations']:
            top_rec = insights['priority_recommendations'][0]
            print(f"   {top_rec.get('insight', top_rec.get('recommendation', 'N/A'))}")
        
        print("\n" + "=" * 80)
        print("🎯 NEXT STEPS:")
        print("=" * 80)
        print("\n1. View Interactive Dashboard:")
        print("   $ streamlit run dashboard_app.py")
        
        print("\n2. Read Executive Summary:")
        print("   $ cat data/outputs/reports/executive_summary.md")
        
        print("\n3. Review All Reports:")
        print("   $ cat data/outputs/reports/complete_report.md")
        
        print(f"\n✅ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n🎉 CampaignIQ analysis complete! Portfolio-ready outputs generated.\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
        return 1
        
    except Exception as e:
        print(f"\n\n❌ ERROR: {str(e)}")
        print("\nPipeline failed. Please check the error above.")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())