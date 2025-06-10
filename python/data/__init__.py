# python/data/__init__.py
"""
Data handling module for Heat Reuse Tool

This module automatically loads and provides access to all CSV data files.
The csv_data dictionary is automatically populated when the module is imported.
"""

from .loader import csv_data, load_csv_files, get_csv_data, is_csv_loaded, list_loaded_csvs
from .converter import universal_float_convert

# Auto-load CSV files when module is imported
import os

def _auto_load_csv_files():
    """Automatically find and load CSV files from common locations"""
    possible_paths = [
        "Data",           # From notebook directory
        "../Data",        # From python subdirectory
        "../../Data",     # From deeper nested structure
        "./",             # Current directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.path.isdir(path):
            # Check if there are CSV files in this directory
            csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
            if csv_files:
                # print(f"🔧 Auto-loading CSV files from: {path}")
                load_csv_files(path)
                return True
    
    print("⚠️ No CSV data directory found. Available paths searched:")
    for path in possible_paths:
        print(f"   - {path} {'✓' if os.path.exists(path) else '✗'}")
    
    return False

# Attempt auto-loading when the module is imported
try:
    _auto_load_csv_files()
except Exception as e:
    print(f"⚠️ Failed to auto-load CSV files: {e}")
    print("You may need to manually call load_csv_files('path_to_data')")

__all__ = [
    'csv_data',
    'load_csv_files',
    'get_csv_data', 
    'is_csv_loaded',
    'list_loaded_csvs',
    'universal_float_convert'
]