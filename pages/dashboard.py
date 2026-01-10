"""
Main Dashboard Page - Overview of all sports predictions
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from components import render_header, render_stat_card, render_prediction_card
from utils.charts import (
    create_accuracy_by_sport_radar,
    create_model_performance_chart,
    create_trend_chart
)
from utils.api_client import get_api_client
from config import SPORTS, MODELS


def render_dashboard():
    """Render the main dashboard page"""

    render_header(
        title="Dashboard",
        subtitle="Overview of predictions and model performance across all sports"
    )

    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card(
            title="Today's Predictions",
            value="24",
            delta="+8 from yesterday",
            delta_type="positive",
            icon="📊",
            color="#0078D4"
        )

    with col2:
        render_stat_card(
            title="Accuracy (7 Days)",
            value="57.8%",
            delta="+2.3%",
            delta_type="positive",
            icon="🎯",
            color="#4CAF50"
        )

    with col3:
        render_stat_card(
            title="Active Models",
            value="4",
            delta="All healthy",
            delta_type="positive",
            icon="🤖",
            color="#00BCF2"
        )

    with col4:
        render_stat_card(
            title="Simulations Run",
            value="10K",
            delta="Per prediction",
            delta_type="positive",
            icon="🔬",
            color="#9C27B0"
        )

    st.divider()

    # Main content area
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Today's top predictions
        st.subheader("🔥 Top Predictions Today")
        st.caption("Highest confidence picks across all sports")

        # Sample predictions (would come from API)
        predictions = [
            {
                "sport": "NFL",
                "home_team": "Kansas City Chiefs",
                "away_team": "Buffalo Bills",
                "home_prob": 0.62,
                "confidence": 0.68,
                "game_time": "Today, 8:20 PM EST",
                "home_record": "10-3",
                "away_record": "9-4"
            },
            {
                "sport": "NBA",
                "home_team": "Boston Celtics",
                "away_team": "Miami Heat",
                "home_prob": 0.71,
                "confidence": 0.72,
                "game_time": "Today, 7:30 PM EST",
                "home_record": "22-5",
                "away_record": "15-12"
            },
            {
                "sport": "NHL",
                "home_team": "Colorado Avalanche",
                "away_team": "Vegas Golden Knights",
                "home_prob": 0.55,
                "confidence": 0.58,
                "game_time": "Today, 9:00 PM EST",
                "home_record": "18-10",
                "away_record": "20-8"
            }
        ]

        for pred in predictions:
            with st.container():
                sport_icon = SPORTS.get(pred['sport'], {}).get('icon', '🏆')
                st.markdown(f"**{sport_icon} {pred['sport']}**")

                render_prediction_card(
                    home_team=pred['home_team'],
                    away_team=pred['away_team'],
                    home_prob=pred['home_prob'],
                    confidence=pred['confidence'],
                    game_time=pred['game_time'],
                    home_record=pred['home_record'],
                    away_record=pred['away_record'],
                    show_details=False
                )

    with col_right:
        # Model performance radar chart
        st.subheader("📈 Model Performance")

        # Performance by sport
        sports = ["NFL", "NBA", "MLB", "NHL"]
        accuracies = [0.589, 0.571, 0.563, 0.552]
        roc_aucs = [0.64, 0.61, 0.59, 0.55]

        radar_fig = create_accuracy_by_sport_radar(sports, accuracies, roc_aucs)
        st.plotly_chart(radar_fig, width="stretch", config={'displayModeBar': False}, key="radar_dashboard")

        # Model weights
        st.subheader("Ensemble Weights")

        for model_name, config in MODELS.items():
            weight = config['weight']
            color = config['color']
            st.progress(weight, text=f"{model_name}: {weight*100:.0f}%")

    st.divider()

    # Historical accuracy trend
    st.subheader("📊 7-Day Accuracy Trend")

    # Generate sample trend data
    dates = [(datetime.now() - timedelta(days=i)).strftime('%m/%d') for i in range(6, -1, -1)]
    values = [55.2, 58.1, 54.8, 59.3, 57.5, 60.2, 57.8]

    trend_fig = create_trend_chart(dates, values, title="", color="#0078D4")
    st.plotly_chart(trend_fig, width="stretch", config={'displayModeBar': False}, key="trend_dashboard")

    # Sport-specific quick stats
    st.subheader("🏆 Sport Breakdown")

    col1, col2, col3, col4 = st.columns(4)

    sport_stats = [
        {"sport": "NFL", "games": 16, "accuracy": "58.9%", "icon": "🏈"},
        {"sport": "NBA", "games": 12, "accuracy": "57.1%", "icon": "🏀"},
        {"sport": "MLB", "games": 0, "accuracy": "56.3%", "icon": "⚾"},
        {"sport": "NHL", "games": 8, "accuracy": "55.2%", "icon": "🏒"}
    ]

    for col, stat in zip([col1, col2, col3, col4], sport_stats):
        with col:
            st.metric(
                label=f"{stat['icon']} {stat['sport']}",
                value=stat['accuracy'],
                delta=f"{stat['games']} games today"
            )
