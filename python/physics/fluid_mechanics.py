# =============================================================================
# FLUID MECHANICS MODULE  
# =============================================================================

# python/physics/fluid_mechanics.py
"""
Standard Fluid Mechanics Formulas and Correlations
Reference: VDI Heat Atlas, Introduction to Fluid Mechanics (Fox & McDonald, 8th Ed.)
European standards and correlations prioritized
"""

import math
from .constants import (
    WATER_PROPERTIES, AIR_PROPERTIES, STEEL_PROPERTIES, 
    VELOCITY_LIMITS, VALIDATION_DATA, EUROPEAN_PIPE_SIZES
)

# =============================================================================
# FUNDAMENTAL FLOW CALCULATIONS
# =============================================================================

def reynolds_number(velocity, diameter, kinematic_viscosity=None, 
                   temperature_c=20, fluid='water'):
    """
    Calculate Reynolds number for pipe flow.
    
    Formula: Re = ρVD/μ = VD/ν
    Reference: Any fluid mechanics textbook, VDI Heat Atlas
    
    Args:
        velocity (float): Average velocity [m/s]
        diameter (float): Pipe diameter [m]
        kinematic_viscosity (float, optional): Kinematic viscosity [m²/s]
        temperature_c (float): Temperature for property lookup [°C]
        fluid (str): Fluid type ('water' or 'air')
    
    Returns:
        float: Reynolds number [dimensionless]
        
    Example:
        >>> reynolds_number(2.0, 0.1, temperature_c=20)
        199203.19
    """
    if kinematic_viscosity is None:
        if fluid == 'water':
            # Enhanced temperature selection with more options
            if temperature_c <= 25:
                props = WATER_PROPERTIES['20C']
            elif temperature_c <= 37.5:
                props = WATER_PROPERTIES['30C']
            elif temperature_c <= 52.5:
                props = WATER_PROPERTIES['45C']
            else:
                props = WATER_PROPERTIES['60C']
            kinematic_viscosity = props['kinematic_viscosity']
        elif fluid == 'air':
            if temperature_c <= 27.5:
                props = AIR_PROPERTIES['20C']
            else:
                props = AIR_PROPERTIES['35C']
            kinematic_viscosity = props['kinematic_viscosity']
        else:
            raise ValueError("Must provide kinematic_viscosity for non-standard fluids")
    
    return velocity * diameter / kinematic_viscosity


def friction_factor_laminar(reynolds_number):
    """
    Calculate friction factor for laminar pipe flow.
    
    Formula: f = 64/Re (for Re < 2300)
    Reference: Moody diagram, laminar flow region
    
    Args:
        reynolds_number (float): Reynolds number
    
    Returns:
        float: Darcy friction factor [dimensionless]
    
    Raises:
        ValueError: If Reynolds number indicates turbulent flow
    """
    if reynolds_number >= VALIDATION_DATA['reynolds_transition']['critical_re']:
        raise ValueError(f"Use turbulent friction factor correlation for Re >= {VALIDATION_DATA['reynolds_transition']['critical_re']}")
    
    return 64.0 / reynolds_number


def friction_factor_turbulent(reynolds_number, relative_roughness=0.0):
    """
    Calculate friction factor for turbulent pipe flow.
    
    For smooth pipes, uses Petukhov correlation (VDI Heat Atlas recommended):
    f = (0.790 ln(Re) - 1.64)^(-2)  for 3000 < Re < 5×10⁶
    
    For rough pipes, uses Haaland approximation of Colebrook equation.
    
    Reference: VDI Heat Atlas, Petukhov correlation
    
    Args:
        reynolds_number (float): Reynolds number (Re > 2300)
        relative_roughness (float): ε/D, pipe roughness ratio
    
    Returns:
        float: Darcy friction factor [dimensionless]
    
    Raises:
        ValueError: If Reynolds number indicates laminar flow
    """
    critical_re = VALIDATION_DATA['reynolds_transition']['critical_re']
    if reynolds_number < critical_re:
        raise ValueError(f"Use laminar friction factor correlation for Re < {critical_re}")
    
    if relative_roughness == 0.0:  # Smooth pipe
        # Petukhov correlation for smooth pipes (VDI Heat Atlas)
        if reynolds_number > 5e6:
            # Use Blasius for very high Re
            return 0.3164 / (reynolds_number ** 0.25)
        else:
            return (0.790 * math.log(reynolds_number) - 1.64) ** (-2)
    else:
        # Haaland approximation of Colebrook equation (European preference)
        term1 = (relative_roughness / 3.7) ** 1.11
        term2 = 6.9 / reynolds_number
        return (-1.8 * math.log10(term1 + term2)) ** (-2)


def pressure_drop_pipe(friction_factor, length, diameter, velocity, density):
    """
    Calculate pressure drop in pipe using Darcy-Weisbach equation.
    
    Formula: ΔP = f × (L/D) × (ρV²/2)
    Reference: Darcy-Weisbach equation, fluid mechanics fundamentals
    
    Args:
        friction_factor (float): Darcy friction factor
        length (float): Pipe length [m]
        diameter (float): Pipe diameter [m]
        velocity (float): Average velocity [m/s]
        density (float): Fluid density [kg/m³]
    
    Returns:
        float: Pressure drop [Pa]
    """
    return friction_factor * (length / diameter) * (density * velocity**2 / 2)


def pump_power_required(volume_flow_rate, pressure_head, efficiency=0.75, 
                       include_motor_efficiency=True, motor_efficiency=0.92):
    """
    Calculate pump power requirement (European standard calculation).
    
    Formula: P_shaft = (Q × ΔP) / η_pump
             P_electrical = P_shaft / η_motor (if motor efficiency included)
    
    Reference: VDI 2056, European pump efficiency standards
    
    Args:
        volume_flow_rate (float): Volume flow rate [m³/s]
        pressure_head (float): Pressure head [Pa]
        efficiency (float): Pump hydraulic efficiency [dimensionless]
        include_motor_efficiency (bool): Include motor efficiency in calculation
        motor_efficiency (float): Motor efficiency [dimensionless]
    
    Returns:
        dict: Power requirements with breakdown
    """
    hydraulic_power = volume_flow_rate * pressure_head
    shaft_power = hydraulic_power / efficiency
    
    result = {
        'hydraulic_power_w': hydraulic_power,
        'shaft_power_w': shaft_power,
        'pump_efficiency': efficiency
    }
    
    if include_motor_efficiency:
        electrical_power = shaft_power / motor_efficiency
        result.update({
            'electrical_power_w': electrical_power,
            'motor_efficiency': motor_efficiency,
            'overall_efficiency': efficiency * motor_efficiency
        })
    
    return result


def pipe_velocity(volume_flow_rate, diameter):
    """
    Calculate average flow velocity in pipe.
    
    Formula: V = Q / A = Q / (πD²/4)
    
    Args:
        volume_flow_rate (float): Volume flow rate [m³/s]
        diameter (float): Pipe diameter [m]
    
    Returns:
        float: Average velocity [m/s]
    """
    area = math.pi * diameter**2 / 4
    return volume_flow_rate / area


# =============================================================================
# EUROPEAN PIPE SIZING AND SELECTION
# =============================================================================

def select_pipe_size_european(flow_rate_m3s, max_velocity=None, fluid='water', 
                             temperature_c=20, material='carbon_steel'):
    """
    Select appropriate European DN pipe size based on flow rate and velocity limits.
    
    Uses European standards (VDI 2056) for velocity limits:
    - Water supply: ≤ 2.0 m/s (recommended ≤ 1.5 m/s)
    - Water return: ≤ 1.5 m/s
    
    Args:
        flow_rate_m3s (float): Volume flow rate [m³/s]
        max_velocity (float, optional): Maximum allowable velocity [m/s]
        fluid (str): Fluid type
        temperature_c (float): Operating temperature [°C]
        material (str): Pipe material for roughness
    
    Returns:
        dict: Recommended pipe size with analysis
    """
    if max_velocity is None:
        max_velocity = VELOCITY_LIMITS['water_systems']['supply_lines']
    
    # Get fluid properties
    if fluid == 'water':
        if temperature_c <= 25:
            props = WATER_PROPERTIES['20C']
        elif temperature_c <= 37.5:
            props = WATER_PROPERTIES['30C']
        elif temperature_c <= 52.5:
            props = WATER_PROPERTIES['45C']
        else:
            props = WATER_PROPERTIES['60C']
    else:
        raise ValueError("Only water fluid supported currently")
    
    # Get material roughness
    if material in STEEL_PROPERTIES:
        roughness = STEEL_PROPERTIES[material]['roughness']
    else:
        roughness = STEEL_PROPERTIES['carbon_steel']['roughness']  # Default
    
    suitable_sizes = []
    
    for dn, pipe_data in EUROPEAN_PIPE_SIZES.items():
        inner_diameter_m = pipe_data['inner_diameter_mm'] / 1000
        velocity = pipe_velocity(flow_rate_m3s, inner_diameter_m)
        
        if velocity <= max_velocity:
            # Calculate Reynolds number and pressure drop
            re = reynolds_number(velocity, inner_diameter_m, 
                               props['kinematic_viscosity'])
            
            # Calculate friction factor
            relative_roughness = roughness / inner_diameter_m
            if re < VALIDATION_DATA['reynolds_transition']['critical_re']:
                f = friction_factor_laminar(re)
                flow_regime = 'laminar'
            else:
                f = friction_factor_turbulent(re, relative_roughness)
                flow_regime = 'turbulent'
            
            # Pressure drop per 100m (European standard reporting)
            pressure_drop_per_100m = pressure_drop_pipe(
                f, 100, inner_diameter_m, velocity, props['density']
            )
            
            suitable_sizes.append({
                'dn': dn,
                'inner_diameter_mm': pipe_data['inner_diameter_mm'],
                'outer_diameter_mm': pipe_data['outer_diameter_mm'],
                'wall_thickness_mm': pipe_data['wall_thickness_mm'],
                'velocity_ms': velocity,
                'reynolds_number': re,
                'flow_regime': flow_regime,
                'friction_factor': f,
                'pressure_drop_pa_per_100m': pressure_drop_per_100m,
                'velocity_rating': 'excellent' if velocity <= 1.0 else
                                 'good' if velocity <= 1.5 else
                                 'acceptable' if velocity <= 2.0 else 'high'
            })
    
    # Sort by pressure drop (European efficiency preference)
    suitable_sizes.sort(key=lambda x: x['pressure_drop_pa_per_100m'])
    
    return {
        'flow_rate_m3s': flow_rate_m3s,
        'max_velocity_limit_ms': max_velocity,
        'fluid_properties': props,
        'material_roughness_m': roughness,
        'suitable_pipe_sizes': suitable_sizes,
        'recommended': suitable_sizes[0] if suitable_sizes else None,
        'total_options': len(suitable_sizes)
    }


def pipe_system_analysis(flow_rate_m3s, pipe_length_m, dn_size, 
                        fluid='water', temperature_c=20, material='carbon_steel'):
    """
    Complete analysis of a specific pipe system configuration.
    
    European approach: comprehensive analysis including efficiency metrics.
    
    Args:
        flow_rate_m3s (float): Volume flow rate [m³/s]
        pipe_length_m (float): Total pipe length [m]
        dn_size (int): European DN pipe size
        fluid (str): Fluid type
        temperature_c (float): Operating temperature [°C]
        material (str): Pipe material
    
    Returns:
        dict: Complete pipe system analysis
    """
    if dn_size not in EUROPEAN_PIPE_SIZES:
        raise ValueError(f"DN{dn_size} not available. Available sizes: {list(EUROPEAN_PIPE_SIZES.keys())}")
    
    pipe_data = EUROPEAN_PIPE_SIZES[dn_size]
    inner_diameter_m = pipe_data['inner_diameter_mm'] / 1000
    
    # Get fluid properties
    if fluid == 'water':
        if temperature_c <= 25:
            props = WATER_PROPERTIES['20C']
        elif temperature_c <= 37.5:
            props = WATER_PROPERTIES['30C']
        elif temperature_c <= 52.5:
            props = WATER_PROPERTIES['45C']
        else:
            props = WATER_PROPERTIES['60C']
    else:
        raise ValueError("Only water fluid supported currently")
    
    # Calculate flow parameters
    velocity = pipe_velocity(flow_rate_m3s, inner_diameter_m)
    re = reynolds_number(velocity, inner_diameter_m, props['kinematic_viscosity'])
    
    # Get material properties
    if material in STEEL_PROPERTIES:
        roughness = STEEL_PROPERTIES[material]['roughness']
    else:
        roughness = STEEL_PROPERTIES['carbon_steel']['roughness']
    
    relative_roughness = roughness / inner_diameter_m
    
    # Calculate friction factor and pressure drop
    if re < VALIDATION_DATA['reynolds_transition']['critical_re']:
        f = friction_factor_laminar(re)
        flow_regime = 'laminar'
    else:
        f = friction_factor_turbulent(re, relative_roughness)
        flow_regime = 'turbulent'
    
    total_pressure_drop = pressure_drop_pipe(
        f, pipe_length_m, inner_diameter_m, velocity, props['density']
    )
    
    # European velocity assessment
    velocity_limits = VELOCITY_LIMITS['water_systems']
    if velocity <= velocity_limits['suction_lines']:
        velocity_assessment = 'very_low'
    elif velocity <= velocity_limits['return_lines']:
        velocity_assessment = 'optimal'
    elif velocity <= velocity_limits['supply_lines']:
        velocity_assessment = 'acceptable'
    else:
        velocity_assessment = 'too_high'
    
    # Calculate pump power requirement (if needed)
    pump_analysis = pump_power_required(flow_rate_m3s, total_pressure_drop)
    
    return {
        'pipe_specification': {
            'dn_size': dn_size,
            'inner_diameter_mm': pipe_data['inner_diameter_mm'],
            'outer_diameter_mm': pipe_data['outer_diameter_mm'],
            'wall_thickness_mm': pipe_data['wall_thickness_mm'],
            'material': material,
            'length_m': pipe_length_m
        },
        'flow_conditions': {
            'flow_rate_m3s': flow_rate_m3s,
            'velocity_ms': velocity,
            'reynolds_number': re,
            'flow_regime': flow_regime,
            'velocity_assessment': velocity_assessment
        },
        'pressure_analysis': {
            'friction_factor': f,
            'relative_roughness': relative_roughness,
            'total_pressure_drop_pa': total_pressure_drop,
            'pressure_drop_per_100m_pa': total_pressure_drop * 100 / pipe_length_m,
            'pressure_drop_bar': total_pressure_drop / 1e5  # European pressure unit
        },
        'pump_requirements': pump_analysis,
        'fluid_properties': props,
        'efficiency_rating': 'excellent' if total_pressure_drop < 5000 else
                           'good' if total_pressure_drop < 15000 else
                           'acceptable' if total_pressure_drop < 30000 else 'poor'
    }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def flow_regime_classification(reynolds_number):
    """
    Classify flow regime based on Reynolds number.
    
    Uses standard fluid mechanics classifications with European conservative approach.
    
    Args:
        reynolds_number (float): Reynolds number
    
    Returns:
        str: Flow regime classification
    """
    critical_re = VALIDATION_DATA['reynolds_transition']['critical_re']
    turbulent_re = VALIDATION_DATA['reynolds_transition']['fully_turbulent_re']
    
    if reynolds_number < critical_re:
        return 'laminar'
    elif reynolds_number < turbulent_re:
        return 'transitional'
    else:
        return 'turbulent'


def validate_velocity_limits(velocity, application='supply', fluid='water'):
    """
    Validate velocity against European standards.
    
    Reference: VDI 2056, EN 806
    
    Args:
        velocity (float): Flow velocity [m/s]
        application (str): Application type ('supply', 'return', 'suction', 'drain')
        fluid (str): Fluid type
    
    Returns:
        dict: Validation results with recommendations
    """
    if fluid == 'water':
        limits = VELOCITY_LIMITS['water_systems']
        limit_key = f"{application}_lines"
        
        if limit_key in limits:
            limit = limits[limit_key]
            status = 'acceptable' if velocity <= limit else 'excessive'
            
            return {
                'velocity_ms': velocity,
                'limit_ms': limit,
                'status': status,
                'recommendation': 'within limits' if status == 'acceptable' else 
                                f'reduce velocity to ≤{limit} m/s',
                'standard': 'VDI 2056'
            }
        else:
            return {'error': f"Unknown application type: {application}"}
    else:
        return {'error': f"Velocity limits not defined for fluid: {fluid}"}


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_fluid_mechanics():
    """
    Validate fluid mechanics calculations with known test cases.
    
    Returns:
        list: Validation results
    """
    results = []
    
    # Test 1: Reynolds number calculation
    try:
        re = reynolds_number(2.0, 0.1, temperature_c=20)
        expected = 199203  # Approximate expected value
        error = abs(re - expected) / expected * 100
        results.append({
            'test': 'Reynolds number calculation',
            'calculated': re,
            'expected': expected,
            'error_percent': error,
            'status': 'PASS' if error < 1.0 else 'FAIL'
        })
    except Exception as e:
        results.append({
            'test': 'Reynolds number calculation',
            'status': 'ERROR',
            'error': str(e)
        })
    
    # Test 2: Laminar friction factor
    try:
        f = friction_factor_laminar(2000)
        expected = 0.032  # 64/2000
        error = abs(f - expected) / expected * 100
        results.append({
            'test': 'Laminar friction factor',
            'calculated': f,
            'expected': expected,
            'error_percent': error,
            'status': 'PASS' if error < 0.1 else 'FAIL'
        })
    except Exception as e:
        results.append({
            'test': 'Laminar friction factor',
            'status': 'ERROR',
            'error': str(e)
        })
    
    # Test 3: Pipe velocity calculation
    try:
        v = pipe_velocity(0.001, 0.1)  # 1 L/s through 100mm pipe
        expected = 0.1273  # Q/(π×0.05²)
        error = abs(v - expected) / expected * 100
        results.append({
            'test': 'Pipe velocity calculation',
            'calculated': v,
            'expected': expected,
            'error_percent': error,
            'status': 'PASS' if error < 0.1 else 'FAIL'
        })
    except Exception as e:
        results.append({
            'test': 'Pipe velocity calculation',
            'status': 'ERROR',
            'error': str(e)
        })
    
    return results


if __name__ == "__main__":
    print("Fluid Mechanics Module - European Standards")
    print("=" * 45)
    
    # Run validation tests
    validation_results = validate_fluid_mechanics()
    for result in validation_results:
        print(f"{result['test']}: {result['status']}")
        if 'calculated' in result:
            print(f"  Calculated: {result['calculated']:.6f}")
            print(f"  Expected: {result['expected']:.6f}")
            print(f"  Error: {result.get('error_percent', 0):.3f}%")
    
    print(f"\nAvailable DN pipe sizes: {list(EUROPEAN_PIPE_SIZES.keys())}")
    
    # Example usage
    print("\nExample: DN50 pipe analysis")
    try:
        flow_rate = 0.001  # 1 L/s = 0.001 m³/s
        analysis = pipe_system_analysis(flow_rate, 100, 50)
        print(f"Velocity: {analysis['flow_conditions']['velocity_ms']:.2f} m/s")
        print(f"Reynolds: {analysis['flow_conditions']['reynolds_number']:.0f}")
        print(f"Pressure drop: {analysis['pressure_analysis']['pressure_drop_bar']:.4f} bar")
    except Exception as e:
        print(f"Example error: {e}")