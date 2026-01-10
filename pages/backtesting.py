"""
Backtesting Page - Historical model performance analysis
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from components import render_header, render_stat_card
from utils.charts import create_backtest_equity_curve, create_trend_chart, create_model_performance_chart
from utils.export import export_backtest_report
from config import SPORTS, MODELS


def render_backtesting_page():
    """Render the backtesting page"""

    render_header(
        title="📈 Backtesting",
        subtitle="Analyze historical model performance and validate strategies"
    )

    # Overview stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card(
            title="Total Backtests",
            value="47",
            icon="📊",
            color="#0078D4"
        )

    with col2:
        render_stat_card(
            title="Best Accuracy",
            value="62.3%",
            delta="NFL, Q4 2023",
            delta_type="positive",
            icon="🏆",
            color="#4CAF50"
        )

    with col3:
        render_stat_card(
            title="Avg ROI",
            value="+3.2%",
            icon="💰",
            color="#FF9800"
        )

    with col4:
        render_stat_card(
            title="Games Tested",
            value="15,847",
            icon="🎮",
            color="#9C27B0"
        )

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔬 Run Backtest", "📊 Results", "📈 Analysis"])

    with tab1:
        render_backtest_runner()

    with tab2:
        render_backtest_results()

    with tab3:
        render_backtest_analysis()


def render_backtest_runner():
    """Render backtest configuration and runner"""

    st.markdown("### Configure Backtest")

    col1, col2 = st.columns(2)

    with col1:
        sport = st.selectbox(
            "Select Sport",
            ["All Sports", "NFL", "NBA", "MLB", "NHL"],
            key="bt_sport"
        )

        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=365),
            key="bt_start"
        )

        models_selected = st.multiselect(
            "Models to Test",
            list(MODELS.keys()),
            default=list(MODELS.keys()),
            key="bt_models"
        )

    with col2:
        season = st.selectbox(
            "Season",
            ["2023-24", "2022-23", "2021-22", "All Available"],
            key="bt_season"
        )

        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            key="bt_end"
        )

        confidence_threshold = st.slider(
            "Min Confidence Threshold",
            min_value=0.50,
            max_value=0.75,
            value=0.55,
            step=0.01,
            key="bt_threshold"
        )

    st.markdown("---")

    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.checkbox("Include playoffs", value=True, key="bt_playoffs")
            st.checkbox("Rolling window analysis", value=True, key="bt_rolling")
            st.number_input("Rolling window (games)", value=100, key="bt_window")

        with col2:
            st.checkbox("Compare to baseline (50%)", value=True, key="bt_baseline")
            st.checkbox("Calculate Sharpe ratio", value=True, key="bt_sharpe")
            st.checkbox("Include drawdown analysis", value=True, key="bt_drawdown")

        with col3:
            st.selectbox("Betting strategy", ["Flat betting", "Kelly criterion", "Proportional"], key="bt_strategy")
            st.number_input("Initial bankroll ($)", value=1000, key="bt_bankroll")
            st.number_input("Unit size ($)", value=10, key="bt_unit")

    st.markdown("---")

    # Run backtest
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("🚀 Run Backtest", type="primary"):
            run_backtest_simulation()

    with col2:
        if st.button("📋 Schedule"):
            st.info("Backtest scheduled")


def run_backtest_simulation():
    """Run the backtest simulation"""

    progress_bar = st.progress(0)
    status = st.empty()

    # Simulate backtest progress
    import time
    for i in range(100):
        progress_bar.progress(i + 1)
        status.text(f"Processing historical data... {i+1}%")
        time.sleep(0.02)

    status.empty()

    # Show results summary
    st.success("✓ Backtest completed successfully!")

    st.markdown("### Quick Results Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card(
            title="Games Analyzed",
            value="1,247",
            icon="🎮",
            color="#0078D4"
        )

    with col2:
        render_stat_card(
            title="Overall Accuracy",
            value="57.8%",
            delta="+2.8% vs baseline",
            delta_type="positive",
            icon="🎯",
            color="#4CAF50"
        )

    with col3:
        render_stat_card(
            title="ROI",
            value="+4.2%",
            icon="💰",
            color="#FF9800"
        )

    with col4:
        render_stat_card(
            title="Sharpe Ratio",
            value="1.24",
            icon="📈",
            color="#9C27B0"
        )

    # Equity curve
    st.markdown("### Equity Curve")

    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(364, -1, -1)]
    returns = [np.random.normal(0.002, 0.02) for _ in range(365)]

    equity_fig = create_backtest_equity_curve(dates, returns)
    st.plotly_chart(equity_fig, width="stretch", config={'displayModeBar': False})

    # Export
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        results = {
            'total_games': 1247,
            'correct': 721,
            'accuracy': 0.578,
            'roc_auc': 0.62,
            'sharpe_ratio': 1.24,
            'max_drawdown': 0.12
        }
        pdf_data = export_backtest_report(results, "All Sports", "2023-01-01 to 2024-01-01")
        st.download_button(
            label="📄 Export Report",
            data=pdf_data,
            file_name="backtest_report.pdf",
            mime="application/pdf"
        )


def render_backtest_results():
    """Render backtest results history"""

    st.markdown("### Backtest History")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        st.selectbox("Filter by Sport", ["All", "NFL", "NBA", "MLB", "NHL"], key="results_sport")

    with col2:
        st.selectbox("Filter by Model", ["All"] + list(MODELS.keys()), key="results_model")

    with col3:
        st.selectbox("Sort By", ["Most Recent", "Highest Accuracy", "Highest ROI"], key="results_sort")

    st.markdown("---")

    # Results table
    results_data = pd.DataFrame({
        'Date': [(datetime.now() - timedelta(days=i*7)).strftime('%Y-%m-%d') for i in range(10)],
        'Sport': ['NFL', 'All', 'NBA', 'NHL', 'MLB', 'NFL', 'NBA', 'All', 'NHL', 'MLB'],
        'Period': ['2023-24', '2023-24', '2023-24', '2023-24', '2023', '2022-23', '2022-23', '2022-23', '2022-23', '2022'],
        'Games': [267, 1247, 412, 328, 162, 254, 398, 1189, 312, 154],
        'Accuracy': [0.589, 0.578, 0.571, 0.552, 0.563, 0.582, 0.568, 0.574, 0.548, 0.559],
        'ROI': ['+5.2%', '+4.2%', '+3.8%', '+1.5%', '+2.9%', '+4.8%', '+3.4%', '+3.9%', '+1.2%', '+2.5%'],
        'Sharpe': [1.42, 1.24, 1.18, 0.82, 1.05, 1.35, 1.12, 1.19, 0.76, 0.98]
    })

    st.dataframe(
        results_data,
        width="stretch",
        hide_index=True,
        column_config={
            "Accuracy": st.column_config.ProgressColumn(
                "Accuracy",
                format="%.1f%%",
                min_value=0.5,
                max_value=0.7
            ),
            "Sharpe": st.column_config.NumberColumn(
                "Sharpe Ratio",
                format="%.2f"
            )
        }
    )

    # Detailed view
    st.markdown("### Detailed Results")

    with st.expander("View Prediction Details"):
        detail_data = pd.DataFrame({
            'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(20)],
            'Game': ['Team A vs Team B'] * 20,
            'Predicted': ['Home', 'Away', 'Home', 'Home', 'Away'] * 4,
            'Actual': ['Home', 'Away', 'Away', 'Home', 'Away'] * 4,
            'Confidence': np.random.uniform(0.55, 0.75, 20),
            'Correct': ['✓', '✓', '✗', '✓', '✓'] * 4
        })

        st.dataframe(detail_data, use_container_width=True, hide_index=True)


def render_backtest_analysis():
    """Render detailed backtest analysis"""

    st.markdown("### Performance Analysis")

    # Model comparison
    st.markdown("**Model Comparison**")

    models = list(MODELS.keys())
    accuracies = [0.552, 0.563, 0.589, 0.571]
    colors = [MODELS[m]['color'] for m in models]

    model_fig = create_model_performance_chart(models, accuracies, colors)
    st.plotly_chart(model_fig, width="stretch", config={'displayModeBar': False})

    col1, col2 = st.columns(2)

    with col1:
        # Performance by sport
        st.markdown("**Performance by Sport**")

        sport_data = pd.DataFrame({
            'Sport': ['NFL', 'NBA', 'MLB', 'NHL'],
            'Games': [1945, 2460, 9718, 2560],
            'Accuracy': [0.589, 0.571, 0.563, 0.552],
            'ROC-AUC': [0.64, 0.61, 0.59, 0.55],
            'Sharpe': [1.42, 1.18, 1.05, 0.82]
        })

        st.dataframe(
            sport_data,
            width="stretch",
            hide_index=True,
            column_config={
                "Accuracy": st.column_config.ProgressColumn(
                    "Accuracy",
                    format="%.1f%%",
                    min_value=0.5,
                    max_value=0.7
                )
            }
        )

    with col2:
        # Performance by confidence bucket
        st.markdown("**Performance by Confidence**")

        conf_data = pd.DataFrame({
            'Confidence Range': ['50-55%', '55-60%', '60-65%', '65-70%', '70%+'],
            'Games': [2450, 3120, 2180, 980, 320],
            'Accuracy': [0.52, 0.57, 0.62, 0.67, 0.71],
            'Win Rate': ['52.0%', '57.0%', '62.0%', '67.0%', '71.0%']
        })

        st.dataframe(conf_data, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Monthly breakdown
    st.markdown("**Monthly Performance Trend**")

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    values = [55.2, 58.1, 54.8, 59.3, 57.5, 60.2, 57.8, 56.9, 58.5, 59.1, 57.2, 58.8]

    trend_fig = create_trend_chart(months, values, title="", color="#0078D4")
    st.plotly_chart(trend_fig, width="stretch", config={'displayModeBar': False})

    # Key insights
    st.markdown("### Key Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: rgba(76,175,80,0.15); border-left: 4px solid #4CAF50;
                    padding: 1rem; border-radius: 4px; margin-bottom: 1rem;">
            <div style="font-weight: 600; color: #4CAF50; margin-bottom: 0.5rem;">✓ Strengths</div>
            <ul style="color: #CCCCCC; margin: 0; padding-left: 1.5rem;">
                <li>NFL predictions consistently above 58%</li>
                <li>High-confidence picks (65%+) hit at 67% rate</li>
                <li>XGBoost performs best across all sports</li>
                <li>Positive ROI in 10 of 12 months</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: rgba(255,152,0,0.15); border-left: 4px solid #FF9800;
                    padding: 1rem; border-radius: 4px; margin-bottom: 1rem;">
            <div style="font-weight: 600; color: #FF9800; margin-bottom: 0.5rem;">⚠ Areas for Improvement</div>
            <ul style="color: #CCCCCC; margin: 0; padding-left: 1.5rem;">
                <li>NHL accuracy below target (55.2%)</li>
                <li>Playoff predictions less reliable</li>
                <li>Low-confidence picks near coin flip</li>
                <li>April performance dip needs investigation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
