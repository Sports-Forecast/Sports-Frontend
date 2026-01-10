"""
Sidebar navigation component for the Sports Prediction Platform
"""
import streamlit as st
from streamlit_option_menu import option_menu
from config import SPORTS, APP_NAME, APP_VERSION


def render_sidebar() -> str:
    """Render the sidebar navigation and return selected page"""

    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0 1.5rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎯</div>
            <div style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF;">Sports Prediction</div>
            <div style="font-size: 0.75rem; color: #8A8A8A;">Platform v{}</div>
        </div>
        """.format(APP_VERSION), unsafe_allow_html=True)

        st.markdown("---")

        # Main navigation menu
        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "🏀 NBA",
                "🏈 NFL",
                "⚾ MLB",
                "🏒 NHL",
                "Models",
                "Simulations",
                "Backtesting",
                "Logs",
                "Settings"
            ],
            icons=[
                "speedometer2",
                "",
                "",
                "",
                "",
                "cpu",
                "graph-up-arrow",
                "clock-history",
                "terminal",
                "gear"
            ],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "0",
                    "background-color": "transparent"
                },
                "icon": {
                    "color": "#00BCF2",
                    "font-size": "1rem"
                },
                "nav-link": {
                    "font-size": "0.875rem",
                    "text-align": "left",
                    "padding": "0.75rem 1rem",
                    "border-radius": "8px",
                    "margin": "2px 0",
                    "color": "#CCCCCC",
                    "background-color": "transparent",
                    "--hover-color": "#2D2D30"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #0078D4 0%, #106EBE 100%)",
                    "color": "white",
                    "font-weight": "600"
                }
            }
        )

        st.markdown("---")

        # Quick stats section
        st.markdown("""
        <div style="padding: 0.5rem;">
            <div style="font-size: 0.75rem; color: #8A8A8A; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.75rem;">
                Quick Stats
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sport stats cards
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(145deg, #2D2D30 0%, #252526 100%);
                        border-radius: 8px; padding: 0.75rem; text-align: center;
                        border: 1px solid rgba(255,255,255,0.08);">
                <div style="font-size: 1.25rem; font-weight: 700; color: #4CAF50;">58.9%</div>
                <div style="font-size: 0.625rem; color: #8A8A8A;">NFL Accuracy</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background: linear-gradient(145deg, #2D2D30 0%, #252526 100%);
                        border-radius: 8px; padding: 0.75rem; text-align: center;
                        border: 1px solid rgba(255,255,255,0.08);">
                <div style="font-size: 1.25rem; font-weight: 700; color: #00BCF2;">57.1%</div>
                <div style="font-size: 0.625rem; color: #8A8A8A;">NBA Accuracy</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(145deg, #2D2D30 0%, #252526 100%);
                        border-radius: 8px; padding: 0.75rem; text-align: center;
                        border: 1px solid rgba(255,255,255,0.08);">
                <div style="font-size: 1.25rem; font-weight: 700; color: #FF9800;">56.3%</div>
                <div style="font-size: 0.625rem; color: #8A8A8A;">MLB Accuracy</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown("""
            <div style="background: linear-gradient(145deg, #2D2D30 0%, #252526 100%);
                        border-radius: 8px; padding: 0.75rem; text-align: center;
                        border: 1px solid rgba(255,255,255,0.08);">
                <div style="font-size: 1.25rem; font-weight: 700; color: #F44336;">55.2%</div>
                <div style="font-size: 0.625rem; color: #8A8A8A;">NHL Accuracy</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Backend status indicator
        if 'backend_status' not in st.session_state:
            st.session_state.backend_status = "checking"

        status_color = "#4CAF50" if st.session_state.get('backend_online', False) else "#F44336"
        status_text = "Online" if st.session_state.get('backend_online', False) else "Offline"

        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem;
                    background: rgba(255,255,255,0.05); border-radius: 8px;">
            <div style="width: 8px; height: 8px; border-radius: 50%; background: {status_color};
                        box-shadow: 0 0 8px {status_color};"></div>
            <span style="font-size: 0.75rem; color: #CCCCCC;">Backend: {status_text}</span>
        </div>
        """, unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div style="position: absolute; bottom: 1rem; left: 1rem; right: 1rem;">
            <div style="font-size: 0.625rem; color: #666; text-align: center;">
                © 2024 Sports Prediction Platform
            </div>
        </div>
        """, unsafe_allow_html=True)

    return selected


def render_sport_submenu(sport: str) -> str:
    """Render sport-specific submenu"""
    config = SPORTS.get(sport, {})

    tabs = ["Predictions", "Team Analysis"]

    selected_tab = option_menu(
        menu_title=None,
        options=tabs,
        icons=["lightning", "people"],
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0",
                "background-color": "rgba(45,45,48,0.5)",
                "border-radius": "10px",
                "margin-bottom": "1rem"
            },
            "icon": {
                "font-size": "0.875rem"
            },
            "nav-link": {
                "font-size": "0.8125rem",
                "padding": "0.625rem 1rem",
                "margin": "0 2px",
                "border-radius": "8px",
                "color": "#CCCCCC"
            },
            "nav-link-selected": {
                "background": f"linear-gradient(135deg, {config.get('color', '#0078D4')} 0%, #106EBE 100%)",
                "color": "white"
            }
        }
    )

    return selected_tab
