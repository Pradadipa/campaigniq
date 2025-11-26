"""
Agent 3: Insight Generator Agent
Uses AI to generate actionable business insights from performance data.
"""

import json
from typing import Dict, List
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environtment variables
load_dotenv()

class InsightGeneratorAgent:
    """
    Agent that uses GPT-4 to generate business insights from campaign performance data.
    Focuses on: Budget Efficiency, Creative Performance, Ad Fatigue, Platform Insights.
    """

    def __init__(self, performance_analysis: Dict):
        """
        Initialize Insight Generator Agent.
        
        Args:
            performance_analysis: Complete analysis from Agent 2
        """
        self.analysis = performance_analysis
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.insights = {
            'budget_efficiency':[],
            'creative_performance':[],
            'ad_fatigue':[],
            'platform_insights':[],
            'priority_recommendations':[]
        }
    
    def _create_analysis_context(self) -> str:
        """Create a comprehensive context summary for GPT-4."""
        overall = self.analysis['overall_kpis']
        platforms = self.analysis['platform_analysis']
        weekly = self.analysis['weekly_analysis']
        creatives = self.analysis['creative_analysis']

        context = f"""
            CAMPAIGN PERFORMANCE SUMMARY:

            OVERALL METRICS:
            - Total Impressions: {overall['total_impressions']:,}
            - Total Clicks: {overall['total_clicks']:,}
            - Total Spend: ${overall['total_spend']}
            - Average CPM: ${overall['average_cpm']}
            - Average CTR: {overall['average_ctr']}
            - Campaign Duration: {overall['campaign_days']} days

            PLATFORM PERFORMANCE:
        """

        for platform, metrics in platforms.items():
            context += f"""
            {platform.upper()}:
            - Impressions: {metrics['impressions']:,}
            - CTR: {metrics['avg_ctr']:.2%}
            - CPM: ${metrics['avg_cpm']}
            - Cost Per Click: ${metrics['cost_per_click']}
            - Spend: ${metrics['spend']:,} ({metrics['spend_percentage']}% of budget)
            - Engagement Rate: {metrics['avg_engagement_rate']:.2%}
            """
        
        context += "\nWEEKLY TRENDS:\n"
        for week_key in sorted(weekly.keys()):
            week = weekly[week_key]
            change = ""
            if 'ctr_change_pct' in week:
                change = f" (Change: {week['ctr_change_pct']:+1f}%)"
            context += f"Week {week['week_number']} : CTR {week['avg_ctr']:.2%}, CPM ${week['avg_cpm']}{change}\n"
        
        context += "\nCREATIVE PERFORMANCE (Top & Bottom):\n"
        sortted_creatives = sorted(
            creatives.items(),
            key=lambda x: x[1]['avg_ctr'],
            reverse=True
        )

        # Top 3
        context += "Top Performers:\n"
        for creative_id, metrics in sortted_creatives[:3]:
            context += f"- {creative_id}: CTR {metrics['avg_ctr']:.2%}, Spend ${metrics['spend']:,}\n"

        # Bottom 3
        context += "Bottom Performers:\n"
        for creative_id, metrics in sortted_creatives[-3:]:
            context += f"- {creative_id}: CTR {metrics['avg_ctr']:.2%}, Spend ${metrics['spend']:,}\n"
        
        return context
    
    def generate_budget_efficiency_insight(self) -> List[Dict]:
        """Generate insights about budget allocation and cost efficiency."""
        print("\n💰 Generating budget efficiency insights...")

        context = self._create_analysis_context()
        platforms = self.analysis['platform_analysis']

        prompt = f"""You are a marketing analystics expert analyzing a brand awareness campaign.
        {context}

        Task: Generate 2-3 actionable insight about BUDGET EFFICIENCY and COST EFFECTIVENESS.
        
        Focus on:
        1. Which platform delivers the best value (lowest CPM, lowest CPC)?
        2. Are there budget reallocation opportunities?
        3. Where might we br wasting money?

        For each insight, provide:
        - Clear observation with specific numbers
        - Business impact
        - Specifi recommendation with dollar amounts if possible

        Format as JSON array:
        [
            {{
                "insight": "Clear statement of what you found",
                "impact": "Why this matters to busniness outcomes",
                "recommendation": "Specific action to take",
                "priority": "high/medium/low"
            }}
        ] 

        Be specific with numbers and percentages. Focus on actionable recommendations."""

        try:
            response = self.client.chat.completions.create(
                model= "gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a marketing analytics expert who provides clear, actionable insight."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            insights_text = response.choices[0].message.content
            # Extract JSON from response (handle markdowb code blocks)
            if "```json" in insights_text:
                insights_text = insights_text.split("```json")[1].split('```')[0].strip()
            elif "```" in insights_text:
                insights_text = insights_text.split("```")[1].split("```")[0].strip()
            
            insights = json.loads(insights_text)

            print(f"✅ Generated {len(insights)} budget efficiency insights")
            return insights
        
        except Exception as e:
            print(f"⚠️  Error generating budget insights: {str(e)}")
            return []
    
    def generate_creative_performance_insights(self) -> List[Dict]:
        """Generate insights about creative performance."""
        print("\n🎨 Generating creative performance insights...")

        context = self._create_analysis_context()

        prompt = f"""You are a marketing analystics expert analyzing a brand awarness campaign.
        {context}

        Task: Generate 2-3 actionable insight about CREATIVE PERFORMANCE.

        Focus on:
        1. Which creatives are top performers vs underperformers?
        2. What's the performance gap between best and worst?
        3. Which creatives should be scaled, paused, or replaced?

        For each insight, provide:
        - Clear observation with specific performance metrics
        - Business impact (wasted spend, opportunity cost)
        - Specific recommendation (pause, scale, test new variants)

        Format as JSON array with same structure as before

        Be specific about which creative IDs and include performance percentages."""

        try:
            response = self.client.chat.completions.create(
                model= "gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a marketing analytics expert who provides clear, actionable insight."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            insights_text = response.choices[0].message.content
            # Extract JSON from response (handle markdowb code blocks)
            if "```json" in insights_text:
                insights_text = insights_text.split("```json")[1].split('```')[0].strip()
            elif "```" in insights_text:
                insights_text = insights_text.split("```")[1].split("```")[0].strip()
            
            insights = json.loads(insights_text)

            print(f"✅ Generated {len(insights)} creative performance insights")
            return insights
        
        except Exception as e:
            print(f"⚠️  Error generating creative insights: {str(e)}")
            return []
    
    def generate_ad_fatigue_insights(self) -> List[Dict]:
        """Generate insights about ad fatigue and creative refresh timing."""

        context = self._create_analysis_context()

        prompt = f"""You are a marketing analytics expert analyzing a brand awareness campaign.
        {context}

        Task: Generate 2-3 actionable insights about AD FATIGUE and CREATIVE REFRESH TIMING.

        Focus on:
        1. Is there evidence of ad fatigue (declining performance over time)?
        2. When did perfromance start declining?
        3. When should creatives be refreshed?

        For each insight, provide:
        - Clear observation about performance trends
        - Impact on campaign effectiveness
        - Specific timing recommendation for refresh

        Format as JSON array same structure as before.

        Pay special attention to week-over-week CTR changes."""

        try:
            response = self.client.chat.completions.create(
                model= "gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a marketing analytics expert who provides clear, actionable insight."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            insights_text = response.choices[0].message.content
            # Extract JSON from response (handle markdowb code blocks)
            if "```json" in insights_text:
                insights_text = insights_text.split("```json")[1].split('```')[0].strip()
            elif "```" in insights_text:
                insights_text = insights_text.split("```")[1].split("```")[0].strip()
            
            insights = json.loads(insights_text)

            print(f"✅ Generated {len(insights)} ad fatigue insights")
            return insights
        
        except Exception as e:
            print(f"⚠️  Error generating ad fatigue insights: {str(e)}")
            return []
    
    def generate_platform_insights(self) -> List[Dict]:
        """Generate platform-specific insights and comparisons."""
        print("\n📱 Generating platform-specific insights...")

        context = self._create_analysis_context()
        day_patterns = self.analysis['day_of_week_analysis']

        prompt = f"""You are a marketing analytics expert analyzing a brand awareness campaign.
        {context}

        DAY-OF-WEEK PATTERNS:
        {json.dumps(day_patterns, indent=2)}

        Task: Generate 2-3 actionable insigts about PLATFROM-SPECIFIC PERFORMANCE.

        Focus on:
        - Platform comparison with specific metrics
        - Strategic implication
        - Platform-specific recommendation

        Format as JSON array with same structure as before


        Include cross-platform comparisons and timing recommendations."""

        try:
            response = self.client.chat.completions.create(
                model= "gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a marketing analytics expert who provides clear, actionable insight."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            insights_text = response.choices[0].message.content
            # Extract JSON from response (handle markdowb code blocks)
            if "```json" in insights_text:
                insights_text = insights_text.split("```json")[1].split('```')[0].strip()
            elif "```" in insights_text:
                insights_text = insights_text.split("```")[1].split("```")[0].strip()
            
            insights = json.loads(insights_text)

            print(f"✅ Generated {len(insights)} platform insights")
            return insights
        
        except Exception as e:
            print(f"⚠️  Error generating platform insights: {str(e)}")
            return []
    
    def prioritize_recommendations(self) -> List[Dict]:
        """Use AI to prioritize all insights by business impact."""
        print("\n🎯 Prioritizing recommendations...")

        all_insights = (
            self.insights['budget_efficiency'] + 
            self.insights['creative_performance'] +
            self.insights['ad_fatigue'] +
            self.insights['platform_insights']
        )

        prompt = f"""You are a marketing director reviewing these insights from your campaign analysis:
        {json.dumps(all_insights, indent=2)}

        Task: Select the TOP 5 MOST IMPORTANT  recommendations and rank them by:
        1. Potential business impact (revenue, cost savings)
        2. Urgency (how quickly action is needed)
        3.  Ease of implementation

        Return ONLY the top 5 as a JSON array, adding an 'estimated_impact' field describing potential outcomes.

        Format:
        [
        {{
            "rank": 1,
            "insight": "...",
            "recommendation": "...",
            "estimated_impact": "Specific outcome (e.g., 'Could save $X' or 'Increase CTR by Y%')",
            "urgency": "immediate/this_week/next_week"
        }}]
        """
        try:
            response = self.client.chat.completions.create(
                model= "gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a strategic marketing director."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            insights_text = response.choices[0].message.content
            # Extract JSON from response (handle markdowb code blocks)
            if "```json" in insights_text:
                insights_text = insights_text.split("```json")[1].split('```')[0].strip()
            elif "```" in insights_text:
                insights_text = insights_text.split("```")[1].split("```")[0].strip()
            
            insights = json.loads(insights_text)

            print(f"✅ Prioritized top {len(insights)} recommendations")
            return insights
        
        except Exception as e:
            print(f"⚠️  Error prioritizing recommendations: {str(e)}")
            return []
    
    def run(self) -> Dict:
        """Execute complete insight generation pipeline."""
        print("🚀 Starting Insight Generator Agent...")
        print("=" * 60)

        # Generate insights for each category
        self.insights['budget_efficiency'] = self.generate_budget_efficiency_insight()
        self.insights['creative_performance'] = self.generate_creative_performance_insights()
        self.insights['ad_fatigue'] = self.generate_ad_fatigue_insights()
        self.insights['platform_insights'] = self.generate_platform_insights()

        # Prioritize all recommendations
        self.insights['priority_recommendations'] = self.prioritize_recommendations()

        # Add metadata
        self.insights['metadata'] = {
            'generated_at':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_insights': sum([
                len(self.insights['budget_efficiency']),
                len(self.insights['creative_performance']),
                len(self.insights['ad_fatigue']),
                len(self.insights['platform_insights'])
            ])
        }

        print("\n"+"="*60)
        print("✅ INSIGHT GENERATION COMPLETE")
        print("="*60)
        print(f"\n📊 Total insights generated: {self.insights['metadata']['total_insights']}")
        print(f"🎯 Priority recommendations: {len(self.insights['priority_recommendations'])}")

        return self.insights

    def save_insights(self, output_path: str = 'data/processed/insights.json'):
        """Save insights to JSON file."""
        if not self.insights:
            raise Exception("No insights to save. Run analysis first.")
        
        with open(output_path, 'w') as f:
            json.dump(self.insights, f, indent=2)
        
        print(f"\n💾 Insights saved to: {output_path}")
    
