# =============================================================================
# THERMODYNAMICS MODULE
# =============================================================================

# python/physics/thermodynamics.py
"""
Standard Thermodynamic Formulas and Relationships
Reference: Fundamentals of Heat and Mass Transfer (Incropera & DeWitt, 8th Ed.)
"""

import math
from .constants import WATER_PROPERTIES, CONVERSION_FACTORS

def sensible_heat_transfer(mass_flow_rate, specific_heat, delta_temperature):
    """
    Calculate sensible heat transfer rate using fundamental thermodynamic relationship.
    
    Formula: Q̇ = ṁ × cp × ΔT
    Reference: Any thermodynamics textbook, First Law of Thermodynamics
    
    Args:
        mass_flow_rate (float): Mass flow rate [kg/s]
        specific_heat (float): Specific heat capacity [J/(kg·K)]
        delta_temperature (float): Temperature difference [K or °C]
    
    Returns:
        float: Heat transfer rate [W]
        
    Example:
        >>> sensible_heat_transfer(2.5, 4182, 10)  # Water heating
        104550.0
    """
    return mass_flow_rate * specific_heat * delta_temperature


def power_from_heat_flow(volume_flow_lpm, inlet_temp_c, outlet_temp_c, fluid='water'):
    """
    Calculate power from volumetric flow and temperature change.
    Commonly used in datacenter cooling calculations.
    
    Args:
        volume_flow_lpm (float): Volume flow rate [L/min]
        inlet_temp_c (float): Inlet temperature [°C]
        outlet_temp_c (float): Outlet temperature [°C]
        fluid (str): Fluid type ('water' or 'air')
    
    Returns:
        float: Power [W]
        
    Example:
        >>> power_from_heat_flow(1493, 20, 30)  # 1MW system
        1041616.67
    """
    # Convert L/min to kg/s
    if fluid == 'water':
        # Use temperature-dependent properties
        avg_temp = (inlet_temp_c + outlet_temp_c) / 2
        if avg_temp <= 25:
            props = WATER_PROPERTIES['20C']
        elif avg_temp <= 37.5:
            props = WATER_PROPERTIES['30C']
        else:
            props = WATER_PROPERTIES['45C']
            
        mass_flow = (volume_flow_lpm * CONVERSION_FACTORS['liters_to_m3'] / 
                    CONVERSION_FACTORS['minutes_to_seconds'] * props['density'])
        
        return sensible_heat_transfer(mass_flow, props['specific_heat'], 
                                    abs(outlet_temp_c - inlet_temp_c))
    else:
        raise ValueError("Only water properties implemented currently")


def temperature_approach(hot_inlet, hot_outlet, cold_inlet, cold_outlet):
    """
    Calculate approach temperature difference in heat exchanger.
    
    Args:
        hot_inlet (float): Hot fluid inlet temperature [°C]
        hot_outlet (float): Hot fluid outlet temperature [°C]
        cold_inlet (float): Cold fluid inlet temperature [°C]
        cold_outlet (float): Cold fluid outlet temperature [°C]
    
    Returns:
        float: Approach temperature difference [°C]
        
    Example:
        >>> temperature_approach(30, 20, 18, 28)
        -2.0  # Cold outlet approaches hot inlet
    """
    return min(hot_inlet - cold_outlet, hot_outlet - cold_inlet)


def pinch_point_analysis(hot_streams, cold_streams, min_approach_temp=10.0):
    """
    Perform basic pinch point analysis for heat integration.
    
    Reference: Process Heat Transfer (Hewitt et al.), Chapter 19
    
    Args:
        hot_streams (list): List of (T_inlet, T_outlet, heat_capacity_rate) for hot streams
        cold_streams (list): List of (T_inlet, T_outlet, heat_capacity_rate) for cold streams  
        min_approach_temp (float): Minimum approach temperature [°C]
    
    Returns:
        dict: Analysis results including pinch temperatures and utility requirements
    """
    # Simplified pinch analysis implementation
    # In practice, use specialized software like HINT, SPRINT, or SuperTarget
    
    hot_pinch_temp = None
    cold_pinch_temp = None
    
    # Find temperature ranges
    all_temps = []
    for stream in hot_streams + cold_streams:
        all_temps.extend([stream[0], stream[1]])
    
    temp_range = (min(all_temps), max(all_temps))
    
    # For detailed pinch analysis, implement composite curve construction
    # This is a placeholder for the full algorithm
    
    return {
        'hot_pinch_temperature': hot_pinch_temp,
        'cold_pinch_temperature': cold_pinch_temp,
        'minimum_heating_utility': None,  # Would be calculated from composite curves
        'minimum_cooling_utility': None,  # Would be calculated from composite curves
        'temperature_range': temp_range,
        'recommendation': 'Use specialized pinch analysis software for detailed calculations'
    }
