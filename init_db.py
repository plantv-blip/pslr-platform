#!/usr/bin/env python3
"""
Database initialization script
Run this to create tables for the first time
"""

from app import app, db

with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")
    print("Tables:")
    print("- pslr_analysis")
    print("- batch_experiments")
