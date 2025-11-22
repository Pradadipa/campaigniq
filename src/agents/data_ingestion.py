"""
Agent 1: Data Ingestion Agent
Loads, validates, and prepares campaign data for analysis.
"""

import numpy as np 
import pandas as pd 
from datetime import datetime 
from typing import Dict, List, Tuple
import json

class DataIngestionAgent:
    """
    Agent responsible for loading and preparing campaign data.
    Validates data quality and structures it for downstream agents.
    """

    def __init__(self, data_path: str):
        """
        Initialize the Data Ingestion Agent.
        
        Args:
            data_path: Path to the campaign data CSV file
        """
        self.data_path = data_path
        self.raw_data = None
        self.processed_data = None
        self.data_quality_report = {}

    def load_data(self) -> pd.DataFrame:
        """Load campaign data from CSV."""
        print("📥 Loading campaign data ...")
        try:
            self.raw_data = pd.read_csv(self.data_path)
            print(f"✅ Loaded {len(self.raw_data)} rows")
            return self.raw_data
        except FileNotFoundError:
            raise Exception(f"❌ Data file not found: {self.data_path}")
        except Exception as e:
            raise Exception(f"❌ Error loading data: {str(e)}")
    
    def validate_data_quality(self) -> Dict:
        """
        Validate data quality and generate report.
        Checks for: missing values, date range, budget consistency, outliers.
        """
        print("\n🔍 Validating data quality...")

        if self.raw_data is None:
            raise Exception("No data loaded. Call load_data() first.")
        
        df = self.raw_data.copy()
        df['date'] = pd.to_datetime(df['date'])

        report = {
            'total_rows':len(df),
            'date_range': {
                'start': df['date'].min().strftime('%Y-%m-%d'),
                'end': df['date'].max().strftime('%Y-%m-%d'),
                'days_covered': (df['date'].max() - df['date'].min()).days + 1
            },
            'platforms':df['platform'].unique().tolist(),
            'missing_values': {},
            'data_completeness': {},
            'outliers': {},
            'budget_summary': {}
        }

        # Check missing values
        missing_counts = df.isnull().sum()
        report['missing_values'] = {
            col : int(count) for col, count in missing_counts.items() if count > 0 
        }

        # Check data completeness (missing days)
        expected_days = (df['date'].max() - df['date'].min()).days + 1
        for platform in df['platform'].unique():
            platform_data = df[df['platform'] == platform]
            actual_days = platform_data['date'].unique()
            expected_rows = expected_days * 3
            actual_rows = len(platform_data)

            report['data_completeness'][platform] = {
                'expected_rows':expected_rows,
                'actual_rows':actual_rows,
                'missing_rows': expected_rows - actual_rows,
                'completeness_percentage':round((actual_rows/expected_rows) * 100)
            }

        # Detect outliers using IQR method
        for metric in ['impressions', 'clicks', 'spend']:
            Q1 = df[metric].quantile(0.25)
            Q3 = df[metric].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5*IQR
            upper_bound = Q3 + 1.5*IQR

            outliers = df[(df[metric] < lower_bound) | (df[metric] > upper_bound)]

            if len(outliers) > 0:
                report['outliers'][metric] = {
                    'count':len(outliers),
                    'percentage':round((len(outliers)/len(df))*100, 2),
                    'max_value':float(outliers[metric].max()),
                    'dates': outliers['date'].dt.strftime('%Y-%m-%d').tolist()[:3]
                }
        
        # Budget summary
        total_spend = df['spend'].sum()
        report['budget_summary'] = {
            'total_spend':round(total_spend, 2),
            'by_platform': {}
        }

        for platform in df['platform'].unique():
            platform_spend = df[df['platform']==platform]['spend'].sum()
            report['budget_summary']['by_platform'][platform] = {
                'spend':round(platform_spend, 2),
                'percentage':round((platform_spend/total_spend)*100, 2)
            }
        
        self.data_quality_report = report
        print(f"✅ Data validation complete")
        print(f"   Total rows: {report['total_rows']}")
        print(f"   Date range: {report['date_range']['start']} to {report['date_range']['end']}")
        print(f"   Missing values: {sum(report['missing_values'].values())} total")
        print(f"   Outliers detected: {sum([v['count'] for v in report['outliers'].values()])} rows")
        
        return report
    
    def add_derived_features(self) -> pd.DataFrame:
        """
        Add calculated features to support analysis.
        Features: week_number, day_of_week, is_weekend, days_since_start
        """
        print("\n🔧 Adding derived features...")

        if self.raw_data is None:
            raise Exception("No data loaded. Call load_data() first.")
        
        df = self.raw_data.copy()
        df['date'] = pd.to_datetime(df['date'])

        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)

        # Calculate derived features
        start_date = df['date'].min()
        df['days_since_start'] = (df['date'] - start_date).dt.days
        df['week_number'] = (df['days_since_start']//7)+1
        df['day_of_week'] = df['date'].dt.day_of_week
        df['day_name'] = df['date'].dt.day_name()
        df['is_weekend'] = df['day_of_week'] >= 5

        # Add Mont and Year
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year

        print(f"✅ Added 7 derived features")
        
        self.processed_data = df
        return df
    
    def normalize_platforms(self) -> pd.DataFrame:
        """
        Ensure consistent platform naming and structure.
        Standardize metric formats across platforms.
        """
        print("\n🔄 Normalizing platform data...")

        if self.processed_data is None:
            raise Exception("No processed data. Call add_derived_features() first.")
        
        df = self.processed_data.copy()

        # Standarize platform names
        platform_mapping = {
            'google_display':'Google Display',
            'meta':'Meta',
            'tiktok':'TikTok'
        }
        df['platform_display'] = df['platform'].map(platform_mapping)

        # Round metrics to appropiate precision
        df['cpm'] = df['cpm'].round(2)
        df['ctr'] = df['ctr'].round(4)
        df['engagement_rate'] = df['engagement_rate'].round(4)
        df['spend'] = df['spend'].round(2)

        # Ensure integer types for count metrics
        df['impressions'] = df['impressions'].astype(int)
        df['reach'] = df['reach'].astype(int)
        df['clicks'] = df['clicks'].astype(int)
        df['engagements'] = df['engagements'].astype(int)
        df['video_views'] = df['video_views'].astype(int)

        print(f"✅ Platform data normalized")

        self.processed_data = df
        return df

    def get_summary_statistics(self) -> Dict:
        """Generate summary statistics for the dataset."""
        if self.processed_data is None:
            raise Exception("No processed data available.")
        
        df = self.processed_data

        summary = {
            'overall': {
                'total_impressions': int(df['impressions'].sum()),
                'total_clicks': int(df['clicks'].sum()),
                'total_spend': round(df['spend'].sum(), 2),
                'avg_cpm': round(df['cpm'].mean(), 2),
                'avg_ctr': round(df['ctr'].mean(), 4),
                'total_engagemnets': int(df['engagements'].sum())
            }, 
            'by_platform':{}
        }

        for platform in df['platform'].unique():
            platform_data = df[df['platform']==platform]
            summary['by_platform'][platform] = {
                'impression': int(platform_data['impressions'].sum()),
                'clicks': int(platform_data['clicks'].sum()),
                'spend': round(platform_data['spend'].sum(),2),
                'avg_cpm': round(platform_data['cpm'].mean(),2),
                'avg_ctr': round(platform_data['ctr'].mean(), 4),
                'engagements': int(platform_data['engagements'].sum())
            }
        return summary
    
    def run(self) -> Tuple[pd.DataFrame, Dict]:
        """
        Execute complete data ingestion pipeline.
        Returns: (processed_data, data_quality_report)
        """
        print("🚀 Starting Data Ingestion Agent...")
        print("=" * 60)

        # Step 1: Load Data
        self.load_data()

        # Step 2: Validate quality
        quality_report = self.validate_data_quality()

        # Step 3: Add derived features
        self.add_derived_features()

        # Step 4: Normalize platform
        self.normalize_platforms()

        # Step 5: Generate summary
        summary_stats = self.get_summary_statistics()

        print("\n" + "=" * 60)
        print("✅ DATA INGESTION COMPLETE")
        print("=" * 60)
        print(f"\n📊 Summary Statistics:")
        print(f"   Total Impressions: {summary_stats['overall']['total_impressions']:,}")
        print(f"   Total Clicks: {summary_stats['overall']['total_clicks']:,}")
        print(f"   Total Spend: ${summary_stats['overall']['total_spend']:,}")
        print(f"   Average CPM: ${summary_stats['overall']['avg_cpm']}")
        print(f"   Average CTR: {summary_stats['overall']['avg_ctr']:.2%}")

        # Combine reports
        full_report = {
            'data_quality': quality_report,
            'summary_statistics': summary_stats
        }

        return self.processed_data, full_report
    
    def save_processed_data(self, output_path: str = 'data/processed/campaign_data_processed.csv'):
        """Save processed data to CSV."""
        if self.processed_data is None:
            raise Exception("No processed data to save.")
        
        self.processed_data.to_csv(output_path, index=False)
        print(f"\n💾 Processed data saved to: {output_path}")
    
    def save_report(self, report: Dict, output_path: str = 'data/processed/data_quality_report.json'):
        """Save data quality report to JSON."""
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"💾 Quality report saved to: {output_path}")