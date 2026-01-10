"""
Plotly chart configurations for the Sports Prediction Platform
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict, Optional

CHART_THEME = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font_color": "#CCCCCC",
    "font_family": "Inter, Segoe UI, sans-serif",
    "grid_color": "rgba(255,255,255,0.1)",
    "primary": "#0078D4",
    "secondary": "#00BCF2",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336"
}


def apply_dark_theme(fig: go.Figure) -> go.Figure:
    """Apply dark theme to a plotly figure"""
    fig.update_layout(
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(
            family=CHART_THEME["font_family"],
            color=CHART_THEME["font_color"],
            size=12
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            gridcolor=CHART_THEME["grid_color"],
            linecolor=CHART_THEME["grid_color"],
            zerolinecolor=CHART_THEME["grid_color"]
        ),
        yaxis=dict(
            gridcolor=CHART_THEME["grid_color"],
            linecolor=CHART_THEME["grid_color"],
            zerolinecolor=CHART_THEME["grid_color"]
        ),
        hoverlabel=dict(
            bgcolor="#2D2D30",
            bordercolor="#0078D4",
            font=dict(color="#FFFFFF", size=12)
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.1)"
        )
    )
    return fig


def create_win_probability_gauge(
    home_prob: float,
    home_team: str,
    away_team: str
) -> go.Figure:
    """Create a gauge chart showing win probabilities"""
    away_prob = 1 - home_prob

    fig = go.Figure()

    # Home team gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=home_prob * 100,
        number={"suffix": "%", "font": {"size": 40, "color": "#4CAF50"}},
        title={"text": home_team, "font": {"size": 16, "color": "#FFFFFF"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#CCCCCC"},
            "bar": {"color": "#4CAF50"},
            "bgcolor": "rgba(255,255,255,0.1)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50], "color": "rgba(244,67,54,0.2)"},
                {"range": [50, 100], "color": "rgba(76,175,80,0.2)"}
            ],
            "threshold": {
                "line": {"color": "#FFFFFF", "width": 2},
                "value": 50,
                "thickness": 0.8
            }
        },
        domain={"x": [0, 0.45], "y": [0, 1]}
    ))

    # Away team gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=away_prob * 100,
        number={"suffix": "%", "font": {"size": 40, "color": "#F44336"}},
        title={"text": away_team, "font": {"size": 16, "color": "#FFFFFF"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#CCCCCC"},
            "bar": {"color": "#F44336"},
            "bgcolor": "rgba(255,255,255,0.1)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50], "color": "rgba(244,67,54,0.2)"},
                {"range": [50, 100], "color": "rgba(76,175,80,0.2)"}
            ]
        },
        domain={"x": [0.55, 1], "y": [0, 1]}
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#CCCCCC"},
        height=250,
        margin=dict(l=30, r=30, t=30, b=30)
    )

    return fig


def create_probability_bar(
    home_prob: float,
    home_team: str,
    away_team: str,
    home_color: str = "#4CAF50",
    away_color: str = "#F44336"
) -> go.Figure:
    """Create a horizontal stacked bar showing win probabilities"""
    away_prob = 1 - home_prob

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=["Win Probability"],
        x=[home_prob * 100],
        orientation="h",
        name=home_team,
        marker=dict(color=home_color, line=dict(width=0)),
        text=f"{home_team}: {home_prob*100:.1f}%",
        textposition="inside",
        textfont=dict(color="white", size=14, family="Inter"),
        hovertemplate=f"{home_team}: %{{x:.1f}}%<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        y=["Win Probability"],
        x=[away_prob * 100],
        orientation="h",
        name=away_team,
        marker=dict(color=away_color, line=dict(width=0)),
        text=f"{away_team}: {away_prob*100:.1f}%",
        textposition="inside",
        textfont=dict(color="white", size=14, family="Inter"),
        hovertemplate=f"{away_team}: %{{x:.1f}}%<extra></extra>"
    ))

    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=80,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False, range=[0, 100]),
        yaxis=dict(visible=False)
    )

    return fig


def create_model_performance_chart(
    models: List[str],
    accuracies: List[float],
    colors: Optional[List[str]] = None
) -> go.Figure:
    """Create a bar chart showing model performance comparison"""
    if colors is None:
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=models,
        y=[acc * 100 for acc in accuracies],
        marker=dict(
            color=colors[:len(models)],
            line=dict(width=0)
        ),
        text=[f"{acc*100:.1f}%" for acc in accuracies],
        textposition="outside",
        textfont=dict(color="#CCCCCC", size=14)
    ))

    fig = apply_dark_theme(fig)
    fig.update_layout(
        title=dict(
            text="Model Performance Comparison",
            font=dict(size=18, color="#FFFFFF")
        ),
        xaxis_title="Model",
        yaxis_title="Accuracy (%)",
        yaxis=dict(range=[0, 100]),
        height=400
    )

    return fig


def create_trend_chart(
    dates: List[str],
    values: List[float],
    title: str = "Historical Trend",
    color: str = "#0078D4"
) -> go.Figure:
    """Create a line chart showing historical trends"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode="lines+markers",
        line=dict(color=color, width=2),
        marker=dict(size=8, color=color),
        fill="tozeroy",
        fillcolor=f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)",
        hovertemplate="%{x}<br>Value: %{y:.2f}<extra></extra>"
    ))

    fig = apply_dark_theme(fig)
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color="#FFFFFF")
        ),
        height=350,
        xaxis_title="Date",
        yaxis_title="Value"
    )

    return fig


def create_odds_movement_chart(
    timestamps: List[str],
    home_odds: List[float],
    away_odds: List[float],
    home_team: str,
    away_team: str
) -> go.Figure:
    """Create a chart showing odds movement over time"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=timestamps,
        y=home_odds,
        mode="lines+markers",
        name=home_team,
        line=dict(color="#4CAF50", width=2),
        marker=dict(size=6)
    ))

    fig.add_trace(go.Scatter(
        x=timestamps,
        y=away_odds,
        mode="lines+markers",
        name=away_team,
        line=dict(color="#F44336", width=2),
        marker=dict(size=6)
    ))

    fig = apply_dark_theme(fig)
    fig.update_layout(
        title=dict(
            text="Odds Movement",
            font=dict(size=16, color="#FFFFFF")
        ),
        height=300,
        xaxis_title="Time",
        yaxis_title="Odds",
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )

    return fig


def create_monte_carlo_distribution(
    simulations: List[float],
    home_team: str,
    away_team: str
) -> go.Figure:
    """Create a histogram showing Monte Carlo simulation distribution"""
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=simulations,
        nbinsx=50,
        marker=dict(
            color="#0078D4",
            line=dict(color="#FFFFFF", width=0.5)
        ),
        opacity=0.8,
        hovertemplate="Score Diff: %{x}<br>Count: %{y}<extra></extra>"
    ))

    # Add vertical line at 0
    fig.add_vline(
        x=0,
        line_dash="dash",
        line_color="#FFFFFF",
        annotation_text="Even",
        annotation_position="top"
    )

    fig = apply_dark_theme(fig)
    fig.update_layout(
        title=dict(
            text="Monte Carlo Simulation Distribution",
            font=dict(size=16, color="#FFFFFF")
        ),
        xaxis_title=f"Point Differential ({home_team} - {away_team})",
        yaxis_title="Frequency",
        height=350
    )

    return fig


def create_team_form_chart(
    games: List[str],
    results: List[str],  # "W" or "L"
    point_diffs: List[float]
) -> go.Figure:
    """Create a chart showing team's recent form"""
    colors = ["#4CAF50" if r == "W" else "#F44336" for r in results]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=games,
        y=point_diffs,
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"+{pd:.0f}" if pd > 0 else f"{pd:.0f}" for pd in point_diffs],
        textposition="outside",
        textfont=dict(color="#CCCCCC", size=11)
    ))

    fig = apply_dark_theme(fig)
    fig.update_layout(
        title=dict(
            text="Recent Form (Last 10 Games)",
            font=dict(size=16, color="#FFFFFF")
        ),
        xaxis_title="Games",
        yaxis_title="Point Differential",
        height=300,
        showlegend=False
    )

    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")

    return fig


def create_shap_waterfall(
    features: List[str],
    values: List[float],
    base_value: float = 0.5
) -> go.Figure:
    """Create a SHAP-style waterfall chart for feature importance"""
    # Sort by absolute value
    sorted_indices = sorted(range(len(values)), key=lambda i: abs(values[i]), reverse=True)
    features = [features[i] for i in sorted_indices]
    values = [values[i] for i in sorted_indices]

    colors = ["#4CAF50" if v > 0 else "#F44336" for v in values]

    fig = go.Figure()

    fig.add_trace(go.Waterfall(
        orientation="h",
        measure=["relative"] * len(values),
        y=features,
        x=values,
        connector=dict(line=dict(color="rgba(255,255,255,0.2)")),
        decreasing=dict(marker=dict(color="#F44336")),
        increasing=dict(marker=dict(color="#4CAF50")),
        totals=dict(marker=dict(color="#0078D4"))
    ))

    fig = apply_dark_theme(fig)
    fig.update_layout(
        title=dict(
            text="Feature Impact (SHAP Values)",
            font=dict(size=16, color="#FFFFFF")
        ),
        height=400,
        xaxis_title="Impact on Prediction",
        showlegend=False
    )

    return fig


def create_accuracy_by_sport_radar(
    sports: List[str],
    accuracies: List[float],
    roc_aucs: List[float]
) -> go.Figure:
    """Create a radar chart comparing model performance across sports"""
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=accuracies + [accuracies[0]],
        theta=sports + [sports[0]],
        fill="toself",
        fillcolor="rgba(0,120,212,0.2)",
        line=dict(color="#0078D4", width=2),
        name="Accuracy"
    ))

    fig.add_trace(go.Scatterpolar(
        r=roc_aucs + [roc_aucs[0]],
        theta=sports + [sports[0]],
        fill="toself",
        fillcolor="rgba(0,188,242,0.2)",
        line=dict(color="#00BCF2", width=2),
        name="ROC-AUC"
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0.5, 0.7],
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)"
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)"
            )
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CCCCCC"),
        title=dict(
            text="Model Performance by Sport",
            font=dict(size=16, color="#FFFFFF")
        ),
        height=400,
        showlegend=True,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom",
            y=-0.2
        )
    )

    return fig


def create_prediction_confidence_donut(
    confidence: float,
    label: str = "Confidence"
) -> go.Figure:
    """Create a donut chart showing prediction confidence"""
    fig = go.Figure()

    color = "#4CAF50" if confidence >= 0.6 else "#FF9800" if confidence >= 0.55 else "#F44336"

    fig.add_trace(go.Pie(
        values=[confidence * 100, (1 - confidence) * 100],
        labels=[label, ""],
        hole=0.7,
        marker=dict(colors=[color, "rgba(255,255,255,0.1)"]),
        textinfo="none",
        hoverinfo="skip"
    ))

    fig.add_annotation(
        text=f"<b>{confidence*100:.1f}%</b>",
        x=0.5, y=0.5,
        font=dict(size=28, color="#FFFFFF"),
        showarrow=False
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=200,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig


def create_backtest_equity_curve(
    dates: List[str],
    returns: List[float],
    benchmark: Optional[List[float]] = None
) -> go.Figure:
    """Create an equity curve chart for backtesting results"""
    # Calculate cumulative returns
    cumulative = [1]
    for r in returns:
        cumulative.append(cumulative[-1] * (1 + r))
    cumulative = cumulative[1:]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=cumulative,
        mode="lines",
        name="Strategy",
        line=dict(color="#0078D4", width=2),
        fill="tozeroy",
        fillcolor="rgba(0,120,212,0.1)"
    ))

    if benchmark:
        cum_bench = [1]
        for r in benchmark:
            cum_bench.append(cum_bench[-1] * (1 + r))
        cum_bench = cum_bench[1:]

        fig.add_trace(go.Scatter(
            x=dates,
            y=cum_bench,
            mode="lines",
            name="Benchmark",
            line=dict(color="#FF9800", width=2, dash="dash")
        ))

    fig = apply_dark_theme(fig)
    fig.update_layout(
        title=dict(
            text="Backtest Equity Curve",
            font=dict(size=16, color="#FFFFFF")
        ),
        xaxis_title="Date",
        yaxis_title="Cumulative Return",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )

    return fig
