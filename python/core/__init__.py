# python/core/__init__.py
"""
Core business logic and calculations for Heat Reuse Tool

This module contains the main calculation functions and business logic
for datacenter heat reuse system analysis.
"""

# Import main calculation functions and make them available at package level
from .original_calculations import (
    get_MW, 
    get_MW_divd,
    quick_power_calculation
)

# Make functions available when importing from core
__all__ = [
    'get_MW',
    'get_MW_divd', 
    'quick_power_calculation'
]

__version__ = "1.0.0"