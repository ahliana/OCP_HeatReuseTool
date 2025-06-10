"""
Display Formatting and Input Validation
Extracted from Interactive Analysis Tool.ipynb
"""

from .config import DISPLAY_ROUNDING, VALIDATION_RULES, MESSAGE_STYLES

# =============================================================================
# DISPLAY FORMATTING FUNCTIONS
# =============================================================================

def format_display_value(value, rounding_type, include_units=True, units=""):
    """
    Format a value for display according to the rounding preferences.
    
    Args:
        value: The numerical value to format
        rounding_type: Key from DISPLAY_ROUNDING dict
        include_units: Whether to include units in the output
        units: Unit string to append (e.g., "°C", "€", "l/m")
    
    Returns:
        Formatted string ready for display
    """
    if value is None:
        return "N/A"
    
    try:
        decimal_places = DISPLAY_ROUNDING.get(rounding_type, 0)
        
        if decimal_places >= 0:
            # Standard decimal rounding
            rounded_value = round(float(value), decimal_places)
            if decimal_places == 0:
                formatted = f"{int(rounded_value):,}"
            else:
                formatted = f"{rounded_value:,.{decimal_places}f}"
        else:
            # Round to nearest 10^(-decimal_places)
            # e.g., -2 means round to nearest 100, -3 means round to nearest 1000
            multiplier = 10 ** (-decimal_places)
            rounded_value = round(float(value) / multiplier) * multiplier
            formatted = f"{int(rounded_value):,}"
        
        if include_units and units:
            return f"{formatted}{units}"
        else:
            return formatted
            
    except (ValueError, TypeError):
        return str(value)

# =============================================================================
# HTML GENERATION FUNCTIONS
# =============================================================================

def create_result_html(title, data_rows, border_color, title_color):
    """
    Generate HTML for result displays with consistent styling.
    
    Args:
        title: Section title
        data_rows: List of (label, value) tuples
        border_color: CSS color for border
        title_color: CSS color for title
    
    Returns:
        HTML string for display
    """
    rows_html = ""
    for i, (label, value) in enumerate(data_rows):
        border_style = "border-bottom: 1px solid #eee;" if i < len(data_rows) - 1 else ""
        if i == len(data_rows) - 1 and "TOTAL" in label.upper():
            # Special styling for total row
            rows_html += f"""
            <tr><td style="padding: 10px; font-weight: bold; font-size: 18px; color: #f44336; border-bottom: 2px solid #333;">{label}</td>
                <td style="padding: 10px; font-weight: bold; font-size: 18px; color: #f44336; border-bottom: 2px solid #333;">{value}</td></tr>"""
        else:
            rows_html += f"""
            <tr><td style="padding: 8px; font-weight: bold; {border_style}">{label}</td>
                <td style="padding: 8px; {border_style}">{value}</td></tr>"""
    
    return f"""
    <div style="background-color: white; padding: 15px; border-radius: 8px; border: 2px solid {border_color}; margin: 10px 0;">
        <h3 style="color: {title_color}; margin-top: 0;">{title}</h3>
        <table style="width: 100%; border-collapse: collapse;">
            {rows_html}
        </table>
    </div>
    """

def create_error_html(message, message_type='error'):
    """
    Generate error/warning/info HTML with consistent styling.
    
    Args:
        message: Message to display
        message_type: Type of message ('error', 'warning', 'info', 'success')
    
    Returns:
        HTML string for display
    """
    style = MESSAGE_STYLES.get(message_type, MESSAGE_STYLES['error'])
    
    return f"""
    <div style="background-color: {style['background_color']}; color: {style['text_color']}; 
                padding: 10px; border-radius: 5px; margin: 10px 0; border: 1px solid {style['border_color']};">
        <strong>{style['icon']} {message}</strong>
    </div>
    """

def create_validation_errors_html(errors):
    """
    Generate HTML for multiple validation errors.
    
    Args:
        errors: List of error messages
    
    Returns:
        HTML string for display
    """
    error_list = "<br>".join([f"• {error}" for error in errors])
    return f"""
    <div style="background-color: #ffe6e6; color: #990000; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <strong>Input Validation Errors:</strong><br>
        {error_list}
    </div>
    """

# =============================================================================
# INPUT VALIDATION FUNCTIONS
# =============================================================================

def validate_user_inputs(power, t1, temp_diff, approach):
    """
    Validate user inputs against configured rules.
    
    Args:
        power: Selected power value
        t1: Selected T1 temperature
        temp_diff: Selected temperature difference
        approach: Selected approach value
    
    Returns:
        List of error messages (empty if all valid)
    """
    errors = []
    
    # Validate power
    power_rule = VALIDATION_RULES['power']
    if power not in power_rule['valid_options']:
        errors.append(f"{power_rule['error_message']} (got {power})")
    
    # Validate T1
    t1_rule = VALIDATION_RULES['t1']
    if t1 not in t1_rule['valid_options']:
        errors.append(f"{t1_rule['error_message']} (got {t1})")
    
    # Validate temperature difference
    temp_diff_rule = VALIDATION_RULES['temp_diff']
    if temp_diff not in temp_diff_rule['valid_options']:
        errors.append(f"{temp_diff_rule['error_message']} (got {temp_diff})")
    
    # Validate approach
    approach_rule = VALIDATION_RULES['approach']
    if approach not in approach_rule['valid_options']:
        errors.append(f"{approach_rule['error_message']} (got {approach})")
    
    return errors

def validate_single_input(field_name, value):
    """
    Validate a single input field.
    
    Args:
        field_name: Name of the field to validate
        value: Value to validate
    
    Returns:
        True if valid, False otherwise
    """
    rule = VALIDATION_RULES.get(field_name)
    if not rule:
        return True  # No rule defined, assume valid
    
    return value in rule['valid_options']

# =============================================================================
# VALUE EXTRACTION AND FORMATTING HELPERS
# =============================================================================

def extract_formatted_system_params(system_data):
    """
    Extract and format system parameters for display.
    
    Args:
        system_data: System analysis data dictionary
    
    Returns:
        List of (label, formatted_value) tuples
    """
    return [
        ("T1 (Outlet to TCS):", format_display_value(system_data['T1'], 'temperature', True, '°C')),
        ("T2 (Inlet from TCS):", format_display_value(system_data['T2'], 'temperature', True, '°C')),
        ("T3 (Outlet to Consumer):", format_display_value(system_data['T3'], 'temperature', True, '°C')),
        ("T4 (Inlet from Consumer):", format_display_value(system_data['T4'], 'temperature', True, '°C')),
        ("F1 (TCS Flow Rate):", format_display_value(system_data['F1'], 'flow_rate', True, ' l/m')),
        ("F2 (FWS Flow Rate):", format_display_value(system_data['F2'], 'flow_rate', True, ' l/m'))
    ]

def extract_formatted_cost_analysis(costs_data, sizing_data):
    """
    Extract and format cost analysis data for display.
    
    Args:
        costs_data: Cost analysis data dictionary
        sizing_data: Sizing data dictionary
    
    Returns:
        List of (label, formatted_value) tuples
    """
    return [
        ("Room Size:", format_display_value(sizing_data['room_size'], 'room_size', True, ' m')),
        ("Suggested Pipe Size:", format_display_value(sizing_data['primary_pipe_size'], 'pipe_size', False)),
        ("Pipe Cost per Meter:", f"€{format_display_value(costs_data['pipe_cost_per_meter'], 'pipe_cost_per_meter', False)}/m"),
        ("Total Pipe Cost:", f"€{format_display_value(costs_data['total_pipe_cost'], 'total_pipe_cost', False)}"),
        ("Heat Exchanger Cost:", f"€{format_display_value(costs_data['hx_cost'], 'hx_cost', False)}"),
        ("Valve Costs:", f"€{format_display_value(costs_data['total_valve_cost'], 'valve_costs', False)}"),
        ("Pump Cost:", f"€{format_display_value(costs_data['pump_cost'], 'pump_cost', False)}"),
        ("TOTAL SYSTEM COST:", f"€{format_display_value(costs_data['total_cost'], 'total_cost', False)}")
    ]

def extract_delta_t_values(system_data):
    """
    Calculate and format Delta T values for display.
    
    Args:
        system_data: System analysis data dictionary
    
    Returns:
        List of (label, formatted_value) tuples for Delta T values
    """
    # Import the calculation functions
    from core.original_calculations import get_DeltaT_TCS, get_DeltaT_FWS
    
    delta_t_tcs = get_DeltaT_TCS(system_data['T1'], system_data['T2'])
    delta_t_fws = get_DeltaT_FWS(system_data['T3'], system_data['T4'])
    
    return [
        ("Delta T for TCS (IT Medium):", format_display_value(delta_t_tcs, 'temperature', True, '°C')),
        ("Delta T for FWS (Heating Medium):", format_display_value(delta_t_fws, 'temperature', True, '°C'))
    ]

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def safe_float_convert(value):
    """
    Safely convert any value to float, handling strings with commas.
    
    Args:
        value: Value to convert
    
    Returns:
        Float value or 0.0 if conversion fails
    """
    from data.converter import universal_float_convert
    
    if isinstance(value, str):
        return universal_float_convert(value)
    elif isinstance(value, (int, float)):
        return float(value)
    else:
        return 0.0