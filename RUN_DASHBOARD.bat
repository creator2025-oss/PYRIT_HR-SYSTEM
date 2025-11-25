@echo off
echo ============================================
echo Starting Compliance Dashboard (Streamlit)
echo ============================================
echo.
echo Dashboard will open at: http://localhost:8501
echo.
echo Make sure HR Simulator is running first!
echo (Run RUN_SIMULATOR.bat if you haven't)
echo.
echo Press Ctrl+C to stop
echo.
echo ============================================

streamlit run pyrit_demo_harness/streamlit_app.py
