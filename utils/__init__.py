"""
Utility modules for the Sports Prediction Platform
"""
from .api_client import APIClient, get_api_client, check_backend_status
from .styles import MAIN_STYLES, get_sport_gradient, get_confidence_color, create_metric_card, create_alert, create_status_badge
from .charts import (
    create_win_probability_gauge,
    create_probability_bar,
    create_model_performance_chart,
    create_trend_chart,
    create_odds_movement_chart,
    create_monte_carlo_distribution,
    create_team_form_chart,
    create_shap_waterfall,
    create_accuracy_by_sport_radar,
    create_prediction_confidence_donut,
    create_backtest_equity_curve
)
from .export import (
    export_predictions_to_csv,
    export_predictions_to_pdf,
    export_backtest_report,
    export_model_performance_report,
    create_download_link,
    export_dataframe_to_excel
)

__all__ = [
    'APIClient',
    'get_api_client',
    'check_backend_status',
    'MAIN_STYLES',
    'get_sport_gradient',
    'get_confidence_color',
    'create_metric_card',
    'create_alert',
    'create_status_badge',
    'create_win_probability_gauge',
    'create_probability_bar',
    'create_model_performance_chart',
    'create_trend_chart',
    'create_odds_movement_chart',
    'create_monte_carlo_distribution',
    'create_team_form_chart',
    'create_shap_waterfall',
    'create_accuracy_by_sport_radar',
    'create_prediction_confidence_donut',
    'create_backtest_equity_curve',
    'export_predictions_to_csv',
    'export_predictions_to_pdf',
    'export_backtest_report',
    'export_model_performance_report',
    'create_download_link',
    'export_dataframe_to_excel'
]
