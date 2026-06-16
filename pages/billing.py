"""
Billing and Subscription Page
"""

import streamlit as st

from components.header import render_breadcrumb, render_header
from config import THEME, SUCCESS_URL, CANCEL_URL
from utils.api_client import get_api_client


def render_billing_page():
    """Render the billing and subscription page"""

    # Header and Breadcrumbs
    render_breadcrumb(["Main", "Billing"])
    render_header("Billing & Subscription", "Manage your plan and payments")

    st.markdown("---")

    # Billing Cycle Toggle
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        billing_cycle = st.radio(
            "Select Billing Cycle",
            ["Monthly", "Yearly"],
            horizontal=True,
            label_visibility="collapsed",
        )

    is_yearly = "Yearly" in billing_cycle

    # primary_color = THEME.get("primary_color")
    surface_color = THEME.get("surface")
    text_secondary = THEME.get("text_secondary")
    plans = [
        {
            "name": "Basic",
            "key": "basic",
            "monthly_price": 1.99,
            "yearly_price": 19.99,
            "features": [
                "Standard Machine Learning Models",
                "NBA & NFL Predictions",
                "Daily Model Updates",
                "Basic Statistics Dashboard",
                "Standard Support",
            ],
        },
        {
            "name": "Pro",
            "key": "pro",
            "monthly_price": 4.99,
            "yearly_price": 49.99,
            "features": [
                "Advanced Machine Learning Models",
                "NBA, NFL, MLB, NHL Predictions",
                "Daily Model Updates",
                "Advanced Statistics Dashboard",
            ],
        },
    ]

    # Pricing Plans
    plan_columns = st.columns(len(plans), gap="medium")

    from streamlit_redirect import redirect


    for i, plan in enumerate(plans):
        with plan_columns[i]:
            price = plan["yearly_price"] if is_yearly else plan["monthly_price"]
            period = "year" if is_yearly else "mo"
            features_html = "".join(f"<li>{f}</li>" for f in plan["features"])

            st.markdown(
                f"""
                <div style="background: {surface_color}; padding: 2rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); height: 500px;">
                    <h3 style="margin-top: 0;">{plan["name"]} Plan</h3>
                    <h1 style="margin: 1.5rem 0;">${price}<span style="font-size: 1rem; font-weight: normal; color: {text_secondary};"> /{period}</span></h1>
                    <ul style="padding-left: 1.2rem; margin-bottom: 2rem;">
                        {features_html}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")
            if st.button(
                f"Subscribe to {plan['name']}",
                type="primary",
                use_container_width=True,
                key=f"sub_{plan['name'].lower()}",
            ):
                if not st.session_state.get('is_logged_in', False):
                    st.warning("Please login first before subscribing to a plan.")
                else:
                    client = get_api_client()
                    price_key = f"{plan['key']}_{billing_cycle.lower()}"
                    response = client.create_checkout_session(price_key, success_url=SUCCESS_URL, cancel_url=CANCEL_URL)
                    
                    if response.get("success"):
                        checkout_url = response["data"]["checkout_url"]
                        print('stripe_checkout_url:', checkout_url)
                        redirect(checkout_url)
                    else:
                        st.error(f"Failed to initiate checkout: {response.get('error')}")

