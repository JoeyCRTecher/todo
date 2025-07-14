# Todo App Launcher Script
Write-Host "Starting Todo App..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\Activate.ps1
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to activate virtual environment"
    }
} catch {
    Write-Host "Error: Failed to activate virtual environment." -ForegroundColor Red
    Write-Host "Please make sure the virtual environment exists in .venv directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Virtual environment activated successfully." -ForegroundColor Green
Write-Host ""

# Run the Streamlit app
Write-Host "Starting Streamlit app..." -ForegroundColor Yellow
Write-Host "The app will open in your default web browser." -ForegroundColor Cyan
Write-Host "To stop the app, press Ctrl+C in this window." -ForegroundColor Cyan
Write-Host ""

try {
    streamlit run todo_app.py
} catch {
    Write-Host ""
    Write-Host "Error: Failed to start the Streamlit app." -ForegroundColor Red
    Write-Host "Please check if all dependencies are installed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
}

# Deactivate virtual environment when done
deactivate 