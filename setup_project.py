#!/usr/bin/env python3
"""
Setup script to create required directories
"""

import os

def create_directories():
    directories = [
        'logs',
        'results/plots',
        'results/data',
        'tests',
        'simulations'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

if __name__ == "__main__":
    print("Setting up DQC project directories...")
    create_directories()
    print("✅ Setup complete!")