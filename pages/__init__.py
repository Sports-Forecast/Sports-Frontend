"""
Page modules for the Sports Prediction Platform
"""
from .dashboard import render_dashboard
from .sport_dashboard import render_sport_dashboard
from .models import render_models_page
from .simulations import render_simulations_page
from .backtesting import render_backtesting_page
from .logs import render_logs_page
from .settings import render_settings_page

__all__ = [
    'render_dashboard',
    'render_sport_dashboard',
    'render_models_page',
    'render_simulations_page',
    'render_backtesting_page',
    'render_logs_page',
    'render_settings_page'
]
