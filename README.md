# Sports Prediction Platform - Frontend

A modern, analytics-ready Streamlit interface for the Sports Prediction Platform backend.

## Features

- **Dashboard**: Overview of all sports predictions and model performance
- **Sport-specific Views**: Dedicated dashboards for NBA, NFL, MLB, and NHL
- **Model Management**: View, configure, and train ensemble prediction models
- **Simulations**: Run Monte Carlo simulations with detailed analysis
- **Backtesting**: Historical model performance validation
- **Logs**: System monitoring and analytics
- **Settings**: Full application configuration

## Quick Start

### Prerequisites

- Python 3.9+
- Backend API running (see [Sports-Prediction-Platform](https://github.com/OsamaASidd/Sports-Prediction-Platform))

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run the application:
```bash
# Windows
run.bat

# macOS/Linux
chmod +x run.sh
./run.sh

# Or directly
streamlit run app.py
```

5. Open http://localhost:8501 in your browser

## Project Structure

```
Predictive Frontend/
├── app.py                 # Main application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── components/
│   ├── __init__.py
│   ├── sidebar.py        # Navigation sidebar
│   ├── header.py         # Page headers
│   ├── cards.py          # UI card components
│   └── status_panel.py   # Status and notification panel
├── pages/
│   ├── __init__.py
│   ├── dashboard.py      # Main dashboard
│   ├── sport_dashboard.py # Sport-specific views
│   ├── models.py         # Model management
│   ├── simulations.py    # Monte Carlo simulations
│   ├── backtesting.py    # Historical analysis
│   ├── logs.py           # System logs
│   └── settings.py       # Application settings
├── utils/
│   ├── __init__.py
│   ├── api_client.py     # Backend API client
│   ├── charts.py         # Plotly chart configurations
│   ├── styles.py         # Custom CSS styles
│   └── export.py         # Export functionality (CSV/PDF)
└── assets/               # Static assets
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | Backend API URL | `http://localhost:8000` |
| `API_TIMEOUT` | API request timeout (seconds) | `30` |
| `DEBUG_MODE` | Enable debug mode | `false` |

### Backend Connection

Ensure the backend is running at the configured `API_BASE_URL`. The frontend will display connection status in the sidebar.

## UI Features

### Design System

- **Fluent Design**: Windows 11 inspired with rounded corners, soft shadows, and gradients
- **Dark Theme**: Optimized for extended use with carefully chosen contrast ratios
- **Responsive**: Adapts to different screen sizes
- **Animations**: Smooth transitions for view switching and data updates

### Components

- **Prediction Cards**: Display game predictions with probability bars
- **Stat Cards**: Metric displays with delta indicators
- **Model Cards**: Model performance with status indicators
- **Interactive Charts**: Plotly-based visualizations with dark theme

### Export Options

- **CSV Export**: Raw data for further analysis
- **PDF Reports**: Formatted reports with charts and statistics

## Development

### Adding New Features

1. Create new page in `pages/` directory
2. Add route in `app.py`
3. Add navigation item in `components/sidebar.py`

### Styling

Custom styles are defined in `utils/styles.py`. The main CSS is injected into each page for consistent styling.

### API Integration

The API client in `utils/api_client.py` provides methods for all backend endpoints. Add new methods as needed.

## License

MIT License - See LICENSE file for details.
