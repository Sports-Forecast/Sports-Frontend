import os
from dotenv import load_dotenv

load_dotenv()


def get_config(key: str, default: str = "") -> str:
    """Get config value from Streamlit secrets or environment variables"""
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)


# API Configuration
API_BASE_URL = get_config("API_BASE_URL", "http://localhost:8000")
API_TIMEOUT = int(get_config("API_TIMEOUT", "30"))

# Application Settings
APP_NAME = "Sports Prediction Platform"
APP_VERSION = "1.0.0"
DEBUG_MODE = get_config("DEBUG_MODE", "false").lower() == "true"

# Theme Configuration
THEME = {
    "primary_color": "#0078D4",
    "secondary_color": "#106EBE",
    "accent_color": "#00BCF2",
    "background_dark": "#1E1E1E",
    "background_light": "#252526",
    "surface": "#2D2D30",
    "text_primary": "#FFFFFF",
    "text_secondary": "#CCCCCC",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336",
    "info": "#2196F3",
}

# Sport Configuration
SPORTS = {
    "NBA": {
        "icon": "🏀",
        "color": "#C9082A",
        "endpoint": "/api/predict/nba",
        "name": "NBA Basketball"
    },
    "NFL": {
        "icon": "🏈",
        "color": "#013369",
        "endpoint": "/api/predict/nfl",
        "name": "NFL Football"
    },
    "MLB": {
        "icon": "⚾",
        "color": "#041E42",
        "endpoint": "/api/predict/mlb",
        "name": "MLB Baseball"
    },
    "NHL": {
        "icon": "🏒",
        "color": "#000000",
        "endpoint": "/api/predict/nhl",
        "name": "NHL Hockey"
    }
}

# Model Configuration
MODELS = {
    "Logistic Regression": {"weight": 0.15, "color": "#FF6B6B"},
    "Random Forest": {"weight": 0.25, "color": "#4ECDC4"},
    "XGBoost": {"weight": 0.35, "color": "#45B7D1"},
    "LightGBM": {"weight": 0.25, "color": "#96CEB4"}
}

# Refresh Intervals (in seconds)
REFRESH_INTERVALS = {
    "live_odds": 30,
    "predictions": 60,
    "dashboard": 120,
    "logs": 5
}
