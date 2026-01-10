"""
Header and top navigation components
"""
import streamlit as st
from datetime import datetime


def render_header(title: str, subtitle: str = None, show_refresh: bool = True):
    """Render the page header with optional refresh button"""

    col1, col2 = st.columns([3, 1])

    with col1:
        st.title(title)
        if subtitle:
            st.caption(subtitle)

    with col2:
        if show_refresh:
            col_time, col_btn = st.columns([2, 1])
            with col_time:
                st.caption("Last Updated")
                st.text(datetime.now().strftime('%H:%M:%S'))

            with col_btn:
                if st.button("🔄", help="Refresh data"):
                    st.rerun()


def render_breadcrumb(items: list):
    """Render breadcrumb navigation"""
    breadcrumb_text = " › ".join(items)
    st.caption(breadcrumb_text)


def render_quick_actions():
    """Render quick action buttons in header area"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.button("📊 New Prediction", use_container_width=True)
    with col2:
        st.button("🔬 Run Simulation", use_container_width=True)
    with col3:
        st.button("📈 Backtest", use_container_width=True)
    with col4:
        st.button("📥 Export", use_container_width=True)


def render_notification_bar():
    """Render notification/alert bar"""
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []

    if st.session_state.notifications:
        for notif in st.session_state.notifications:
            notif_type = notif.get('type', 'info')
            message = notif.get('message', '')

            if notif_type == "success":
                st.success(message)
            elif notif_type == "warning":
                st.warning(message)
            elif notif_type == "error":
                st.error(message)
            else:
                st.info(message)


def render_tabs_header(tabs: list, icons: list = None):
    """Render tabs using native Streamlit tabs"""
    if icons is None:
        icons = [""] * len(tabs)

    tab_labels = [f"{icon} {tab}" if icon else tab for icon, tab in zip(icons, tabs)]
    return st.tabs(tab_labels)
