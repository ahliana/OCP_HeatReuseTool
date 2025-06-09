
from .loader import load_csv_files, get_csv_data, is_csv_loaded, list_loaded_csvs
from .converter import universal_float_convert

# Auto-load CSV files when module is imported
import os

# Try to load CSV files automatically
if os.path.exists("Data"):
    print("🔧 Auto-loading CSV files...")
    load_csv_files("Data")
elif os.path.exists("../Data"):
    print("🔧 Auto-loading CSV files from parent directory...")
    load_csv_files("../Data")
else:
    print("⚠️ CSV data directory not found. Please load manually with load_csv_files()")

__all__ = [
    'load_csv_files',
    'get_csv_data', 
    'is_csv_loaded',
    'list_loaded_csvs',
    'universal_float_convert'
]

