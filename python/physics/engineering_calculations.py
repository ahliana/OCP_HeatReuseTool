# =============================================================================
# ENGINEERING CALCULATIONS MODULE
# =============================================================================

# python/physics/engineering_calculations.py
"""
High-Level Engineering Calculations for Common Datacenter Applications
Combines multiple physics principles for practical engineering solutions
"""

import math
from .constants import WATER_PROPERTIES, CONVERSION_FACTORS
from .thermodynamics import heat_capacity_flow, sensible_heat_transfer
from .fluid_mechanics import reynolds_number, pipe_velocity
from .units import celsius_to_kelvin, celsius_to_fahrenheit, liters_per_minute_to_m3_per_second

def datacenter_cooling_analysis(server_power_kw, supply_temp_c=18, return_temp_c=28, 
                               flow_type='water'):
    """
    Complete cooling analysis for datacenter application.
    
    Args:
        server_power_kw (float): Server heat load [kW]
        supply_temp_c (float): Supply temperature [°C]
        return_temp_c (float): Return temperature [°C] 
        flow_type (str): Cooling fluid type
    
    Returns:
        dict: Complete analysis including flow rates, sizing, etc.
    """
    # Convert power to watts
    heat_load_w = server_power_kw * 1000
    
    # Calculate required flow rate
    if flow_type == 'water':
        # Use water properties at average temperature
        avg_temp = (supply_temp_c + return_temp_c) / 2
        if avg_temp <= 25:
            props = WATER_PROPERTIES['20C']
        elif avg_temp <= 37.5:
            props = WATER_PROPERTIES['30C']
        else:
            props = WATER_PROPERTIES['45C']
        
        delta_t = return_temp_c - supply_temp_c
        mass_flow_rate = heat_load_w / (props['specific_heat'] * delta_t)
        volume_flow_m3s = mass_flow_rate / props['density']
        volume_flow_lpm = volume_flow_m3s / CONVERSION_FACTORS['liters_to_m3'] * CONVERSION_FACTORS['minutes_to_seconds']
        
        return {
            'heat_load_w': heat_load_w,
            'mass_flow_rate_kg_s': mass_flow_rate,
            'volume_flow_rate_m3_s': volume_flow_m3s,
            'volume_flow_rate_lpm': volume_flow_lpm,
            'supply_temperature_c': supply_temp_c,
            'return_temperature_c': return_temp_c,
            'temperature_rise_c': delta_t,
            'fluid_properties': props
        }
    else:
        raise NotImplementedError("Only water cooling implemented currently")


def pipe_sizing_analysis(flow_rate_lpm, velocity_limit_ms=2.0, temperature_c=20):
    """
    Determine optimal pipe size based on flow rate and velocity constraints.
    
    Args:
        flow_rate_lpm (float): Flow rate [L/min]
        velocity_limit_ms (float): Maximum allowable velocity [m/s]
        temperature_c (float): Operating temperature [°C]
    
    Returns:
        dict: Pipe sizing recommendations
    """
    # Convert flow rate
    flow_rate_m3s = liters_per_minute_to_m3_per_second(flow_rate_lpm)
    
    # Calculate minimum pipe diameter
    min_diameter = math.sqrt(4 * flow_rate_m3s / (math.pi * velocity_limit_ms))
    
    # Get standard pipe sizes (European DN sizing - this should be imported from materials.py or similar)
    pipe_sizes = {
        15: 15.8,    # DN15 pipe, inner diameter in mm
        20: 20.9,    # DN20 pipe
        25: 26.6,    # DN25 pipe
        32: 35.1,    # DN32 pipe
        40: 40.9,    # DN40 pipe
        50: 52.5,    # DN50 pipe
        65: 62.7,    # DN65 pipe
        80: 77.9,    # DN80 pipe
        100: 102.3,  # DN100 pipe
        150: 154.1,  # DN150 pipe
        200: 202.7,  # DN200 pipe
        250: 254.5,  # DN250 pipe
        300: 303.2   # DN300 pipe
    }
    
    # Find suitable pipe sizes
    suitable_sizes = []
    for nominal_size_dn, inner_diameter_mm in pipe_sizes.items():
        inner_diameter_m = inner_diameter_mm / 1000
        if inner_diameter_m >= min_diameter:
            velocity = pipe_velocity(flow_rate_m3s, inner_diameter_m)
            
            # Get water properties for Reynolds calculation
            if temperature_c <= 25:
                props = WATER_PROPERTIES['20C']
            elif temperature_c <= 37.5:
                props = WATER_PROPERTIES['30C']
            else:
                props = WATER_PROPERTIES['45C']
            
            re = reynolds_number(velocity, inner_diameter_m, props['kinematic_viscosity'])
            
            suitable_sizes.append({
                'nominal_size_dn': nominal_size_dn,
                'inner_diameter_mm': inner_diameter_mm,
                'inner_diameter_m': inner_diameter_m,
                'velocity_ms': velocity,
                'reynolds_number': re,
                'flow_regime': 'laminar' if re < 2300 else 'turbulent'
            })
    
    return {
        'flow_rate_lpm': flow_rate_lpm,
        'flow_rate_m3s': flow_rate_m3s,
        'minimum_diameter_m': min_diameter,
        'velocity_limit_ms': velocity_limit_ms,
        'suitable_pipe_sizes': suitable_sizes[:3] if suitable_sizes else [],
        'recommended_size': suitable_sizes[0] if suitable_sizes else None
    }


def heat_exchanger_analysis(hot_inlet, hot_outlet, cold_inlet, cold_outlet,
                           hot_flow_lpm, cold_flow_lpm=None, exchanger_type='counterflow'):
    """
    Complete heat exchanger analysis including sizing and performance.
    
    Args:
        hot_inlet (float): Hot fluid inlet temperature [°C]
        hot_outlet (float): Hot fluid outlet temperature [°C]
        cold_inlet (float): Cold fluid inlet temperature [°C]
        cold_outlet (float): Cold fluid outlet temperature [°C]
        hot_flow_lpm (float): Hot fluid flow rate [L/min]
        cold_flow_lpm (float, optional): Cold fluid flow rate [L/min]
        exchanger_type (str): Heat exchanger type
    
    Returns:
        dict: Complete heat exchanger analysis
    """
    # Calculate heat duty from hot side
    hot_avg_temp = (hot_inlet + hot_outlet) / 2
    if hot_avg_temp <= 25:
        hot_props = WATER_PROPERTIES['20C']
    elif hot_avg_temp <= 37.5:
        hot_props = WATER_PROPERTIES['30C']
    else:
        hot_props = WATER_PROPERTIES['45C']
    
    hot_mass_flow = liters_per_minute_to_m3_per_second(hot_flow_lpm) * hot_props['density']
    heat_duty = sensible_heat_transfer(hot_mass_flow, hot_props['specific_heat'], hot_inlet - hot_outlet)
    
    # Calculate LMTD
    if exchanger_type == 'counterflow':
        delta_t1 = hot_inlet - cold_outlet
        delta_t2 = hot_outlet - cold_inlet
        
        if abs(delta_t1 - delta_t2) < 1e-6:
            lmtd = delta_t1
        else:
            if delta_t1 <= 0 or delta_t2 <= 0:
                lmtd = None  # Invalid configuration
            else:
                lmtd = (delta_t1 - delta_t2) / math.log(delta_t1 / delta_t2)
    else:
        delta_t1 = hot_inlet - cold_inlet
        delta_t2 = hot_outlet - cold_outlet
        
        if abs(delta_t1 - delta_t2) < 1e-6:
            lmtd = delta_t1
        else:
            if delta_t1 <= 0 or delta_t2 <= 0:
                lmtd = None  # Invalid configuration
            else:
                lmtd = (delta_t1 - delta_t2) / math.log(delta_t1 / delta_t2)
    
    # Calculate capacity rates and effectiveness
    hot_capacity_rate = hot_mass_flow * hot_props['specific_heat']
    
    if cold_flow_lpm:
        cold_avg_temp = (cold_inlet + cold_outlet) / 2
        if cold_avg_temp <= 25:
            cold_props = WATER_PROPERTIES['20C']
        elif cold_avg_temp <= 37.5:
            cold_props = WATER_PROPERTIES['30C']
        else:
            cold_props = WATER_PROPERTIES['45C']
        
        cold_mass_flow = liters_per_minute_to_m3_per_second(cold_flow_lpm) * cold_props['density']
        cold_capacity_rate = cold_mass_flow * cold_props['specific_heat']
        
        c_min = min(hot_capacity_rate, cold_capacity_rate)
        c_max = max(hot_capacity_rate, cold_capacity_rate)
        capacity_ratio = c_min / c_max
        
        q_max = c_min * (hot_inlet - cold_inlet)
        effectiveness = heat_duty / q_max if q_max > 0 else 0
    else:
        capacity_ratio = None
        effectiveness = None
        cold_mass_flow = None
        cold_capacity_rate = None
    
    # Calculate approach and pinch temperatures
    approach = hot_inlet - cold_outlet
    pinch = hot_outlet - cold_inlet
    
    return {
        'heat_duty_w': heat_duty,
        'lmtd_c': lmtd,
        'hot_capacity_rate': hot_capacity_rate,
        'cold_capacity_rate': cold_capacity_rate,
        'capacity_ratio': capacity_ratio,
        'effectiveness': effectiveness,
        'approach_temperature_c': approach,
        'pinch_temperature_c': pinch,
        'hot_mass_flow_kg_s': hot_mass_flow,
        'cold_mass_flow_kg_s': cold_mass_flow,
        'exchanger_type': exchanger_type,
        'performance_rating': 'excellent' if effectiveness and effectiveness > 0.8 else 
                             'good' if effectiveness and effectiveness > 0.6 else 
                             'fair' if effectiveness else 'unknown'
    }


# =============================================================================
# VALIDATION AND EXAMPLES
# =============================================================================

def validate_physics_calculations():
    """
    Validate physics calculations with known examples.
    Returns test results for verification.
    """
    results = []
    
    # Test 1: Water heating power calculation
    try:
        mass_flow = liters_per_minute_to_m3_per_second(1493) * WATER_PROPERTIES['20C']['density']
        power = sensible_heat_transfer(mass_flow, WATER_PROPERTIES['20C']['specific_heat'], 10)
        expected = 1039193  # Expected power in watts
        error = abs(power - expected) / expected * 100
        results.append({
            'test': 'Water heating power calculation',
            'calculated': power,
            'expected': expected,
            'error_percent': error,
            'status': 'PASS' if error < 1.0 else 'FAIL'
        })
    except Exception as e:
        results.append({'test': 'Water heating power calculation', 'status': 'ERROR', 'error': str(e)})
    
    # Test 2: Reynolds number calculation
    try:
        velocity = 2.0
        diameter = 0.1
        kinematic_viscosity = WATER_PROPERTIES['20C']['kinematic_viscosity']
        re = reynolds_number(velocity, diameter, kinematic_viscosity)
        expected = 199203  # Expected Reynolds number
        error = abs(re - expected) / expected * 100
        results.append({
            'test': 'Reynolds number calculation',
            'calculated': re,
            'expected': expected,
            'error_percent': error,
            'status': 'PASS' if error < 1.0 else 'FAIL'
        })
    except Exception as e:
        results.append({'test': 'Reynolds number calculation', 'status': 'ERROR', 'error': str(e)})
    
    return results


def quick_power_calculation(flow_lpm, temp_rise_c, fluid='water'):
    """
    Quick power calculation for common applications.
    Equivalent to your original get_MW function but using standard physics.
    
    Args:
        flow_lpm (float): Flow rate [L/min]
        temp_rise_c (float): Temperature rise [°C]
        fluid (str): Fluid type
    
    Returns:
        float: Power [W]
    """
    if fluid == 'water':
        # Use average properties (simplified for quick calculations)
        avg_props = WATER_PROPERTIES['30C']  # Representative properties
        mass_flow = liters_per_minute_to_m3_per_second(flow_lpm) * avg_props['density']
        return sensible_heat_transfer(mass_flow, avg_props['specific_heat'], temp_rise_c)
    else:
        raise ValueError("Only water implemented")


# Additional quick-access functions for compatibility with existing code
def get_MW_equivalent(F1, T1, T2):
    """Equivalent to your get_MW function using standard physics."""
    return quick_power_calculation(F1, T2 - T1)

def get_MW_divd_equivalent(F1, T1, T2):
    """Equivalent to your get_MW_divd function."""
    return get_MW_equivalent(F1, T1, T2) / 1_000_000


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("Engineering Calculations Module for Heat Reuse Systems")
    print("=" * 55)
    
    try:
        # Run validation tests
        test_results = validate_physics_calculations()
        for result in test_results:
            print(f"{result['test']}: {result['status']}")
            if result['status'] not in ['ERROR']:
                print(f"  Calculated: {result.get('calculated', 'N/A')}")
                print(f"  Expected: {result.get('expected', 'N/A')}")
                print(f"  Error: {result.get('error_percent', 'N/A'):.2f}%")
        
        print("\nExample Applications:")
        print("-" * 30)
        
        # Example 1: Datacenter cooling analysis
        cooling_analysis = datacenter_cooling_analysis(1000, 20, 30)  # 1MW server load
        print(f"1MW Server Cooling:")
        print(f"  Required flow rate: {cooling_analysis['volume_flow_rate_lpm']:.0f} L/min")
        print(f"  Mass flow rate: {cooling_analysis['mass_flow_rate_kg_s']:.1f} kg/s")
        
        # Example 2: Pipe sizing
        pipe_analysis = pipe_sizing_analysis(1493, velocity_limit_ms=2.0)
        if pipe_analysis['recommended_size']:
            rec = pipe_analysis['recommended_size']
            print(f"\nPipe Sizing for 1493 L/min:")
            print(f"  Recommended: DN{rec['nominal_size_dn']} pipe")
            print(f"  Velocity: {rec['velocity_ms']:.2f} m/s")
            print(f"  Reynolds: {rec['reynolds_number']:.0f} ({rec['flow_regime']})")
        
        # Example 3: Heat exchanger analysis
        hx_analysis = heat_exchanger_analysis(30, 20, 18, 28, 1493, 1440)
        print(f"\nHeat Exchanger Analysis:")
        print(f"  Heat duty: {hx_analysis['heat_duty_w']/1000:.0f} kW")
        if hx_analysis['lmtd_c']:
            print(f"  LMTD: {hx_analysis['lmtd_c']:.1f}°C")
        if hx_analysis['effectiveness']:
            print(f"  Effectiveness: {hx_analysis['effectiveness']:.3f}")
        print(f"  Approach: {hx_analysis['approach_temperature_c']:.1f}°C")
        print(f"  Performance: {hx_analysis['performance_rating']}")
        
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Make sure the physics module constants and functions are available.")