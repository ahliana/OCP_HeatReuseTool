# Heat Reuse Tool - Python Package Initialization
"""
Heat Reuse System Calculator - Modular Python Implementation

This package provides modular components for heat reuse system analysis.
Starting with core data handling, then expanding to calculations and UI.
"""

__version__ = "0.1.0"
__author__ = "Heat Reuse Tool Team"

# Import core modules as they become available
try:
    from .data.converter import universal_float_convert
    print("✅ Data converter module loaded")
except ImportError as e:
    print(f"⚠️ Data converter not available: {e}")
    universal_float_convert = None

# Future imports will be added progressively:
# from .core.calculations import *
# from .ui.interface import create_heat_reuse_tool
# from .physics.constants import *

# Make key functions available at package level
__all__ = [
    'universal_float_convert',
]

def get_module_status():
    """Get status of all available modules"""
    status = {
        'data_converter': universal_float_convert is not None,
        'version': __version__
    }
    return status

print(f"🔧 Heat Reuse Tool v{__version__} - Modular Architecture")
print(f"📊 Module status: {get_module_status()}")