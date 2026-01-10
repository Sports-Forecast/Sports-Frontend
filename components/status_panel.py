"""
Status panel and notification components
"""
import streamlit as st
from datetime import datetime
from typing import List, Dict, Optional
import time


def render_status_panel():
    """Render the bottom status panel with system status and alerts"""

    # Initialize session state for logs if not exists
    if 'system_logs' not in st.session_state:
        st.session_state.system_logs = [
            {"time": datetime.now(), "level": "INFO", "message": "Application started successfully"},
            {"time": datetime.now(), "level": "INFO", "message": "Connected to backend API"},
        ]

    with st.expander("📊 System Status & Logs", expanded=False):
        # Status bar
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            backend_status = st.session_state.get('backend_online', False)
            status_color = "#4CAF50" if backend_status else "#F44336"
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: {status_color};
                            box-shadow: 0 0 8px {status_color};"></div>
                <span style="font-size: 0.8125rem; color: #CCCCCC;">Backend</span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: #4CAF50;
                            box-shadow: 0 0 8px #4CAF50;"></div>
                <span style="font-size: 0.8125rem; color: #CCCCCC;">Database</span>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: #4CAF50;
                            box-shadow: 0 0 8px #4CAF50;"></div>
                <span style="font-size: 0.8125rem; color: #CCCCCC;">Models</span>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style="font-size: 0.8125rem; color: #8A8A8A;">
                Memory: <span style="color: #00BCF2;">45%</span>
            </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
            <div style="font-size: 0.8125rem; color: #8A8A8A;">
                CPU: <span style="color: #4CAF50;">12%</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Log viewer
        log_container = st.container()
        with log_container:
            for log in st.session_state.system_logs[-10:]:  # Show last 10 logs
                level = log.get('level', 'INFO')
                level_colors = {
                    "INFO": "#2196F3",
                    "WARNING": "#FF9800",
                    "ERROR": "#F44336",
                    "DEBUG": "#8A8A8A",
                    "SUCCESS": "#4CAF50"
                }
                color = level_colors.get(level, "#8A8A8A")
                timestamp = log['time'].strftime('%H:%M:%S')

                st.markdown(f"""
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;
                            padding: 0.25rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);
                            display: flex; gap: 1rem;">
                    <span style="color: #666;">{timestamp}</span>
                    <span style="color: {color}; font-weight: 600; min-width: 60px;">[{level}]</span>
                    <span style="color: #CCCCCC;">{log['message']}</span>
                </div>
                """, unsafe_allow_html=True)


def add_log(level: str, message: str):
    """Add a log entry to the system logs"""
    if 'system_logs' not in st.session_state:
        st.session_state.system_logs = []

    st.session_state.system_logs.append({
        "time": datetime.now(),
        "level": level,
        "message": message
    })

    # Keep only last 100 logs
    if len(st.session_state.system_logs) > 100:
        st.session_state.system_logs = st.session_state.system_logs[-100:]


def show_notification(message: str, type: str = "info", duration: int = 3):
    """Show a toast notification"""
    if type == "success":
        st.success(message)
    elif type == "error":
        st.error(message)
    elif type == "warning":
        st.warning(message)
    else:
        st.info(message)


def render_progress_toast(title: str, message: str, progress: float):
    """Render a progress notification"""
    st.toast(f"{title}: {progress*100:.0f}% - {message}")


def render_alert_banner(alerts: List[Dict]):
    """Render alert banners at the top of the page"""
    for alert in alerts:
        alert_type = alert.get('type', 'info')
        message = alert.get('message', '')
        dismissible = alert.get('dismissible', True)

        colors = {
            "success": ("#4CAF50", "rgba(76, 175, 80, 0.15)"),
            "warning": ("#FF9800", "rgba(255, 152, 0, 0.15)"),
            "error": ("#F44336", "rgba(244, 67, 54, 0.15)"),
            "info": ("#2196F3", "rgba(33, 150, 243, 0.15)")
        }
        icons = {
            "success": "✓",
            "warning": "⚠",
            "error": "✕",
            "info": "ℹ"
        }

        border_color, bg_color = colors.get(alert_type, colors['info'])
        icon = icons.get(alert_type, 'ℹ')

        col1, col2 = st.columns([20, 1])
        with col1:
            st.markdown(f"""
            <div style="background: {bg_color}; border-left: 4px solid {border_color};
                        padding: 0.75rem 1rem; border-radius: 4px; margin-bottom: 0.5rem;
                        display: flex; align-items: center; gap: 0.75rem;">
                <span style="color: {border_color}; font-size: 1.25rem;">{icon}</span>
                <span style="color: #FFFFFF; font-size: 0.875rem;">{message}</span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if dismissible:
                if st.button("×", key=f"dismiss_{hash(message)}", help="Dismiss"):
                    pass  # Handle dismiss


def render_connection_status():
    """Render connection status indicator"""
    backend_online = st.session_state.get('backend_online', False)

    st.markdown(f"""
    <div style="position: fixed; bottom: 1rem; right: 1rem; z-index: 1000;
                background: rgba(30, 30, 30, 0.95); padding: 0.5rem 1rem;
                border-radius: 50px; border: 1px solid rgba(255,255,255,0.1);
                display: flex; align-items: center; gap: 0.5rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
        <div style="width: 8px; height: 8px; border-radius: 50%;
                    background: {'#4CAF50' if backend_online else '#F44336'};
                    box-shadow: 0 0 8px {'#4CAF50' if backend_online else '#F44336'};
                    animation: pulse 2s infinite;"></div>
        <span style="font-size: 0.75rem; color: #CCCCCC;">
            {'Connected' if backend_online else 'Disconnected'}
        </span>
    </div>
    """, unsafe_allow_html=True)
