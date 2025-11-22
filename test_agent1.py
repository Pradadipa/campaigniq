from src.agents.data_ingestion import DataIngestionAgent
import json

def main():
    print("🧪 Testing Data Ingestion Agent")
    print("=" * 70)
    agent = DataIngestionAgent(data_path="data/raw/baliglow_campaign_data.csv")

    processed_data, report = agent.run()

    # Save outputs
    agent.save_processed_data()
    agent.save_report(report)

    # Display quality report highlights
    print("\n" + "=" * 70)
    print("📋 DATA QUALITY REPORT HIGHLIGHTS")
    print("=" * 70)

    print("\n🔍 Data Completeness:")
    for platform, stats in report['data_quality']['data_completeness'].items():
        print(f"   {platform}: {stats['completeness_percentage']}% complete "
                f"({stats['missing_rows']} rows missing)")
    
    print("\n⚠️  Outliers Detected:")
    if report['data_quality']['outliers']:
        for metric, details in report['data_quality']['outliers'].items():
            print(f"   {metric}: {details['count']} outlier(s) ({details['percentage']}%)")
            print(f"      Max value: {details['max_value']:,}")
            print(f"      Dates: {', '.join(details['dates'][:3])}")
    else:
        print("   No significant outliers detected")
    
    print("\n✅ Agent 1 testing complete!")
    print("🎯 Next: Build Agent 2 (Performance Analyzer)\n")

if __name__ == "__main__":
    main()