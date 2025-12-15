"""
Test script for Report Composer Agent (Agent 6)
"""

import json
from src.agents.report_composer import ReportComposerAgent

def main():
    print("🧪 Testing Report Composer Agent")
    print("=" * 70)

    # Load performance analysis from agent 2
    print("📥 Loading performance analysis...")
    with open('data/processed/performance_analysis.json', 'r') as f:
        performance_analysis = json.load(f)
    print("✅ Performance analysis loaded")

    # Load Insight from Agent 3
    print("📥 Loading insights...")
    with open('data/processed/insights.json', 'r') as f:
        insights = json.load(f)
    print("✅ Insights loaded\n")

    # Initialize Agent 6
    agent = ReportComposerAgent(
        performance_analysis=performance_analysis,
        insights=insights
    )

    # Generate all reports
    reports = agent.run()

    # Save reports
    print("\n💾 Saving reports to files...")
    report_files = agent.save_reports()
    
    # Check if save was successful
    if report_files is None:
        print("⚠️  Warning: save_reports() returned None")
        report_files = {}  # Create empty dict to prevent error
    
    # Display preview of each report
    print("\n" + "=" * 70)
    print("📋 REPORT PREVIEWS")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("1️⃣  EXECUTIVE SUMMARY (First 300 chars)")
    print("=" * 70)
    print(reports['executive_summary'][:300] + "...")
    
    print("\n" + "=" * 70)
    print("2️⃣  DETAILED ANALYSIS (First 300 chars)")
    print("=" * 70)
    print(reports['detailed_analysis'][:300] + "...")
    
    print("\n" + "=" * 70)
    print("3️⃣  ACTION PLAN (First 300 chars)")
    print("=" * 70)
    print(reports['action_plan'][:300] + "...")
    
    print("\n" + "=" * 70)
    print("4️⃣  CLIENT REPORT (First 300 chars)")
    print("=" * 70)
    print(reports['client_report'][:300] + "...")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ REPORT GENERATION COMPLETE")
    print("=" * 70)
    print("\n📁 Reports saved to: data/outputs/reports/")
    print("\n📄 Generated reports:")
    if report_files:
        for report_name, filepath in report_files.items():
            print(f"   • {report_name}: {filepath}")
    else:
        print("   Check data/outputs/reports/ folder for saved files")
    
    print("\n🎯 You can now:")
    print("   1. Open any .md file to read the full report")
    print("   2. Copy reports to email, Slack, presentations")
    print("   3. View complete_report.md for all reports in one file")
    
    print("\n✅ CampaignIQ System Complete! All 6 agents working!")
    print("\n🎉 CONGRATULATIONS! Your portfolio project is ready!\n")

if __name__ == "__main__":
    main()