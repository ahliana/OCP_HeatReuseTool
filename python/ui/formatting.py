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
    


def generate_smart_insights(analysis):
    """
    Generate smart recommendations based on current system analysis.
    
    Args:
        analysis: Complete system analysis dictionary
    
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    try:
        system = analysis['system']
        costs = analysis['costs']
        
        power = system['power']
        total_cost = costs['total_cost']
        cost_per_mw = total_cost / power
        
        # Get heat exchanger effectiveness if available
        effectiveness = analysis.get('validation', {}).get('hx_effectiveness', 0.75)  # Default estimate
        
        # Cost efficiency recommendations
        if cost_per_mw < 20000:
            recommendations.append("💰 Excellent cost efficiency - below €20,000 per MW")
        elif cost_per_mw > 30000:
            recommendations.append("📈 Consider larger system size for better cost efficiency")
        else:
            recommendations.append("✅ Good cost efficiency for this system size")
        
        # Power size recommendations
        if power < 1.5:
            next_size_cost_per_mw = estimate_cost_per_mw(power + 0.5)
            improvement = ((cost_per_mw - next_size_cost_per_mw) / cost_per_mw) * 100
            if improvement > 10:
                recommendations.append(f"🎯 Scaling to {power + 0.5} MW could improve cost efficiency by {improvement:.0f}%")
        
        # Temperature recommendations
        t1 = system['T1']
        t2 = system['T2']
        temp_rise = t2 - t1
        
        if t1 == 20:
            recommendations.append("🌟 Optimal T1 temperature for server cooling compatibility")
        elif t1 < 18:
            recommendations.append("❄️ Low T1 may require additional server cooling consideration")
        
        if temp_rise >= 12:
            recommendations.append("🔥 High temperature rise enables excellent heat recovery potential")
        elif temp_rise < 8:
            recommendations.append("⚡ Consider higher temperature rise for better heat recovery")
        
        # European compliance
        approach = system.get('approach', analysis.get('validation', {}).get('approach_calculated', 2))
        if approach >= 3:
            recommendations.append("✅ Conservative approach temperature - excellent for European standards")
        elif approach >= 2:
            recommendations.append("✅ Meets European minimum approach temperature requirements")
        
        # Flow rate insights
        f1 = system['F1']
        f2 = system['F2']
        if abs(f1 - f2) / max(f1, f2) < 0.1:
            recommendations.append("⚖️ Well-balanced flow rates for optimal heat transfer")
        
    except Exception as e:
        recommendations.append("⚠️ Unable to generate recommendations - check system data")
    
    return recommendations[:4]  # Limit to 4 recommendations for clean display

def estimate_cost_per_mw(target_mw):
    """
    Estimate cost per MW for a target power size.
    Based on your MW price data trends.
    """
    # Simplified estimation based on your price data
    if target_mw <= 1:
        return 21000
    elif target_mw <= 2:
        return 19000
    elif target_mw <= 3:
        return 17300
    else:
        return 16000

def create_recommendations_html(recommendations, border_color="#4CAF50", title_color="#2E7D32"):
    """
    Create HTML for recommendations display matching cost analysis style.
    
    Args:
        recommendations: List of recommendation strings
        border_color: Border color for the box
        title_color: Title color
    
    Returns:
        HTML string for recommendations
    """
    rec_rows = ""
    for rec in recommendations:
        rec_rows += f"""
        <tr>
            <td style="padding: 8px 0; color: #333; font-size: 14px;">
                {rec}
            </td>
        </tr>"""
    
    return f"""
    <div style="border: 2px solid {border_color}; border-radius: 12px; padding: 20px; margin: 15px 0; background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3 style="color: {title_color}; margin: 0 0 15px 0; font-size: 18px; font-weight: bold; text-align: center;">
            🧠 Smart Recommendations
        </h3>
        <table style="width: 100%; border-collapse: collapse;">
            {rec_rows}
        </table>
    </div>
    """
    

def generate_performance_rating(cost_per_mw, effectiveness):
    """
    Generate performance rating based on cost efficiency and effectiveness.
    
    Returns:
        Dictionary with rating info
    """
    # Cost efficiency scoring
    if cost_per_mw < 20000:
        cost_score = 5
    elif cost_per_mw < 25000:
        cost_score = 4
    elif cost_per_mw < 30000:
        cost_score = 3
    else:
        cost_score = 2
    
    # Effectiveness scoring
    if effectiveness > 0.8:
        eff_score = 5
    elif effectiveness > 0.7:
        eff_score = 4
    elif effectiveness > 0.6:
        eff_score = 3
    else:
        eff_score = 2
    
    # Overall rating
    overall_score = (cost_score + eff_score) / 2
    
    if overall_score >= 4.5:
        rating = "⭐⭐⭐⭐⭐ EXCELLENT"
        color = "#4CAF50"
    elif overall_score >= 3.5:
        rating = "⭐⭐⭐⭐ VERY GOOD"
        color = "#8BC34A"
    elif overall_score >= 2.5:
        rating = "⭐⭐⭐ GOOD"
        color = "#FFC107"
    else:
        rating = "⭐⭐ ACCEPTABLE"
        color = "#FF9800"
    
    return {
        'rating': rating,
        'color': color,
        'cost_score': cost_score,
        'eff_score': eff_score
    }

def create_summary_cards_html(power, total_cost, cost_per_mw, effectiveness, rating_info, eu_compliant):
    """
    Create HTML for visual summary cards.
    """
    return f"""
    <div style="margin: 20px 0;">
        <h3 style="color: #2E7D32; margin: 0 0 20px 0; font-size: 20px; font-weight: bold; text-align: center;">
            📊 System Overview
        </h3>
        <div style="display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap;">
            
            <!-- System Performance Card -->
            <div style="border: 2px solid #4CAF50; padding: 20px; border-radius: 12px; flex: 1; min-width: 280px; background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%); box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h4 style="color: #2E7D32; margin: 0 0 15px 0; font-size: 16px; display: flex; align-items: center;">
                    🏢 System Performance
                </h4>
                <div style="margin-bottom: 10px;">
                    <strong>{power} MW</strong> Heat Recovery System
                </div>
                <div style="margin-bottom: 10px;">
                    Effectiveness: <strong>{effectiveness:.1%}</strong>
                    <div style="background: #e0e0e0; height: 8px; border-radius: 4px; margin-top: 5px;">
                        <div style="background: #4CAF50; height: 8px; border-radius: 4px; width: {effectiveness*100}%;"></div>
                    </div>
                </div>
                <div style="margin-bottom: 10px;">
                    EU Compliant: <strong>{"✅ Yes" if eu_compliant else "❌ No"}</strong>
                </div>
                <div style="color: {rating_info['color']}; font-weight: bold; font-size: 12px;">
                    {rating_info['rating']}
                </div>
            </div>
            
            <!-- Investment Summary Card -->
            <div style="border: 2px solid #2196F3; padding: 20px; border-radius: 12px; flex: 1; min-width: 280px; background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%); box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h4 style="color: #1976D2; margin: 0 0 15px 0; font-size: 16px; display: flex; align-items: center;">
                    💰 Investment Summary
                </h4>
                <div style="margin-bottom: 10px;">
                    Total Cost: <strong>€{total_cost:,.0f}</strong>
                </div>
                <div style="margin-bottom: 10px;">
                    Cost/MW: <strong>€{cost_per_mw:,.0f}</strong>
                </div>
                <div style="margin-bottom: 15px;">
                    <div style="background: #e0e0e0; height: 20px; border-radius: 10px; position: relative; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 50%, #FFC107 100%); height: 20px; border-radius: 10px; width: 70%;"></div>
                        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">
                            Cost Efficiency
                        </div>
                    </div>
                </div>
                <div style="color: {rating_info['color']}; font-weight: bold; font-size: 12px;">
                    Performance Rating: {rating_info['cost_score']}/5 ⭐
                </div>
            </div>
            
        </div>
    </div>
    """
    
    