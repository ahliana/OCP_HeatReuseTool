"""
Output Display Functions
Extracted from Interactive Analysis Tool.ipynb
"""

from IPython.display import display, HTML
import matplotlib.pyplot as plt  # Add this line
from .config import OUTPUT_CONFIG
from .formatting import (
    create_result_html, create_error_html, create_validation_errors_html,
    extract_formatted_system_params, extract_formatted_cost_analysis, 
    extract_delta_t_values,
    generate_smart_insights, generate_performance_rating,
    create_recommendations_html, create_summary_cards_html,
    calculate_effectiveness 
)
from .charts import create_system_charts

# =============================================================================
# MAIN OUTPUT DISPLAY FUNCTIONS
# =============================================================================

def display_system_parameters(output_area, analysis):
    """
    Display system parameters with proper formatting.
    
    Args:
        output_area: Output widget to display in
        analysis: Complete system analysis dictionary
    """
    with output_area:
        try:
            system = analysis['system']
            
            # Extract and format basic parameters
            basic_params = extract_formatted_system_params(system)
            
            # Extract and format Delta T values
            delta_t_params = extract_delta_t_values(system)
            
            # Combine all parameters
            all_params = basic_params + delta_t_params
            
            # Get styling configuration
            config = OUTPUT_CONFIG['system_params']
            
            # Create and display HTML
            html_content = create_result_html(
                title=config['title'],
                data_rows=all_params,
                border_color=config['border_color'],
                title_color=config['title_color']
            )
            
            display(HTML(html_content))
            
        except Exception as e:
            display_error(output_area, f"Error displaying system parameters: {str(e)}")

def display_cost_analysis(output_area, analysis):
    """
    Display cost analysis with proper formatting.
    
    Args:
        output_area: Output widget to display in
        analysis: Complete system analysis dictionary
    """
    with output_area:
        try:
            costs = analysis['costs']
            sizing = analysis['sizing']
            
            # Extract and format cost data
            cost_params = extract_formatted_cost_analysis(costs, sizing)
            
            # Get styling configuration
            config = OUTPUT_CONFIG['cost_analysis']
            
            # Create and display HTML
            html_content = create_result_html(
                title=config['title'],
                data_rows=cost_params,
                border_color=config['border_color'],
                title_color=config['title_color']
            )
            
            display(HTML(html_content))
            
        except Exception as e:
            display_error(output_area, f"Error displaying cost analysis: {str(e)}")

def display_charts(output_area, analysis):
    """
    Display charts with guaranteed fresh creation.
    
    Args:
        output_area: Output widget to display in
        analysis: Complete system analysis dictionary
    """
    # Double-clear to ensure fresh start
    output_area.clear_output()
    
    with output_area:
        try:
            # Force matplotlib to close any existing figures
            plt.close('all')
            
            # Create fresh charts
            create_system_charts(analysis)
            
        except Exception as e:
            display_error(output_area, f"Error creating charts: {str(e)}")

# =============================================================================
# ERROR AND MESSAGE DISPLAY FUNCTIONS
# =============================================================================

def display_validation_errors(output_area, errors):
    """
    Display validation errors in the output area.
    
    Args:
        output_area: Output widget to display in
        errors: List of error messages
    """
    with output_area:
        html_content = create_validation_errors_html(errors)
        display(HTML(html_content))

def display_no_data_error(output_area):
    """
    Display error when no data is found for selected parameters.
    
    Args:
        output_area: Output widget to display in
    """
    with output_area:
        html_content = create_error_html(
            "No data found for the selected parameters. Please try a different combination.",
            'error'
        )
        display(HTML(html_content))

def display_error(output_area, message, message_type='error'):
    """
    Display a general error message.
    
    Args:
        output_area: Output widget to display in
        message: Error message to display
        message_type: Type of message ('error', 'warning', 'info')
    """
    with output_area:
        html_content = create_error_html(message, message_type)
        display(HTML(html_content))

def display_success_message(output_area, message):
    """
    Display a success message.
    
    Args:
        output_area: Output widget to display in
        message: Success message to display
    """
    display_error(output_area, message, 'success')

def display_info_message(output_area, message):
    """
    Display an info message.
    
    Args:
        output_area: Output widget to display in
        message: Info message to display
    """
    display_error(output_area, message, 'info')

# =============================================================================
# COMBINED DISPLAY FUNCTIONS
# =============================================================================

def display_complete_analysis(outputs_dict, analysis):
    """
    Display complete analysis in all output areas including new sections.
    
    Args:
        outputs_dict: Dictionary of output widgets
        analysis: Complete system analysis dictionary
    """
    try:
        display_system_parameters(outputs_dict['system_params'], analysis)
        display_cost_analysis(outputs_dict['cost_analysis'], analysis)
        display_charts(outputs_dict['charts'], analysis)
        
        # Smart recommendations in their own section
        if 'smart_recommendations' in outputs_dict:
            display_smart_recommendations(outputs_dict['smart_recommendations'], analysis)
        
        # Visual summary at the bottom
        if 'visual_summary' in outputs_dict:
            display_visual_summary_cards(outputs_dict['visual_summary'], analysis)
            
    except Exception as e:
        display_error(outputs_dict['system_params'], f"Error displaying complete analysis: {str(e)}")
        
def clear_all_displays(outputs_dict):
    """
    Clear all output displays.
    
    Args:
        outputs_dict: Dictionary of output widgets
    """
    for output in outputs_dict.values():
        output.clear_output()

# =============================================================================
# UTILITY FUNCTIONS FOR OUTPUT MANAGEMENT
# =============================================================================

def display_loading_message(output_area, message="Calculating..."):
    """
    Display a loading message while calculations are in progress.
    
    Args:
        output_area: Output widget to display in
        message: Loading message to display
    """
    with output_area:
        html_content = f"""
        <div style="background-color: #e3f2fd; color: #0d47a1; padding: 15px; 
                    border-radius: 8px; border: 2px solid #bbdefb; margin: 10px 0; text-align: center;">
            <strong>⏳ {message}</strong>
        </div>
        """
        display(HTML(html_content))

def display_calculation_summary(output_area, summary_data):
    """
    Display a quick calculation summary.
    
    Args:
        output_area: Output widget to display in
        summary_data: Dictionary with summary information
    """
    with output_area:
        try:
            power = summary_data.get('power_mw', 'N/A')
            total_cost = summary_data.get('total_cost_eur', 'N/A')
            
            html_content = f"""
            <div style="background-color: #f8f9fa; color: #343a40; padding: 15px; 
                        border-radius: 8px; border: 2px solid #dee2e6; margin: 10px 0; text-align: center;">
                <h4 style="margin-top: 0; color: #495057;">📊 Quick Summary</h4>
                <p style="margin: 5px 0; font-size: 16px;">
                    <strong>System Power:</strong> {power} MW | 
                    <strong>Total Cost:</strong> €{total_cost:,} 
                </p>
            </div>
            """
            display(HTML(html_content))
            
        except Exception as e:
            display_error(output_area, f"Error displaying summary: {str(e)}")

# =============================================================================
# ADVANCED DISPLAY OPTIONS
# =============================================================================

def display_detailed_breakdown(output_area, analysis, show_validation=True):
    """
    Display detailed breakdown including validation results.
    
    Args:
        output_area: Output widget to display in
        analysis: Complete system analysis dictionary
        show_validation: Whether to show validation results
    """
    with output_area:
        try:
            # Display main results
            display_system_parameters(output_area, analysis)
            
            # Display validation if available and requested
            if show_validation and 'validation' in analysis:
                validation = analysis['validation']
                
                validation_html = f"""
                <div style="background-color: #fff3cd; color: #856404; padding: 10px; 
                            border-radius: 5px; margin: 10px 0; border: 1px solid #ffeaa7;">
                    <h4 style="margin-top: 0;">🔬 Validation Results</h4>
                    <p><strong>Calculated MW:</strong> {validation.get('calculated_mw', 'N/A')}</p>
                    <p><strong>Delta T TCS:</strong> {validation.get('delta_t_tcs', 'N/A')}°C</p>
                    <p><strong>Delta T FWS:</strong> {validation.get('delta_t_fws', 'N/A')}°C</p>
                    <p><strong>Approach:</strong> {validation.get('approach_calculated', 'N/A')}</p>
                </div>
                """
                display(HTML(validation_html))
                
        except Exception as e:
            display_error(output_area, f"Error displaying detailed breakdown: {str(e)}")

def display_export_options(output_area, analysis):
    """
    Display export options for the analysis results.
    
    Args:
        output_area: Output widget to display in
        analysis: Complete system analysis dictionary
    """
    with output_area:
        try:
            export_html = f"""
            <div style="background-color: #e8f5e8; color: #2e7d32; padding: 15px; 
                        border-radius: 8px; border: 2px solid #c8e6c9; margin: 10px 0;">
                <h4 style="margin-top: 0;">📤 Export Options</h4>
                <p>Results are ready for export. Available formats:</p>
                <ul>
                    <li>Charts: PNG/PDF format</li>
                    <li>Data: CSV/Excel format</li>
                    <li>Report: PDF summary</li>
                </ul>
                <p><small>Contact your system administrator for export functionality.</small></p>
            </div>
            """
            display(HTML(export_html))
            
        except Exception as e:
            display_error(output_area, f"Error displaying export options: {str(e)}")

# =============================================================================
# RESPONSIVE DISPLAY HELPERS
# =============================================================================

def get_display_mode():
    """
    Determine display mode based on available space.
    
    Returns:
        Display mode string ('compact', 'normal', 'detailed')
    """
    # This could be enhanced to detect screen size or user preferences
    return 'normal'

def display_responsive_results(outputs_dict, analysis):
    """
    Display results in a responsive manner based on display mode.
    
    Args:
        outputs_dict: Dictionary of output widgets
        analysis: Complete system analysis dictionary
    """
    mode = get_display_mode()
    
    if mode == 'compact':
        # Show only summary and key metrics
        display_calculation_summary(outputs_dict['system_params'], analysis.get('summary', {}))
        display_charts(outputs_dict['charts'], analysis)
    elif mode == 'detailed':
        # Show everything including validation
        display_detailed_breakdown(outputs_dict['system_params'], analysis, show_validation=True)
        display_cost_analysis(outputs_dict['cost_analysis'], analysis)
        display_charts(outputs_dict['charts'], analysis)
        display_export_options(outputs_dict['cost_analysis'], analysis)
    else:
        # Normal mode - standard display
        display_complete_analysis(outputs_dict, analysis)
        
        
        
def display_smart_recommendations(output_area, analysis):
    """
    Display smart recommendations in a rounded box below cost analysis.
    
    Args:
        output_area: Output widget to display in
        analysis: Complete system analysis dictionary
    """
    with output_area:
        try:
            # Extract key metrics for analysis
            system = analysis['system']
            costs = analysis['costs']
            sizing = analysis['sizing']
            
            power = system['power']
            total_cost = costs['total_cost']
            cost_per_mw = total_cost / power
            
            # Generate smart insights
            recommendations = generate_smart_insights(analysis)
            
            # Get styling configuration (reuse cost analysis style)
            config = OUTPUT_CONFIG['cost_analysis']  # Reuse existing styling
            
            # Create recommendations HTML
            rec_html = create_recommendations_html(
                recommendations=recommendations,
                border_color=config['border_color'],
                title_color=config['title_color']
            )
            
            display(HTML(rec_html))
            
        except Exception as e:
            display_error(output_area, f"Error displaying recommendations: {str(e)}")
            
            
def display_visual_summary_cards(output_area, analysis):
    """
    Display visual summary cards above charts section.
    
    Args:
        output_area: Output widget to display in
        analysis: Complete system analysis dictionary
    """
    with output_area:
        try:
            # Extract key metrics
            system = analysis['system']
            costs = analysis['costs']
            sizing = analysis['sizing']
            
            power = system['power']
            total_cost = costs['total_cost']
            cost_per_mw = total_cost / power
            
            # Get effectiveness estimate
            effectiveness = calculate_effectiveness(analysis)
            
            # Generate performance rating
            rating_info = generate_performance_rating(cost_per_mw, effectiveness)
            
            # Create cards HTML
            cards_html = create_summary_cards_html(
                power=power,
                total_cost=total_cost,
                cost_per_mw=cost_per_mw,
                effectiveness=effectiveness,
                rating_info=rating_info,
                eu_compliant=True  # Based on your validation
            )
            
            display(HTML(cards_html))
            
        except Exception as e:
            display_error(output_area, f"Error displaying summary cards: {str(e)}")
            
