"""
Logs Page - System logs and monitoring
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from components import render_header, render_stat_card, render_log_entry


def render_logs_page():
    """Render the logs page"""

    render_header(
        title="System Logs",
        subtitle="Monitor system activity, errors, and performance metrics"
    )

    # Stats overview
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card(
            title="Total Entries",
            value="2,847",
            icon="📊",
            color="#0078D4"
        )

    with col2:
        render_stat_card(
            title="Errors (24h)",
            value="3",
            icon="⚠️",
            color="#F44336"
        )

    with col3:
        render_stat_card(
            title="Warnings (24h)",
            value="12",
            icon="⚡",
            color="#FF9800"
        )

    with col4:
        render_stat_card(
            title="API Calls (24h)",
            value="1,456",
            icon="🔗",
            color="#4CAF50"
        )

    st.divider()

    # Tabs
    tab1, tab2, tab3 = st.tabs(["All Logs", "Errors & Warnings", "Analytics"])

    with tab1:
        render_all_logs()

    with tab2:
        render_error_logs()

    with tab3:
        render_log_analytics()


def render_all_logs():
    """Render all logs view"""

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        level_filter = st.selectbox(
            "Log Level",
            ["All", "INFO", "WARNING", "ERROR", "DEBUG"],
            key="log_level"
        )

    with col2:
        source_filter = st.selectbox(
            "Source",
            ["All", "API", "Models", "Database", "Scheduler", "Frontend"],
            key="log_source"
        )

    with col3:
        time_filter = st.selectbox(
            "Time Range",
            ["Last Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days"],
            key="log_time"
        )

    with col4:
        search = st.text_input("Search logs...", key="log_search")

    st.divider()

    # Real-time toggle
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        auto_refresh = st.checkbox("Auto-refresh", value=True, key="auto_refresh")

    with col2:
        if st.button("🔄 Refresh Now"):
            st.rerun()

    # Sample log entries
    logs = generate_sample_logs(50)

    # Filter logs based on selection
    if level_filter != "All":
        logs = [log for log in logs if log['level'] == level_filter]
    if source_filter != "All":
        logs = [log for log in logs if log['source'] == source_filter]
    if search:
        logs = [log for log in logs if search.lower() in log['message'].lower()]

    # Display logs
    st.subheader(f"Showing {len(logs)} log entries")

    for log in logs:
        render_log_entry(
            timestamp=log['timestamp'],
            level=log['level'],
            message=log['message'],
            source=log['source']
        )

    # Export
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        logs_df = pd.DataFrame(logs)
        csv = logs_df.to_csv(index=False)
        st.download_button(
            label="📥 Export CSV",
            data=csv,
            file_name=f"logs_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

    with col2:
        if st.button("🗑️ Clear Old Logs"):
            st.info("Cleared logs older than 7 days")


def render_error_logs():
    """Render error and warning logs"""

    st.subheader("Recent Errors")

    # Error cards
    errors = [
        {
            "timestamp": "2024-01-15 14:32:15",
            "level": "ERROR",
            "message": "Database connection timeout after 30s",
            "source": "Database",
            "stack_trace": "ConnectionError: Failed to establish connection to database\n  at connect() in db_client.py:45\n  at get_predictions() in api/routes.py:128"
        },
        {
            "timestamp": "2024-01-15 12:18:42",
            "level": "ERROR",
            "message": "Model inference failed: insufficient memory",
            "source": "Models",
            "stack_trace": "MemoryError: Unable to allocate 512MB for model inference\n  at predict() in models/ensemble.py:89"
        },
        {
            "timestamp": "2024-01-14 23:45:10",
            "level": "ERROR",
            "message": "ESPN API rate limit exceeded",
            "source": "API",
            "stack_trace": "RateLimitError: 429 Too Many Requests\n  at fetch_games() in data_fetchers/espn.py:67"
        }
    ]

    for error in errors:
        st.error(f"**{error['level']}** - {error['timestamp']}\n\n{error['message']}\n\n_Source: {error['source']}_")

        with st.expander("View Stack Trace"):
            st.code(error['stack_trace'], language="python")

    st.divider()

    st.subheader("Recent Warnings")

    warnings = [
        {"timestamp": "2024-01-15 15:20:33", "message": "Model accuracy below threshold (54.2%)", "source": "Models"},
        {"timestamp": "2024-01-15 14:55:18", "message": "High memory usage detected (85%)", "source": "System"},
        {"timestamp": "2024-01-15 14:12:45", "message": "Slow API response time (>2s)", "source": "API"},
        {"timestamp": "2024-01-15 13:45:22", "message": "Missing data for 3 games", "source": "Database"},
        {"timestamp": "2024-01-15 12:30:10", "message": "Backup job delayed by 30 minutes", "source": "Scheduler"},
    ]

    for warning in warnings:
        st.warning(f"**{warning['timestamp']}** | _{warning['source']}_\n\n{warning['message']}")


def render_log_analytics():
    """Render log analytics"""

    st.subheader("Log Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Log distribution by level
        st.markdown("**Log Distribution by Level**")

        level_data = pd.DataFrame({
            'Level': ['INFO', 'DEBUG', 'WARNING', 'ERROR'],
            'Count': [2456, 312, 67, 12],
            'Percentage': [86.3, 11.0, 2.4, 0.4]
        })

        st.dataframe(level_data, use_container_width=True, hide_index=True)

        # Visual bars using progress
        for _, row in level_data.iterrows():
            level = row['Level']
            pct = row['Percentage']
            st.progress(pct / 100, text=f"{level}: {row['Count']} ({pct}%)")

    with col2:
        # Log distribution by source
        st.markdown("**Log Distribution by Source**")

        source_data = pd.DataFrame({
            'Source': ['API', 'Models', 'Database', 'Scheduler', 'Frontend', 'System'],
            'Count': [1245, 567, 423, 312, 189, 111],
            'Percentage': [43.7, 19.9, 14.9, 11.0, 6.6, 3.9]
        })

        st.dataframe(source_data, use_container_width=True, hide_index=True)

    st.divider()

    # Activity over time
    st.markdown("**Activity Over Time (Last 24 Hours)**")

    # Generate hourly data
    hours = [(datetime.now() - timedelta(hours=i)).strftime('%H:00') for i in range(23, -1, -1)]
    activity = [int(50 + 100 * abs(np.sin(i/4)) + np.random.randint(-20, 20)) for i in range(24)]

    activity_df = pd.DataFrame({'Hour': hours, 'Log Count': activity})
    st.bar_chart(activity_df.set_index('Hour'))

    st.divider()

    # System health
    st.subheader("System Health")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🖥️ Uptime",
            value="98.5%",
            delta="30 days"
        )

    with col2:
        st.metric(
            label="⚡ Avg Response",
            value="245ms",
            delta="-15ms"
        )

    with col3:
        st.metric(
            label="💾 Memory",
            value="65%",
            delta="5%",
            delta_color="inverse"
        )

    with col4:
        st.metric(
            label="🔥 CPU",
            value="12%",
            delta="-3%"
        )


def generate_sample_logs(count: int):
    """Generate sample log entries"""
    levels = ['INFO', 'INFO', 'INFO', 'INFO', 'DEBUG', 'WARNING', 'ERROR']
    sources = ['API', 'Models', 'Database', 'Scheduler', 'Frontend']
    messages = {
        'INFO': [
            'Prediction request processed successfully',
            'Model loaded into memory',
            'Database query completed in 45ms',
            'Scheduled job started: data_sync',
            'User session created',
            'API endpoint /predict/nfl called',
            'Cache hit for game prediction'
        ],
        'DEBUG': [
            'Feature extraction completed: 45 features',
            'Model weights: LR=0.15, RF=0.25, XGB=0.35, LGB=0.25',
            'Database connection pool: 5/10 active'
        ],
        'WARNING': [
            'Slow query detected (>1s)',
            'Model confidence below threshold',
            'Memory usage above 80%',
            'API rate limit approaching'
        ],
        'ERROR': [
            'Database connection failed',
            'Model inference timeout',
            'External API unavailable'
        ]
    }

    logs = []
    for i in range(count):
        level = np.random.choice(levels)
        logs.append({
            'timestamp': (datetime.now() - timedelta(minutes=i*2)).strftime('%Y-%m-%d %H:%M:%S'),
            'level': level,
            'source': np.random.choice(sources),
            'message': np.random.choice(messages[level])
        })

    return logs
