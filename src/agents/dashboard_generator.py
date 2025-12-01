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