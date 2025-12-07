"""
Agent 5: Dashboard Generator Agent
Directly builds an interactive Streamlit dashboard from campaign analysis and insights.
"""

import streamlit as st 
import plotly.express as px 
import plotly.graph_objects as go 
import pandas as pd 
from typing import Dict
from datetime import datetime

class DashboardGeneratorAgent:
    """
    Agent that directly builds and displays an interactive Streamlit dashboard.
    Visualizes campaign performance, trends, and AI-generated insights.
    """
    def __init__(self, performance_analysis: Dict, insights: Dict, processed_data: pd.DataFrame):
        """
        Initialize Dashboard Generator Agent.
        
        Args:
            performance_analysis: Complete analysis from Agent 2
            insights: AI-generated insights from Agent 3
            processed_data: Processed campaign data from Agent 1
        """
        self.analysis = performance_analysis
        self.insights = insights
        self.data = processed_data

    def build_dashboard(self):
        """Build and display the complete Streamlit dashboard."""

        # Page configuration
        st.set_page_config(
            page_title="CampaignIQ Dashboard",
            page_icon="🎯",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Custom CSS
        st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stMetric {
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #333;
        }
        h1 {
            color: #00d4ff;
            padding-bottom: 20px;
        }
        h2 {
            color: #00d4ff;
            padding-top: 20px;
        }
        .insight-box {
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #00d4ff;
            margin: 10px 0;
        } 
        </style>
        """, unsafe_allow_html=True)

        # Header
        self._render_header()

        # Executive Summary (KPI Cards)
        self._render_kpi_cards()

        # Main content in tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Performance Trends", 
            "🎯 Platform Analysis", 
            "🎨 Creative Performance",
            "💡 AI Insights"
        ])

        with tab1:
            self._render_performance_trends()
        
        with tab2:
            self._render_platform_analysis()

        with tab3:
            self._render_creative_performance()
        
        with tab4:
            self._render_ai_insights()
    
    def _render_header(self):
        """Render dashboard header"""
        col1, col2 = st.columns([3,1])

        with col1:
            st.title("🎯 CampaignIQ Dashboard")
            st.markdown("**BaliGlow Brand Awareness Campaign**")
        
        with col2:
            overall = self.analysis['overall_kpis']
            date_range = self.analysis.get('data_quality', {}).get('date_range', {})
            start = date_range.get('start', 'N/A')
            end = date_range.get('end', 'N/A')
            st.metric("Campaign Duration", f"{overall['campaign_days']} days")
            st.caption(f"📅 {start} to {end}")
    
    def _render_kpi_cards(self):
        """Render KPI metrics cards."""
        st.markdown("---")
        st.subheader("📊 Executive Summary")

        overall = self.analysis['overall_kpis']

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Impressions",
                f"{overall['total_impressions']:,}",
                help="Total number of times ads were displayed"
            )
        
        with col2:
            st.metric(
                "Total Clicks",
                f"{overall['total_clicks']:,}",
                help="Total clicks across all platforms"
            )
        
        with col3:
            st.metric(
                "Total Spend",
                f"{overall['total_spend']:,.2f}",
                help="Total campaign budget spent"
            )

        with col4:
            st.metric(
                "Average CTR",
                f"{overall['average_ctr']:.2%}",
                help="Average click-through rate"
            )

        # Second row of metrics
        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.metric(
                "Average CPM",
                f"${overall['average_cpm']:.2f}",
                help="Average cost per thousand impressions"
            )
        
        with col6:
            st.metric(
                "Cost Per Click",
                f"${overall['cost_per_click']:.2f}",
                help="Average cost per click"
            )
        
        with col7:
            st.metric(
                "Total Reach",
                f"{overall['total_reach']:,}",
                help="Unique users reached"
            )
        
        with col8:
            st.metric(
                "Frequency",
                f"{overall['frequency']:.2f}",
                help="Average times each user saw ads"
            )
    
    def _render_performance_trends(self):
        """Render weekly performance trends."""
        st.markdown("### 📈 Week-over-Week Performance")

        # Prepare weekly data
        weekly_data = []
        for week_key, week_data in sorted(self.analysis['weekly_analysis'].items()):
            weekly_data.append({
                'Week': f"Week {week_data['week_number']}",
                'CTR': week_data['avg_ctr'] * 100,
                'CPM': week_data['avg_cpm'],
                'Engagement Rate': week_data['avg_engagement_rate'] * 100,
                'Spend': week_data['spend']
            })
        df_weekly = pd.DataFrame(weekly_data)

        # CTR Trend Chart
        st.markdown('#### Click-Through Rate Trend')
        fig_ctr = go.Figure()
        fig_ctr.add_trace(go.Scatter(
            x=df_weekly['Week'],
            y=df_weekly['CTR'],
            mode='lines+markers',
            name='CTR',
            line=dict(color='#00d4ff', width=3),
            marker=dict(size=10)
        ))
        fig_ctr.update_layout(
            xaxis_title="Week",
            yaxis_title="CTR (%)",
            template="plotly_dark",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_ctr, use_container_width=True)

        # CPM and Spend trends
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('#### CPM Trend')
            fig_cpm = px.line(
                df_weekly,
                x='Week',
                y='CPM',
                markers=True,
                template="plotly_dark"
            )
            fig_cpm.update_traces(line_color='#ff6b6b')
            st.plotly_chart(fig_cpm, use_container_width=True)

        with col2:
            st.markdown('#### Weekly Spend')
            fig_spend = px.bar(
                df_weekly,
                x='Week',
                y='Spend',
                template="plotly_dark"
            )
            fig_spend.update_traces(marker_color='#51cf66')
            st.plotly_chart(fig_spend, use_container_width=True)
        
        # Weekly data table
        with st.expander("📋 View Detailed Weekly Data"):
            st.dataframe(df_weekly, use_container_width=True)
    
    def _render_platform_analysis(self):
        """Render platform comparison analysis"""
        st.markdown("### 🎯 Platform Performance Comparison")

        # Prepare platform data
        platform_data = []
        for platform, metrics in self.analysis['platform_analysis'].items():
            platform_data.append({
                'Platform': platform.replace('_', ' ').title(),
                'Impressions': metrics['impressions'],
                'Clicks': metrics['clicks'],
                'CTR (%)': metrics['avg_ctr']*100,
                'CPM ($)': metrics['avg_cpm'],
                'CPC ($)': metrics['cost_per_click'],
                'Spend ($)': metrics['spend'],
                'Engagement Rate (%)': metrics['avg_engagement_rate'] * 100
            })
        
        df_platforms = pd.DataFrame(platform_data)

        # Platform comparison charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### CTR by Platform")
            fig_ctr = px.bar(
                df_platforms,
                x='Platform',
                y='CTR (%)',
                color='Platform',
                template="plotly_dark",
                color_discrete_sequence=['#00d4ff', '#ff6b6b', '#51cf66']
            )
            fig_ctr.update_layout(showlegend=False)
            st.plotly_chart(fig_ctr, use_container_width=True)
        
        with col2:
            st.markdown("#### CPM by Platform")
            fig_cpm = px.bar(
                df_platforms,
                x='Platform',
                y='CPM ($)',
                color='Platform',
                template="plotly_dark",
                color_discrete_sequence=['#00d4ff', '#ff6b6b', '#51cf66']
            )
            fig_cpm.update_layout(showlegend=False)
            st.plotly_chart(fig_cpm, use_container_width=True)
        
        # Cost efficiency comparison
        st.markdown('#### Cost Efficiency Comparison')
        fig_efficiency = go.Figure()
        fig_efficiency.add_trace(go.Bar(
            name='CPC',
            x=df_platforms['Platform'],
            y=df_platforms['CPC ($)'],
            marker_color='#ff6b6b'
        ))
        fig_efficiency.update_layout(
            yaxis_title="Cost Per Click ($)",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig_efficiency, use_container_width=True)

        # Budget allocation
        st.markdown("#### Budget Allocation")
        fig_budget = px.pie(
            df_platforms,
            values='Spend ($)',
            names='Platform',
            template="plotly_dark",
            color_discrete_sequence=['#00d4ff', '#ff6b6b', '#51cf66']
        )
        st.plotly_chart(fig_budget, use_container_width=True)

        # Platfrom metrics table
        with st.expander("📋 View Detailed Platform Metrics"):
            st.dataframe(df_platforms, use_container_width=True)

    def _render_creative_performance(self):
        """Render creative performance analysis."""
        st.markdown("### 🎨 Creative Performance Rankings")

        # Prepare creative data
        creative_data = []
        for creative_id, metrics in self.analysis['creative_analysis'].items():
            creative_data.append({
                'Creative': creative_id,
                'Platform': metrics['platform'].replace('_', ' ').title(),
                'CTR (%)': metrics['avg_ctr']*100,
                'CPM ($)': metrics['avg_cpm'],
                'Clicks': metrics['clicks'],
                'Spend ($)': metrics['spend'],
                'Renk': metrics.get('rank_by_ctr', 0)
            })
        
        df_creatives = pd.DataFrame(creative_data)
        df_creatives = df_creatives.sort_values('CTR (%)', ascending=False)

        # Top performers
        st.markdown("#### 🏆 Top Performing Creatives")
        top_creatives = df_creatives.head(5)

        fig_top = px.bar(
            top_creatives,
            x='Creative',
            y='CTR (%)',
            color='Platform',
            template="plotly_dark",
            color_discrete_map={
                'Google Display': '#00d4ff',
                'Meta': '#ff6b6b',
                'Tiktok': '#51cf66'
            }
        )
        st.plotly_chart(fig_top, use_container_width=True)

        # Bottom performers
        st.markdown("#### ⚠️ Underperforming Creatives")
        bottom_creatives = df_creatives.tail(5)

        fig_bottom = px.bar(
            bottom_creatives,
            x='Creative',
            y='CTR (%)',
            color='Platform',
            template="plotly_dark",
            color_discrete_map={
                'Google Display': '#00d4ff',
                'Meta': '#ff6b6b',
                'Tiktok': '#51cf66'
            }
        )
        st.plotly_chart(fig_bottom, use_container_width=True)

        # Creative comparison by platform
        for platform in df_creatives['Platform'].unique():
            platform_creatives = df_creatives[df_creatives['Platform']==platform]
            
            with st.expander(f"📊 {platform} Creative Breakdown"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**CTR Comparison**")
                    fig = px.bar(
                        platform_creatives,
                        x='Creative',
                        y='CTR (%)',
                        template="plotly_dark"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("**Spend Distribution**")
                    fig = px.pie(
                        platform_creatives,
                        values='Spend ($)',
                        names='Creative',
                        template="plotly_dark"
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View All Creative Performance Data"):
            st.dataframe(df_creatives, use_container_width=True)

    def _render_ai_insights(self):
        """Render AI-generated insights and recommendations."""
        st.markdown("### 💡 AI-Powered Insights & Recommendations")

        # Priority recommendations
        st.markdown("#### 🎯 Top Priority Actions")

        priority_recs = self.insights.get('priority_recommendations', [])
        if priority_recs:
            for rec in priority_recs:
                rank = rec.get('rank', '?')
                insight = rec.get('insight', rec.get('recommendation', 'N/A'))
                action = rec.get('recommendation', rec.get('action', 'N/A'))
                impact = rec.get('estimated_impact', rec.get('impact', 'N/A'))
                urgency = rec.get('urgency', 'unknown').upper()

                # Color coding by urgency
                if urgency == 'IMMEDIATE':
                    border_color = '#ff6b6b'
                    urgency_emoji = '🔴'
                elif urgency == 'THIS_WEEK':
                    border_color = '#ffa500'
                    urgency_emoji = '🟡'
                else:
                    border_color = '#00d4ff'
                    urgency_emoji = '🟢'
                
                st.markdown(f"""
                <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; 
                            border-left: 5px solid {border_color}; margin: 15px 0;">
                    <h4 style="color: {border_color};">#{rank} {urgency_emoji} {insight}</h4>
                    <p><strong>📌 Action:</strong> {action}</p>
                    <p><strong>💰 Impact:</strong> {impact}</p>
                    <p><strong>⏰ Urgency:</strong> {urgency}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No priority recommendations available")
        
        # Category insights
        st.markdown("---")
        st.markdown("#### 📊 Insights by Category")

        insight_tabs = st.tabs([
            "💰 Budget Efficiency",
            "🎨 Creative Performance",
            "⏱️ Ad Fatigue",
            "📱 Platform Insights"
        ])

        categories = [
            ('budget_efficiency', insight_tabs[0]),
            ('creative_performance', insight_tabs[1]),
            ('ad_fatigue', insight_tabs[2]),
            ('platform_insights', insight_tabs[3])
        ]

        for category_key, tab in categories:
            with tab:
                category_insights = self.insights.get(category_key, [])

                if category_insights:
                    for i, insight in enumerate(category_insights, 1):
                        insight_text = insight.get('insight', insight.get('observation', 'N/A'))
                        impact = insight.get('impact', insight.get('business_impact', 'N/A'))
                        recommendation = insight.get('recommendation', 'N/A')
                        priority = insight.get('priority', 'medium').upper()

                        with st.expander(f"Insight {i}: {insight_text[:60]}..."):
                            st.markdown(f"**📊 Finding:** {insight_text}")
                            st.markdown(f"**💼 Impact:** {impact}")
                            st.markdown(f"**✅ Recommendation:** {recommendation}")
                            st.markdown(f"**⚡ Priority:** {priority}")
                else:
                    st.info(f"No {category_key.replace('_', ' ')} insights available")
    
    def _render_footer(self):
        """Render dashboard footer"""
        st.markdown("---")

        col1, col2, co3 = st.columns(3)

        with col1:
            st.markdown("**🤖 Powered by CampaignIQ**")
            st.caption("Multi-Agent AI Marketing Analytics System")

        with col2:
            analysis_time = self.insights.get('metadata', {}).get('generate_at', 'N/A')
            st.markdown(f"**📅 Analysis Generated**")     
            st.caption(analysis_time)

        with col3:
            total_insights = self.insights.get('metadata', {}).get('total_insights', 0)
            st.markdown(f"**💡 Total Insights**")
            st.caption(f"{total_insights} insights generated")                   


            