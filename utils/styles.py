"""
Custom CSS styles for the Sports Prediction Platform
Modern Fluent Design inspired styling
"""

MAIN_STYLES = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Root Variables */
:root {
    --primary: #0078D4;
    --primary-dark: #106EBE;
    --primary-light: #00BCF2;
    --accent: #00BCF2;
    --bg-dark: #1E1E1E;
    --bg-light: #252526;
    --surface: #2D2D30;
    --surface-hover: #3E3E42;
    --text-primary: #FFFFFF;
    --text-secondary: #CCCCCC;
    --text-muted: #8A8A8A;
    --success: #4CAF50;
    --warning: #FF9800;
    --error: #F44336;
    --info: #2196F3;
    --border-radius: 8px;
    --border-radius-lg: 12px;
    --shadow-sm: 0 2px 4px rgba(0,0,0,0.2);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.3);
    --shadow-lg: 0 8px 24px rgba(0,0,0,0.4);
    --transition: all 0.2s ease-in-out;
}

/* Global Styles */
.stApp {
    background: linear-gradient(135deg, var(--bg-dark) 0%, #1a1a2e 100%);
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Container */
.main .block-container {
    padding: 1rem 2rem;
    max-width: 100%;
}

/* Sidebar Styles */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, var(--bg-dark) 100%);
    border-right: 1px solid rgba(255,255,255,0.1);
}

section[data-testid="stSidebar"] .stRadio > label {
    color: var(--text-secondary);
    font-weight: 500;
}

/* Card Styles */
.metric-card {
    background: linear-gradient(145deg, var(--surface) 0%, var(--bg-light) 100%);
    border-radius: var(--border-radius-lg);
    padding: 1.5rem;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: var(--shadow-md);
    transition: var(--transition);
    margin-bottom: 1rem;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
}

.metric-label {
    font-size: 0.875rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 0.5rem;
}

.metric-delta-positive {
    color: var(--success);
    font-size: 0.875rem;
}

.metric-delta-negative {
    color: var(--error);
    font-size: 0.875rem;
}

/* Prediction Card */
.prediction-card {
    background: linear-gradient(145deg, var(--surface) 0%, var(--bg-light) 100%);
    border-radius: var(--border-radius-lg);
    padding: 1.5rem;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: var(--shadow-md);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.prediction-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
}

.prediction-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

/* Team Display */
.team-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0;
}

.team-name {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
}

.team-record {
    font-size: 0.875rem;
    color: var(--text-muted);
}

.vs-badge {
    background: var(--primary);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.875rem;
}

/* Probability Bar */
.prob-bar-container {
    background: var(--bg-dark);
    border-radius: 50px;
    height: 40px;
    overflow: hidden;
    position: relative;
    margin: 1rem 0;
}

.prob-bar-fill {
    height: 100%;
    border-radius: 50px;
    transition: width 0.5s ease-out;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    color: white;
}

/* Button Styles */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    border: none;
    border-radius: var(--border-radius);
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    transition: var(--transition);
    box-shadow: var(--shadow-sm);
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Secondary Button */
.secondary-btn > button {
    background: transparent;
    border: 2px solid var(--primary);
    color: var(--primary);
}

.secondary-btn > button:hover {
    background: var(--primary);
    color: white;
}

/* Tab Styles */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: var(--bg-light);
    padding: 0.5rem;
    border-radius: var(--border-radius-lg);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: var(--border-radius);
    padding: 0.75rem 1.5rem;
    color: var(--text-secondary);
    font-weight: 500;
    transition: var(--transition);
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--surface-hover);
    color: var(--text-primary);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    color: white !important;
}

/* Select Box */
.stSelectbox > div > div {
    background: var(--surface);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: var(--border-radius);
    color: var(--text-primary);
}

.stSelectbox > div > div:hover {
    border-color: var(--primary);
}

/* Input Fields */
.stTextInput > div > div > input {
    background: var(--surface);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: var(--border-radius);
    color: var(--text-primary);
    padding: 0.75rem 1rem;
}

.stTextInput > div > div > input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(0,120,212,0.2);
}

/* Data Table */
.stDataFrame {
    border-radius: var(--border-radius-lg);
    overflow: hidden;
}

.stDataFrame > div > div > div > div {
    background: var(--surface);
}

/* Metric Styling */
[data-testid="stMetricValue"] {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary);
}

[data-testid="stMetricDelta"] svg {
    display: none;
}

/* Progress Bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
    border-radius: 50px;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface);
    border-radius: var(--border-radius);
    color: var(--text-primary);
    font-weight: 500;
}

.streamlit-expanderHeader:hover {
    background: var(--surface-hover);
}

/* Alert/Notification Styles */
.alert {
    padding: 1rem 1.5rem;
    border-radius: var(--border-radius);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.alert-success {
    background: rgba(76, 175, 80, 0.15);
    border-left: 4px solid var(--success);
    color: var(--success);
}

.alert-warning {
    background: rgba(255, 152, 0, 0.15);
    border-left: 4px solid var(--warning);
    color: var(--warning);
}

.alert-error {
    background: rgba(244, 67, 54, 0.15);
    border-left: 4px solid var(--error);
    color: var(--error);
}

.alert-info {
    background: rgba(33, 150, 243, 0.15);
    border-left: 4px solid var(--info);
    color: var(--info);
}

/* Status Badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.375rem 0.75rem;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-online {
    background: rgba(76, 175, 80, 0.2);
    color: var(--success);
}

.status-offline {
    background: rgba(244, 67, 54, 0.2);
    color: var(--error);
}

.status-pending {
    background: rgba(255, 152, 0, 0.2);
    color: var(--warning);
}

/* Header Styles */
.page-header {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.page-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.page-subtitle {
    font-size: 1rem;
    color: var(--text-muted);
}

/* Sport Icon Badge */
.sport-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: var(--surface);
    border-radius: var(--border-radius);
    font-weight: 600;
}

/* Model Card */
.model-card {
    background: var(--surface);
    border-radius: var(--border-radius-lg);
    padding: 1.5rem;
    border: 1px solid rgba(255,255,255,0.08);
    transition: var(--transition);
}

.model-card:hover {
    border-color: var(--primary);
}

.model-name {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
}

.model-weight {
    font-size: 0.875rem;
    color: var(--primary);
}

/* Log Entry */
.log-entry {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 0.8125rem;
    padding: 0.5rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex;
    gap: 1rem;
}

.log-timestamp {
    color: var(--text-muted);
    flex-shrink: 0;
}

.log-level-info {
    color: var(--info);
}

.log-level-warning {
    color: var(--warning);
}

.log-level-error {
    color: var(--error);
}

.log-message {
    color: var(--text-secondary);
}

/* Animation Classes */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.animate-fade-in {
    animation: fadeIn 0.3s ease-out;
}

.animate-slide-in {
    animation: slideIn 0.3s ease-out;
}

.animate-pulse {
    animation: pulse 2s infinite;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-dark);
}

::-webkit-scrollbar-thumb {
    background: var(--surface-hover);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary);
}

/* Tooltip */
.tooltip {
    position: relative;
}

.tooltip::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: var(--bg-dark);
    color: var(--text-primary);
    padding: 0.5rem 0.75rem;
    border-radius: var(--border-radius);
    font-size: 0.75rem;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: var(--transition);
    z-index: 1000;
}

.tooltip:hover::after {
    opacity: 1;
    visibility: visible;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem;
    }

    .metric-value {
        font-size: 1.75rem;
    }

    .page-title {
        font-size: 1.5rem;
    }
}

/* Dark mode chart backgrounds */
.js-plotly-plot .plotly .bg {
    fill: transparent !important;
}

/* Glass Effect */
.glass {
    background: rgba(45, 45, 48, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
"""


def get_sport_gradient(sport: str) -> str:
    """Get gradient color for a sport"""
    gradients = {
        "NBA": "linear-gradient(135deg, #C9082A 0%, #552583 100%)",
        "NFL": "linear-gradient(135deg, #013369 0%, #D50A0A 100%)",
        "MLB": "linear-gradient(135deg, #041E42 0%, #BF0D3E 100%)",
        "NHL": "linear-gradient(135deg, #000000 0%, #A2AAAD 100%)"
    }
    return gradients.get(sport, "linear-gradient(135deg, #0078D4 0%, #106EBE 100%)")


def get_confidence_color(confidence: float) -> str:
    """Get color based on confidence level"""
    if confidence >= 0.7:
        return "#4CAF50"
    elif confidence >= 0.6:
        return "#8BC34A"
    elif confidence >= 0.55:
        return "#FF9800"
    else:
        return "#F44336"


def create_metric_card(title: str, value: str, delta: str = None, delta_color: str = "normal") -> str:
    """Generate HTML for a metric card"""
    delta_html = ""
    if delta:
        delta_class = "metric-delta-positive" if delta_color == "positive" else "metric-delta-negative"
        delta_html = f'<div class="{delta_class}">{delta}</div>'

    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{title}</div>
        {delta_html}
    </div>
    """


def create_alert(message: str, alert_type: str = "info") -> str:
    """Generate HTML for an alert"""
    icons = {
        "success": "✓",
        "warning": "⚠",
        "error": "✕",
        "info": "ℹ"
    }
    return f"""
    <div class="alert alert-{alert_type}">
        <span>{icons.get(alert_type, 'ℹ')}</span>
        <span>{message}</span>
    </div>
    """


def create_status_badge(status: str) -> str:
    """Generate HTML for a status badge"""
    status_map = {
        "online": ("🟢", "status-online", "Online"),
        "offline": ("🔴", "status-offline", "Offline"),
        "pending": ("🟡", "status-pending", "Pending")
    }
    dot, css_class, label = status_map.get(status.lower(), ("⚪", "", status))
    return f'<span class="status-badge {css_class}">{dot} {label}</span>'
