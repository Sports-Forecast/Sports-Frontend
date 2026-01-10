"""
Sports Prediction Platform - Main Streamlit Application
A modern, analytics-ready interface for sports predictions
"""
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Sports Prediction Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/OsamaASidd/Sports-Prediction-Platform',
        'Report a bug': 'https://github.com/OsamaASidd/Sports-Prediction-Platform/issues',
        'About': """
        ## Sports Prediction Platform

        A comprehensive sports analytics and prediction platform powered by
        ensemble machine learning models and Monte Carlo simulations.

        **Features:**
        - NFL, NBA, MLB, NHL predictions
        - Real-time odds tracking
        - Model performance analytics
        - Historical backtesting

        Version 1.0.0
        """
    }
)

# Import styles and components
from utils.styles import MAIN_STYLES
from utils.api_client import get_api_client, check_backend_status
from components.sidebar import render_sidebar
from components.status_panel import render_status_panel, add_log

# Import page modules
from pages.dashboard import render_dashboard
from pages.sport_dashboard import render_sport_dashboard
from pages.models import render_models_page
from pages.simulations import render_simulations_page
from pages.backtesting import render_backtesting_page
from pages.logs import render_logs_page
from pages.settings import render_settings_page


def init_session_state():
    """Initialize session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.backend_online = False
        st.session_state.notifications = []
        st.session_state.system_logs = []
        st.session_state.active_page = "Dashboard"


def check_backend():
    """Check backend connectivity"""
    try:
        client = get_api_client()
        result = client.health_check()
        st.session_state.backend_online = result.get('success', False)
    except Exception:
        st.session_state.backend_online = False


def main():
    """Main application entry point"""

    # Initialize session state
    init_session_state()

    # Apply custom styles
    st.markdown(MAIN_STYLES, unsafe_allow_html=True)

    # Check backend status periodically
    check_backend()

    # Render sidebar navigation
    selected_page = render_sidebar()

    # Main content area
    main_container = st.container()

    with main_container:
        # Route to appropriate page
        if selected_page == "Dashboard":
            render_dashboard()

        elif selected_page == "🏀 NBA":
            render_sport_dashboard("NBA")

        elif selected_page == "🏈 NFL":
            render_sport_dashboard("NFL")

        elif selected_page == "⚾ MLB":
            render_sport_dashboard("MLB")

        elif selected_page == "🏒 NHL":
            render_sport_dashboard("NHL")

        elif selected_page == "Models":
            render_models_page()

        elif selected_page == "Simulations":
            render_simulations_page()

        elif selected_page == "Backtesting":
            render_backtesting_page()

        elif selected_page == "Logs":
            render_logs_page()

        elif selected_page == "Settings":
            render_settings_page()

    # Render bottom status panel
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    render_status_panel()


if __name__ == "__main__":
    main()
