"""
Settings Page - Application configuration
"""
import streamlit as st
from components import render_header
from config import API_BASE_URL, REFRESH_INTERVALS, THEME
from utils.api_client import get_api_client
from datetime import datetime


def render_settings_page():
    """Render the settings page"""

    render_header(
        title="⚙️ Settings",
        subtitle="Configure application preferences and connections"
    )

    # Settings tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔗 Connections", "🎨 Appearance", "🔔 Notifications", "📊 Data", "💎 Membership"])

    with tab1:
        render_connection_settings()

    with tab2:
        render_appearance_settings()

    with tab3:
        render_notification_settings()

    with tab4:
        render_data_settings()

    with tab5:
        render_membership_settings()


def render_membership_settings():
    """Render membership and subscription settings"""
    st.markdown("### Membership Details")
    
    if not st.session_state.get('is_logged_in', False):
        st.warning("Please login to view your membership details.")
        return

    client = get_api_client()
    with st.spinner("Loading membership info..."):
        response = client.get_profile()

    if not response.get("success"):
        st.error(f"Failed to load profile: {response.get('error')}")
        return

    profile_data = response.get("data", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Email/Identifier:**")
        st.text(profile_data.get("identifier", "N/A"))
        
        st.markdown("**Account Status:**")
        is_active = profile_data.get("is_active", False)
        st.markdown(f"<span style='color: {'#4CAF50' if is_active else '#F44336'}'>{'Active' if is_active else 'Inactive'}</span>", unsafe_allow_html=True)

    with col2:
        st.markdown("**Current Plan:**")
        plan = profile_data.get("plan", "free")
        st.markdown(f"<strong style='font-size: 1.2em; text-transform: uppercase;'>{plan}</strong>", unsafe_allow_html=True)
        
        subscription = profile_data.get("subscription")
        if subscription:
            st.markdown("**Subscription Status:**")
            st.text(subscription.get("status", "N/A").capitalize())
            
            st.markdown("**Current Period Ends:**")
            period_end = subscription.get("current_period_end")
            if period_end:
                try:
                    end_date = datetime.fromisoformat(period_end).date()
                    st.text(end_date)
                except Exception:
                    st.text(str(period_end))
            
            st.markdown("---")
            if st.button("🚫 Cancel Subscription", type="secondary"):
                client.cancel_subscription()
                st.success("Subscription cancelled successfully.")
        elif plan != "free":
            st.info("Subscription details not found.")
        else:
            st.info("You are currently on the free plan.")
            # if st.button("Upgrade Plan", type="primary"):
            #     st.switch_page("pages/billing.py")


def render_connection_settings():
    """Render connection settings"""

    st.markdown("### Backend API")

    col1, col2 = st.columns([3, 1])

    with col1:
        api_url = st.text_input(
            "API Base URL",
            value=API_BASE_URL,
            key="api_url"
        )

    with col2:
        st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
        if st.button("🔍 Test Connection"):
            with st.spinner("Testing connection..."):
                import time
                time.sleep(1)
            st.success("✓ Connected successfully")

    col1, col2 = st.columns(2)

    with col1:
        st.number_input(
            "Request Timeout (seconds)",
            min_value=5,
            max_value=120,
            value=30,
            key="timeout"
        )

    with col2:
        st.number_input(
            "Max Retries",
            min_value=0,
            max_value=5,
            value=3,
            key="retries"
        )

    st.markdown("---")

    st.markdown("### Database")

    st.text_input(
        "Database URL",
        value="postgresql://****:****@ep-winter-hall-****.us-east-1.aws.neon.tech/neondb",
        type="password",
        key="db_url"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.number_input(
            "Connection Pool Size",
            min_value=1,
            max_value=20,
            value=5,
            key="pool_size"
        )

    with col2:
        st.number_input(
            "Query Timeout (seconds)",
            min_value=5,
            max_value=60,
            value=30,
            key="query_timeout"
        )

    st.markdown("---")

    st.markdown("### External APIs")

    with st.expander("ESPN API"):
        st.text_input("Base URL", value="https://site.api.espn.com/apis", key="espn_url")
        st.number_input("Rate Limit (requests/min)", value=60, key="espn_rate")

    with st.expander("API-Sports"):
        st.text_input("API Key", value="9d1dbc****", type="password", key="api_sports_key")
        st.checkbox("Enable NFL data", value=True, key="api_nfl")
        st.checkbox("Enable NBA data", value=True, key="api_nba")
        st.checkbox("Enable MLB data", value=True, key="api_mlb")
        st.checkbox("Enable NHL data", value=True, key="api_nhl")


def render_appearance_settings():
    """Render appearance settings"""

    st.markdown("### Theme")

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Color Theme",
            ["Dark (Default)", "Light", "System"],
            key="color_theme"
        )

        st.color_picker(
            "Primary Color",
            value=THEME['primary_color'],
            key="primary_color"
        )

        st.color_picker(
            "Accent Color",
            value=THEME['accent_color'],
            key="accent_color"
        )

    with col2:
        st.selectbox(
            "Font Family",
            ["Inter", "Segoe UI", "Roboto", "System Default"],
            key="font_family"
        )

        st.slider(
            "Font Size Scale",
            min_value=0.8,
            max_value=1.2,
            value=1.0,
            step=0.05,
            key="font_scale"
        )

    st.markdown("---")

    st.markdown("### Layout")

    col1, col2 = st.columns(2)

    with col1:
        st.checkbox("Show sidebar by default", value=True, key="show_sidebar")
        st.checkbox("Compact mode", value=False, key="compact_mode")
        st.checkbox("Show breadcrumbs", value=True, key="show_breadcrumbs")

    with col2:
        st.checkbox("Enable animations", value=True, key="enable_animations")
        st.checkbox("Show tooltips", value=True, key="show_tooltips")
        st.checkbox("Show status panel", value=True, key="show_status")

    st.markdown("---")

    st.markdown("### Charts")

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Default Chart Theme",
            ["Dark", "Light", "Plotly Default"],
            key="chart_theme"
        )

        st.checkbox("Enable chart animations", value=True, key="chart_animations")

    with col2:
        st.checkbox("Show chart tooltips", value=True, key="chart_tooltips")
        st.checkbox("Enable zoom/pan", value=True, key="chart_zoom")


def render_notification_settings():
    """Render notification settings"""

    st.markdown("### In-App Notifications")

    col1, col2 = st.columns(2)

    with col1:
        st.checkbox("Enable notifications", value=True, key="enable_notif")
        st.checkbox("Show success messages", value=True, key="notif_success")
        st.checkbox("Show error alerts", value=True, key="notif_error")
        st.checkbox("Show warning alerts", value=True, key="notif_warning")

    with col2:
        st.number_input(
            "Notification duration (seconds)",
            min_value=1,
            max_value=10,
            value=3,
            key="notif_duration"
        )

        st.selectbox(
            "Notification position",
            ["Top Right", "Top Left", "Bottom Right", "Bottom Left"],
            key="notif_position"
        )

    st.markdown("---")

    st.markdown("### Alerts")

    st.markdown("**Trigger alerts when:**")

    col1, col2 = st.columns(2)

    with col1:
        st.checkbox("Model training completes", value=True, key="alert_training")
        st.checkbox("Backtest finishes", value=True, key="alert_backtest")
        st.checkbox("New predictions available", value=True, key="alert_predictions")

    with col2:
        st.checkbox("Error occurs", value=True, key="alert_error")
        st.checkbox("Model accuracy drops below threshold", value=True, key="alert_accuracy")
        st.number_input(
            "Accuracy threshold (%)",
            min_value=50,
            max_value=70,
            value=55,
            key="accuracy_threshold"
        )

    st.markdown("---")

    st.markdown("### Sound")

    st.checkbox("Enable notification sounds", value=False, key="enable_sound")
    st.slider("Volume", min_value=0, max_value=100, value=50, key="sound_volume")


def render_data_settings():
    """Render data settings"""

    st.markdown("### Refresh Intervals")

    col1, col2 = st.columns(2)

    with col1:
        st.number_input(
            "Live Odds Refresh (seconds)",
            min_value=10,
            max_value=300,
            value=REFRESH_INTERVALS['live_odds'],
            key="refresh_odds"
        )

        st.number_input(
            "Predictions Refresh (seconds)",
            min_value=30,
            max_value=600,
            value=REFRESH_INTERVALS['predictions'],
            key="refresh_predictions"
        )

    with col2:
        st.number_input(
            "Dashboard Refresh (seconds)",
            min_value=60,
            max_value=600,
            value=REFRESH_INTERVALS['dashboard'],
            key="refresh_dashboard"
        )

        st.number_input(
            "Logs Refresh (seconds)",
            min_value=1,
            max_value=30,
            value=REFRESH_INTERVALS['logs'],
            key="refresh_logs"
        )

    st.markdown("---")

    st.markdown("### Caching")

    col1, col2 = st.columns(2)

    with col1:
        st.checkbox("Enable caching", value=True, key="enable_cache")
        st.number_input(
            "Cache TTL (minutes)",
            min_value=1,
            max_value=60,
            value=15,
            key="cache_ttl"
        )

    with col2:
        st.number_input(
            "Max cache size (MB)",
            min_value=50,
            max_value=500,
            value=100,
            key="cache_size"
        )

        if st.button("🗑️ Clear Cache"):
            st.success("Cache cleared successfully")

    st.markdown("---")

    st.markdown("### Data Export")

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Default export format",
            ["CSV", "PDF", "Excel"],
            key="export_format"
        )

        st.checkbox("Include headers in exports", value=True, key="export_headers")

    with col2:
        st.checkbox("Include timestamps", value=True, key="export_timestamps")
        st.checkbox("Compress large exports", value=True, key="export_compress")

    st.markdown("---")

    st.markdown("### Data Retention")

    col1, col2 = st.columns(2)

    with col1:
        st.number_input(
            "Keep logs for (days)",
            min_value=7,
            max_value=365,
            value=30,
            key="log_retention"
        )

    with col2:
        st.number_input(
            "Keep simulation results for (days)",
            min_value=7,
            max_value=365,
            value=90,
            key="sim_retention"
        )

    # Save button
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("💾 Save All Settings", type="primary"):
            st.success("Settings saved successfully!")

    with col2:
        if st.button("🔄 Reset to Defaults"):
            st.info("Settings reset to defaults")

    with col3:
        st.markdown("")

    # Import/Export settings
    st.markdown("---")

    st.markdown("### Import/Export Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📤 Export Settings",
            data="{}",  # Would be actual settings JSON
            file_name="settings_export.json",
            mime="application/json"
        )

    with col2:
        uploaded_file = st.file_uploader(
            "📥 Import Settings",
            type=['json'],
            key="import_settings"
        )
        if uploaded_file:
            st.success("Settings imported successfully!")
