# Sports Prediction Platform - Frontend

<div align="center">

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

**A modern, analytics-ready dashboard for AI-powered sports predictions**

[Live Demo](https://sports-predictors.streamlit.app) · [Backend API](https://github.com/OsamaASidd/Sports-Prediction-Backend) · [Report Bug](https://github.com/OsamaASidd/Sports-Frontend/issues)

</div>

---

## Overview

The Sports Prediction Platform Frontend provides a sleek, intuitive interface for viewing machine learning-powered sports predictions across multiple leagues. Built with Streamlit and featuring a modern Fluent Design-inspired dark theme.

### Main Dashboard
![Dashboard](screenshots/dashboard.png)
*Overview showing today's predictions, 7-day accuracy metrics, model performance radar chart, and ensemble weights*

### NBA Predictions
![NBA Dashboard](screenshots/nba_dashboard.png)
*NBA predictions with win probabilities, confidence scores, star player impact, and team form analysis*

---

## Features

### Multi-Sport Support

| Sport | Features |
|-------|----------|
| 🏀 **NBA** | Player impact analysis, team form, injury adjustments |
| 🏈 **NFL** | Quarterback impact ratings, weekly matchups |
| ⚾ **MLB** | Starting pitcher analysis, venue factors |
| 🏒 **NHL** | Goalie performance tracking, home ice advantage |

### Key Capabilities

- **Real-time Predictions** - Live predictions from backend API with confidence scores
- **Date Selection** - View predictions for any date
- **Team Analysis** - Deep dive into team performance and recent form
- **Model Transparency** - View feature weights and prediction factors
- **Export Options** - Download predictions as CSV or PDF reports
- **Responsive Design** - Modern dark theme optimized for all screen sizes

### Dashboard Views

| Page | Description |
|------|-------------|
| **Dashboard** | Overview of all predictions and model performance metrics |
| **NBA/NFL/MLB/NHL** | Sport-specific predictions with date selection |
| **Models** | Ensemble model details, weights, and accuracy tracking |
| **Simulations** | Monte Carlo simulation configuration |
| **Backtesting** | Historical performance analysis |
| **Logs** | System logs and API activity monitoring |
| **Settings** | Application configuration |

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Framework** | Streamlit 1.28+ |
| **UI Components** | streamlit-option-menu, streamlit-extras |
| **Visualization** | Plotly |
| **Data Processing** | Pandas, NumPy |
| **API Communication** | Requests |
| **Export** | ReportLab (PDF), FPDF2, OpenPyXL |
| **Styling** | Custom CSS (Fluent Design) |

---

## Project Structure

```
Sports-Frontend/
├── app.py                    # Main application entry point
├── config.py                 # Configuration & environment variables
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in repo)
├── .gitignore               # Git ignore rules
│
├── components/              # Reusable UI components
│   ├── __init__.py
│   ├── cards.py             # Prediction, stat, and model cards
│   ├── header.py            # Page headers with timestamps
│   ├── sidebar.py           # Navigation sidebar & sport submenu
│   └── status_panel.py      # Backend status indicator
│
├── pages/                   # Application pages
│   ├── __init__.py
│   ├── dashboard.py         # Main dashboard with overview
│   ├── sport_dashboard.py   # Sport-specific predictions
│   ├── models.py            # Model performance & configuration
│   ├── simulations.py       # Monte Carlo simulations
│   ├── backtesting.py       # Historical backtesting
│   ├── logs.py              # System logs viewer
│   └── settings.py          # App settings
│
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── api_client.py        # Backend API client class
│   ├── charts.py            # Plotly chart generators
│   ├── export.py            # CSV/PDF export functions
│   └── styles.py            # Custom CSS styles
│
└── screenshots/             # README screenshots
    ├── dashboard.png
    └── nba_dashboard.png
```

---

## Installation

### Prerequisites

- Python 3.9+
- pip package manager
- Access to the Sports Prediction Backend API

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/OsamaASidd/Sports-Frontend.git
   cd Sports-Frontend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the root directory:
   ```env
   # Backend API Configuration
   API_BASE_URL=https://sportspredictor-backend-app.herokuapp.com
   API_TIMEOUT=150

   # Database (optional - for direct queries)
   DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

   # Application Settings
   DEBUG_MODE=true
   APP_ENV=development

   # Refresh Intervals (seconds)
   LIVE_ODDS_REFRESH=45
   PREDICTIONS_REFRESH=60
   DASHBOARD_REFRESH=120
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**

   Open your browser to `http://localhost:8501`

---

## Deployment

### Streamlit Cloud (Recommended)

1. **Push code to GitHub**

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Connect your GitHub repository**

4. **Configure secrets** in App Settings > Secrets (TOML format):

   ```toml
   API_BASE_URL = "https://sportspredictor-backend-app.herokuapp.com"
   API_TIMEOUT = 150
   DATABASE_URL = "postgresql://user:pass@host/db?sslmode=require"
   DEBUG_MODE = false
   APP_ENV = "production"
   LIVE_ODDS_REFRESH = 45
   PREDICTIONS_REFRESH = 60
   DASHBOARD_REFRESH = 120
   ```

5. **Deploy!**

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t sports-frontend .
docker run -p 8501:8501 --env-file .env sports-frontend
```

---

## API Integration

The frontend connects to a FastAPI backend. Key endpoints:

| Endpoint | Method | Parameters | Description |
|----------|--------|------------|-------------|
| `/api/predict/nba` | GET | `date`, `include_players`, `include_form` | NBA predictions |
| `/api/predict/nfl` | GET | `date` | NFL predictions |
| `/api/predict/mlb` | GET | `date` | MLB predictions |
| `/api/predict/nhl` | GET | `date` | NHL predictions |
| `/health` | GET | - | Backend health check |

### Example Response (NBA)

```json
{
  "date": "20260110",
  "total_games": 6,
  "predictions": [
    {
      "game_id": 401810398,
      "home_team": "Indiana Pacers",
      "away_team": "Miami Heat",
      "home_win_probability": 0.202,
      "away_win_probability": 0.798,
      "confidence": 0.798,
      "venue": "Gainbridge Fieldhouse",
      "star_impact": {
        "home_stars": [...],
        "away_stars": [...]
      },
      "team_form": {
        "home_form": { "record_last_5": "2-3" },
        "away_form": { "record_last_5": "4-1" }
      }
    }
  ]
}
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | Backend API URL | `http://localhost:8000` |
| `API_TIMEOUT` | Request timeout (seconds) | `30` |
| `DEBUG_MODE` | Enable debug logging | `false` |
| `APP_ENV` | Environment mode | `development` |

### Theme Customization

Modify colors in `utils/styles.py`:

```css
:root {
    --primary: #0078D4;
    --primary-dark: #106EBE;
    --accent: #00BCF2;
    --bg-dark: #1E1E1E;
    --bg-light: #252526;
    --success: #4CAF50;
    --warning: #FF9800;
    --error: #F44336;
}
```

---

## Usage Guide

### Viewing Predictions

1. Select a sport from the sidebar (🏀 NBA, 🏈 NFL, ⚾ MLB, 🏒 NHL)
2. Choose a date using the date picker
3. View predictions sorted by game time or confidence
4. Click "View Detailed Analysis" for Monte Carlo simulation and SHAP analysis

### Understanding Predictions

| Metric | Description |
|--------|-------------|
| **Win Probability** | Model's predicted chance of winning (0-100%) |
| **Confidence** | How confident the model is in its prediction |
| **Star Impact** | Adjustment based on key player availability |
| **Form Adjustment** | Recent team performance factor (last 5/10 games) |

### Exporting Data

- **CSV** - Raw data for spreadsheet analysis
- **PDF** - Formatted reports with visualizations

---

## Development

### Adding New Features

1. Create new page in `pages/` directory
2. Add route in `app.py` main function
3. Add navigation item in `components/sidebar.py`

### API Client

Extend `utils/api_client.py` for new endpoints:

```python
def get_custom_data(self, param: str) -> Dict[str, Any]:
    return self._make_request("GET", f"/api/custom/{param}")
```

### Custom Components

Add reusable components in `components/cards.py`:

```python
def render_custom_card(title: str, value: str):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{title}</div>
    </div>
    """, unsafe_allow_html=True)
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Related Projects

- [Sports Prediction Backend](https://github.com/OsamaASidd/Sports-Prediction-Backend) - FastAPI backend with ML ensemble models
- [Heroku Backend](https://sportspredictor-backend-app-6e075ffc23f5.herokuapp.com/docs) - API Documentation

---

## License

This project is licensed under the MIT License.

---

<div align="center">

**Built with Streamlit** · **Powered by Machine Learning**

Made with ❤️ by [OsamaASidd](https://github.com/OsamaASidd)

</div>
