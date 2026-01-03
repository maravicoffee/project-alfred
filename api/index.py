"""
Project Alfred - Vercel Serverless Entry Point
This file adapts the FastAPI app for Vercel's serverless environment
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# Import the FastAPI app
from app.main import app

# Vercel serverless handler
# The app variable is automatically used by Vercel's Python runtime
handler = app
