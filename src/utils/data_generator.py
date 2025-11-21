import pandas as pd 
import numpy as np 
from datetime import datetime, timedelta
import yaml
import random

class CampaignDataGenerator:
    """
    Generates realistic synthetic campaign data for brand awareness campaigns
    across multiple platforms (Google Display, Meta, TikTok).
    
    Includes realistic patterns:
    - Platform performance differences
    - Ad fatigue over time
    - Day-of-week effects
    - Creative variance
    - Learning phase (first 7 days)
    - Data quality issues (missing values, outliers)
    """
    def __init__(self, config_path='config.yaml'):
        """Initialize generator with configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        np.random.seed(42)
        random.seed(42)

        # Extract config value
        self.campaign_config = self.config['campaign']
        self.platforms_config = self.config['platforms']

        # Campaign Basics
        self.brand_name = self.campaign_config['brand_name']
        self.campaign_name = self.campaign_config['campaign_name']
        self.duration_days = self.campaign_config['duration_days']
        self.total_budget = self.campaign_config['total_budget']
        self.start_date = datetime.strptime(
            self.campaign_config['start_date'],
            '%Y-%m-%d'
        )

        # Platform names
        self.platforms = ['google_display', 'meta', 'tiktok']
    
    def _get_date_features(self, date):
        """Extract features from date for pattern generation."""
        day_of_week = date.weekday()  # 0=Monday, 6=Sunday
        is_weekend = day_of_week >= 5
        days_since_start = (date - self.start_date).days
        week_number = days_since_start // 7 + 1
        
        return {
            'day_of_week': day_of_week,
            'is_weekend': is_weekend,
            'days_since_start': days_since_start,
            'week_number': week_number
        }
    
    def _calculate_learning_phase_multiplier(self, days_since_start):
        """
        Learning phase: First 7 days have suboptimal performance.
        CPM is higher, CTR is lower as algorithms learn.
        """
        if days_since_start >= 7:
            return 1.0  # Normal performance
        
        # Gradual improvement from day 0 to day 7
        # Day 0: 1.3x CPM, Day 7: 1.0x CPM
        cpm_multiplier = 1.3 - (days_since_start * 0.3 / 7)
        ctr_multiplier = 0.85 + (days_since_start * 0.15 / 7)
        
        return {
            'cpm_multiplier': cpm_multiplier,
            'ctr_multiplier': ctr_multiplier
        }
    
    def _calculate_ad_fatigue_multiplier(self, week_number):
        """
        Ad fatigue: Performance degrades in week 4.
        CTR and engagement drop as audience sees ads repeatedly.
        """
        if week_number <= 3:
            return 1.0  # No fatigue
        
        # Week 4: reduce CTR by 15-25%, engagement by 10-20%
        ctr_multiplier = np.random.uniform(0.75, 0.85)
        engagement_multiplier = np.random.uniform(0.80, 0.90)
        
        return {
            'ctr_multiplier': ctr_multiplier,
            'engagement_multiplier': engagement_multiplier
        }
    
    def _calculate_day_of_week_multiplier(self, platform, is_weekend):
        """
        Day-of-week effects: Weekends perform differently.
        B2C beauty brand sees different behavior on weekends.
        """
        if not is_weekend:
            return 1.0  # Baseline weekday performance
        
        # Weekend multipliers by platform
        weekend_effects = {
            'google_display': 0.95,  # Slightly lower on weekends
            'meta': 1.10,  # Better on weekends
            'tiktok': 1.20  # Much better on weekends
        }
        
        return weekend_effects.get(platform, 1.0)
    
    def _get_creative_multiplier(self, creative_id):
        """
        Creative variance: Some ads perform better than others.
        Creative 1: Best (+30%)
        Creative 2: Average (baseline)
        Creative 3: Worst (-20%)
        """
        creative_multipliers = {
            1: 1.30,  # Best performer
            2: 1.00,  # Average
            3: 0.80   # Underperformer
        }
        
        return creative_multipliers.get(creative_id, 1.0)
    
    def _generate_daily_metrics(self, date, platform, creative_id, platform_config):
        """
        Generate daily performance metrics for a specific platform and creative.
        Applies all realistic patterns (learning phase, fatigue, day-of-week, creative variance).
        """
        # Get date features
        date_features = self._get_date_features(date)
        days_since_start = date_features['days_since_start']
        week_number = date_features['week_number']
        is_weekend = date_features['is_weekend']
        
        # Get baseline metrics from config
        baseline_cpm = platform_config['avg_cpm']
        baseline_ctr = platform_config['avg_ctr']
        baseline_engagement = platform_config.get('avg_engagement_rate', 0.03)
        
        # Calculate daily budget (total budget / duration / num_creatives)
        num_creatives = platform_config['num_creatives']
        platform_daily_budget = (
            self.total_budget * 
            platform_config['budget_percentage'] / 
            self.duration_days / 
            num_creatives
        )
        
        # Apply pattern multipliers
        
        # 1. Learning phase
        learning_mult = self._calculate_learning_phase_multiplier(days_since_start)
        if isinstance(learning_mult, dict):
            cpm = baseline_cpm * learning_mult['cpm_multiplier']
            ctr = baseline_ctr * learning_mult['ctr_multiplier']
        else:
            cpm = baseline_cpm
            ctr = baseline_ctr
        
        # 2. Ad fatigue (week 4)
        fatigue_mult = self._calculate_ad_fatigue_multiplier(week_number)
        if isinstance(fatigue_mult, dict):
            ctr *= fatigue_mult['ctr_multiplier']
            engagement_rate = baseline_engagement * fatigue_mult['engagement_multiplier']
        else:
            engagement_rate = baseline_engagement
        
        # 3. Day-of-week effects
        dow_mult = self._calculate_day_of_week_multiplier(platform, is_weekend)
        ctr *= dow_mult
        engagement_rate *= dow_mult
        
        # 4. Creative variance
        creative_mult = self._get_creative_multiplier(creative_id)
        ctr *= creative_mult
        engagement_rate *= creative_mult
        
        # Add random noise (±10%) to make it realistic
        cpm *= np.random.uniform(0.90, 1.10)
        ctr *= np.random.uniform(0.90, 1.10)
        engagement_rate *= np.random.uniform(0.90, 1.10)
        
        # Calculate actual spend (slight variation from planned budget)
        actual_spend = platform_daily_budget * np.random.uniform(0.95, 1.05)
        
        # Calculate other metrics based on spend and CPM
        impressions = int((actual_spend / cpm) * 1000)
        
        # Reach is typically 70-90% of impressions (frequency > 1)
        reach = int(impressions * np.random.uniform(0.70, 0.90))
        
        # Clicks based on CTR
        clicks = int(impressions * ctr)
        
        # Engagements based on engagement rate (only for social platforms)
        if platform in ['meta', 'tiktok']:
            engagements = int(impressions * engagement_rate)
        else:
            engagements = 0
        
        # Video views (80-95% of impressions for video ads)
        video_views = int(impressions * np.random.uniform(0.80, 0.95))
        
        return {
            'date': date.strftime('%Y-%m-%d'),
            'platform': platform,
            'creative_id': f"{platform}_creative_{creative_id}",
            'impressions': impressions,
            'reach': reach,
            'clicks': clicks,
            'spend': round(actual_spend, 2),
            'engagements': engagements,
            'video_views': video_views,
            'cpm': round(cpm, 2),
            'ctr': round(ctr, 4),
            'engagement_rate': round(engagement_rate, 4) if platform in ['meta', 'tiktok'] else 0
        }
    
    def _add_data_quality_issues(self, df):
        """
        Add realistic data quality issues:
        1. Missing days (1-2 per platform - reporting delays)
        2. Outlier days (1 day with unusually high performance)
        """
        df_modified = df.copy()
        
        # 1. Add missing days (remove 1-2 random days per platform)
        for platform in self.platforms:
            platform_data = df_modified[df_modified['platform'] == platform]
            if len(platform_data) > 5:  # Only if we have enough data
                num_missing = random.randint(1, 2)
                rows_to_drop = platform_data.sample(n=num_missing).index
                df_modified = df_modified.drop(rows_to_drop)
        
        # 2. Add one outlier day (viral post effect - 2-3x normal performance)
        outlier_idx = df_modified.sample(n=1).index[0]
        multiplier = np.random.uniform(2.0, 3.0)
        
        df_modified.loc[outlier_idx, 'impressions'] = int(
            df_modified.loc[outlier_idx, 'impressions'] * multiplier
        )
        df_modified.loc[outlier_idx, 'reach'] = int(
            df_modified.loc[outlier_idx, 'reach'] * multiplier
        )
        df_modified.loc[outlier_idx, 'clicks'] = int(
            df_modified.loc[outlier_idx, 'clicks'] * multiplier
        )
        df_modified.loc[outlier_idx, 'engagements'] = int(
            df_modified.loc[outlier_idx, 'engagements'] * multiplier
        )
        df_modified.loc[outlier_idx, 'video_views'] = int(
            df_modified.loc[outlier_idx, 'video_views'] * multiplier
        )
        
        # Recalculate CPM and CTR for outlier day
        df_modified.loc[outlier_idx, 'cpm'] = round(
            df_modified.loc[outlier_idx, 'spend'] / 
            df_modified.loc[outlier_idx, 'impressions'] * 1000, 2
        )
        df_modified.loc[outlier_idx, 'ctr'] = round(
            df_modified.loc[outlier_idx, 'clicks'] / 
            df_modified.loc[outlier_idx, 'impressions'], 4
        )
        
        return df_modified
    
    def generate_campaign_data(self):
        """
        Main method to generate complete campaign dataset.
        Returns a pandas DataFrame with all daily performance data.
        """
        all_data = []
        
        # Generate data for each platform
        for platform in self.platforms:
            platform_config = self.platforms_config[platform]
            num_creatives = platform_config['num_creatives']
            
            # For each creative
            for creative_id in range(1, num_creatives + 1):
                
                # For each day in campaign
                for day in range(self.duration_days):
                    current_date = self.start_date + timedelta(days=day)
                    
                    # Generate daily metrics
                    daily_metrics = self._generate_daily_metrics(
                        date=current_date,
                        platform=platform,
                        creative_id=creative_id,
                        platform_config=platform_config
                    )
                    
                    all_data.append(daily_metrics)
        
        # Convert to DataFrame
        df = pd.DataFrame(all_data)
        
        # Add campaign metadata
        df['campaign_id'] = 'CAMP_001'
        df['campaign_name'] = self.campaign_name
        df['brand_name'] = self.brand_name
        
        # Reorder columns for better readability
        column_order = [
            'campaign_id', 'campaign_name', 'brand_name', 'date', 
            'platform', 'creative_id', 'impressions', 'reach', 'clicks', 
            'spend', 'engagements', 'video_views', 'cpm', 'ctr', 'engagement_rate'
        ]
        df = df[column_order]
        
        # Add data quality issues
        df = self._add_data_quality_issues(df)
        
        # Sort by date and platform
        df = df.sort_values(['date', 'platform', 'creative_id']).reset_index(drop=True)
        
        return df
    
    def save_to_csv(self, df, filename='campaign_data.csv'):
        """Save generated data to CSV file."""
        output_path = f'data/raw/{filename}'
        df.to_csv(output_path, index=False)
        print(f"✅ Campaign data saved to {output_path}")
        print(f"📊 Generated {len(df)} rows of data")
        print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"💰 Total spend: ${df['spend'].sum():,.2f}")
        return output_path