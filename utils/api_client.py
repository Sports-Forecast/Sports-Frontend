"""
API Client for communicating with the Sports Prediction Backend
"""
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime
import streamlit as st
from config import API_BASE_URL, API_TIMEOUT

class APIClient:
    """Handles all API communications with the backend"""

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        timeout: int = API_TIMEOUT
    ) -> Dict[str, Any]:
        """Make HTTP request to the API"""
        url = f"{self.base_url}{endpoint}"
        
        # Add API Key from session state if available
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if 'api_key' in st.session_state and st.session_state.api_key:
            headers["X-API-Key"] = st.session_state.api_key

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=timeout,
                headers=headers
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Connection failed. Is the backend running?"}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out"}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": f"HTTP Error: {e.response.status_code} {e.response.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Authentication Endpoints
    def login(self, identifier: str, api_key: str) -> Dict[str, Any]:
        """Authenticate user with the backend"""
        data = {
            "identifier": identifier,
            "api_key": api_key
        }
        return self._make_request("POST", "/login", data=data)

    def get_profile(self) -> Dict[str, Any]:
        """Get user profile and subscription info"""
        return self._make_request("GET", "/profile")

    # Subscription Endpoints
    def create_checkout_session(self, plan: str, success_url: str, cancel_url: str) -> Dict[str, Any]:
        """Create a checkout session for a subscription plan"""
        data = {
            "plan_name": plan,
            "success_url": success_url,
            "cancel_url": cancel_url,
        }
        return self._make_request("POST", "/subscriptions/checkout", data=data)

    def cancel_subscription(self) -> Dict[str, Any]:
        """Cancel the user's subscription"""
        data = {
            "cancel_at_period_end": False
        }
        return self._make_request("POST", "/subscriptions/cancel", data=data)

    # Health Check
    def health_check(self) -> Dict[str, Any]:
        """Check if the backend is running"""
        return self._make_request("GET", "/health")

    # NFL Endpoints
    def get_nfl_predictions(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Get NFL predictions for upcoming games"""
        params = {"date": date, "use_odds": True} if date else None
        return self._make_request("GET", "/api/predict/nfl", params=params)

    def get_nfl_qbs(self) -> Dict[str, Any]:
        """Get NFL quarterback database with tier ratings"""
        return self._make_request("GET", "/api/nfl/qbs")

    def get_nfl_team_form(self, team_abbr: str) -> Dict[str, Any]:
        """Get recent team performance metrics"""
        return self._make_request("GET", f"/api/nfl/team/{team_abbr}/form")

    # NBA Endpoints
    def get_nba_predictions(
        self,
        date: Optional[str] = None,
        include_players: bool = True,
        include_form: bool = True,
        force_refresh: bool = False
    ) -> Dict[str, Any]:
        """Get NBA predictions for upcoming games"""
        params = {
            "include_players": include_players,
            "include_form": include_form,
            "force_refresh": force_refresh,
            "use_odds": True
        }
        if date:
            params["date"] = date
        return self._make_request("GET", "/api/predict/nba", params=params)

    def get_nba_players(self) -> Dict[str, Any]:
        """Get NBA star players database"""
        return self._make_request("GET", "/api/nba/players")

    def get_nba_team_form(self, team_abbr: str) -> Dict[str, Any]:
        """Get NBA team recent performance"""
        return self._make_request("GET", f"/api/nba/team/{team_abbr}/form")

    # MLB Endpoints
    def get_mlb_predictions(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Get MLB predictions for upcoming games"""
        params = {"date": date, "use_odds": True} if date else None
        return self._make_request("GET", "/api/predict/mlb", params=params)

    def get_mlb_pitchers(self) -> Dict[str, Any]:
        """Get MLB pitcher database"""
        return self._make_request("GET", "/api/mlb/pitchers")

    # NHL Endpoints
    def get_nhl_predictions(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Get NHL predictions for upcoming games"""
        params = {"date": date, "use_odds": True} if date else None
        return self._make_request("GET", "/api/predict/nhl", params=params)

    # Live Prediction Endpoints
    def get_live_predictions(self, sport: str) -> Dict[str, Any]:
        """Get live predictions for a specific sport"""
        sport_lower = sport.lower()
        return self._make_request("GET", f"/api/predict/live/{sport_lower}")

    def get_nhl_goalies(self) -> Dict[str, Any]:
        """Get NHL goalie database"""
        return self._make_request("GET", "/api/nhl/goalies")

    # Generic Prediction
    def get_prediction(self, league: str, game_id: str) -> Dict[str, Any]:
        """Get prediction for a specific game"""
        return self._make_request("GET", f"/api/predict/{league}/{game_id}")

    # Models Endpoints
    def get_models(self) -> Dict[str, Any]:
        """Get available prediction models"""
        return self._make_request("GET", "/api/models")

    def get_model_performance(self, model_name: str) -> Dict[str, Any]:
        """Get model performance metrics"""
        return self._make_request("GET", f"/api/models/{model_name}/performance")

    def train_model(self, league: str, model_config: Dict) -> Dict[str, Any]:
        """Trigger model training"""
        return self._make_request("POST", f"/api/models/train/{league}", data=model_config)

    # Simulations
    def run_simulation(self, config: Dict) -> Dict[str, Any]:
        """Run a Monte Carlo simulation"""
        return self._make_request("POST", "/api/simulations/run", data=config)

    def get_simulation_results(self, simulation_id: str) -> Dict[str, Any]:
        """Get simulation results"""
        return self._make_request("GET", f"/api/simulations/{simulation_id}")

    # Backtesting
    def run_backtest(self, config: Dict) -> Dict[str, Any]:
        """Run backtesting on historical data"""
        return self._make_request("POST", "/api/backtest/run", data=config)

    def get_backtest_results(self, backtest_id: str) -> Dict[str, Any]:
        """Get backtest results"""
        return self._make_request("GET", f"/api/backtest/{backtest_id}")

    # Logs
    def get_logs(self, level: str = "all", limit: int = 100) -> Dict[str, Any]:
        """Get system logs"""
        return self._make_request(
            "GET", "/api/logs", params={"level": level, "limit": limit}
        )


@st.cache_resource
def get_api_client() -> APIClient:
    """Get a cached API client instance"""
    return APIClient()


def check_backend_status() -> bool:
    """Quick check if backend is available"""
    client = get_api_client()
    result = client.health_check()
    return result.get("success", False)
