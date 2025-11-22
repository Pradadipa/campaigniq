"""
Agent 2: Performance Analyzer Agent
Calculates KPIs, analyzes trends, and identifies performance patterns.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime
import json

class PerformanceAnalyzerAgent:
    """
    Agent responsible for analyzing campaign performance.
    Calculates KPIs, trends, and patterns across platforms, time, and creatives.
    """
    
    def __init__(self, processed_data: pd.DataFrame):
        """
        Initialize Performance Analyzer Agent.
        
        Args:
            processed_data: Cleaned and processed campaign data from Agent 1
        """
        self.data = processed_data
        self.analysis_result = {}

    def calculate_overall_kpis(self) -> Dict:
        """Calculate campaign-level KPIs."""
        print("\n📊 Calculating overall KPIs...")

        df = self.data

        kpis = {
            'total_impressions': int(df['impressions'].sum()),
            'total_reach': int(df['reach'].sum()),
            'total_clicks': int(df['clicks'].sum()),
            'total_spend': round(df['spend'].sum(), 2),
            'total_engagements': int(df['engagements'].sum()),
            'total_video_views': int(df['video_views'].sum()),
            'average_cpm': round(df['cpm'].mean(), 2),
            'average_ctr': round(df['ctr'].mean(), 4),
            'average_engagement_rate': round(df['engagement_rate'].mean(), 4),
            'frequency': round(df['impressions'].sum() / df['reach'].sum(), 2),
            'cost_per_click': round(df['spend'].sum() / df['clicks'].sum(), 2),
            'campaign_days': int(df['days_since_start'].max()+1),
            'platforms_count': int(df['platform'].nunique()),
            'creative_count': int(df['creative_id'].nunique())
        }

        print(f"✅ Overall KPIs calculated")
        print(f"   Total Impressions: {kpis['total_impressions']:,}")
        print(f"   Total Spend: ${kpis['total_spend']:,}")
        print(f"   Average CPM: ${kpis['average_cpm']}")
        print(f"   Average CTR: {kpis['average_ctr']:.2%}")

        return kpis
    
    def analyze_by_platform(self) -> Dict:
        """Analyze performance broken down by platform."""
        print("\n📊 Analyzing performance by platform...")


        df = self.data
        platform_analysis = {}

        for platform in df['platform'].unique():
            platform_data = df[df['platform']==platform]

            platform_analysis[platform] = {
                'impressions': int(platform_data['impressions'].sum()),
                'reach': int(platform_data['reach'].sum()),
                'clicks': int(platform_data['clicks'].sum()),
                'spend': round(platform_data['spend'].sum(), 2),
                'engagements': int(platform_data['engagements'].sum()),
                'video_views': int(platform_data['video_views'].sum()),
                'avg_cpm': round(platform_data['cpm'].mean(), 2),
                'avg_ctr': round(platform_data['ctr'].mean(), 4),
                'avg_engagement_rate': round(platform_data['engagement_rate'].mean(), 4),
                'frequency': round(platform_data['impressions'].sum() / platform_data['reach'].sum(), 2),
                'cost_per_click': round(platform_data['spend'].sum() / platform_data['clicks'].sum(), 2) if platform_data['clicks'].sum() > 0 else 0,
                'spend_percentage': round((platform_data['spend'].sum()/df['spend'].sum())* 100, 2),
                'impression_share': round((platform_data['impressions'].sum()/df['impressions'].sum())*100, 2)
            }
        print(f"✅ Platform analysis complete for {len(platform_analysis)} platforms")

        return platform_analysis
    
    def anlyze_by_week(self) -> Dict:
        """Analyze week-over-week performance trends."""
        print("\n📊 Analyzing week-over-week trends...")

        df = self.data
        weekly_analysis = {}

        for week in sorted(df['week_number'].unique()):
            week_data = df[df['week_number']==week]

            weekly_analysis[f'week_{week}'] = {
                'week_number': int(week),
                'impressions': int(week_data['impressions'].sum()),
                'clicks': int(week_data['clicks'].sum()),
                'spend': round(week_data['spend'].sum(), 2),
                'avg_cpm': round(week_data['cpm'].mean(), 2),
                'avg_ctr': round(week_data['ctr'].mean(), 3),
                'avg_engagement_rate': round(week_data['engagement_rate'].mean(), 4),
                'days_with_data': int(week_data['date'].nunique())
            }
        
        weeks = sorted([int(k.split('_')[1]) for k in weekly_analysis.keys()])
        for i in range(1, len(weeks)):
            current_week = f'week_{weeks[i]}'
            previous_week = f'week_{weeks[i-1]}'

            weekly_analysis[current_week]['ctr_change_pct'] = round(
                ((weekly_analysis[current_week]['avg_ctr'] - 
                    weekly_analysis[previous_week]['avg_ctr']) / 
                    weekly_analysis[previous_week]['avg_ctr']) * 100 , 2
            ) if weekly_analysis[previous_week]['avg_ctr'] > 0 else 0

            weekly_analysis[current_week]['cpm_change_pct'] = round(
                ((weekly_analysis[current_week]['avg_cpm'] - 
                    weekly_analysis[previous_week]['avg_cpm']) / 
                    weekly_analysis[previous_week]['avg_cpm']) * 100 , 2
            ) if weekly_analysis[previous_week]['avg_cpm'] > 0 else 0

        print(f"✅ Weekly analysis complete for {len(weekly_analysis)} weeks")

        return weekly_analysis
    
    def analyze_by_creative(self) -> Dict:
        """Analyze performance by creative."""
        print("\n📊 Analyzing creative performance...")

        df = self.data
        creative_analysis = {}

        for creative in df['creative_id'].unique():
            creative_data = df[df['creative_id'] == creative]
            platform = creative_data['platform'].iloc[0]

            creative_analysis[creative] = {
                'platform': platform,
                'impressions': int(creative_data['impressions'].sum()),
                'clicks': int(creative_data['clicks'].sum()),
                'spend': round(creative_data['spend'].sum(), 2),
                'avg_ctr': round(creative_data['ctr'].mean(), 4),
                'avg_cpm': round(creative_data['cpm'].mean(), 2),
                'avg_engagement_rate': round(creative_data['engagement_rate'].mean(), 4),
                'days_active': int(creative_data['date'].nunique())
            }
        
        for platform in df['platform'].unique():
            platform_creatives = {
                k: v for k, v in creative_analysis.items()
                if v['platform'] == platform
            }

            # Sort by CTR
            sorted_creative = sorted(
                platform_creatives.items(),
                key=lambda x: x[1]['avg_ctr'],
                reverse=True
            )

            for rank, (creative_id, _) in enumerate(sorted_creative, 1):
                creative_analysis[creative_id]['rank_by_ctr'] = rank
        
        print(f"✅ Creative analysis complete for {len(creative_analysis)} creatives")

        return creative_analysis
    
    def analyze_day_of_week_patterns(self) -> Dict:
        """Analyze performance patterns by day of week."""
        print("\n📊 Analyzing day-of-week patterns...")

        df = self.data

        # Overall weekdays vs weekend
        weekday_weekend = {
            'weekday': df[~df['is_weekend']].agg({
                'ctr':'mean',
                'cpm':'mean',
                'engagement_rate':'mean',
                'impressions':'sum',
                'clicks':'sum'
            }).to_dict(),
            'weekend': df[df['is_weekend']].agg({
                'ctr':'mean',
                'cpm':'mean',
                'engagement_rate':'mean',
                'impressions':'sum',
                'clicks':'sum'
            }).to_dict()
        }

        # Round values
        for period in weekday_weekend:
            for metric in weekday_weekend[period]:
                if isinstance(weekday_weekend[period][metric], (int, np.integer)):
                    weekday_weekend[period][metric] = int(weekday_weekend[period][metric])
                else:
                    weekday_weekend[period][metric] = round(float(weekday_weekend[period][metric]), 4)
        
        # By Platform
        platform_day_patterns = {}
        for platform in df['platform'].unique():
            platform_data = df[df['platform'] == platform]

            platform_day_patterns[platform] = {
                'weekday_avg_ctr': round(
                    platform_data[~platform_data['is_weekend']]['ctr'].mean(), 4),
                'weekend_avg_ctr': round(
                    platform_data[platform_data['is_weekend']]['ctr'].mean(), 4),
                'weekday_avg_engagement': round(
                    platform_data[~platform_data['is_weekend']]['engagement_rate'].mean(), 4),
                'weekend_avg_engagement': round(
                    platform_data[platform_data['is_weekend']]['engagement_rate'].mean(), 4)
            }

            # Calculate improvement percentage
            if platform_day_patterns[platform]['weekday_avg_ctr'] > 0:
                platform_day_patterns[platform]['weekend_ctr_lift'] = round(
                    ((platform_day_patterns[platform]['weekend_avg_ctr'] - 
                    platform_day_patterns[platform]['weekday_avg_ctr'])/
                    platform_day_patterns[platform]['weekday_avg_ctr']) * 100 ,2
                )
        day_analysis = {
            'weekday_vs_weekend': weekday_weekend,
            'by_platform': platform_day_patterns
        }

        print(f"✅ Day-of-week analysis complete")

        return day_analysis
    
    def detect_anomalies(self) -> Dict:
        """Detect unusual performance days (outliers)."""
        print("\n📊 Detecting performance anomalies...")

        df = self.data
        anomalies = {
            'high_performance_days':[],
            'low_performance_days':[],
            'summary':{}
        }

        # Calculate dialy agregate
        dialy_performance = df.groupby('date').agg({
            'impressions':'sum',
            'clicks':'sum',
            'ctr':'mean',
            'spend':'sum'
        }).reset_index()

        # Detect anomalies using z-score method
        for metric in ['impressions', 'clicks']:
            mean_val = dialy_performance[metric].mean()
            std_val = dialy_performance[metric].std()

            # High performance (>2 Std above mean)
            high_threshold = mean_val + (2 * std_val)
            high_days = dialy_performance[dialy_performance[metric] > high_threshold]

            if len(high_days) > 0:
                for _, row in high_days.iterrows():
                    anomalies['high_performance_days'].append({
                        'date': row['date'].strftime('%Y-%m-%d'),
                        'metric': metric,
                        'value': int(row[metric]),
                        'times_above_average': round(row[metric] / mean_val, 2)
                    })
        
        anomalies['summary'] = {
            'total_high_performance_days': len(anomalies['high_performance_days']),
            'total_low_performance_days': len(anomalies['low_performance_days'])
        }

        print(f"✅ Anomaly detection complete")
        print(f"   High performance days: {anomalies['summary']['total_high_performance_days']}")

        return anomalies
    
    def run(self) -> Dict:
        """Execute complete performance analysis pipeline."""
        print("🚀 Starting Performance Analyzer Agent...")
        print("=" * 60)

        self.analysis_results = {
            'overall_kpis':self.calculate_overall_kpis(),
            'platform_analysis':self.analyze_by_platform(),
            'weekly_analysis':self.anlyze_by_week(),
            'creative_analysis': self.analyze_by_creative(),
            'day_of_week_analysis': self.analyze_day_of_week_patterns(),
            'anomalies': self.detect_anomalies(),
            'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        print("\n" + "=" * 60)
        print("✅ PERFORMANCE ANALYSIS COMPLETE")
        print("=" * 60)
        
        return self.analysis_results
    
    def save_analysis(self, output_path: str = 'data/processed/performance_analysis.json'):
        """Save analysis results to JSON"""
        if not self.analysis_results:
            raise Exception("No analysis results to save. Run analysis first.")
        
        with open(output_path, 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
        
        print(f"\n💾 Performance analysis saved to: {output_path}")