"""
Project Alfred - Vercel Serverless Entry Point
This file adapts the FastAPI app for Vercel's serverless environment
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.main import app

# Vercel expects a variable named 'app' or a handler function
# FastAPI apps work directly with Vercel's Python runtime
