@echo off
echo Starting Todo App...
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if activation was successful
if errorlevel 1 (
    echo Error: Failed to activate virtual environment.
    echo Please make sure the virtual environment exists in .venv directory.
    pause
    exit /b 1
)

echo Virtual environment activated successfully.
echo.

REM Run the Streamlit app
echo Starting Streamlit app...
echo The app will open in your default web browser.
echo To stop the app, press Ctrl+C in this window.
echo.

streamlit run todo_app.py

REM Keep the window open if there's an error
if errorlevel 1 (
    echo.
    echo Error: Failed to start the Streamlit app.
    echo Please check if all dependencies are installed.
    pause
)

REM Deactivate virtual environment when done
call deactivate 