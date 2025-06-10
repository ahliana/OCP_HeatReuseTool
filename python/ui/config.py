"""
UI Configuration - All UI settings in one place for easy maintenance
Extracted from Interactive Analysis Tool.ipynb
"""

import ipywidgets as widgets

# =============================================================================
# DROPDOWN CONFIGURATION - Easy to modify for global deployment
# =============================================================================

UI_CONFIG = {
    'dropdowns': {
        'power': {
            'options': [1, 2, 3, 4, 5],
            'default': 1,
            'label': 'Power/Capacity:',
            'tooltip': 'System power capacity in MW'
        },
        't1': {
            'options': [20, 30, 45],
            'default': 20,
            'label': 'T1 Temperature:',
            'tooltip': 'T1 outlet temperature in °C'
        },
        'temp_diff': {
            'options': [10, 12, 14],
            'default': 10,
            'label': 'Temperature Rise:',
            'tooltip': 'Temperature difference (T2 - T1) in °C'
        },
        'approach': {
            'options': [2, 3, 5],
            'default': 2,
            'label': 'Approach:',
            'tooltip': 'System approach value'
        }
    },
    'button': {
        'text': 'Calculate System',
        'style': 'success',
        'icon': 'calculator',
        'tooltip': 'Calculate system parameters and costs'
    },
    'layout': {
        'widget_width': '300px',
        'description_width': '140px',
        'button_width': '200px',
        'button_height': '45px',
        'button_margin': '10px 0'
    }
}

# =============================================================================
# DISPLAY ROUNDING CONFIGURATION - Centralized for consistency
# =============================================================================

DISPLAY_ROUNDING = {
    # Temperature values (no decimals)
    'temperature': 0,
    
    # Flow rates (no decimals) 
    'flow_rate': 0,
    
    # Room size (nearest 0.1)
    'room_size': 1,
    
    # Pipe size (nearest 1)
    'pipe_size': 0,
    
    # Pipe cost per meter (nearest 1)
    'pipe_cost_per_meter': 0,
    
    # Total pipe cost (nearest 1K = nearest 1000)
    'total_pipe_cost': -3,  # -3 means round to nearest 1000
    
    # Heat exchanger cost (nearest 1)
    'hx_cost': 0,
    
    # Valve costs (nearest 100)
    'valve_costs': -2,  # -2 means round to nearest 100
    
    # Pump cost (nearest 100)
    'pump_cost': -2,  # -2 means round to nearest 100
    
    # Total cost (nearest 1K for large amounts)
    'total_cost': -3
}

# =============================================================================
# INPUT VALIDATION RULES - Easy to modify for different regions
# =============================================================================

VALIDATION_RULES = {
    'power': {
        'valid_options': [1, 2, 3, 4, 5],
        'error_message': 'Power must be 1, 2, 3, 4, or 5 MW'
    },
    't1': {
        'valid_options': [20, 30, 45],
        'error_message': 'T1 must be 20, 30, or 45°C'
    },
    'temp_diff': {
        'valid_options': [10, 12, 14],
        'error_message': 'Temperature difference must be 10, 12, or 14°C'
    },
    'approach': {
        'valid_options': [2, 3, 5],
        'error_message': 'Approach must be 2, 3, or 5'
    }
}

# =============================================================================
# CHART CONFIGURATION - Easy to reconfigure chart types and styles
# =============================================================================

CHART_CONFIG = {
    'layout': {
        'figure_size': (14, 14),  
        'subplot_rows': 3,        
        'subplot_cols': 2,
        'style': 'ggplot'
    },
    'charts': {
        'temperatures': {
            'type': 'bar',
            'title': 'System Temperatures',
            'ylabel': 'Temperature (°C)',
            'colors': ['#ff9999', '#ff6666', '#66b3ff', '#3399ff'],
            'position': (0, 0),
            'labels': ['T1\\n(Out to TCS)', 'T2\\n(In from TCS)', 'T3\\n(Out to Consumer)', 'T4\\n(In from Consumer)']
        },
        'flow_rates': {
            'type': 'bar',
            'title': 'Flow Rates',
            'ylabel': 'Flow Rate (l/m)',
            'colors': ['#99ff99', '#66cc66'],
            'position': (0, 1),
            'labels': ['F1\\n(TCS Flow)', 'F2\\n(FWS Flow)']
        },
        'cost_breakdown': {
            'type': 'pie',
            'title': 'Cost Breakdown',
            'colors': ['#ffcc99', '#ff9999', '#cc99ff', '#99ccff', '#ffff99'],
            'position': (1, 0),
            'labels': ['Pipe\\nCost', 'Heat\\nExchanger', 'Valves', 'Pump', 'Installation'],
            'autopct': '%1.1f%%'
        },
        'system_metrics': {
            'type': 'bar',
            'title': 'System Metrics',
            'ylabel': 'Values',
            'colors': ['#ff6666', '#66ff66', '#6666ff', '#ffcc66'],
            'position': (1, 1),
            'labels': ['Power\\n(MW)', 'Temp Rise\\n(°C)', 'Pipe Size', 'Room Size\\n(m)']
        },
        'approach_profiles': {
            'type': 'line',
            'title': 'TCS/FWS Approach Profiles',
            'ylabel': 'Temperature (°C)',
            'xlabel': 'Process Completion (%)',
            'colors': ['#ff6666', '#66b3ff'],
            'position': (2, 0),
            'labels': ['TCS Internal', 'FWS External']
        },
        'efficiency_metrics': {
            'type': 'bar',
            'title': 'System Efficiency Metrics',
            'ylabel': 'Efficiency Values',
            'colors': ['#ff9999', '#99ff99', '#9999ff'],
            'position': (2, 1),
            'labels': ['Cost/MW', 'Cost/Flow', 'Flow/MW']
        }
    }
}


# =============================================================================
# ERROR AND SUCCESS MESSAGE STYLING
# =============================================================================

MESSAGE_STYLES = {
    'success': {
        'background_color': '#d4edda',
        'border_color': '#c3e6cb',
        'text_color': '#155724',
        'icon': '✅'
    },
    'error': {
        'background_color': '#f8d7da',
        'border_color': '#f5c6cb',
        'text_color': '#721c24',
        'icon': '❌'
    },
    'warning': {
        'background_color': '#fff3cd',
        'border_color': '#ffeaa7',
        'text_color': '#856404',
        'icon': '⚠️'
    },
    'info': {
        'background_color': '#e3f2fd',
        'border_color': '#bbdefb',
        'text_color': '#0d47a1',
        'icon': 'ℹ️'
    }
}

# =============================================================================
# OUTPUT DISPLAY CONFIGURATION
# =============================================================================

OUTPUT_CONFIG = {
    'system_params': {
        'title': '📊 System Parameters (Auto-Calculated)',
        'border_color': '#4CAF50',
        'title_color': '#4CAF50'
    },
    'cost_analysis': {
        'title': '💰 Cost Analysis',
        'border_color': '#2196F3',
        'title_color': '#2196F3'
    },
    'charts': {
        'title_template': 'Heat Reuse System Analysis - {power}MW System'
    }
}

# =============================================================================
# INTERNATIONALIZATION SUPPORT (for future use)
# =============================================================================

LABELS = {
    'en': {
        'power': 'Power/Capacity:',
        'temperature': 'T1 Temperature:',
        'temp_rise': 'Temperature Rise:',
        'approach': 'Approach:',
        'calculate': 'Calculate System',
        'system_params': 'System Parameters (Auto-Calculated)',
        'cost_analysis': 'Cost Analysis'
    }
    # Add other languages as needed:
    # 'fr': {...}, 'de': {...}, etc.
}

# =============================================================================
# UTILITY FUNCTIONS FOR CONFIG ACCESS
# =============================================================================

def get_dropdown_config(dropdown_name):
    """Get configuration for a specific dropdown"""
    return UI_CONFIG['dropdowns'].get(dropdown_name, {})

def get_chart_config(chart_name):
    """Get configuration for a specific chart"""
    return CHART_CONFIG['charts'].get(chart_name, {})

def get_validation_rule(field_name):
    """Get validation rule for a specific field"""
    return VALIDATION_RULES.get(field_name, {})

def get_rounding_precision(value_type):
    """Get rounding precision for a specific value type"""
    return DISPLAY_ROUNDING.get(value_type, 0)