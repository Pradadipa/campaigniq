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
    def __init__(self, performance_analysis: Dict, insights: Dict, processed_data: pd.Dataframe):
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
        self._rander_header()

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
                'Platform': platform_data.replace('_', ' ').title(),
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
        fig_efficiency = go.Figure
