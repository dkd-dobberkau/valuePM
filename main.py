"""Main entry point for the application"""

import sys
import subprocess
import threading
import time
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent))


def run_api():
    """Run FastAPI server"""
    print("Starting API server...")
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "src.api.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])


def run_ui():
    """Run Streamlit UI"""
    print("Waiting for API to start...")
    time.sleep(3)  # Give API time to start
    print("Starting Streamlit UI...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "src/ui/app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])


def main():
    """Run both API and UI"""
    print("Starting Value-Based IT Project Management System...")
    
    # Start API in a separate thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Run UI in main thread
    run_ui()


if __name__ == "__main__":
    main()