"""
Main UI Interface for Heat Reuse Tool
Assembled from extracted components
"""

from IPython.display import display
from .inputs import create_input_widgets, create_output_areas, create_interface_layout
from .handlers import create_handlers_suite
from .outputs import display_error

# =============================================================================
# MAIN INTERFACE CREATION
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
    Display the complete interface - main function called from notebook.
    
    Args:
        options: Dictionary of interface options
    
    Returns:
        Interface components dictionary
    """
    try:
        # Create interface
        interface_components = create_heat_reuse_interface(options)
        
        # Display the interface
        display(interface_components['interface'])
        
        return interface_components
        
    except Exception as e:
        print(f"Error displaying interface: {str(e)}")
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
    """
    Create interface with minimal options for basic users.
    
    Returns:
        Interface components dictionary
    """
    options = {
        'safe_mode': True,
        'enable_real_time': False,
        'monitor_performance': False
    }
    
    return display_interface(options)

def create_advanced_interface():
    """
    Create interface with advanced features for power users.
    
    Returns:
        Interface components dictionary
    """
    options = {
        'safe_mode': True,
        'enable_real_time': True,
        'monitor_performance': True,
        'enable_debug': True,
        'enable_reset': True
    }
    
    return display_interface(options)

def create_production_interface():
    """
    Create interface optimized for production use.
    
    Returns:
        Interface components dictionary
    """
    options = {
        'safe_mode': True,
        'enable_real_time': False,
        'monitor_performance': False,
        'enable_debug': False,
        'enable_reset': False
    }
    
    return display_interface(options)

# =============================================================================
# CONFIGURATION HELPERS
# =============================================================================

def update_interface_config(config_updates):
    """
    Update interface configuration at runtime.
    
    Args:
        config_updates: Dictionary of configuration updates
    """
    try:
        from .config import UI_CONFIG, CHART_CONFIG, DISPLAY_ROUNDING
        
        # Update UI config
        if 'ui' in config_updates:
            UI_CONFIG.update(config_updates['ui'])
        
        # Update chart config
        if 'charts' in config_updates:
            CHART_CONFIG.update(config_updates['charts'])
        
        # Update rounding config
        if 'rounding' in config_updates:
            DISPLAY_ROUNDING.update(config_updates['rounding'])
            
        print("Configuration updated successfully")
        
    except Exception as e:
        print(f"Error updating configuration: {str(e)}")

def get_interface_config():
    """
    Get current interface configuration.
    
    Returns:
        Dictionary of current configuration
    """
    try:
        from .config import UI_CONFIG, CHART_CONFIG, DISPLAY_ROUNDING
        
        return {
            'ui': UI_CONFIG,
            'charts': CHART_CONFIG,
            'rounding': DISPLAY_ROUNDING
        }
        
    except Exception as e:
        print(f"Error getting configuration: {str(e)}")
        return {}

# =============================================================================
# TESTING AND DEBUGGING
# =============================================================================

def test_interface_components():
    """
    Test all interface components for proper initialization.
    
    Returns:
        Dictionary of test results
    """
    results = {
        'widgets': False,
        'outputs': False,
        'handlers': False,
        'core_functions': False,
        'layout': False
    }
    
    try:
        # Test widget creation
        widgets_dict = create_input_widgets()
        results['widgets'] = len(widgets_dict) >= 5  # 4 dropdowns + 1 button
        
        # Test output creation
        outputs_dict = create_output_areas()
        results['outputs'] = len(outputs_dict) >= 3  # 3 output areas
        
        # Test core function import
        core_functions = import_core_functions()
        results['core_functions'] = len(core_functions) >= 2  # validation + calculation
        
        # Test handler creation
        handlers = create_handlers_suite(widgets_dict, outputs_dict, core_functions)
        results['handlers'] = len(handlers) >= 1  # at least calculate handler
        
        # Test layout creation
        interface = create_interface_layout(widgets_dict, outputs_dict)
        results['layout'] = interface is not None
        
    except Exception as e:
        print(f"Test error: {str(e)}")
    
    return results

def validate_interface_setup():
    """
    Validate that interface can be created and displayed.
    
    Returns:
        True if validation passes, False otherwise
    """
    try:
        test_results = test_interface_components()
        all_passed = all(test_results.values())
        
        print("Interface Component Validation:")
        for component, passed in test_results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {component}: {status}")
        
        return all_passed
        
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return False

# =============================================================================
# MIGRATION HELPERS
# =============================================================================

def migrate_from_notebook():
    """
    Helper function to migrate from notebook-based UI to modular UI.
    
    Returns:
        Migration instructions
    """
    instructions = """
    Migration Instructions:
    
    1. Replace notebook cells with these two lines:
       ```python
       from ui import display_interface
       interface = display_interface()
       ```
    
    2. Configuration can be updated in ui/config.py
    
    3. Chart types can be changed in CHART_CONFIG
    
    4. Validation rules can be modified in VALIDATION_RULES
    
    5. Styling can be customized in MESSAGE_STYLES and OUTPUT_CONFIG
    """
    
    return instructions

# =============================================================================
# VERSION AND COMPATIBILITY
# =============================================================================

__version__ = "1.0.0"
__compatibility__ = {
    'notebook_version': '6.0+',
    'ipywidgets_version': '8.0+',
    'matplotlib_version': '3.5+',
    'pandas_version': '1.5+'
}

def check_compatibility():
    """
    Check if all required packages are available and compatible.
    
    Returns:
        Dictionary of compatibility results
    """
    compatibility_results = {}
    
    try:
        import ipywidgets
        compatibility_results['ipywidgets'] = ipywidgets.__version__
    except ImportError:
        compatibility_results['ipywidgets'] = 'Not installed'
    
    try:
        import matplotlib
        compatibility_results['matplotlib'] = matplotlib.__version__
    except ImportError:
        compatibility_results['matplotlib'] = 'Not installed'
    
    try:
        import pandas
        compatibility_results['pandas'] = pandas.__version__
    except ImportError:
        compatibility_results['pandas'] = 'Not installed'
    
    return compatibility_results

# =============================================================================
# EXPORTS
# =============================================================================

# Main functions for external use
__all__ = [
    'display_interface',
    'create_heat_reuse_interface',
    'create_simple_interface',
    'create_advanced_interface', 
    'create_production_interface',
    'update_interface_config',
    'get_interface_config',
    'validate_interface_setup',
    'migrate_from_notebook'
]

# Default interface function (most commonly used)
def main():
    """Default function - creates and displays standard interface."""
    return display_interface()

# Set up default interface if imported directly
if __name__ == "__main__":
    print("Heat Reuse Tool UI Module")
    print("=" * 30)
    
    # Run compatibility check
    print("Checking compatibility...")
    compat = check_compatibility()
    for package, version in compat.items():
        print(f"  {package}: {version}")
    
    # Run validation
    print("\nValidating interface components...")
    if validate_interface_setup():
        print("✅ All components validated successfully")
        print("\nTo use in notebook:")
        print("  from ui import display_interface")
        print("  interface = display_interface()")
    else:
        print("❌ Validation failed - check error messages above")