"""
Card components for displaying predictions, stats, and other data
Using native Streamlit components instead of raw HTML
"""
import streamlit as st
from typing import Dict, Any, Optional
import plotly.graph_objects as go


def render_prediction_card(
    home_team: str,
    away_team: str,
    home_prob: float,
    confidence: float,
    game_time: str,
    venue: str = "",
    spread: str = "",
    over_under: str = "",
    home_record: str = "",
    away_record: str = "",
    show_details: bool = True
):
    """Render a prediction card for a game using native Streamlit"""

    # Determine winner prediction
    predicted_winner = home_team if home_prob > 0.5 else away_team
    win_prob = home_prob if home_prob > 0.5 else (1 - home_prob)
    away_prob = 1 - home_prob

    # Confidence level
    if confidence >= 0.65:
        conf_label = "High Confidence"
    elif confidence >= 0.55:
        conf_label = "Medium Confidence"
    else:
        conf_label = "Low Confidence"

    # Card container
    with st.container():
        # Game info header
        st.caption(f"{game_time} {'| ' + venue if venue else ''}")

        # Teams and probabilities
        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            if home_prob > 0.5:
                st.markdown(f"**:green[{home_team}]**")
            else:
                st.markdown(f"**{home_team}**")
            st.caption(home_record)
            st.metric(
                label="Win Probability",
                value=f"{home_prob*100:.1f}%",
                label_visibility="collapsed"
            )

        with col2:
            st.markdown(
                "<div style='text-align: center; padding-top: 20px;'>"
                "<b>VS</b></div>",
                unsafe_allow_html=True
            )

        with col3:
            if away_prob > 0.5:
                st.markdown(f"**:green[{away_team}]**")
            else:
                st.markdown(f"**{away_team}**")
            st.caption(away_record)
            st.metric(
                label="Win Probability",
                value=f"{away_prob*100:.1f}%",
                label_visibility="collapsed"
            )

        # Probability bar chart
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
        st.plotly_chart(fig, width="stretch", config={'displayModeBar': False}, key=f"prob_{home_team}_{away_team}")

        # Additional details
        if show_details:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Spread", spread or "N/A")
            with col2:
                st.metric("Over/Under", over_under or "N/A")
            with col3:
                st.metric("Confidence", f"{confidence*100:.1f}%")

        st.divider()


def render_stat_card(
    title: str,
    value: str,
    delta: str = None,
    delta_type: str = "positive",
    icon: str = None,
    color: str = "#0078D4"
):
    """Render a statistics card using native Streamlit metric"""
    with st.container():
        if icon:
            st.markdown(f"### {icon}")
        st.metric(
            label=title,
            value=value,
            delta=delta if delta else None,
            delta_color="normal" if delta_type == "positive" else "inverse"
        )


def render_model_card(
    model_name: str,
    accuracy: float,
    weight: float,
    status: str = "Active",
    color: str = "#0078D4",
    last_trained: str = "",
    roc_auc: float = None
):
    """Render a model information card using native Streamlit"""
    with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**{model_name}**")
            if last_trained:
                st.caption(last_trained)

        with col2:
            if status == "Active":
                st.success(status)
            elif status == "Training":
                st.warning(status)
            else:
                st.error(status)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Accuracy", f"{accuracy*100:.1f}%")
        with col2:
            st.metric("Weight", f"{weight*100:.0f}%")
        if roc_auc:
            with col3:
                st.metric("ROC-AUC", f"{roc_auc:.3f}")

        # Progress bar for weight
        st.progress(weight, text=f"Ensemble Weight: {weight*100:.0f}%")
        st.divider()


def render_team_card(
    team_name: str,
    record: str,
    win_pct: float,
    streak: str,
    last_5: str,
    logo_url: str = None
):
    """Render a team information card using native Streamlit"""
    with st.container():
        col1, col2 = st.columns([1, 3])

        with col1:
            if logo_url:
                st.image(logo_url, width=48)
            else:
                st.markdown("### 🏆")

        with col2:
            st.markdown(f"**{team_name}**")
            st.caption(f"{record} ({win_pct*100:.1f}%)")

        col1, col2 = st.columns(2)
        with col1:
            if "W" in streak:
                st.success(f"Streak: {streak}")
            else:
                st.error(f"Streak: {streak}")
        with col2:
            st.info(f"Last 5: {last_5}")

        st.divider()


def render_log_entry(
    timestamp: str,
    level: str,
    message: str,
    source: str = ""
):
    """Render a log entry using native Streamlit"""
    level_upper = level.upper()

    # Format the log line
    source_text = f"[{source}] " if source else ""
    log_text = f"`{timestamp}` **[{level_upper}]** {source_text}{message}"

    if level_upper == "ERROR":
        st.error(log_text)
    elif level_upper == "WARNING":
        st.warning(log_text)
    elif level_upper == "SUCCESS":
        st.success(log_text)
    elif level_upper == "DEBUG":
        st.caption(log_text)
    else:
        st.info(log_text)


def render_simulation_progress(
    current: int,
    total: int,
    elapsed_time: str,
    estimated_remaining: str
):
    """Render simulation progress indicator using native Streamlit"""
    progress = current / total if total > 0 else 0

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Progress", f"{current:,} / {total:,}")

    with col2:
        st.metric("Time", f"{elapsed_time} / {estimated_remaining}")

    st.progress(progress, text=f"{progress*100:.1f}% Complete")
