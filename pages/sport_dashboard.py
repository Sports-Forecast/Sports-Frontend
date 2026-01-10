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

    # Date selector and filters
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

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
            render_prediction_card(
                home_team=pred['home_team'],
                away_team=pred['away_team'],
                home_prob=pred['home_win_prob'],
                confidence=pred['confidence'],
                game_time=pred['game_time'],
                venue=pred.get('venue', ''),
                spread=pred.get('spread', ''),
                over_under=pred.get('over_under', ''),
                home_record=pred.get('home_record', ''),
                away_record=pred.get('away_record', '')
            )

            # Expandable details
            with st.expander("📊 View Detailed Analysis"):
                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:
                    st.markdown("**Monte Carlo Simulation**")
                    # Generate sample MC data
                    mc_data = np.random.normal(
                        (pred['home_win_prob'] - 0.5) * 10, 5, 1000
                    ).tolist()
                    mc_fig = create_monte_carlo_distribution(
                        mc_data, pred['home_team'], pred['away_team']
                    )
                    mc_key = f"mc_{sport}_{pred['home_team'].replace(' ', '_')}_{pred['away_team'].replace(' ', '_')}"
                    st.plotly_chart(
                        mc_fig, width="stretch",
                        config={'displayModeBar': False}, key=mc_key
                    )

                with detail_col2:
                    st.markdown("**Feature Importance (SHAP)**")
                    features = [
                        "Home Advantage", "Recent Form", "Star Player",
                        "Rest Days", "H2H History"
                    ]
                    values = [0.08, 0.12, -0.05, 0.03, 0.02]
                    shap_fig = create_shap_waterfall(features, values)
                    shap_key = f"shap_{sport}_{pred['home_team'].replace(' ', '_')}_{pred['away_team'].replace(' ', '_')}"
                    st.plotly_chart(
                        shap_fig, width="stretch",
                        config={'displayModeBar': False}, key=shap_key
                    )


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

                over_under = pred.get(
                    "over_under", pred.get("total", "")
                )
                transformed.append({
                    "home_team": pred.get("home_team", ""),
                    "away_team": pred.get("away_team", ""),
                    "home_win_prob": home_prob,
                    "confidence": pred.get("confidence", 0.5),
                    "game_time": game_time,
                    "venue": pred.get("venue", ""),
                    "spread": pred.get("spread", ""),
                    "over_under": over_under,
                    "home_record": pred.get("home_record", ""),
                    "away_record": pred.get("away_record", "")
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
