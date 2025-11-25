"""
EU AI Act HR Simulator — Startup Script
Runs the biased HR system API on port 8600
"""

import uvicorn
import sys
from pathlib import Path

if __name__ == "__main__":
    print("=" * 70)
    print("EU AI ACT HR SIMULATOR")
    print("=" * 70)
    print("Starting biased HR system for compliance testing...")
    print("API will be available at: http://localhost:8600")
    print("API Documentation: http://localhost:8600/docs")
    print("=" * 70)
    
    # Add src to Python path for imports
    src_path = str(Path(__file__).parent / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Import the app directly
    from api.main import app
    
    # Run without reload to avoid import issues
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8600,
        log_level="info"
    )
