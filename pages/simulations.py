"""
Simulations Page - Run Monte Carlo simulations and analyze results
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from components import render_header, render_stat_card, render_simulation_progress
from utils.charts import create_monte_carlo_distribution, create_trend_chart
from config import SPORTS


def render_simulations_page():
    """Render the simulations page"""

    render_header(
        title="🔬 Simulations",
        subtitle="Run Monte Carlo simulations and analyze probability distributions"
    )

    # Overview stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card(
            title="Default Simulations",
            value="10,000",
            icon="🎲",
            color="#0078D4"
        )

    with col2:
        render_stat_card(
            title="Avg Runtime",
            value="2.3s",
            icon="⏱️",
            color="#4CAF50"
        )

    with col3:
        render_stat_card(
            title="Today's Runs",
            value="156",
            icon="📊",
            color="#FF9800"
        )

    with col4:
        render_stat_card(
            title="Queue",
            value="0",
            icon="📋",
            color="#9C27B0"
        )

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Run Simulation", "📊 Results History", "⚙️ Settings"])

    with tab1:
        render_simulation_runner()

    with tab2:
        render_simulation_history()

    with tab3:
        render_simulation_settings()


def render_simulation_runner():
    """Render simulation runner section"""

    st.markdown("### Configure Simulation")

    col1, col2 = st.columns(2)

    with col1:
        # Sport selection
        sport = st.selectbox(
            "Select Sport",
            ["NFL", "NBA", "MLB", "NHL"],
            key="sim_sport"
        )

        # Game selection (sample data)
        games = {
            "NFL": ["Chiefs vs Bills", "Eagles vs Cowboys", "49ers vs Seahawks"],
            "NBA": ["Celtics vs Heat", "Nuggets vs Lakers", "Bucks vs 76ers"],
            "MLB": ["Yankees vs Red Sox", "Dodgers vs Giants", "Astros vs Rangers"],
            "NHL": ["Avalanche vs Knights", "Maple Leafs vs Canadiens", "Bruins vs Rangers"]
        }

        game = st.selectbox(
            "Select Game",
            games.get(sport, []),
            key="sim_game"
        )

    with col2:
        # Simulation parameters
        n_simulations = st.number_input(
            "Number of Simulations",
            min_value=1000,
            max_value=100000,
            value=10000,
            step=1000,
            key="sim_count"
        )

        confidence_level = st.slider(
            "Confidence Interval (%)",
            min_value=80,
            max_value=99,
            value=95,
            key="sim_confidence"
        )

    st.markdown("---")

    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.checkbox("Include home advantage adjustment", value=True)
            st.checkbox("Account for injuries", value=True)

        with col2:
            st.checkbox("Include weather factors", value=False)
            st.checkbox("Use recent form weighting", value=True)

        with col3:
            st.number_input("Random seed (0 for random)", value=0, min_value=0, max_value=99999)
            st.selectbox("Distribution type", ["Normal", "Student-t", "Bootstrap"])

    st.markdown("---")

    # Run simulation
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        run_button = st.button("🚀 Run Simulation", type="primary", key="run_sim")

    with col2:
        if st.button("📋 Add to Queue", key="queue_sim"):
            st.success("Added to queue")

    if run_button or st.session_state.get('sim_running', False):
        st.session_state.sim_running = True

        # Show progress
        st.markdown("### Simulation Progress")

        progress_bar = st.progress(0)
        status_text = st.empty()

        # Simulate progress (in real app, this would be async)
        import time
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"Running simulation... {i+1}% ({(i+1) * n_simulations // 100:,} / {n_simulations:,})")
            if i < 99:
                time.sleep(0.02)

        st.session_state.sim_running = False

        # Show results
        st.markdown("### Simulation Results")

        # Generate sample results
        teams = game.split(" vs ")
        home_team = teams[0] if len(teams) > 1 else "Home"
        away_team = teams[1] if len(teams) > 1 else "Away"

        # Generate simulation data
        np.random.seed(42)
        point_diffs = np.random.normal(3.5, 12, n_simulations)
        home_wins = (point_diffs > 0).sum()
        home_win_prob = home_wins / n_simulations

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            render_stat_card(
                title=f"{home_team} Win %",
                value=f"{home_win_prob*100:.1f}%",
                icon="📊",
                color="#4CAF50" if home_win_prob > 0.5 else "#F44336"
            )

        with col2:
            render_stat_card(
                title=f"{away_team} Win %",
                value=f"{(1-home_win_prob)*100:.1f}%",
                icon="📊",
                color="#4CAF50" if home_win_prob < 0.5 else "#F44336"
            )

        with col3:
            render_stat_card(
                title="Mean Margin",
                value=f"{point_diffs.mean():+.1f}",
                icon="📈",
                color="#0078D4"
            )

        with col4:
            render_stat_card(
                title="Std Dev",
                value=f"{point_diffs.std():.1f}",
                icon="📉",
                color="#FF9800"
            )

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # Distribution chart
        st.markdown("**Score Differential Distribution**")
        dist_fig = create_monte_carlo_distribution(point_diffs.tolist(), home_team, away_team)
        st.plotly_chart(dist_fig, width="stretch", config={'displayModeBar': False})

        # Detailed stats
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Summary Statistics**")

            stats_df = pd.DataFrame({
                'Statistic': ['Mean', 'Median', 'Std Dev', '5th Percentile', '95th Percentile',
                              'Min', 'Max', 'Skewness'],
                'Value': [
                    f"{point_diffs.mean():.2f}",
                    f"{np.median(point_diffs):.2f}",
                    f"{point_diffs.std():.2f}",
                    f"{np.percentile(point_diffs, 5):.2f}",
                    f"{np.percentile(point_diffs, 95):.2f}",
                    f"{point_diffs.min():.2f}",
                    f"{point_diffs.max():.2f}",
                    f"{pd.Series(point_diffs).skew():.3f}"
                ]
            })
            st.dataframe(stats_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("**Win Probability Breakdown**")

            prob_df = pd.DataFrame({
                'Outcome': [f'{home_team} by 10+', f'{home_team} by 1-10',
                            f'{away_team} by 1-10', f'{away_team} by 10+'],
                'Probability': [
                    f"{(point_diffs > 10).sum() / n_simulations * 100:.1f}%",
                    f"{((point_diffs > 0) & (point_diffs <= 10)).sum() / n_simulations * 100:.1f}%",
                    f"{((point_diffs < 0) & (point_diffs >= -10)).sum() / n_simulations * 100:.1f}%",
                    f"{(point_diffs < -10).sum() / n_simulations * 100:.1f}%"
                ],
                'Count': [
                    (point_diffs > 10).sum(),
                    ((point_diffs > 0) & (point_diffs <= 10)).sum(),
                    ((point_diffs < 0) & (point_diffs >= -10)).sum(),
                    (point_diffs < -10).sum()
                ]
            })
            st.dataframe(prob_df, use_container_width=True, hide_index=True)

        # Export results
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 4])

        with col1:
            results_csv = pd.DataFrame({'point_diff': point_diffs}).to_csv(index=False)
            st.download_button(
                label="📥 Export CSV",
                data=results_csv,
                file_name=f"simulation_{game.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

        with col2:
            st.button("📊 Save to Dashboard")


def render_simulation_history():
    """Render simulation history section"""

    st.markdown("### Recent Simulations")

    # Filter options
    col1, col2, col3 = st.columns(3)

    with col1:
        st.selectbox("Filter by Sport", ["All", "NFL", "NBA", "MLB", "NHL"], key="hist_sport")

    with col2:
        st.date_input("From Date", value=datetime.now(), key="hist_date")

    with col3:
        st.selectbox("Sort By", ["Most Recent", "Highest Confidence", "Lowest Confidence"], key="hist_sort")

    st.markdown("---")

    # History table
    history_data = pd.DataFrame({
        'Date': [datetime.now().strftime('%Y-%m-%d %H:%M')] * 10,
        'Sport': ['NFL', 'NBA', 'NFL', 'NHL', 'NBA', 'MLB', 'NFL', 'NBA', 'NHL', 'MLB'],
        'Game': ['Chiefs vs Bills', 'Celtics vs Heat', 'Eagles vs Cowboys', 'Avalanche vs Knights',
                 'Nuggets vs Lakers', 'Yankees vs Red Sox', '49ers vs Seahawks', 'Bucks vs 76ers',
                 'Maple Leafs vs Canadiens', 'Dodgers vs Giants'],
        'Simulations': [10000] * 10,
        'Home Win %': [58.2, 71.5, 62.3, 52.1, 65.8, 54.2, 55.9, 58.7, 68.2, 51.3],
        'Mean Margin': [3.5, 8.2, 5.1, 0.8, 6.3, 1.2, 2.4, 3.8, 7.1, 0.5],
        'Runtime': ['2.3s', '2.1s', '2.4s', '2.2s', '2.1s', '2.3s', '2.2s', '2.4s', '2.1s', '2.3s']
    })

    st.dataframe(
        history_data,
        width="stretch",
        hide_index=True,
        column_config={
            "Home Win %": st.column_config.ProgressColumn(
                "Home Win %",
                format="%.1f%%",
                min_value=0,
                max_value=100
            )
        }
    )

    # Pagination
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 0.5rem;">
            <button style="background: #2D2D30; border: none; color: #CCCCCC; padding: 0.5rem 1rem;
                          border-radius: 4px; cursor: pointer;">← Prev</button>
            <span style="color: #8A8A8A; padding: 0.5rem;">1 / 5</span>
            <button style="background: #2D2D30; border: none; color: #CCCCCC; padding: 0.5rem 1rem;
                          border-radius: 4px; cursor: pointer;">Next →</button>
        </div>
        """, unsafe_allow_html=True)


def render_simulation_settings():
    """Render simulation settings section"""

    st.markdown("### Default Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.number_input(
            "Default number of simulations",
            min_value=1000,
            max_value=100000,
            value=10000,
            step=1000,
            key="default_sims"
        )

        st.slider(
            "Default confidence interval (%)",
            min_value=80,
            max_value=99,
            value=95,
            key="default_ci"
        )

        st.selectbox(
            "Default distribution",
            ["Normal", "Student-t", "Bootstrap"],
            key="default_dist"
        )

    with col2:
        st.checkbox("Auto-run for new predictions", value=True, key="auto_run")
        st.checkbox("Cache simulation results", value=True, key="cache_sims")
        st.checkbox("Show detailed statistics", value=True, key="show_details")

        st.number_input(
            "Cache expiry (hours)",
            min_value=1,
            max_value=24,
            value=6,
            key="cache_expiry"
        )

    st.markdown("---")

    st.markdown("### Performance Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Computation backend",
            ["NumPy (CPU)", "CuPy (GPU)", "JAX (Accelerated)"],
            key="compute_backend"
        )

        st.number_input(
            "Parallel workers",
            min_value=1,
            max_value=16,
            value=4,
            key="workers"
        )

    with col2:
        st.checkbox("Use batch processing", value=True, key="batch_process")
        st.number_input(
            "Batch size",
            min_value=100,
            max_value=10000,
            value=1000,
            key="batch_size"
        )

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("💾 Save Settings", type="primary"):
            st.success("Settings saved!")

    with col2:
        if st.button("🔄 Reset Defaults"):
            st.info("Settings reset to defaults")
