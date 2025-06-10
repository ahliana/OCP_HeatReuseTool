"""
Chart Generation Module - Configurable chart creation
Extracted from Interactive Analysis Tool.ipynb
"""

import matplotlib.pyplot as plt
from .config import CHART_CONFIG
from .formatting import format_display_value, safe_float_convert

# =============================================================================
# MAIN CHART CREATION FUNCTION
# =============================================================================

def create_system_charts(analysis):
    """
    Create visualization charts for the system analysis with configurable layouts.
    Now includes approach profiles chart.
    
    Args:
        analysis: Complete system analysis dictionary
    
    Returns:
        None (displays charts)
    """
    try:
        # Get layout configuration - expand to 2x3 grid for approach profiles
        layout = CHART_CONFIG['layout']
        fig, axs = plt.subplots(
            3, 2,  # Changed to 3 rows, 2 columns for new chart
            figsize=(layout['figure_size'][0], layout['figure_size'][1] + 4)  # Make taller
        )
        
        # Apply matplotlib style
        plt.style.use(layout['style'])
        
        # Extract data
        system = analysis['system']
        costs = analysis['costs']
        sizing = analysis['sizing']
        
        # Create each chart based on configuration
        create_temperature_chart(axs[0, 0], system)
        create_flow_rates_chart(axs[0, 1], system)
        create_cost_breakdown_chart(axs[1, 0], costs)
        create_system_metrics_chart(axs[1, 1], system, sizing)
        
        # NEW: Create approach profiles chart
        create_approach_profiles_chart(axs[2, 0], system)
        
        # Create efficiency comparison chart in the remaining space
        create_efficiency_chart(axs[2, 1], system, costs)
        
        # Set overall title
        power_display = format_display_value(float(system['power']), 'temperature', False)
        title_template = CHART_CONFIG['charts']['system_metrics'].get('title_template', 
                        'Heat Reuse System Analysis - {power}MW System')
        plt.suptitle(title_template.format(power=power_display), 
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Chart creation error: {str(e)}")
        create_error_chart(str(e))

# =============================================================================
# INDIVIDUAL CHART CREATION FUNCTIONS
# =============================================================================

def create_temperature_chart(ax, system_data):
    """Create temperature flow chart."""
    config = CHART_CONFIG['charts']['temperatures']
    
    # Prepare data
    temp_values = [
        float(system_data['T1']),
        float(system_data['T2']),
        float(system_data['T3']),
        float(system_data['T4'])
    ]
    
    # Create chart
    bars = ax.bar(config['labels'], temp_values, color=config['colors'])
    ax.set_title(config['title'], fontsize=14, fontweight='bold')
    ax.set_ylabel(config['ylabel'])
    
    # Add value labels
    for i, v in enumerate(temp_values):
        display_value = format_display_value(v, 'temperature', True, '°C')
        ax.text(i, v + max(temp_values)*0.02, display_value, ha='center', fontweight='bold')

def create_flow_rates_chart(ax, system_data):
    """Create flow rates comparison chart."""
    config = CHART_CONFIG['charts']['flow_rates']
    
    # Prepare data
    flow_values = [
        float(system_data['F1']),
        float(system_data['F2'])
    ]
    
    # Create chart
    bars = ax.bar(config['labels'], flow_values, color=config['colors'])
    ax.set_title(config['title'], fontsize=14, fontweight='bold')
    ax.set_ylabel(config['ylabel'])
    
    # Add value labels
    for i, v in enumerate(flow_values):
        display_value = format_display_value(v, 'flow_rate', False)
        ax.text(i, v + max(flow_values)*0.02, display_value, ha='center', fontweight='bold')

def create_cost_breakdown_chart(ax, costs_data):
    """Create cost breakdown chart (pie chart for better total cost visualization)."""
    config = CHART_CONFIG['charts']['cost_breakdown']
    
    # Prepare data
    cost_values = [
        float(costs_data['total_pipe_cost']),
        float(costs_data['hx_cost']),
        float(costs_data['total_valve_cost']),
        float(costs_data['pump_cost']),
        float(costs_data['installation_cost'])
    ]
    
    # Create chart based on type
    if config['type'] == 'pie':
        # Pie chart for cost breakdown
        wedges, texts, autotexts = ax.pie(cost_values, labels=config['labels'], 
                                         colors=config['colors'], autopct=config.get('autopct', '%1.1f%%'),
                                         startangle=90)
        ax.set_title(config['title'], fontsize=14, fontweight='bold')
        
        # Format the percentage labels
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    else:
        # Bar chart fallback
        bars = ax.bar(config['labels'], cost_values, color=config['colors'])
        ax.set_title(config['title'], fontsize=14, fontweight='bold')
        ax.set_ylabel('Cost (€)')
        
        # Add cost labels
        cost_rounding_types = ['total_pipe_cost', 'hx_cost', 'valve_costs', 'pump_cost', 'pump_cost']
        for i, (v, rounding_type) in enumerate(zip(cost_values, cost_rounding_types)):
            display_value = format_display_value(v, rounding_type, False)
            ax.text(i, v + max(cost_values)*0.02, f"€{display_value}", 
                   ha='center', fontweight='bold', rotation=45)

def create_system_metrics_chart(ax, system_data, sizing_data):
    """Create system summary metrics chart."""
    config = CHART_CONFIG['charts']['system_metrics']
    
    # Prepare data
    metric_values = [
        float(system_data['power']),
        float(system_data['T2']) - float(system_data['T1']),
        float(sizing_data['primary_pipe_size']),
        float(sizing_data['room_size'])
    ]
    
    # Create chart
    bars = ax.bar(config['labels'], metric_values, color=config['colors'])
    ax.set_title(config['title'], fontsize=14, fontweight='bold')
    ax.set_ylabel(config['ylabel'])
    
    # Add metric labels with appropriate formatting
    metric_rounding_types = ['temperature', 'temperature', 'pipe_size', 'room_size']
    metric_units = ['', '°C', '', 'm']
    for i, (v, rounding_type, unit) in enumerate(zip(metric_values, metric_rounding_types, metric_units)):
        display_value = format_display_value(v, rounding_type, False)
        label = f"{display_value}{unit}" if unit else display_value
        ax.text(i, v + max(metric_values)*0.02, label, ha='center', fontweight='bold')

# =============================================================================
# ALTERNATIVE CHART TYPES (EASILY CONFIGURABLE)
# =============================================================================

def create_cost_breakdown_bar_chart(ax, costs_data):
    """Alternative bar chart for cost breakdown."""
    config = CHART_CONFIG['charts']['cost_breakdown']
    
    cost_values = [
        float(costs_data['total_pipe_cost']),
        float(costs_data['hx_cost']),
        float(costs_data['total_valve_cost']),
        float(costs_data['pump_cost']),
        float(costs_data['installation_cost'])
    ]
    
    bars = ax.bar(config['labels'], cost_values, color=config['colors'])
    ax.set_title(config['title'], fontsize=14, fontweight='bold')
    ax.set_ylabel('Cost (€)')
    
    # Add cost labels
    cost_rounding_types = ['total_pipe_cost', 'hx_cost', 'valve_costs', 'pump_cost', 'pump_cost']
    for i, (v, rounding_type) in enumerate(zip(cost_values, cost_rounding_types)):
        display_value = format_display_value(v, rounding_type, False)
        ax.text(i, v + max(cost_values)*0.02, f"€{display_value}", 
               ha='center', fontweight='bold', rotation=45)

def create_cost_breakdown_donut_chart(ax, costs_data):
    """Alternative donut chart for cost breakdown."""
    config = CHART_CONFIG['charts']['cost_breakdown']
    
    cost_values = [
        float(costs_data['total_pipe_cost']),
        float(costs_data['hx_cost']),
        float(costs_data['total_valve_cost']),
        float(costs_data['pump_cost']),
        float(costs_data['installation_cost'])
    ]
    
    # Create donut chart
    wedges, texts, autotexts = ax.pie(cost_values, labels=config['labels'], 
                                     colors=config['colors'], autopct='%1.1f%%',
                                     startangle=90, pctdistance=0.85)
    
    # Add center circle for donut effect
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    ax.add_artist(centre_circle)
    
    ax.set_title(config['title'], fontsize=14, fontweight='bold')
    
    # Format labels
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

# =============================================================================
# CHART CONFIGURATION SWITCHER
# =============================================================================

def switch_chart_type(chart_name, new_type):
    """
    Switch chart type dynamically.
    
    Args:
        chart_name: Name of chart to modify
        new_type: New chart type ('bar', 'pie', 'donut')
    """
    if chart_name in CHART_CONFIG['charts']:
        CHART_CONFIG['charts'][chart_name]['type'] = new_type

def get_available_chart_types():
    """Get list of available chart types for cost breakdown."""
    return ['bar', 'pie', 'donut']

# =============================================================================
# ERROR HANDLING AND FALLBACKS
# =============================================================================

def create_error_chart(error_message):
    """Create a simple error display when charts fail."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.text(0.5, 0.5, f"Chart Error:\n{error_message}", 
            ha='center', va='center', fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.show()

def validate_chart_data(analysis):
    """
    Validate that analysis data contains required fields for charting.
    
    Args:
        analysis: System analysis dictionary
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = {
        'system': ['power', 'T1', 'T2', 'T3', 'T4', 'F1', 'F2'],
        'costs': ['total_pipe_cost', 'hx_cost', 'total_valve_cost', 'pump_cost', 'installation_cost'],
        'sizing': ['primary_pipe_size', 'room_size']
    }
    
    try:
        for section, fields in required_fields.items():
            if section not in analysis:
                return False
            for field in fields:
                if field not in analysis[section]:
                    return False
                # Try to convert to float to ensure it's numeric
                safe_float_convert(analysis[section][field])
        return True
    except:
        return False

# =============================================================================
# UTILITY FUNCTIONS FOR CHART CUSTOMIZATION
# =============================================================================

def update_chart_colors(chart_name, new_colors):
    """
    Update colors for a specific chart.
    
    Args:
        chart_name: Name of chart to modify
        new_colors: List of new color codes
    """
    if chart_name in CHART_CONFIG['charts']:
        CHART_CONFIG['charts'][chart_name]['colors'] = new_colors

def update_chart_labels(chart_name, new_labels):
    """
    Update labels for a specific chart.
    
    Args:
        chart_name: Name of chart to modify
        new_labels: List of new labels
    """
    if chart_name in CHART_CONFIG['charts']:
        CHART_CONFIG['charts'][chart_name]['labels'] = new_labels

def get_chart_config(chart_name):
    """
    Get configuration for a specific chart.
    
    Args:
        chart_name: Name of chart
    
    Returns:
        Chart configuration dictionary
    """
    return CHART_CONFIG['charts'].get(chart_name, {})

# =============================================================================
# EXPORT FUNCTIONS
# =============================================================================

def save_charts_to_file(analysis, filename='heat_reuse_charts.png', dpi=300):
    """
    Save charts to file instead of displaying.
    
    Args:
        analysis: System analysis dictionary
        filename: Output filename
        dpi: Resolution for saved image
    """
    try:
        # Create charts
        layout = CHART_CONFIG['layout']
        fig, axs = plt.subplots(
            layout['subplot_rows'], 
            layout['subplot_cols'], 
            figsize=layout['figure_size']
        )
        
        # Extract data and create charts
        system = analysis['system']
        costs = analysis['costs']
        sizing = analysis['sizing']
        
        create_temperature_chart(axs[0, 0], system)
        create_flow_rates_chart(axs[0, 1], system)
        create_cost_breakdown_chart(axs[1, 0], costs)
        create_system_metrics_chart(axs[1, 1], system, sizing)
        
        # Set title and save
        power_display = format_display_value(float(system['power']), 'temperature', False)
        plt.suptitle(f'Heat Reuse System Analysis - {power_display}MW System', 
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=dpi, bbox_inches='tight')
        plt.close()
        
        return f"Charts saved to {filename}"
        
    except Exception as e:
        return f"Error saving charts: {str(e)}"

    
# Approach charting

def create_system_metrics_chart(ax, system_data, sizing_data):
    """Create system summary metrics chart."""
    config = CHART_CONFIG['charts']['system_metrics']
    
    # Prepare data
    metric_values = [
        float(system_data['power']),
        float(system_data['T2']) - float(system_data['T1']),
        float(sizing_data['primary_pipe_size']),
        float(sizing_data['room_size'])
    ]
    
    # Create chart
    bars = ax.bar(config['labels'], metric_values, color=config['colors'])
    ax.set_title(config['title'], fontsize=14, fontweight='bold')
    ax.set_ylabel(config['ylabel'])
    
    # Add metric labels with appropriate formatting
    metric_rounding_types = ['temperature', 'temperature', 'pipe_size', 'room_size']
    metric_units = ['', '°C', '', 'm']
    for i, (v, rounding_type, unit) in enumerate(zip(metric_values, metric_rounding_types, metric_units)):
        display_value = format_display_value(v, rounding_type, False)
        label = f"{display_value}{unit}" if unit else display_value
        ax.text(i, v + max(metric_values)*0.02, label, ha='center', fontweight='bold')

def create_approach_profiles_chart(ax, system_data):
    """
    Create CDU-style approach profiles chart showing TCS and FWS trajectories.
    
    Args:
        ax: Matplotlib axis to plot on
        system_data: System analysis data dictionary
    """
    try:
        # Import the approach calculation functions
        from core.original_calculations import calculate_combined_approach_profiles
        
        # Calculate approach profiles
        profiles = calculate_combined_approach_profiles(system_data)
        
        if not profiles or not profiles['tcs_profile'] or not profiles['fws_profile']:
            ax.text(0.5, 0.5, 'Approach Profile Data\nNot Available', 
                   ha='center', va='center', fontsize=12, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
            ax.set_title('Approach Profiles', fontsize=14, fontweight='bold')
            return
        
        tcs = profiles['tcs_profile']
        fws = profiles['fws_profile']
        
        # Convert time progression to percentage for x-axis
        time_percent = [t * 100 for t in tcs['time_progression']]
        
        # Plot TCS approach profile (internal system)
        ax.plot(time_percent, tcs['temperatures'], 
               color='#ff6666', linewidth=3, marker='o', markersize=4,
               label=f'TCS Internal ({tcs["start_temp"]:.0f}°C → {tcs["target_temp"]:.0f}°C)')
        
        # Plot FWS approach profile (external system)
        ax.plot(time_percent, fws['temperatures'], 
               color='#66b3ff', linewidth=3, marker='s', markersize=4,
               label=f'FWS External ({fws["start_temp"]:.0f}°C → {fws["target_temp"]:.0f}°C)')
        
        # Chart styling
        ax.set_title('System Approach Profiles', fontsize=14, fontweight='bold')
        ax.set_xlabel('Process Completion (%)')
        ax.set_ylabel('Temperature (°C)')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best')
        
        # Add annotations for key points
        ax.annotate(f'TCS Start\n{tcs["start_temp"]:.0f}°C', 
                   xy=(0, tcs['temperatures'][0]), xytext=(10, tcs['temperatures'][0] + 1),
                   arrowprops=dict(arrowstyle='->', color='#ff6666', alpha=0.7),
                   fontsize=9, ha='left')
        
        ax.annotate(f'FWS Start\n{fws["start_temp"]:.0f}°C', 
                   xy=(0, fws['temperatures'][0]), xytext=(10, fws['temperatures'][0] - 1),
                   arrowprops=dict(arrowstyle='->', color='#66b3ff', alpha=0.7),
                   fontsize=9, ha='left')
        
        # Set reasonable y-axis limits
        all_temps = tcs['temperatures'] + fws['temperatures']
        temp_range = max(all_temps) - min(all_temps)
        ax.set_ylim(min(all_temps) - temp_range * 0.1, max(all_temps) + temp_range * 0.1)
        
    except Exception as e:
        ax.text(0.5, 0.5, f'Chart Error:\n{str(e)}', 
               ha='center', va='center', fontsize=10, 
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
        ax.set_title('Approach Profiles (Error)', fontsize=14, fontweight='bold')

def create_efficiency_chart(ax, system_data, costs_data):
    """
    Create efficiency analysis chart.
    
    Args:
        ax: Matplotlib axis to plot on
        system_data: System data dictionary
        costs_data: Cost data dictionary
    """
    try:
        # Calculate efficiency metrics
        power_mw = float(system_data['power'])
        total_cost = float(costs_data['total_cost'])
        f1_flow = float(system_data['F1'])
        
        # Efficiency metrics
        cost_per_mw = total_cost / power_mw if power_mw > 0 else 0
        cost_per_flow = total_cost / f1_flow if f1_flow > 0 else 0
        flow_per_mw = f1_flow / power_mw if power_mw > 0 else 0
        
        metrics = ['Cost/MW\n(€/MW)', 'Cost/Flow\n(€/L/min)', 'Flow/MW\n(L/min/MW)']
        values = [cost_per_mw, cost_per_flow, flow_per_mw]
        colors = ['#ff9999', '#99ff99', '#9999ff']
        
        bars = ax.bar(metrics, values, color=colors)
        ax.set_title('System Efficiency Metrics', fontsize=14, fontweight='bold')
        ax.set_ylabel('Efficiency Values')
        
        # Add value labels
        for i, v in enumerate(values):
            if v > 1000:
                label = f"{v:,.0f}"
            else:
                label = f"{v:.1f}"
            ax.text(i, v + max(values)*0.02, label, ha='center', fontweight='bold')
            
    except Exception as e:
        ax.text(0.5, 0.5, f'Efficiency Chart Error:\n{str(e)}', 
               ha='center', va='center', fontsize=10, 
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
        ax.set_title('Efficiency Metrics (Error)', fontsize=14, fontweight='bold')