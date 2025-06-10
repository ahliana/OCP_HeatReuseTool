"""
Main UI Interface for Heat Reuse Tool
Simple init file that imports main display function
"""

from .interface import display_interface, auto_initialize_interface

# Make main functions available when importing from ui
__all__ = [
    'display_interface',
    'auto_initialize_interface'
]

__version__ = "1.0.0"