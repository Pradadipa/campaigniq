"""
Agent 6: Report Composer Agent
Generates executive-ready written reports from campaign analysis and insights.
"""

import json
from typing import Dict, List
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class ReportComposerAgent:
    """
    Agent that generates professional written reports for marketing executives.
    Creates multiple report formats: Executive Summary, Detailed Analysis, Action Plan.
    """

    def __init__(self, performance_analysis: Dict, insights: Dict):
        """
        Initialize Report Composer Agent.
        
        Args:
            performance_analysis: Complete analysis from Agent 2
            insights: AI-generated insights from Agent 3
        """

        self.analysis = performance_analysis
        self.insights = insights
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.report = {}
    
    def _create_report_context(self) -> str:
        """Create comprehensive context for report generation."""

        overall = self.analysis['overall_kpis']
        platforms = self.analysis['platform_analysis']
        weekly = self.analysis['weekly_analysis']
        priority_recs = self.insights.get('priority_recommendations', [])

        context = f"""
        CAMPAIGN: BaliGlow Brand Awareness Q4 Campaign

        CAMPAIGN OVERVIEW:
        -  Duration: {overall['campaign_days']} days
        - Total Budget: ${overall['total_spend']:,.2f}
        - Total Impressions: {overall['total_impressions']:,}
        - Total Clicks: {overall['total_clicks']:,}
        - Average CTR: {overall['average_ctr']:.2%}
        - Average CPM: ${overall['average_cpm']}
        - Cost Per Click: ${overall['cost_per_click']} 

        PLATFORM PERFORMANCE:
        {json.dumps(platforms, indent=2)}

        WEEKLLY TRENDS:
        {json.dumps(weekly, indent=2)}

        TOP PRIORITY RECOMMENDATIONS:
        {json.dumps(priority_recs[:5], indent=2)}

        ALL INSIGHTS:
        Budget Efficiency: {json.dumps(self.insights.get('budget_efficiency', []), indent=2)}
        Creative Performance: {json.dumps(self.insights.get('creative_performance', []), indent=2)}
        Ad Fatigue: {json.dumps(self.insights.get('ad_fatigue', []), indent=2)}
        Platform Insights: {json.dumps(self.insights.get('platform_insights', []), indent=2)}
        """

        return context
    
    def generate_executive_summary(self) -> str:
        """Generate a concise executive summary (1 page)."""
        print("\n📄 Generating executive summary...")

        context = self._create_report_context()

        prompt = f"""You are a marketing analytics director writing an executive summary for the CEO and marketing director.
        
        CAMPAIGN DATA:
        {context}

        TASK: Write a concise, profesional executive summary (300-400 words) that covers:

        1. Campaign Overview (2-3 sentences)
            - Campaign objective, duration, budget
        
        2. Key Performance Highlights (3-4 bullet points)
            - Most important metrics and achievements
            - Use specific numbers
        
        3. Critical Findings (2-3 bullet points)
            - Most important insights (both positive and concerning)
            - Be specific with percentages and dollar amounts
        
        4. Top 3 Recommended Actions
            - Prioritized, actionable recommendations
            - Include estimated impact
        
        STYLE REQUIREMENTS:
            - Professional but conversational
            - Use specific numbers and percentages
            - Be direct and clear
            - No jargon - executives are busy
            - Focus on business impact, not technical details
            - Use markdown formatting (headers, bold, bullets)

        Start with: # Executive Summary - BaliGlow Branc Awareness Campaign"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system", "content":"You are a senior marketing analytics director writing for C-level executives."},
                    {"role":"user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            summary = response.choices[0].message.content

            print(f"✅ Executive summary generated ({len(summary)} characters)")
            return summary
        
        except Exception as e:
            print(f"❌ Error generating executive summary: {str(e)}")
            return ""
    
    def generate_detailed_analysis(self) -> str:
        """Generate detailed analytical report (2-3 pages)."""
        print("\n📊 Generating detailed analysis report...")

        context = self._create_report_context()

        prompt = f"""You are a marketing analyst writing a detailed performance report for the marketing team.

        CAMPAIGN DATA:
        {context}

        TASK: Write a comprehensive analysis report (800-1000 words) with these sections:

        ## 1. Campaign Performance Overview
        - Overall metrics and performance against typical benchmarks
        - Key achievements and concerns

        ## 2. Platform Analysis
        - Performance comparison across Google Display, Meta, and TikTok
        - Which platform delivered best ROI
        - Platform-specific insights

        ## 3. Performance Trends
        - Week-over-week analysis
        - When Performance peaked/declined
        - Ad fatigue indicators

        ## 4. Creative Performance
        - Top performing vs underperforming creatives
        - Creative recommendations
        
        ## 5. Budget Efficiency Analysis
        - Cost efficiency by platform
        - Budget allocation recommendations
        - Potential savings/optimizations

        STYLE REQUIREMENTS:
        - Detailed but readable
        - Use specific data points and percentages
        - Include comparisons (e.g., "TikTok delivered 2.7x better CTR than Meta")
        - Use markdown formatting with clear headers
        - Each section should have 2-4 paragraphs
        - Professional tone for marketing professionals
        
        Start with: # Detailed Campaign Analysis - BaliGlow Q4 Brand Awareness"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system", "content":"You are a marketing analyst writing detailed performance reports."},
                    {"role":"user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )

            summary = response.choices[0].message.content

            print(f"✅ Detailed Analysis generated ({len(summary)} characters)")
            return summary
        
        except Exception as e:
            print(f"❌ Error generating detailed Analysis: {str(e)}")
            return ""
    
    def generate_action_plan(self) -> str:
        """Generate actionable recommendations report."""
        print("\n🎯 Generating action plan...")

        context = self._create_report_context

        prompt = f"""You are a marketing strategist creating an action plan based on campaign analysis.

        CAMPAIGN DATA:
        {context}

        TASK: Create a prioritized action plan (500-600 words) with:

        ## Immediate Actions (This Week)
        For each actions:
        - Clear, specific action item
        - Expected impact (with number if possible)
        - Estimated effort/resources needed
        - Owner/responsibility

        ## Short-term Actions (Next 2-4 Weeks)
        Same format as above

        ## Strategic Recommendations (Next Quarter)
        Longer-term strategic moves based on findings

        STYLE REQUIREMENTS:
        - Action-oriented language (start with verbs: "Pause...", "Reallocate...", "Test...")
        - Specific and measurable
        - Include estimated impact where possible
        - Prioritized by urgency and impact
        - Use markdown with clear sections and bullet points
        - Professional but direct tone

        Start with: # Action Plan - BaliGlow Campaign Optimizations"""
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a marketing strategist creating actionable plans."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            action_plan = response.choices[0].message.content
            
            print(f"✅ Action plan generated ({len(action_plan)} characters)")
            return action_plan
            
        except Exception as e:
            print(f"❌ Error generating action plan: {str(e)}")
            return ""
    
    def generate_client_report(self) -> str:
        """Generate client-facing report (simplified, positive tone)."""
        print("\n👥 Generating client-facing report...")

        context = self._create_report_context

        prompt = f"""You are writing a report for the client (BaliGlow brand owner) who is not a marketing expert.

        CAMPAIGN DATA:
        {context}

        TASK: Write a client-friendly report (400-500 words) that:

        ## Campaign Results
        - What we achieved
        - Highlight positive outcomes
        - Use simple language (avoid marketing jargon)

        ## What's Working Well
        - Celebrate successes
        - Show ROI and value

        ## Opportunities for improvement
        - Frame constructively (not as failures)
        - Focus on growth opportunities

        ## Recomended Next Steps
        - Clear, simple recommendations
        - Focus on business outcomes

        STYLE REQUIREMENTS:
        - Warm, positive, professional tone
        - Avoid technical jargon
        - Use analogies if helpful
        - Focus on business value, not marketing metrics
        - Be encouraging while honest about areas to improve
        - Use markdown formatting

        Start with: # BaliGlow Campaign Performance Report"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a marketing consultant communicating with a non-technical client."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=900
            )
            
            client_report = response.choices[0].message.content
            
            print(f"✅ Client report generated ({len(client_report)} characters)")
            return client_report
            
        except Exception as e:
            print(f"❌ Error generating client report: {str(e)}")
            return ""
    
    def run(self) -> Dict[str, str]:
        """Generate all report types."""
        print("🚀 Starting Report Composer Agent...")
        print("=" * 60)
        print("⏳ Generating 4 different report formats...")
        print("   This will take 60-90 seconds (4 AI calls)")
        print("")

        # Generate all reports
        self.reports = {
            'executive_summary': self.generate_executive_summary(),
            'detailed_analysis': self.generate_detailed_analysis(),
            'action_plan': self.generate_action_plan(),
            'client_report': self.generate_client_report(),
            'metadata': {
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'campaign_name': 'BaliGlow Brand Awareness Q4'
            }
        }

        print("\n" + "=" * 60)
        print("✅ REPORT GENERATION COMPLETE")
        print("=" * 60)
        print(f"\n📊 Generated {len([k for k in self.reports.keys() if k != 'metadata'])} report formats")
        
        return self.reports
    
    def save_reports(self, output_dir: str = 'data/outputs/reports'):
        """Save all reports to separate files."""
        import os

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        if not self.reports:
            raise Exception("No reports to save. Run generation first.")
        
        # Save each report type
        report_files = {}

        for report_type, content in self.reports.items():
            if report_type == 'metadata':
                continue

            filename = f"{report_type}.md"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            report_files[report_type] = filepath
            print(f"💾 Saved: {filepath}")
        
        # Save combined report
        combined_path = os.path.join(output_dir, 'complete_report.md')
        with open(combined_path, 'w', encoding='utf-8') as f:
            f.write("# CampaignIQ Complete Report\n\n")
            f.write(f"Generated: {self.reports['metadata']['generated_at']}\n\n")
            f.write("---\n\n")

            for report_type, content in self.reports.items():
                if report_type == 'metadata':
                    continue
                f.write(content)
                f.write("\n\n--\n\n")
        
        report_files['complete_report'] = combined_path
        print(f"💾 Saved: {combined_path}")

        # Save as JSOn for programmatic access
        json_path = os.path.join(output_dir, 'reports.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2)
        print(f"💾 Saved: {json_path}")

        f"💾 Saved: {json_path}"