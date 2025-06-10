"""
CSV Data Loading and Management

This module handles loading and accessing CSV data files.
The csv_data dictionary is the central repository for all CSV files.
"""

import pandas as pd
import os
from typing import Dict, Optional, Any
from .converter import universal_float_convert

# Global CSV data storage - accessible from all modules
csv_data: Dict[str, pd.DataFrame] = {}

def load_csv_files(data_dir: str = "Data") -> Dict[str, pd.DataFrame]:
    """
    Load all CSV files from the specified directory.
    
    Parameters:
    data_dir (str): Path to the directory containing CSV files
    
    Returns:
    dict: Dictionary of dataframes with normalized names as keys
    """
    global csv_data
    
    try:
        # Get all CSV files in the directory
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        
        # Load each CSV file into a dataframe
        for file in csv_files:
            # Create a normalized name for the dataframe (without .csv extension, uppercase)
            df_name = os.path.splitext(file)[0].upper()
            file_path = os.path.join(data_dir, file)
            
            try:
                # Try to read the CSV file
                csv_data[df_name] = pd.read_csv(file_path)
                print(f"✅ Loaded: {file} as {df_name}")
            except Exception as e:
                # Try with different separators if automatic detection fails
                try:
                    csv_data[df_name] = pd.read_csv(file_path, sep=';')
                    print(f"✅ Loaded: {file} as {df_name} (using semicolon separator)")
                except:
                    try:
                        csv_data[df_name] = pd.read_csv(file_path, sep='\\t')
                        print(f"✅ Loaded: {file} as {df_name} (using tab separator)")
                    except Exception as e2:
                        print(f"❌ Failed to load {file}: {e2}")
        
        return csv_data
    
    except Exception as e:
        print(f"❌ Error loading CSV files: {e}")
        return {}

def get_csv_data(csv_name: str) -> Optional[pd.DataFrame]:
    """
    Get a specific CSV dataframe by name.
    
    Parameters:
    csv_name (str): Name of the CSV file (case-insensitive)
    
    Returns:
    pd.DataFrame or None: The dataframe if found, None otherwise
    """
    global csv_data
    
    # Normalize the CSV name
    csv_name = csv_name.upper()
    
    # Check if the CSV has been loaded
    if csv_name not in csv_data:
        available = list(csv_data.keys())
        raise ValueError(f"❌ CSV '{csv_name}' not loaded. Available CSVs: {available}")
    return csv_data[csv_name]

def is_csv_loaded(csv_name: str) -> bool:
    """Check if a CSV file has been loaded."""
    return csv_name.upper() in csv_data

def list_loaded_csvs() -> list:
    """Get list of all loaded CSV names."""
    return list(csv_data.keys())

def validate_required_csvs(required_csvs: list) -> bool:
    """Validate that all required CSV files are loaded."""
    missing = []
    for csv_name in required_csvs:
        if not is_csv_loaded(csv_name):
            missing.append(csv_name)
    
    if missing:
        available = list_loaded_csvs()
        raise ValueError(f"❌ Missing required CSV files: {missing}. Available: {available}")
    
    return True