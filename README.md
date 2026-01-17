# Sports Prediction Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**AI-powered sports prediction platform with real-time market integration**

[Live Demo](https://sports-predictors.streamlit.app) · [Backend API](https://github.com/OsamaASidd/Sports-Prediction-Platform) · [Report Bug](https://github.com/OsamaASidd/Sports-Prediction-Platform/issues)

</div>

---

## Overview

The Sports Prediction Platform is a comprehensive analytics dashboard for game predictions across **NFL, NBA, MLB, and NHL**. It leverages ensemble machine learning models processing **20+ features per game** including team form, player injuries, market signals, and sport-specific metrics.

### Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Sport Support** | Full dashboards for NFL, NBA, MLB, and NHL |
| **Live Predictions** | Real-time game predictions with blinking LIVE indicator |
| **SHAP Explainability** | Visual feature importance breakdown for every prediction |
| **Market Odds Integration** | Spread, over/under, and betting line analysis from API-Sports |
| **Player Impact Tracking** | Track how injuries and star availability affect outcomes |
| **Team Form Analytics** | Recent performance metrics and trends |
| **Monte Carlo Simulations** | Probability distributions for game outcomes |
| **Export Capabilities** | Download predictions as CSV or PDF |

---

## Screenshots

### Main Dashboard
The overview dashboard provides at-a-glance metrics across all sports with model accuracy tracking.

### Sport-Specific Predictions
Each sport dashboard includes detailed game cards with expandable analysis featuring three tabs:

| Tab | Contents |
|-----|----------|
| **Feature Impact** | SHAP waterfall chart + Monte Carlo simulation + Market Odds Analysis |
| **Star Players** | Player availability, tier ratings, and individual impact percentages |
| **Team Form** | Recent records, net ratings, and sport-specific performance metrics |

---

## Prediction Features by Sport

### 🏀 NBA Basketball

| Feature Category | Weight | Metrics |
|------------------|--------|---------|
| **Team Form** | 70% | Net Rating (5/10 games), Point Differential |
| **Star Players** | 20% | MVP/All-Star/Starter/Role tiers with availability status |
| **Home Court** | 8% | Home advantage adjustment |
| **Market Odds** | 20% | Spread adjustment, total adjustment |

**SHAP Features Displayed:**
- Team Form
- Star Players (with individual player impact)
- Back-to-Back penalty
- Market Spread
- Home Advantage

---

### 🏈 NFL Football

| Feature Category | Weight | Metrics |
|------------------|--------|---------|
| **Team Form** | 36% | Point differential over last 3-5 games |
| **QB Impact** | 20% | Quarterback tier (Elite → Below Avg) with passer rating |
| **Rest & Schedule** | 18% | Rest days advantage/disadvantage |
| **Turnover Risk** | 18% | Turnover differential analysis |
| **Home Advantage** | 8% | Home field factor |
| **Weather** | 5% | Cold, wind, precipitation impacts |

**SHAP Features Displayed:**
- QB Impact
- Weather
- Turnover Risk
- Rest Advantage
- Team Form
- Market Spread

---

### ⚾ MLB Baseball

| Feature Category | Weight | Metrics |
|------------------|--------|---------|
| **Starting Pitcher** | 60% | ERA, WHIP, K/9, K/BB ratio, Tier (Ace/Quality/Backend) |
| **Team Offense** | 19% | Runs per game (L7), Run differential |
| **Bullpen** | 13% | Relief pitcher quality and ERA |
| **Market Odds** | 22% | Runline adjustment |
| **Context** | 8% | Venue, weather for outdoor games |

**SHAP Features Displayed:**
- Starting Pitcher (with ERA/WHIP stats)
- Bullpen
- Team Offense
- Weather
- Market Spread

---

### 🏒 NHL Hockey

| Feature Category | Weight | Metrics |
|------------------|--------|---------|
| **Goal Differential** | 32% | Goals for/against over 5/10 games |
| **Goalie Impact** | 18% | Save%, GAA, Tier (Elite/Starting/Backup) |
| **Special Teams** | 18% | Power Play %, Penalty Kill % |
| **Market Odds** | 20% | Puckline adjustment |
| **Season Record** | 8% | Overall win percentage |
| **Home Advantage** | 6% | Home ice factor |

**SHAP Features Displayed:**
- Goalie Impact (with Save%/GAA)
- Goal Differential
- Special Teams
- Market Spread
- Home Advantage

---

## Market Odds Integration

All predictions incorporate real-time betting market signals from API-Sports:

| Metric | Description |
|--------|-------------|
| **Spread** | Point spread with ~2.5-3% probability conversion per point |
| **Over/Under** | Total points/runs/goals line |
| **Spread Adjustment** | How much the spread moved the prediction (capped at 15-18%) |
| **Total Adjustment** | How the total line affected analysis |
| **Data Source** | API-Sports with intelligent fallback defaults |

---

## Live Game Predictions

Click the blinking red **🔴 LIVE** button on any sport dashboard to view games currently in progress:

- **Live Scores**: Updated in real-time
- **Dynamic Probabilities**: Win percentages adjust as the game progresses
- **Period/Quarter Display**: Current game state
- **Live Spread**: Real-time betting line movement

---

## Installation

### Prerequisites

- Python 3.9+
- Backend API running (see [Backend Repository](https://github.com/OsamaASidd/Sports-Prediction-Platform))

### Quick Start

```bash
# Clone the repository
git clone https://github.com/OsamaASidd/Sports-Prediction-Platform.git
cd "Predictive Frontend"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API_BASE_URL

# Run the application
streamlit run app.py
```

### Environment Variables

```env
# Backend API Configuration
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30

# Application Settings
DEBUG_MODE=false
```

---

## Project Structure

```
Predictive Frontend/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration and environment variables
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
│
├── components/               # Reusable UI components
│   ├── cards.py              # Prediction, stat, model cards
│   ├── header.py             # Page headers and breadcrumbs
│   ├── sidebar.py            # Navigation menu and quick stats
│   └── status_panel.py       # Backend status and notifications
│
├── pages/                    # Application pages
│   ├── dashboard.py          # Main overview dashboard
│   ├── sport_dashboard.py    # Sport-specific dashboards
│   ├── models.py             # ML model management
│   ├── simulations.py        # Monte Carlo simulations
│   ├── backtesting.py        # Historical backtesting
│   ├── logs.py               # System logs viewer
│   └── settings.py           # Application settings
│
└── utils/                    # Utility modules
    ├── api_client.py         # Backend API communication
    ├── charts.py             # Plotly chart generators
    ├── export.py             # CSV/PDF export functions
    └── styles.py             # Custom CSS (Fluent Design theme)
```

---

## API Endpoints

### Predictions

| Endpoint | Description |
|----------|-------------|
| `GET /api/predict/nba` | NBA daily predictions with star player impact |
| `GET /api/predict/nfl` | NFL predictions with QB and weather adjustments |
| `GET /api/predict/mlb` | MLB predictions with pitcher analysis |
| `GET /api/predict/nhl` | NHL predictions with goalie impact |
| `GET /api/predict/live/{sport}` | Live game predictions |

### Player/Team Data

| Endpoint | Description |
|----------|-------------|
| `GET /api/nba/stars` | NBA star player database with tiers |
| `GET /api/nfl/qbs` | NFL quarterback tier ratings |
| `GET /api/mlb/pitchers` | MLB pitcher database |
| `GET /api/nhl/goalies` | NHL goalie database |
| `GET /api/{sport}/team/{abbr}/form` | Team recent form metrics |

### System

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Backend health check |
| `GET /api/models` | Available ML models |
| `GET /api/data-sources` | Data source configuration |

---

## Styling & Theme

The platform uses a modern **Fluent Design-inspired** dark theme:

### Color Palette

| Variable | Color | Usage |
|----------|-------|-------|
| `--primary` | `#0078D4` | Primary actions, selected states |
| `--accent` | `#00BCF2` | Highlights, links |
| `--success` | `#4CAF50` | Positive indicators, high confidence |
| `--warning` | `#FF9800` | Medium confidence, alerts |
| `--error` | `#F44336` | LIVE button, negative indicators |
| `--bg-dark` | `#1E1E1E` | Main background |
| `--surface` | `#2D2D30` | Card backgrounds |

### Custom Animations

- **LIVE Button**: Pulsing red glow animation
- **Live Game Cards**: Red border with blinking LIVE badge
- **Hover Effects**: Smooth transitions on all interactive elements

---

## Dependencies

```
streamlit>=1.28.0
streamlit-option-menu>=0.3.6
streamlit-autorefresh>=1.0.1
plotly>=5.18.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
python-dotenv>=1.0.0
fpdf2>=2.7.0
```

---

## Usage Tips

1. **Check predictions close to game time** - Data updates regularly with latest information
2. **Consider confidence scores** - Higher confidence (70%+) predictions tend to be more reliable
3. **Expand detailed analysis** - Click "View Detailed Analysis" for SHAP explanations
4. **Track player injuries** - The Star Players tab shows who's out and impact
5. **Use export features** - Download CSV for your own analysis

---

## Troubleshooting

### Backend Connection Issues
```
Error: "Connection failed. Is the backend running?"
```
**Solution**: Verify `API_BASE_URL` in `.env` and ensure backend is running

### Clear Cache
```bash
streamlit cache clear
```

### Different Port
```bash
streamlit run app.py --server.port 8502
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Streamlit](https://streamlit.io/) - Data app framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [API-Sports](https://api-sports.io/) - Sports data provider
- [SHAP](https://shap.readthedocs.io/) - ML explainability

---

## Contact

**Osama Siddiqui** - [@OsamaASidd](https://github.com/OsamaASidd)

**Live Platform**: [sports-predictors.streamlit.app](https://sports-predictors.streamlit.app)

**Backend API Docs**: [API Documentation](https://sportspredictor-backend-app-6e075ffc23f5.herokuapp.com/docs)

---

<div align="center">

**Sports Prediction Platform** - Making smarter predictions with AI

</div>
