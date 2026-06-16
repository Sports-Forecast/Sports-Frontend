"""
Sport-specific dashboard page - Template for NBA, NFL, MLB, NHL
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from components import (
    render_header, render_stat_card, render_prediction_card,
    render_team_card, render_sport_submenu
)
from utils.charts import (
    create_probability_bar, create_team_form_chart,
    create_monte_carlo_distribution, create_odds_movement_chart,
    create_trend_chart, create_shap_waterfall
)
from utils.export import (
    export_predictions_to_csv, export_predictions_to_pdf,
    create_download_link
)
from utils.api_client import get_api_client
from config import SPORTS


def render_sport_dashboard(sport: str):
    """Render sport-specific dashboard"""

    sport_config = SPORTS.get(sport, {})
    sport_icon = sport_config.get('icon', '🏆')
    sport_color = sport_config.get('color', '#0078D4')
    sport_name = sport_config.get('name', sport)

    render_header(
        title=f"{sport_icon} {sport_name}",
        subtitle=f"Predictions and analytics for {sport_name}"
    )

    # Sport submenu
    selected_tab = render_sport_submenu(sport)

    if selected_tab == "Predictions":
        render_predictions_tab(sport, sport_color)
    elif selected_tab == "Team Analysis":
        render_team_analysis_tab(sport, sport_color)
    elif selected_tab == "Historical Data":
        render_historical_tab(sport, sport_color)
    elif selected_tab == "Live Odds":
        render_live_odds_tab(sport, sport_color)


def render_predictions_tab(sport: str, color: str):
    """Render predictions tab"""

    # Live button and Date selector row
    live_col, col1, col2, col3, col4 = st.columns([1.2, 2, 1, 1, 1])

    with live_col:
        st.write("")  # Spacer for alignment
        st.markdown('<div class="live-button-container">', unsafe_allow_html=True)
        live_clicked = st.button("🔴 LIVE", key=f"{sport}_live_btn", help="View live games with predictions")
        st.markdown('</div>', unsafe_allow_html=True)

    with col1:
        selected_date = st.date_input(
            "Select Date",
            value=datetime.now(),
            key=f"{sport}_date"
        )

    with col2:
        confidence_filter = st.selectbox(
            "Confidence",
            ["All", "High (>65%)", "Medium (55-65%)", "Low (<55%)"],
            key=f"{sport}_confidence"
        )

    with col3:
        sort_by = st.selectbox(
            "Sort By",
            ["Game Time", "Confidence", "Home Win %"],
            key=f"{sport}_sort"
        )

    with col4:
        st.write("")  # Spacer
        if st.button("🔄 Refresh", key=f"{sport}_refresh"):
            st.rerun()

    # Handle live button click
    if live_clicked:
        st.session_state[f"{sport}_show_live"] = True

    # Show live predictions if toggled
    if st.session_state.get(f"{sport}_show_live", False):
        render_live_predictions_modal(sport, color)
        return

    st.divider()

    # Fetch predictions from API for selected date (format: YYYYMMDD)
    predictions = fetch_predictions_from_api(
        sport, selected_date.strftime('%Y%m%d')
    )

    if not predictions:
        st.info(f"No {sport} games scheduled for {selected_date.strftime('%B %d, %Y')}")
        return

    # Stats summary
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card(
            title="Total Games",
            value=str(len(predictions)),
            icon="🎮",
            color=color
        )

    with col2:
        high_conf = sum(1 for p in predictions if p['confidence'] >= 0.65)
        render_stat_card(
            title="High Confidence",
            value=str(high_conf),
            icon="🎯",
            color="#4CAF50"
        )

    with col3:
        avg_conf = sum(p['confidence'] for p in predictions) / len(predictions)
        render_stat_card(
            title="Avg Confidence",
            value=f"{avg_conf*100:.1f}%",
            icon="📊",
            color="#00BCF2"
        )

    with col4:
        render_stat_card(
            title="Model",
            value="Ensemble",
            icon="🤖",
            color="#9C27B0"
        )

    st.write("")

    # Export buttons
    col_export1, col_export2, col_space = st.columns([1, 1, 4])

    with col_export1:
        csv_data = export_predictions_to_csv(predictions)
        st.download_button(
            label="📥 Export CSV",
            data=csv_data,
            file_name=f"{sport}_predictions_{selected_date.strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key=f"{sport}_csv_export"
        )

    with col_export2:
        pdf_data = export_predictions_to_pdf(
            predictions, sport, selected_date.strftime('%Y-%m-%d')
        )
        st.download_button(
            label="📄 Export PDF",
            data=pdf_data,
            file_name=f"{sport}_predictions_{selected_date.strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            key=f"{sport}_pdf_export"
        )

    st.write("")

    # Predictions grid
    for pred in predictions:
        with st.container():
            # Format spread for display
            spread_val = pred.get('spread', '')
            if isinstance(spread_val, (int, float)):
                spread_display = f"{spread_val:+.1f}"
            else:
                spread_display = spread_val

            ml = pred['moneyline_home'] if (pred['predicted_winner'] == pred['home_team_abbr']) else pred['moneyline_away']
            
            render_prediction_card(
                home_team=pred['home_team'],
                away_team=pred['away_team'],
                home_prob=pred['home_win_prob'],
                confidence=pred['confidence'],
                game_time=pred['game_time'],
                venue=pred.get('venue', ''),
                spread=spread_display,
                moneyline=ml,
                over_under=pred.get('over_under', ''),
                home_record=pred.get('home_record', ''),
                away_record=pred.get('away_record', '')
            )

            # Expandable details
            with st.expander("📊 View Detailed Analysis"):
                # Create unique key base for this game
                game_key_base = f"{sport}_{pred['home_team'].replace(' ', '_')}_{pred['away_team'].replace(' ', '_')}"

                # Tab-like sections for different analysis types
                analysis_tab1, analysis_tab2, analysis_tab3 = st.tabs([
                    "📈 Feature Impact", "⭐ Star Players", "📊 Team Form"
                ])

                with analysis_tab1:
                    detail_col1, detail_col2 = st.columns(2)

                    with detail_col1:
                        st.markdown("**Monte Carlo Simulation**")
                        mc_data = np.random.normal(
                            (pred['home_win_prob'] - 0.5) * 10, 5, 1000
                        ).tolist()
                        mc_fig = create_monte_carlo_distribution(
                            mc_data, pred['home_team'], pred['away_team']
                        )
                        st.plotly_chart(
                            mc_fig, width="stretch",
                            config={'displayModeBar': False}, key=f"mc_{game_key_base}"
                        )

                    with detail_col2:
                        st.markdown("**Feature Importance (SHAP)**")
                        # Build SHAP features from actual API data (sport-specific)
                        features, values = build_shap_features(pred, sport)
                        shap_fig = create_shap_waterfall(features, values)
                        st.plotly_chart(
                            shap_fig, width="stretch",
                            config={'displayModeBar': False}, key=f"shap_{game_key_base}"
                        )

                    # Market odds details
                    market_odds = pred.get('market_odds', {})
                    if market_odds:
                        st.markdown("---")
                        st.markdown("**Market Odds Analysis**")
                        odds_col1, odds_col2, odds_col3, odds_col4, odds_col5 = st.columns(5)
                        with odds_col1:
                            st.metric("Moneyline", ml)
                        with odds_col2:
                            spread_val = market_odds.get('spread', 'N/A')
                            st.metric("Spread", f"{spread_val:+.1f}" if isinstance(spread_val, (int, float)) else spread_val)
                        with odds_col3:
                            ou_val = market_odds.get('over_under', 'N/A')
                            st.metric("Over/Under", f"{ou_val}" if ou_val else "N/A")
                        with odds_col4:
                            spread_adj = market_odds.get('spread_adjustment', 0)
                            st.metric("Spread Impact", f"{spread_adj*100:+.2f}%")
                        with odds_col5:
                            total_adj = market_odds.get('total_adjustment', 0)
                            st.metric("Total Impact", f"{total_adj*100:+.2f}%")

                with analysis_tab2:
                    render_star_impact_section(pred, game_key_base, sport)

                with analysis_tab3:
                    render_team_form_section(pred, game_key_base, sport)


def render_team_analysis_tab(sport: str, color: str):
    """Render team analysis tab"""

    col1, col2 = st.columns([1, 3])

    with col1:
        # Team selector
        teams = get_teams_for_sport(sport)
        selected_team = st.selectbox(
            "Select Team",
            teams,
            key=f"{sport}_team_select"
        )

    st.divider()

    if selected_team:
        # Team header
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown("### 🏆")
        with col2:
            st.subheader(selected_team)
            st.caption("Season Overview")

        # Team stats
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            render_stat_card("Record", "12-5", icon="📊", color=color)
        with col2:
            render_stat_card("Win %", "70.6%", delta="+5.2%", delta_type="positive", icon="📈", color="#4CAF50")
        with col3:
            render_stat_card("Streak", "W3", icon="🔥", color="#FF9800")
        with col4:
            render_stat_card("Last 10", "7-3", icon="📅", color="#00BCF2")

        st.write("")

        # Recent form chart
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.markdown("**Recent Performance**")
            games = [f"G{i}" for i in range(1, 11)]
            results = ["W", "W", "L", "W", "W", "L", "W", "W", "W", "L"]
            point_diffs = [12, 8, -5, 15, 3, -12, 7, 20, 5, -8]
            form_fig = create_team_form_chart(games, results, point_diffs)
            st.plotly_chart(form_fig, width="stretch", config={'displayModeBar': False})

        with col_right:
            st.markdown("**Upcoming Games**")
            upcoming = [
                {"opponent": "Lakers", "date": "Dec 15", "location": "Home"},
                {"opponent": "Warriors", "date": "Dec 18", "location": "Away"},
                {"opponent": "Nets", "date": "Dec 20", "location": "Home"},
            ]
            for game in upcoming:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**vs {game['opponent']}**")
                        st.caption(game['location'])
                    with col2:
                        st.caption(game['date'])
                st.divider()


def render_historical_tab(sport: str, color: str):
    """Render historical data tab"""

    # Date range selector
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=30),
            key=f"{sport}_hist_start"
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            key=f"{sport}_hist_end"
        )

    st.divider()

    # Historical accuracy trend
    st.markdown("**Historical Accuracy Trend**")
    dates = [
        (datetime.now() - timedelta(days=i)).strftime('%m/%d')
        for i in range(29, -1, -1)
    ]
    values = [55 + np.random.uniform(-5, 8) for _ in range(30)]
    trend_fig = create_trend_chart(dates, values, title="", color=color)
    st.plotly_chart(
        trend_fig, width="stretch", config={'displayModeBar': False}
    )

    # Historical predictions table
    st.markdown("**Past Predictions**")

    # Sample historical data
    hist_dates = [
        (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        for i in range(10)
    ]
    hist_data = pd.DataFrame({
        'Date': hist_dates,
        'Home Team': ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'] * 2,
        'Away Team': ['Team X', 'Team Y', 'Team Z', 'Team W', 'Team V'] * 2,
        'Predicted': ['Home', 'Away', 'Home', 'Home', 'Away'] * 2,
        'Actual': ['Home', 'Away', 'Away', 'Home', 'Away'] * 2,
        'Confidence': [0.65, 0.72, 0.58, 0.61, 0.68, 0.55, 0.70, 0.63, 0.59, 0.66],
        'Correct': ['✓', '✓', '✗', '✓', '✓', '✓', '✓', '✓', '✗', '✓']
    })

    st.dataframe(
        hist_data,
        width="stretch",
        hide_index=True,
        column_config={
            "Confidence": st.column_config.ProgressColumn(
                "Confidence",
                format="%.0f%%",
                min_value=0,
                max_value=1
            )
        }
    )


def render_live_odds_tab(sport: str, color: str):
    """Render live odds tab"""

    st.warning(
        "Live odds tracking requires integration with a sportsbook API. "
        "Displaying sample data for demonstration."
    )

    # Sample live odds data
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Current Lines**")

        odds_data = [
            {
                "game": "Team A vs Team B", "spread": "-3.5",
                "ou": "218.5", "ml_home": "-150", "ml_away": "+130"
            },
            {
                "game": "Team C vs Team D", "spread": "+1.5",
                "ou": "224.0", "ml_home": "+110", "ml_away": "-130"
            },
            {
                "game": "Team E vs Team F", "spread": "-7.0",
                "ou": "210.5", "ml_home": "-280", "ml_away": "+230"
            },
        ]

        for odds in odds_data:
            with st.container():
                st.markdown(f"**{odds['game']}**")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Spread", odds['spread'])
                with col_b:
                    st.metric("O/U", odds['ou'])
                with col_c:
                    st.metric("ML", f"{odds['ml_home']} / {odds['ml_away']}")
                st.divider()

    with col2:
        st.markdown("**Odds Movement**")
        timestamps = ['9:00', '10:00', '11:00', '12:00', '13:00', '14:00']
        home_odds = [-145, -150, -155, -150, -155, -160]
        away_odds = [125, 130, 135, 130, 135, 140]
        odds_fig = create_odds_movement_chart(
            timestamps, home_odds, away_odds, "Home Team", "Away Team"
        )
        st.plotly_chart(odds_fig, width="stretch", config={'displayModeBar': False})


def render_live_predictions_modal(sport: str, color: str):
    """Render live predictions section with real-time game data"""
    import plotly.graph_objects as go

    # Header with back button
    col_back, col_title, col_refresh = st.columns([1, 4, 1])

    with col_back:
        if st.button("← Back", key=f"{sport}_live_back"):
            st.session_state[f"{sport}_show_live"] = False
            st.rerun()

    with col_title:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="
                    display: inline-block;
                    width: 12px;
                    height: 12px;
                    background: #F44336;
                    border-radius: 50%;
                    animation: liveBlink 1.5s ease-in-out infinite;
                "></span>
                <h2 style="margin: 0; color: white;">Live {sport} Games</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_refresh:
        if st.button("🔄", key=f"{sport}_live_refresh", help="Refresh live data"):
            st.rerun()

    st.divider()

    # Fetch live predictions from API
    api_client = get_api_client()
    result = api_client.get_live_predictions(sport)

    if not result.get("success"):
        error_msg = result.get("error", "Failed to fetch live predictions")
        st.error(f"Could not load live games: {error_msg}")
        st.info("Make sure the backend server is running and the live prediction endpoints are available.")
        return

    data = result.get("data", {})
    live_games = data.get("games", data.get("predictions", []))

    if not live_games:
        st.info(f"No live {sport} games at the moment.")
        st.caption("Live games will appear here when games are in progress.")
        return

    # Stats summary for live games
    col1, col2, col3 = st.columns(3)

    with col1:
        render_stat_card(
            title="Live Games",
            value=str(len(live_games)),
            icon="🔴",
            color="#F44336"
        )

    with col2:
        high_conf = sum(1 for g in live_games if g.get('confidence', 0) >= 0.65)
        render_stat_card(
            title="High Confidence",
            value=str(high_conf),
            icon="🎯",
            color="#4CAF50"
        )

    with col3:
        avg_conf = sum(g.get('confidence', 0.5) for g in live_games) / len(live_games) if live_games else 0
        render_stat_card(
            title="Avg Confidence",
            value=f"{avg_conf*100:.1f}%",
            icon="📊",
            color="#00BCF2"
        )

    st.write("")

    # Render each live game
    for game in live_games:
        render_live_game_card(game, sport, color)


def render_live_game_card(game: dict, sport: str, color: str):
    """Render a single live game card with prediction"""
    import plotly.graph_objects as go

    home_team = game.get("home_team", "Home Team")
    away_team = game.get("away_team", "Away Team")
    home_prob = game.get("home_win_probability", game.get("home_win_prob", 0.5))
    away_prob = 1 - home_prob
    confidence = game.get("confidence", 0.5)
    home_score = game.get("home_score", game.get("home_points", "-"))
    away_score = game.get("away_score", game.get("away_points", "-"))
    period = game.get("period", game.get("quarter", game.get("inning", "")))
    time_remaining = game.get("time_remaining", game.get("clock", ""))
    game_status = game.get("status", "In Progress")

    # Create unique key for this game
    game_key = f"{sport}_{home_team}_{away_team}".replace(" ", "_")

    with st.container():
        # Live game card with red border styling
        st.markdown('<div class="live-game-card">', unsafe_allow_html=True)

        # Game status header
        status_col1, status_col2 = st.columns([3, 1])
        with status_col1:
            period_display = f"Period {period}" if period else ""
            time_display = f" - {time_remaining}" if time_remaining else ""
            st.caption(f"🔴 LIVE {period_display}{time_display}")
        with status_col2:
            st.caption(game_status)

        # Score display
        score_col1, score_col2, score_col3 = st.columns([2, 1, 2])

        with score_col1:
            if home_prob > 0.5:
                st.markdown(f"**:green[{home_team}]**")
            else:
                st.markdown(f"**{home_team}**")
            st.markdown(f"### {home_score}")

        with score_col2:
            st.markdown(
                "<div style='text-align: center; padding-top: 15px;'><b>VS</b></div>",
                unsafe_allow_html=True
            )

        with score_col3:
            if away_prob > 0.5:
                st.markdown(f"**:green[{away_team}]**")
            else:
                st.markdown(f"**{away_team}**")
            st.markdown(f"### {away_score}")

        # Probability bar
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=[''],
            x=[home_prob * 100],
            orientation='h',
            name=home_team,
            marker_color='#4CAF50' if home_prob > 0.5 else '#666666',
            text=f"{home_team}: {home_prob*100:.1f}%",
            textposition='inside',
            insidetextanchor='start'
        ))
        fig.add_trace(go.Bar(
            y=[''],
            x=[away_prob * 100],
            orientation='h',
            name=away_team,
            marker_color='#4CAF50' if away_prob > 0.5 else '#666666',
            text=f"{away_team}: {away_prob*100:.1f}%",
            textposition='inside',
            insidetextanchor='end'
        ))
        fig.update_layout(
            barmode='stack',
            height=50,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0, 100]),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False)
        )
        st.plotly_chart(fig, width="stretch", config={'displayModeBar': False}, key=f"live_prob_{game_key}")

        # Additional live stats
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.metric("Confidence", f"{confidence*100:.1f}%")
        with stat_col2:
            spread = game.get("spread", game.get("live_spread", "N/A"))
            st.metric("Live Spread", spread if spread else "N/A")
        with stat_col3:
            over_under = game.get("over_under", game.get("total", "N/A"))
            st.metric("Over/Under", over_under if over_under else "N/A")

        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")  # Spacing between cards


def build_shap_features(pred: dict, sport: str = "NBA") -> tuple:
    """Build SHAP feature names and values from prediction data - sport-specific"""
    features = []
    values = []

    # Get common data
    team_form = pred.get('team_form', {})
    form_adjustment = team_form.get('form_adjustment', 0)
    star_impact = pred.get('star_impact', {})
    net_star_impact = star_impact.get('net_impact', 0)
    market_odds = pred.get('market_odds', {})
    spread_adjustment = market_odds.get('spread_adjustment', 0)
    total_adjustment = market_odds.get('total_adjustment', 0)
    feature_weights = pred.get('feature_weights', {})
    adjustments = pred.get('adjustments', {})

    # Calculate probability shift for direction hints
    base_prob = pred.get('base_home_probability', 0.5)
    final_prob = pred.get('home_win_prob', 0.5)
    prob_shift = final_prob - base_prob

    # ===== NFL-SPECIFIC FEATURES =====
    if sport.upper() == "NFL":
        # QB adjustment (20% weight in NFL)
        qb_adj = adjustments.get('qb_adjustment', 0)
        if qb_adj != 0:
            features.append("QB Impact")
            values.append(qb_adj)

        # Weather adjustment (5% weight)
        weather_adj = adjustments.get('weather_adjustment', 0)
        if weather_adj != 0:
            features.append("Weather")
            values.append(weather_adj)

        # Turnover adjustment (18% weight)
        turnover_adj = adjustments.get('turnover_adjustment', 0)
        if turnover_adj != 0:
            features.append("Turnover Risk")
            values.append(turnover_adj)

        # Rest adjustment (18% weight)
        rest_adj = adjustments.get('rest_adjustment', 0)
        if rest_adj != 0:
            features.append("Rest Advantage")
            values.append(rest_adj)

        # Form (36% weight)
        if form_adjustment != 0:
            features.append("Team Form")
            values.append(form_adjustment)

    # ===== MLB-SPECIFIC FEATURES =====
    elif sport.upper() == "MLB":
        # Pitcher impact (60% of variance)
        pitcher_impact = pred.get('pitcher_impact', {})
        home_pitcher_adj = pitcher_impact.get('home_starter_impact', 0)
        away_pitcher_adj = pitcher_impact.get('away_starter_impact', 0)
        net_pitcher = home_pitcher_adj - away_pitcher_adj

        if net_pitcher != 0:
            features.append("Starting Pitcher")
            values.append(net_pitcher)
        elif adjustments.get('pitcher_adjustment', 0) != 0:
            features.append("Starting Pitcher")
            values.append(adjustments.get('pitcher_adjustment', 0))

        # Bullpen impact (13%)
        bullpen_adj = adjustments.get('bullpen_adjustment', 0)
        if bullpen_adj != 0:
            features.append("Bullpen")
            values.append(bullpen_adj)

        # Team offense (19%)
        if form_adjustment != 0:
            features.append("Team Offense")
            values.append(form_adjustment)

        # Weather for outdoor games
        weather_adj = adjustments.get('weather_adjustment', 0)
        if weather_adj != 0:
            features.append("Weather")
            values.append(weather_adj)

    # ===== NHL-SPECIFIC FEATURES =====
    elif sport.upper() == "NHL":
        # Goalie impact (18% weight)
        goalie_impact = pred.get('goalie_impact', {})
        net_goalie = goalie_impact.get('net_impact', 0)
        if net_goalie != 0:
            features.append("Goalie Impact")
            values.append(net_goalie)
        elif net_star_impact != 0:
            features.append("Goalie Impact")
            values.append(net_star_impact)

        # Goal differential (32% weight)
        if form_adjustment != 0:
            features.append("Goal Differential")
            values.append(form_adjustment)

        # Special teams (18% weight)
        special_teams = pred.get('special_teams', {})
        pp_diff = special_teams.get('power_play_diff', 0)
        pk_diff = special_teams.get('penalty_kill_diff', 0)
        if pp_diff != 0 or pk_diff != 0:
            features.append("Special Teams")
            values.append((pp_diff + pk_diff) / 2 * 0.18)

    # ===== NBA-SPECIFIC FEATURES =====
    else:  # NBA default
        # Team form (70% signal)
        if form_adjustment != 0:
            features.append("Team Form")
            values.append(form_adjustment)

        # Star player impact (20%)
        if net_star_impact != 0:
            features.append("Star Players")
            values.append(net_star_impact)

        # Back-to-back penalty
        if pred.get('back_to_back_home') or pred.get('back_to_back_away'):
            b2b_penalty = -0.03 if pred.get('back_to_back_home') else 0.03
            features.append("Back-to-Back")
            values.append(b2b_penalty)

    # ===== COMMON FEATURES FOR ALL SPORTS =====
    # Market spread signal
    if spread_adjustment != 0:
        features.append("Market Spread")
        values.append(spread_adjustment)

    # Market total/over-under signal
    if total_adjustment != 0:
        features.append("Market Total")
        values.append(total_adjustment)

    # Home advantage
    home_adv_weight = feature_weights.get('home_advantage', 0.08)
    if home_adv_weight > 0:
        features.append("Home Advantage")
        values.append(home_adv_weight * (1 if prob_shift >= 0 else -0.5))

    # Ensure minimum features
    if len(features) < 3:
        rest_weight = feature_weights.get('rest_days', 0.05)
        features.append("Rest Days")
        values.append(rest_weight * (0.5 if prob_shift > 0 else -0.5))

        h2h_weight = feature_weights.get('h2h_history', 0.03)
        features.append("H2H History")
        values.append(h2h_weight * (0.5 if prob_shift > 0 else -0.5))

    # Sort by absolute value (most impactful first)
    sorted_pairs = sorted(zip(features, values), key=lambda x: abs(x[1]), reverse=True)
    features = [p[0] for p in sorted_pairs]
    values = [p[1] for p in sorted_pairs]

    return features, values


def render_star_impact_section(pred: dict, game_key_base: str, sport: str = "NBA"):
    """Render the star/key player impact section - sport-specific"""

    # Get sport-specific impact data
    star_impact = pred.get('star_impact', {})
    pitcher_impact = pred.get('pitcher_impact', {})
    goalie_impact = pred.get('goalie_impact', {})
    qb_impact = pred.get('qb_impact', {})

    # Determine section title and data based on sport
    sport_upper = sport.upper()
    if sport_upper == "NFL":
        section_title = "Quarterback Impact"
        impact_data = qb_impact if qb_impact else star_impact
        tier_labels = {1: "Elite", 2: "Above Avg", 3: "Average", 4: "Below Avg"}
        player_label = "QB"
    elif sport_upper == "MLB":
        section_title = "Starting Pitcher Impact"
        impact_data = pitcher_impact if pitcher_impact else star_impact
        tier_labels = {1: "Ace", 2: "Quality", 3: "Backend"}
        player_label = "SP"
    elif sport_upper == "NHL":
        section_title = "Goalie Impact"
        impact_data = goalie_impact if goalie_impact else star_impact
        tier_labels = {1: "Elite", 2: "Starting", 3: "Backup"}
        player_label = "G"
    else:  # NBA
        section_title = "Star Player Impact"
        impact_data = star_impact
        tier_labels = {1: "MVP", 2: "All-Star", 3: "Starter", 4: "Role"}
        player_label = "Star"

    if not impact_data:
        st.info(f"No {section_title.lower()} data available for this game.")
        return

    st.markdown(f"### {section_title}")

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        home_impact = impact_data.get('home_impact', 0)
        delta_color = "normal" if home_impact >= 0 else "inverse"
        st.metric(
            f"Home {player_label} Impact",
            f"{home_impact*100:+.1f}%",
            delta=f"{'Boost' if home_impact >= 0 else 'Penalty'}",
            delta_color=delta_color
        )
    with col2:
        away_impact = impact_data.get('away_impact', 0)
        delta_color = "normal" if away_impact >= 0 else "inverse"
        st.metric(
            f"Away {player_label} Impact",
            f"{away_impact*100:+.1f}%",
            delta=f"{'Boost' if away_impact >= 0 else 'Penalty'}",
            delta_color=delta_color
        )
    with col3:
        net_impact = impact_data.get('net_impact', 0)
        weight = impact_data.get('weight', 0.2)
        st.metric(
            "Net Impact (Home)",
            f"{net_impact*100:+.2f}%",
            delta=f"Weight: {weight*100:.0f}%"
        )

    st.markdown("---")

    # Get players list - handle different field names per sport
    home_players = (impact_data.get('home_stars', []) or
                    impact_data.get('home_qbs', []) or
                    impact_data.get('home_pitchers', []) or
                    impact_data.get('home_goalies', []) or [])
    away_players = (impact_data.get('away_stars', []) or
                    impact_data.get('away_qbs', []) or
                    impact_data.get('away_pitchers', []) or
                    impact_data.get('away_goalies', []) or [])

    player_col1, player_col2 = st.columns(2)

    with player_col1:
        st.markdown(f"**{pred.get('home_team', 'Home')}**")
        if home_players:
            for player in home_players:
                render_player_card(player, tier_labels, sport_upper)
        else:
            st.caption(f"No tracked {player_label}s")

    with player_col2:
        st.markdown(f"**{pred.get('away_team', 'Away')}**")
        if away_players:
            for player in away_players:
                render_player_card(player, tier_labels, sport_upper)
        else:
            st.caption(f"No tracked {player_label}s")

    # Sport-specific additional info
    if sport_upper == "MLB" and pitcher_impact:
        st.markdown("---")
        st.markdown("**Pitching Stats**")
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            home_era = pitcher_impact.get('home_starter_era', 'N/A')
            home_whip = pitcher_impact.get('home_starter_whip', 'N/A')
            st.caption(f"Home SP: ERA {home_era}, WHIP {home_whip}")
        with stats_col2:
            away_era = pitcher_impact.get('away_starter_era', 'N/A')
            away_whip = pitcher_impact.get('away_starter_whip', 'N/A')
            st.caption(f"Away SP: ERA {away_era}, WHIP {away_whip}")

    elif sport_upper == "NHL" and goalie_impact:
        st.markdown("---")
        st.markdown("**Goalie Stats**")
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            home_sv = goalie_impact.get('home_save_pct', 'N/A')
            home_gaa = goalie_impact.get('home_gaa', 'N/A')
            st.caption(f"Home G: SV% {home_sv}, GAA {home_gaa}")
        with stats_col2:
            away_sv = goalie_impact.get('away_save_pct', 'N/A')
            away_gaa = goalie_impact.get('away_gaa', 'N/A')
            st.caption(f"Away G: SV% {away_sv}, GAA {away_gaa}")

    elif sport_upper == "NFL" and qb_impact:
        st.markdown("---")
        st.markdown("**QB Stats**")
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            home_rating = qb_impact.get('home_passer_rating', 'N/A')
            st.caption(f"Home QB Rating: {home_rating}")
        with stats_col2:
            away_rating = qb_impact.get('away_passer_rating', 'N/A')
            st.caption(f"Away QB Rating: {away_rating}")


def render_player_card(player: dict, tier_labels: dict, sport: str):
    """Render a single player impact card"""
    status = player.get('status', 'unknown')
    status_emoji = "✅" if status == "available" else "❌" if status == "out" else "⚠️"
    tier = player.get('tier', 0)
    tier_label = tier_labels.get(tier, f"Tier {tier}")
    impact = player.get('impact_applied', player.get('impact_weight', 0))

    player_name = player.get('player_name', player.get('name', 'Unknown'))

    st.markdown(
        f"{status_emoji} **{player_name}** ({tier_label})"
    )

    # Show sport-specific stats
    if sport == "MLB":
        era = player.get('era', '')
        whip = player.get('whip', '')
        stats_str = f"ERA: {era} | WHIP: {whip}" if era else ""
        st.caption(f"Status: {status.title()} | Impact: {impact*100:+.1f}% {stats_str}")
    elif sport == "NHL":
        sv_pct = player.get('save_pct', '')
        gaa = player.get('gaa', '')
        stats_str = f"SV%: {sv_pct} | GAA: {gaa}" if sv_pct else ""
        st.caption(f"Status: {status.title()} | Impact: {impact*100:+.1f}% {stats_str}")
    elif sport == "NFL":
        rating = player.get('passer_rating', '')
        stats_str = f"Rating: {rating}" if rating else ""
        st.caption(f"Status: {status.title()} | Impact: {impact*100:+.1f}% {stats_str}")
    else:
        st.caption(f"Status: {status.title()} | Impact: {impact*100:+.1f}%")


def render_team_form_section(pred: dict, game_key_base: str, sport: str = "NBA"):
    """Render the team form section with recent performance data - sport-specific"""
    team_form = pred.get('team_form', {})
    special_teams = pred.get('special_teams', {})
    adjustments = pred.get('adjustments', {})

    if not team_form:
        st.info("No team form data available for this game.")
        return

    sport_upper = sport.upper()

    # Form adjustment summary
    form_adjustment = team_form.get('form_adjustment', 0)
    adj_direction = "favors Home" if form_adjustment > 0 else "favors Away" if form_adjustment < 0 else "neutral"

    st.metric(
        "Form Adjustment",
        f"{form_adjustment*100:+.2f}%",
        delta=adj_direction
    )

    st.markdown("---")

    # Team form details
    home_form = team_form.get('home_form', {})
    away_form = team_form.get('away_form', {})

    form_col1, form_col2 = st.columns(2)

    # Sport-specific labels
    if sport_upper == "MLB":
        diff_label = "Run Diff"
        period_short = "7"
        period_long = "10"
    elif sport_upper == "NHL":
        diff_label = "Goal Diff"
        period_short = "5"
        period_long = "10"
    else:  # NBA, NFL
        diff_label = "Pt Diff"
        period_short = "5"
        period_long = "10"

    with form_col1:
        st.markdown(f"**{pred.get('home_team', 'Home')} Recent Form**")
        if home_form:
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                record_short = home_form.get(f'record_last_{period_short}', home_form.get('record_last_5', 'N/A'))
                st.metric(f"Last {period_short}", record_short)

                # Net rating or equivalent
                if sport_upper == "NBA":
                    net_rating = home_form.get('net_rating_last_5', 0)
                    st.metric("Net Rating", f"{net_rating:+.1f}")
                elif sport_upper == "NHL":
                    xg_diff = home_form.get('xg_diff_last_5', home_form.get('goal_diff_last_5', 0))
                    st.metric("xG Diff", f"{xg_diff:+.1f}")

            with metric_col2:
                record_long = home_form.get(f'record_last_{period_long}', home_form.get('record_last_10', 'N/A'))
                st.metric(f"Last {period_long}", record_long)

                if sport_upper == "NBA":
                    net_rating_10 = home_form.get('net_rating_last_10', 0)
                    st.metric("Net Rating (10)", f"{net_rating_10:+.1f}")

            # Differential
            diff_short = home_form.get(f'point_diff_last_{period_short}',
                         home_form.get(f'goal_diff_last_{period_short}',
                         home_form.get(f'run_diff_last_{period_short}',
                         home_form.get('point_diff_last_5', 0))))
            diff_long = home_form.get(f'point_diff_last_{period_long}',
                        home_form.get(f'goal_diff_last_{period_long}',
                        home_form.get(f'run_diff_last_{period_long}',
                        home_form.get('point_diff_last_10', 0))))
            st.caption(f"{diff_label}: L{period_short}: {diff_short:+.1f} | L{period_long}: {diff_long:+.1f}")
        else:
            st.caption("No form data available")

    with form_col2:
        st.markdown(f"**{pred.get('away_team', 'Away')} Recent Form**")
        if away_form:
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                record_short = away_form.get(f'record_last_{period_short}', away_form.get('record_last_5', 'N/A'))
                st.metric(f"Last {period_short}", record_short)

                if sport_upper == "NBA":
                    net_rating = away_form.get('net_rating_last_5', 0)
                    st.metric("Net Rating", f"{net_rating:+.1f}")
                elif sport_upper == "NHL":
                    xg_diff = away_form.get('xg_diff_last_5', away_form.get('goal_diff_last_5', 0))
                    st.metric("xG Diff", f"{xg_diff:+.1f}")

            with metric_col2:
                record_long = away_form.get(f'record_last_{period_long}', away_form.get('record_last_10', 'N/A'))
                st.metric(f"Last {period_long}", record_long)

                if sport_upper == "NBA":
                    net_rating_10 = away_form.get('net_rating_last_10', 0)
                    st.metric("Net Rating (10)", f"{net_rating_10:+.1f}")

            diff_short = away_form.get(f'point_diff_last_{period_short}',
                         away_form.get(f'goal_diff_last_{period_short}',
                         away_form.get(f'run_diff_last_{period_short}',
                         away_form.get('point_diff_last_5', 0))))
            diff_long = away_form.get(f'point_diff_last_{period_long}',
                        away_form.get(f'goal_diff_last_{period_long}',
                        away_form.get(f'run_diff_last_{period_long}',
                        away_form.get('point_diff_last_10', 0))))
            st.caption(f"{diff_label}: L{period_short}: {diff_short:+.1f} | L{period_long}: {diff_long:+.1f}")
        else:
            st.caption("No form data available")

    # Sport-specific additional sections
    if sport_upper == "NHL" and (special_teams or home_form.get('power_play')):
        st.markdown("---")
        st.markdown("**Special Teams**")
        st_col1, st_col2 = st.columns(2)
        with st_col1:
            home_pp = home_form.get('power_play', special_teams.get('home_pp', 'N/A'))
            home_pk = home_form.get('penalty_kill', special_teams.get('home_pk', 'N/A'))
            st.caption(f"Home - PP: {home_pp}% | PK: {home_pk}%")
        with st_col2:
            away_pp = away_form.get('power_play', special_teams.get('away_pp', 'N/A'))
            away_pk = away_form.get('penalty_kill', special_teams.get('away_pk', 'N/A'))
            st.caption(f"Away - PP: {away_pp}% | PK: {away_pk}%")

    elif sport_upper == "MLB":
        st.markdown("---")
        st.markdown("**Offensive Stats**")
        off_col1, off_col2 = st.columns(2)
        with off_col1:
            runs_7 = home_form.get('runs_last_7', 'N/A')
            st.caption(f"Home - Runs/G (L7): {runs_7}")
        with off_col2:
            runs_7 = away_form.get('runs_last_7', 'N/A')
            st.caption(f"Away - Runs/G (L7): {runs_7}")

    elif sport_upper == "NFL":
        # Show turnover and rest info for NFL
        st.markdown("---")
        st.markdown("**Schedule & Turnovers**")
        nfl_col1, nfl_col2 = st.columns(2)
        with nfl_col1:
            turnover_adj = adjustments.get('turnover_adjustment', 0)
            st.metric("Turnover Adj", f"{turnover_adj*100:+.2f}%")
        with nfl_col2:
            rest_adj = adjustments.get('rest_adjustment', 0)
            st.metric("Rest Adj", f"{rest_adj*100:+.2f}%")

        # Weather if available
        weather_adj = adjustments.get('weather_adjustment', 0)
        if weather_adj != 0:
            st.caption(f"Weather Impact: {weather_adj*100:+.2f}%")


def fetch_predictions_from_api(sport: str, date: str = None):
    """Fetch predictions from the backend API for a specific date"""
    api_client = get_api_client()

    # Map sport to API endpoint
    sport_lower = sport.lower()
    if sport_lower == "nfl":
        result = api_client.get_nfl_predictions(date)
    elif sport_lower == "nba":
        # NBA uses full parameters: include_players, include_form, force_refresh
        result = api_client.get_nba_predictions(
            date=date,
            include_players=True,
            include_form=True,
            force_refresh=False
        )
    elif sport_lower == "mlb":
        result = api_client.get_mlb_predictions(date)
    elif sport_lower == "nhl":
        result = api_client.get_nhl_predictions(date)
    else:
        result = {"success": False, "error": "Unknown sport"}

    if result.get("success") and result.get("data"):
        data = result["data"]
        # Handle both direct list and nested predictions key
        predictions = data.get("predictions", data) if isinstance(data, dict) else data

        if isinstance(predictions, list):
            # Transform API response to match expected format
            transformed = []

            # Parse the selected date for filtering (format: YYYYMMDD)
            selected_date_str = date if date else ""

            for pred in predictions:
                # Filter by game_date to only show games on the selected date
                game_date_str = pred.get("game_date", "")
                if game_date_str and selected_date_str:
                    # game_date format: "2026-01-10T18:00:00"
                    # Extract just the date part (YYYY-MM-DD) and convert to YYYYMMDD
                    game_date_only = game_date_str.split("T")[0].replace("-", "")
                    if game_date_only != selected_date_str:
                        # Skip games that don't match the selected date
                        continue

                home_prob = pred.get(
                    "home_win_probability", pred.get("home_win_prob", 0.5)
                )
                game_time = pred.get(
                    "game_time", pred.get("commence_time", "")
                )
                # If no game_time, format from game_date
                if not game_time and game_date_str:
                    try:
                        from datetime import datetime as dt
                        game_dt = dt.fromisoformat(game_date_str.replace("Z", ""))
                        game_time = game_dt.strftime("%I:%M %p UTC")
                    except Exception:
                        game_time = game_date_str

                # Extract market odds data
                market_odds = pred.get("market_odds", {})
                moneyline_home = market_odds.get("moneyline_home", "")
                moneyline_away = market_odds.get("moneyline_away", "")
                spread = market_odds.get("spread", pred.get("spread", ""))
                over_under = market_odds.get("over_under", pred.get("over_under", pred.get("total", "")))

                # Extract star impact data
                star_impact = pred.get("star_impact", {})

                # Extract team form data
                team_form = pred.get("team_form", {})
                home_form = team_form.get("home_form", {})
                away_form = team_form.get("away_form", {})

                # Extract feature weights for SHAP
                feature_weights = pred.get("feature_weights", {})

                # Extract sport-specific impact data
                # NFL: QB impact, weather, turnovers
                qb_impact = pred.get("qb_impact", {})
                # MLB: Pitcher impact
                pitcher_impact = pred.get("pitcher_impact", {})
                # NHL: Goalie impact, special teams
                goalie_impact = pred.get("goalie_impact", {})
                special_teams = pred.get("special_teams", {})

                # Extract adjustments object (contains all adjustment breakdowns)
                adjustments = pred.get("adjustments", {})

                transformed.append({
                    "game_id": pred.get("game_id", ""),
                    "home_team": pred.get("home_team", ""),
                    "away_team": pred.get("away_team", ""),
                    "home_team_abbr": pred.get("home_team_abbr", ""),
                    "away_team_abbr": pred.get("away_team_abbr", ""),
                    "home_win_prob": home_prob,
                    "away_win_prob": pred.get("away_win_probability", 1 - home_prob),
                    "confidence": pred.get("confidence", 0.5),
                    "predicted_winner": pred.get("predicted_winner", ""),
                    "predicted_winner_name": pred.get("predicted_winner_name", ""),
                    "game_time": game_time,
                    "venue": pred.get("venue", ""),
                    "spread": spread,
                    "moneyline_home": moneyline_home,
                    "moneyline_away": moneyline_away,
                    "over_under": over_under,
                    "home_record": home_form.get("record_last_10", pred.get("home_record", "")),
                    "away_record": away_form.get("record_last_10", pred.get("away_record", "")),
                    # Base probabilities
                    "base_home_probability": pred.get("base_home_probability", home_prob),
                    "base_away_probability": pred.get("base_away_probability", 1 - home_prob),
                    # Common data
                    "market_odds": market_odds,
                    "star_impact": star_impact,
                    "team_form": team_form,
                    "feature_weights": feature_weights,
                    "adjustments": adjustments,
                    # NFL-specific
                    "qb_impact": qb_impact,
                    # MLB-specific
                    "pitcher_impact": pitcher_impact,
                    # NHL-specific
                    "goalie_impact": goalie_impact,
                    "special_teams": special_teams,
                    # Flags
                    "back_to_back_home": pred.get("back_to_back_home", False),
                    "back_to_back_away": pred.get("back_to_back_away", False),
                    "predicted_at": pred.get("predicted_at", "")
                })
            return transformed
        return []

    # Return empty list if API fails - no fallback to sample data
    error_msg = result.get("error", "Failed to fetch predictions")
    st.error(f"API Error: {error_msg}")
    return []


def get_sample_predictions(sport: str):
    """Get sample predictions for a sport (fallback when API unavailable)"""
    sample_data = {
        "NFL": [
            {
                "home_team": "Kansas City Chiefs",
                "away_team": "Buffalo Bills",
                "home_win_prob": 0.58,
                "confidence": 0.65,
                "game_time": "Sunday, 4:25 PM EST",
                "venue": "Arrowhead Stadium",
                "spread": "KC -2.5",
                "over_under": "52.5",
                "home_record": "10-3",
                "away_record": "9-4"
            },
            {
                "home_team": "Philadelphia Eagles",
                "away_team": "Dallas Cowboys",
                "home_win_prob": 0.62,
                "confidence": 0.68,
                "game_time": "Sunday, 8:20 PM EST",
                "venue": "Lincoln Financial Field",
                "spread": "PHI -4.5",
                "over_under": "48.0",
                "home_record": "11-2",
                "away_record": "9-4"
            }
        ],
        "NBA": [
            {
                "home_team": "Boston Celtics",
                "away_team": "Miami Heat",
                "home_win_prob": 0.71,
                "confidence": 0.72,
                "game_time": "Tonight, 7:30 PM EST",
                "venue": "TD Garden",
                "spread": "BOS -8.5",
                "over_under": "218.5",
                "home_record": "22-5",
                "away_record": "15-12"
            },
            {
                "home_team": "Denver Nuggets",
                "away_team": "Los Angeles Lakers",
                "home_win_prob": 0.65,
                "confidence": 0.63,
                "game_time": "Tonight, 10:00 PM EST",
                "venue": "Ball Arena",
                "spread": "DEN -5.5",
                "over_under": "230.0",
                "home_record": "19-8",
                "away_record": "16-12"
            }
        ],
        "MLB": [
            {
                "home_team": "New York Yankees",
                "away_team": "Boston Red Sox",
                "home_win_prob": 0.54,
                "confidence": 0.58,
                "game_time": "Season Ended",
                "venue": "Yankee Stadium",
                "spread": "NYY -1.5",
                "over_under": "8.5",
                "home_record": "82-80",
                "away_record": "78-84"
            }
        ],
        "NHL": [
            {
                "home_team": "Colorado Avalanche",
                "away_team": "Vegas Golden Knights",
                "home_win_prob": 0.52,
                "confidence": 0.55,
                "game_time": "Tonight, 9:00 PM EST",
                "venue": "Ball Arena",
                "spread": "COL -1.5",
                "over_under": "6.5",
                "home_record": "18-10",
                "away_record": "20-8"
            },
            {
                "home_team": "Toronto Maple Leafs",
                "away_team": "Montreal Canadiens",
                "home_win_prob": 0.68,
                "confidence": 0.66,
                "game_time": "Tonight, 7:00 PM EST",
                "venue": "Scotiabank Arena",
                "spread": "TOR -1.5",
                "over_under": "6.0",
                "home_record": "19-7",
                "away_record": "12-16"
            }
        ]
    }
    return sample_data.get(sport, [])


def get_teams_for_sport(sport: str):
    """Get list of teams for a sport"""
    teams = {
        "NFL": [
            "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens",
            "Buffalo Bills", "Carolina Panthers", "Chicago Bears",
            "Cincinnati Bengals", "Cleveland Browns", "Dallas Cowboys",
            "Denver Broncos", "Detroit Lions", "Green Bay Packers",
            "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars",
            "Kansas City Chiefs"
        ],
        "NBA": [
            "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets",
            "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers",
            "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons",
            "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
            "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies",
            "Miami Heat"
        ],
        "MLB": [
            "Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles",
            "Boston Red Sox", "Chicago Cubs", "Chicago White Sox",
            "Cincinnati Reds", "Cleveland Guardians", "Colorado Rockies",
            "Detroit Tigers", "Houston Astros", "Kansas City Royals",
            "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins",
            "Milwaukee Brewers"
        ],
        "NHL": [
            "Anaheim Ducks", "Arizona Coyotes", "Boston Bruins",
            "Buffalo Sabres", "Calgary Flames", "Carolina Hurricanes",
            "Chicago Blackhawks", "Colorado Avalanche", "Columbus Blue Jackets",
            "Dallas Stars", "Detroit Red Wings", "Edmonton Oilers",
            "Florida Panthers", "Los Angeles Kings", "Minnesota Wild",
            "Montreal Canadiens"
        ]
    }
    return teams.get(sport, [])
