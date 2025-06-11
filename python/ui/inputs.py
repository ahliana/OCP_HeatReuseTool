"""
Input Widget Creation
Extracted from Interactive Analysis Tool.ipynb
"""

import ipywidgets as widgets
from .config import UI_CONFIG

# =============================================================================
# WIDGET CREATION FUNCTIONS
# =============================================================================

def create_input_widgets():
    """
    Create all input widgets based on configuration.
    
    Returns:
        Dictionary of created widgets
    """
    widgets_dict = {}
    
    # Create dropdown widgets
    for widget_name, config in UI_CONFIG['dropdowns'].items():
        widgets_dict[f"{widget_name}_widget"] = create_dropdown_widget(
            options=config['options'],
            default=config['default'], 
            label=config['label'],
            tooltip=config.get('tooltip', '')
        )
    
    # Create calculate button
    widgets_dict['calculate_button'] = create_calculate_button()
    
    return widgets_dict

def create_dropdown_widget(options, default, label, tooltip=""):
    """
    Create a single dropdown widget with consistent styling.
    
    Args:
        options: List of options for the dropdown
        default: Default selected value
        label: Label text for the dropdown
        tooltip: Tooltip text
    
    Returns:
        ipywidgets.Dropdown widget
    """
    layout_config = UI_CONFIG['layout']
    
    style = {'description_width': layout_config['description_width']}
    layout = widgets.Layout(width=layout_config['widget_width'])
    
    return widgets.Dropdown(
        options=options,
        value=default,
        description=label,
        tooltip=tooltip,
        style=style,
        layout=layout
    )

def create_calculate_button():
    """
    Create the calculate button with consistent styling.
    
    Returns:
        ipywidgets.Button widget
    """
    button_config = UI_CONFIG['button']
    layout_config = UI_CONFIG['layout']
    
    return widgets.Button(
        description=button_config['text'],
        button_style=button_config['style'],
        tooltip=button_config['tooltip'],
        icon=button_config['icon'],
        layout=widgets.Layout(
            width=layout_config['button_width'],
            height=layout_config['button_height'],
            margin=layout_config['button_margin']
        )
    )

def create_output_areas():
    """
    Create all output display areas including new sections.
    
    Returns:
        Dictionary of output widgets
    """
    return {
        'system_params': widgets.Output(),
        'cost_analysis': widgets.Output(),      # Just cost analysis now
        'smart_recommendations': widgets.Output(), # NEW - separate section
        'visual_summary': widgets.Output(),     # Section for summary cards
        'charts': widgets.Output()              # This will include gauges
    }


def create_interface_layout(widgets_dict, outputs_dict):
    """
    Create the main interface layout - everything stacked vertically.
    """
    # Input section - 2x2 grid for the dropdowns
    input_grid = widgets.VBox([
        widgets.HBox([
            widgets_dict['power_widget'],
            widgets_dict['t1_widget']
        ]),
        widgets.HBox([
            widgets_dict['temp_diff_widget'],
            widgets_dict['approach_widget']
        ])
    ])
    
    # Complete vertical layout: inputs, button, then all outputs
    return widgets.VBox([
        input_grid,                                              # Power/T1, TempRise/Approach
        widgets_dict['calculate_button'],                        # Calculate button
        outputs_dict['system_params'],                           # 1. System Parameters
        outputs_dict['cost_analysis'],                           # 2. Cost Analysis (now separate)
        outputs_dict['charts'],                                  # 3. Charts
        outputs_dict.get('smart_recommendations', widgets.Output()), # 4. Smart Recommendations
        outputs_dict.get('visual_summary', widgets.Output())    # 5. System Overview Cards
    ], layout=widgets.Layout(margin='10px'))

# =============================================================================
# WIDGET VALUE EXTRACTION
# =============================================================================

def get_widget_values(widgets_dict):
    """
    Extract values from all input widgets.
    
    Args:
        widgets_dict: Dictionary of input widgets
    
    Returns:
        Dictionary of widget values
    """
    return {
        'power': widgets_dict['power_widget'].value,
        't1': widgets_dict['t1_widget'].value,
        'temp_diff': widgets_dict['temp_diff_widget'].value,
        'approach': widgets_dict['approach_widget'].value
    }

def clear_all_outputs(outputs_dict):
    """
    Clear all output areas completely.
    
    Args:
        outputs_dict: Dictionary of output widgets
    """
    for output_name, output_widget in outputs_dict.items():
        output_widget.clear_output(wait=True)  # wait=True ensures complete clearing

# =============================================================================
# WIDGET CONFIGURATION HELPERS
# =============================================================================

def update_dropdown_options(widget, new_options, new_default=None):
    """
    Update dropdown options dynamically.
    
    Args:
        widget: Dropdown widget to update
        new_options: New list of options
        new_default: New default value (optional)
    """
    widget.options = new_options
    if new_default is not None and new_default in new_options:
        widget.value = new_default

def get_dropdown_config_by_name(dropdown_name):
    """
    Get configuration for a specific dropdown by name.
    
    Args:
        dropdown_name: Name of the dropdown
    
    Returns:
        Configuration dictionary
    """
    return UI_CONFIG['dropdowns'].get(dropdown_name, {})

# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def validate_widget_values(widgets_dict):
    """
    Validate all widget values at once.
    
    Args:
        widgets_dict: Dictionary of input widgets
    
    Returns:
        List of validation errors (empty if all valid)
    """
    from .formatting import validate_user_inputs
    
    values = get_widget_values(widgets_dict)
    return validate_user_inputs(
        values['power'],
        values['t1'],
        values['temp_diff'],
        values['approach']
    )