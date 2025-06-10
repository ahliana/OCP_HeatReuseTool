"""
UI Interface Module - Main Interface Logic
Contains the logo display and interface creation functions
"""

from IPython.display import display, Image, HTML
import os
from .inputs import create_input_widgets, create_output_areas, create_interface_layout
from .handlers import create_handlers_suite
from .outputs import display_error

# =============================================================================
# LOGO AND BRANDING FUNCTIONS
# =============================================================================

def display_logo(width: int = 600):
    """
    Display the Heat Reuse Tool logo from Assets directory.
    
    Args:
        width: Image width in pixels
    """
    try:
        # Look for logo in common locations
        possible_paths = [
            os.path.join("Assets", "HeatReuseEconomicsTool_Horizontal.jpg"),
            os.path.join("..", "Assets", "HeatReuseEconomicsTool_Horizontal.jpg"),
            os.path.join(".", "Assets", "HeatReuseEconomicsTool_Horizontal.jpg"),
            "HeatReuseEconomicsTool_Horizontal.jpg"
        ]
        
        logo_path = None
        for path in possible_paths:
            if os.path.exists(path):
                logo_path = path
                break
        
        if logo_path:
            # Display the logo image
            display(Image(filename=logo_path, width=width))
        else:
            # Fallback if logo not found - simple text header
            fallback_html = """
            <div style="text-align: center; margin: 20px 0;">
                <h1 style="color: #2196F3; margin: 0;">🔧 Heat Reuse Economics Tool</h1>
            </div>
            """
            display(HTML(fallback_html))
            
    except Exception as e:
        # Error fallback - simple text header
        error_html = """
        <div style="text-align: center; margin: 20px 0;">
            <h1 style="color: #2196F3; margin: 0;">🔧 Heat Reuse Economics Tool</h1>
        </div>
        """
        display(HTML(error_html))

# =============================================================================
# INTERFACE CREATION
# =============================================================================

def create_heat_reuse_interface(options=None):
    """
    Create the complete Heat Reuse Tool interface.
    
    Args:
        options: Dictionary of interface options
    
    Returns:
        Complete interface widget and handlers
    """
    if options is None:
        options = {}
    
    try:
        # Import core functions
        core_functions = import_core_functions()
        
        # Create UI components
        widgets_dict = create_input_widgets()
        outputs_dict = create_output_areas()
        
        # Create and attach event handlers
        handlers = create_handlers_suite(
            widgets_dict, outputs_dict, core_functions, options
        )
        
        # Assemble layout
        interface = create_interface_layout(widgets_dict, outputs_dict)
        
        return {
            'interface': interface,
            'widgets': widgets_dict,
            'outputs': outputs_dict,
            'handlers': handlers,
            'core_functions': core_functions
        }
        
    except Exception as e:
        print(f"Error creating interface: {str(e)}")
        raise

def display_interface(options=None):
    """
    Display the complete interface with logo - main function called from notebook.
    
    Args:
        options: Dictionary of interface options
    
    Returns:
        Interface components dictionary
    """
    try:
        # Display logo first
        display_logo()
        
        # Create and display interface
        interface_components = create_heat_reuse_interface(options)
        
        if interface_components:
            display(interface_components['interface'])
        
        return interface_components
        
    except Exception as e:
        print(f"Error displaying interface: {str(e)}")
        return None

def auto_initialize_interface():
    """
    Automatically initialize and display the complete interface.
    Clean version for autostart integration.
    
    Returns:
        Interface components or None if failed
    """
    try:
        # Display the complete interface with logo
        interface_components = display_interface()
        return interface_components
        
    except Exception as e:
        print(f"Error initializing interface: {str(e)}")
        return None

# =============================================================================
# CORE FUNCTION IMPORTS
# =============================================================================

def import_core_functions():
    """
    Import and organize core calculation functions.
    
    Returns:
        Dictionary of core functions
    """
    try:
        # Import validation function
        from .formatting import validate_user_inputs
        
        # Import main calculation function
        from core.original_calculations import get_complete_system_analysis
        
        return {
            'validate_user_inputs': validate_user_inputs,
            'get_complete_system_analysis': get_complete_system_analysis
        }
        
    except ImportError as e:
        raise ImportError(f"Failed to import core functions: {str(e)}")

# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_simple_interface():
    """Create interface with minimal options for basic users."""
    options = {
        'safe_mode': True,
        'enable_real_time': False,
        'monitor_performance': False
    }
    
    return display_interface(options)

def create_advanced_interface():
    """Create interface with advanced features for power users."""
    options = {
        'safe_mode': True,
        'enable_real_time': True,
        'monitor_performance': True,
        'enable_debug': True,
        'enable_reset': True
    }
    
    return display_interface(options)