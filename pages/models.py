"""
Models Management Page - View, configure, and train prediction models
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from components import render_header, render_stat_card, render_model_card
from utils.charts import create_model_performance_chart, create_trend_chart
from utils.export import export_model_performance_report, create_download_link
from config import MODELS, SPORTS


def render_models_page():
    """Render the models management page"""

    render_header(
        title="Model Management",
        subtitle="View, configure, and train ensemble prediction models"
    )

    # Model overview stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card(
            title="Active Models",
            value="4",
            icon="🤖",
            color="#0078D4"
        )

    with col2:
        render_stat_card(
            title="Ensemble Accuracy",
            value="57.4%",
            delta="+1.2% this week",
            delta_type="positive",
            icon="🎯",
            color="#4CAF50"
        )

    with col3:
        render_stat_card(
            title="Last Training",
            value="2h ago",
            icon="⏱️",
            color="#FF9800"
        )

    with col4:
        render_stat_card(
            title="Training Queue",
            value="0",
            icon="📋",
            color="#9C27B0"
        )

    st.divider()

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Model Overview", "Configuration", "Training"])

    with tab1:
        render_model_overview()

    with tab2:
        render_model_configuration()

    with tab3:
        render_model_training()


def render_model_overview():
    """Render model overview section"""

    # Model performance comparison chart
    st.subheader("Model Performance Comparison")

    col_chart, col_export = st.columns([4, 1])

    with col_export:
        st.write("")
        if st.button("📥 Export Report"):
            models_data = [
                {"name": name, "accuracy": 0.55 + i * 0.02, "roc_auc": 0.58 + i * 0.02,
                 "weight": config['weight'], "status": "Active"}
                for i, (name, config) in enumerate(MODELS.items())
            ]
            pdf_data = export_model_performance_report(models_data, "All Sports")
            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name="model_performance_report.pdf",
                mime="application/pdf"
            )

    models = list(MODELS.keys())
    accuracies = [0.589, 0.571, 0.563, 0.552]
    colors = [MODELS[m]['color'] for m in models]

    perf_chart = create_model_performance_chart(models, accuracies, colors)
    st.plotly_chart(perf_chart, width="stretch", config={'displayModeBar': False})

    st.subheader("Individual Model Details")

    col1, col2 = st.columns(2)

    # Model cards
    model_details = [
        {
            "name": "Logistic Regression",
            "accuracy": 0.552,
            "weight": 0.15,
            "color": "#FF6B6B",
            "roc_auc": 0.58,
            "last_trained": "2 hours ago",
            "status": "Active"
        },
        {
            "name": "Random Forest",
            "accuracy": 0.563,
            "weight": 0.25,
            "color": "#4ECDC4",
            "roc_auc": 0.61,
            "last_trained": "2 hours ago",
            "status": "Active"
        },
        {
            "name": "XGBoost",
            "accuracy": 0.589,
            "weight": 0.35,
            "color": "#45B7D1",
            "roc_auc": 0.64,
            "last_trained": "2 hours ago",
            "status": "Active"
        },
        {
            "name": "LightGBM",
            "accuracy": 0.571,
            "weight": 0.25,
            "color": "#96CEB4",
            "roc_auc": 0.62,
            "last_trained": "2 hours ago",
            "status": "Active"
        }
    ]

    for i, model in enumerate(model_details):
        with col1 if i % 2 == 0 else col2:
            render_model_card(
                model_name=model['name'],
                accuracy=model['accuracy'],
                weight=model['weight'],
                status=model['status'],
                color=model['color'],
                last_trained=model['last_trained'],
                roc_auc=model['roc_auc']
            )

    # Performance by sport
    st.subheader("Performance by Sport")

    sport_perf = pd.DataFrame({
        'Model': list(MODELS.keys()) * 4,
        'Sport': ['NFL'] * 4 + ['NBA'] * 4 + ['MLB'] * 4 + ['NHL'] * 4,
        'Accuracy': [0.60, 0.58, 0.62, 0.57,  # NFL
                     0.58, 0.56, 0.59, 0.55,  # NBA
                     0.55, 0.54, 0.58, 0.56,  # MLB
                     0.53, 0.52, 0.57, 0.54],  # NHL
        'ROC-AUC': [0.65, 0.62, 0.67, 0.60,  # NFL
                    0.63, 0.60, 0.64, 0.58,  # NBA
                    0.58, 0.57, 0.61, 0.59,  # MLB
                    0.55, 0.54, 0.58, 0.56]  # NHL
    })

    st.dataframe(
        sport_perf,
        width="stretch",
        hide_index=True,
        column_config={
            "Accuracy": st.column_config.ProgressColumn(
                "Accuracy",
                format="%.1f%%",
                min_value=0.5,
                max_value=0.7
            ),
            "ROC-AUC": st.column_config.ProgressColumn(
                "ROC-AUC",
                format="%.3f",
                min_value=0.5,
                max_value=0.7
            )
        }
    )


def render_model_configuration():
    """Render model configuration section"""

    st.subheader("Ensemble Configuration")

    st.info("Adjust the weights for each model in the ensemble. Weights must sum to 1.0")

    # Weight sliders
    col1, col2 = st.columns(2)

    weights = {}

    with col1:
        st.markdown("**Logistic Regression**")
        weights['lr'] = st.slider(
            "Weight",
            min_value=0.0,
            max_value=0.5,
            value=0.15,
            step=0.05,
            key="lr_weight"
        )

        st.markdown("**Random Forest**")
        weights['rf'] = st.slider(
            "Weight",
            min_value=0.0,
            max_value=0.5,
            value=0.25,
            step=0.05,
            key="rf_weight"
        )

    with col2:
        st.markdown("**XGBoost**")
        weights['xgb'] = st.slider(
            "Weight",
            min_value=0.0,
            max_value=0.5,
            value=0.35,
            step=0.05,
            key="xgb_weight"
        )

        st.markdown("**LightGBM**")
        weights['lgb'] = st.slider(
            "Weight",
            min_value=0.0,
            max_value=0.5,
            value=0.25,
            step=0.05,
            key="lgb_weight"
        )

    total_weight = sum(weights.values())

    if abs(total_weight - 1.0) > 0.001:
        st.error(f"Weights sum to {total_weight:.2f}. Please adjust to sum to 1.0")
    else:
        st.success("Weights are valid")

    st.divider()

    # Hyperparameters
    st.subheader("Model Hyperparameters")

    with st.expander("Random Forest Settings"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("n_estimators", value=100, min_value=10, max_value=500)
        with col2:
            st.number_input("max_depth", value=10, min_value=1, max_value=50)
        with col3:
            st.number_input("min_samples_split", value=2, min_value=2, max_value=20)

    with st.expander("XGBoost Settings"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("n_estimators", value=200, min_value=10, max_value=1000, key="xgb_n")
        with col2:
            st.number_input("max_depth", value=6, min_value=1, max_value=20, key="xgb_depth")
        with col3:
            st.number_input("learning_rate", value=0.1, min_value=0.01, max_value=0.5, key="xgb_lr")

    with st.expander("LightGBM Settings"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("n_estimators", value=200, min_value=10, max_value=1000, key="lgb_n")
        with col2:
            st.number_input("max_depth", value=8, min_value=1, max_value=20, key="lgb_depth")
        with col3:
            st.number_input("learning_rate", value=0.1, min_value=0.01, max_value=0.5, key="lgb_lr")

    st.divider()

    # Save configuration
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("💾 Save Configuration", type="primary"):
            st.success("Configuration saved successfully!")

    with col2:
        if st.button("🔄 Reset to Defaults"):
            st.info("Configuration reset to defaults")


def render_model_training():
    """Render model training section"""

    st.subheader("Train Models")

    col1, col2 = st.columns(2)

    with col1:
        sport_select = st.selectbox(
            "Select Sport",
            ["All Sports", "NFL", "NBA", "MLB", "NHL"],
            key="train_sport"
        )

    with col2:
        model_select = st.multiselect(
            "Select Models",
            list(MODELS.keys()),
            default=list(MODELS.keys()),
            key="train_models"
        )

    st.divider()

    # Training options
    st.subheader("Training Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.checkbox("Use cross-validation", value=True)
        st.number_input("CV Folds", value=5, min_value=2, max_value=10)

    with col2:
        st.checkbox("Hyperparameter tuning", value=False)
        st.number_input("Tuning iterations", value=50, min_value=10, max_value=200)

    with col3:
        st.checkbox("Save model checkpoints", value=True)
        st.checkbox("Generate SHAP values", value=True)

    st.divider()

    # Training progress
    st.subheader("Training Status")

    if 'training_active' not in st.session_state:
        st.session_state.training_active = False

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("🚀 Start Training", type="primary", disabled=st.session_state.training_active):
            st.session_state.training_active = True
            st.rerun()

    with col2:
        if st.button("⏹️ Stop Training", disabled=not st.session_state.training_active):
            st.session_state.training_active = False
            st.rerun()

    if st.session_state.training_active:
        st.info("⚙️ **Training in Progress** - Estimated time remaining: 15 minutes")

        # Progress bars for each model
        for model in model_select:
            progress = np.random.uniform(0.3, 0.9)
            st.progress(progress, text=f"{model}: {progress*100:.0f}% complete")
    else:
        st.info("🎯 No training in progress. Click 'Start Training' to begin.")

    # Training history
    st.subheader("Training History")

    history_data = pd.DataFrame({
        'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d %H:%M') for i in range(5)],
        'Sport': ['NFL', 'All Sports', 'NBA', 'NHL', 'MLB'],
        'Models': ['All', 'XGBoost', 'All', 'All', 'All'],
        'Duration': ['45m', '12m', '42m', '38m', '40m'],
        'Accuracy': [0.589, 0.592, 0.571, 0.552, 0.563],
        'Status': ['✓ Complete', '✓ Complete', '✓ Complete', '✓ Complete', '✓ Complete']
    })

    st.dataframe(
        history_data,
        width="stretch",
        hide_index=True,
        column_config={
            "Accuracy": st.column_config.ProgressColumn(
                "Accuracy",
                format="%.1f%%",
                min_value=0.5,
                max_value=0.7
            )
        }
    )
