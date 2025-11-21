"""
Script to generate synthetic campaign data for CampaignIQ.
Run this to create your training dataset.
"""

from src.utils.data_generator import CampaignDataGenerator
import pandas as pd

def main():
    print("🚀 Starting CampaignIQ Data Generation...")
    print("=" * 60)
    
    # Initialize generator
    generator = CampaignDataGenerator(config_path='config.yaml')
    
    # Generate data
    print("\n📊 Generating campaign data...")
    df = generator.generate_campaign_data()
    
    # Display summary statistics
    print("\n" + "=" * 60)
    print("📈 DATA SUMMARY")
    print("=" * 60)
    print(f"\nTotal rows: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Platforms: {df['platform'].unique().tolist()}")
    print(f"Creatives per platform: {df.groupby('platform')['creative_id'].nunique().to_dict()}")
    
    print("\n💰 BUDGET SUMMARY")
    print("-" * 60)
    total_spend = df['spend'].sum()
    print(f"Total spend: ${total_spend:,.2f}")
    for platform in df['platform'].unique():
        platform_spend = df[df['platform'] == platform]['spend'].sum()
        percentage = (platform_spend / total_spend) * 100
        print(f"  {platform}: ${platform_spend:,.2f} ({percentage:.1f}%)")
    
    print("\n📊 PERFORMANCE SUMMARY")
    print("-" * 60)
    summary_stats = df.groupby('platform').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'cpm': 'mean',
        'ctr': 'mean',
        'engagement_rate': 'mean'
    }).round(4)
    print(summary_stats)
    
    # Display sample rows
    print("\n📋 SAMPLE DATA (first 5 rows)")
    print("-" * 60)
    print(df.head())
    
    # Save to CSV
    print("\n💾 Saving data...")
    output_path = generator.save_to_csv(df, filename='baliglow_campaign_data.csv')
    
    print("\n✅ DATA GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\n📁 Your data is ready at: {output_path}")
    print("🎯 Next step: Build the Data Ingestion Agent!\n")

if __name__ == "__main__":
    main()