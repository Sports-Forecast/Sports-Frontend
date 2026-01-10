@echo off
echo ====================================
echo  Sports Prediction Platform
echo  Starting Streamlit Frontend...
echo ====================================
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Using system Python.
)

REM Check if dependencies are installed
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting Streamlit server...
echo Access the application at: http://localhost:8501
echo.

python -m streamlit run app.py --server.port 8501

pause
