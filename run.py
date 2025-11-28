#!/usr/bin/env python3
"""
Simple script to run the Polymer Tracker API
"""
import uvicorn
import os

if __name__ == "__main__":
    print("🚀 Starting Polymer Tracker API...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )