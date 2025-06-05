"""
Heat Reuse Tool - Main Package
Auto-loads all components in the correct order
"""

# Package metadata
__version__ = "1.0.0"
__author__ = "Heat Reuse Tool Team"

# This file intentionally minimal - autostart.py does the heavy lifting
# Just expose the autostart functionality
from . import autostart

# After autostart runs, expose key functions at package level
def _post_autostart_setup():
    """Called by autostart.py after all modules are loaded"""
    # Import and expose key functions after everything is loaded
    try:
        from .core.system_analysis import get_complete_system_analysis
        from .data.converter import universal_float_convert
        from .physics.thermodynamics import get_MW_divd, get_PipeSize_Suggested
        from .ui.interface import create_heat_reuse_tool
        
        # Engineering calculations functions
        from .engineering_calculations import (
            datacenter_cooling_analysis,
            pipe_sizing_analysis, 
            heat_exchanger_analysis,
            quick_power_calculation,
            get_MW_equivalent,
            get_MW_divd_equivalent
        )
        
        # Make them available at package level
        globals().update({
            'get_complete_system_analysis': get_complete_system_analysis,
            'universal_float_convert': universal_float_convert,
            'get_MW_divd': get_MW_divd,
            'get_PipeSize_Suggested': get_PipeSize_Suggested,
            'create_heat_reuse_tool': create_heat_reuse_tool,
            
            # Engineering functions
            'datacenter_cooling_analysis': datacenter_cooling_analysis,
            'pipe_sizing_analysis': pipe_sizing_analysis,
            'heat_exchanger_analysis': heat_exchanger_analysis,
            'quick_power_calculation': quick_power_calculation,
            'get_MW_equivalent': get_MW_equivalent,
            'get_MW_divd_equivalent': get_MW_divd_equivalent,
        })
        
        print("✅ Heat Reuse Tool loaded successfully!")
        print(f"📦 Available functions: {len([k for k in globals() if not k.startswith('_')])} components loaded")
        print("🧮 Engineering calculations available")
        
    except ImportError as e:
        print(f"⚠️ Some components not available: {e}")

# The actual loading happens in autostart.py