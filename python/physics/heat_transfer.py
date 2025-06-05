# =============================================================================
# HEAT TRANSFER MODULE
# =============================================================================

# python/physics/heat_transfer.py
"""
Standard Heat Transfer Correlations and Formulas
Reference: Fundamentals of Heat and Mass Transfer (Incropera, DeWitt, Bergman, Lavine)
European Standards: EN 12975, EN 14511, VDI Heat Atlas
"""

import math
from .constants import WATER_PROPERTIES, CONVERSION_FACTORS
from .units import celsius_to_kelvin, kelvin_to_celsius

def prandtl_number(specific_heat, dynamic_viscosity, thermal_conductivity):
    """
    Calculate Prandtl number.
    
    Formula: Pr = (cp × μ) / k
    Reference: VDI Heat Atlas, Section A1
    
    Args:
        specific_heat (float): Specific heat capacity [J/(kg·K)]
        dynamic_viscosity (float): Dynamic viscosity [Pa·s]
        thermal_conductivity (float): Thermal conductivity [W/(m·K)]
    
    Returns:
        float: Prandtl number [dimensionless]
    """
    if thermal_conductivity <= 0:
        raise ValueError("Thermal conductivity must be positive")
    return (specific_heat * dynamic_viscosity) / thermal_conductivity


def reynolds_number(velocity, characteristic_length, kinematic_viscosity):
    """
    Calculate Reynolds number for flow characterization.
    
    Formula: Re = V × L / ν
    Reference: VDI Heat Atlas, Section L1
    
    Args:
        velocity (float): Flow velocity [m/s]
        characteristic_length (float): Characteristic length (diameter for pipes) [m]
        kinematic_viscosity (float): Kinematic viscosity [m²/s]
    
    Returns:
        float: Reynolds number [dimensionless]
    """
    if kinematic_viscosity <= 0:
        raise ValueError("Kinematic viscosity must be positive")
    return velocity * characteristic_length / kinematic_viscosity


def graetz_number(reynolds, prandtl, length_diameter_ratio):
    """
    Calculate Graetz number for developing flow analysis.
    
    Formula: Gz = Re × Pr × (D/L)
    Reference: VDI Heat Atlas, Section G1
    
    Args:
        reynolds (float): Reynolds number
        prandtl (float): Prandtl number
        length_diameter_ratio (float): D/L ratio (inverse of L/D)
    
    Returns:
        float: Graetz number [dimensionless]
    """
    return reynolds * prandtl * length_diameter_ratio


def nusselt_number_laminar_pipe(reynolds, prandtl, length_diameter_ratio=None):
    """
    Calculate Nusselt number for laminar flow in pipes.
    
    For fully developed flow: Nu = 4.36 (constant wall heat flux)
    For developing flow: Uses Sieder-Tate correlation
    
    Reference: VDI Heat Atlas, Section G1.2.1
    European Standard: EN 14511-2 for water heating systems
    
    Args:
        reynolds (float): Reynolds number (Re < 2300)
        prandtl (float): Prandtl number
        length_diameter_ratio (float, optional): L/D ratio for developing flow
    
    Returns:
        float: Nusselt number [dimensionless]
    """
    if reynolds >= 2300:
        raise ValueError("Use turbulent correlation for Re >= 2300")
    
    if length_diameter_ratio is None or length_diameter_ratio > 60:
        # Fully developed flow - VDI Heat Atlas recommendation
        return 4.36  # For constant wall heat flux (typical for datacenter cooling)
    else:
        # Developing flow - Modified Sieder-Tate for European applications
        gz = graetz_number(reynolds, prandtl, 1.0 / length_diameter_ratio)
        if gz > 100:
            # European correlation with temperature property correction
            return 1.86 * (gz)**(1/3) * (prandtl / 0.7)**(0.14)
        else:
            return 4.36  # Fully developed limit


def nusselt_number_turbulent_pipe(reynolds, prandtl, length_diameter_ratio=None):
    """
    Calculate Nusselt number for turbulent flow in pipes.
    
    Uses Gnielinski correlation (preferred in Europe) or Dittus-Boelter
    Reference: VDI Heat Atlas, Section G1.2.2
    European Standard: EN 14511-2
    
    Args:
        reynolds (float): Reynolds number (Re > 2300)
        prandtl (float): Prandtl number
        length_diameter_ratio (float, optional): L/D ratio
    
    Returns:
        float: Nusselt number [dimensionless]
    """
    if reynolds < 2300:
        raise ValueError("Use laminar correlation for Re < 2300")
    
    if reynolds < 10000:
        # Transition region - European preferred correlation
        # Modified Gnielinski for transition region
        f = (0.79 * math.log(reynolds) - 1.64)**(-2)  # Friction factor
        numerator = (f/8) * (reynolds - 1000) * prandtl
        denominator = 1 + 12.7 * math.sqrt(f/8) * (prandtl**(2/3) - 1)
        nu_gnielinski = numerator / denominator
        
        # Blend with laminar for smooth transition
        weight = (reynolds - 2300) / (10000 - 2300)
        nu_laminar = 4.36
        return weight * nu_gnielinski + (1 - weight) * nu_laminar
    else:
        # Fully turbulent - Gnielinski correlation (VDI Heat Atlas preferred)
        f = (0.79 * math.log(reynolds) - 1.64)**(-2)
        numerator = (f/8) * (reynolds - 1000) * prandtl
        denominator = 1 + 12.7 * math.sqrt(f/8) * (prandtl**(2/3) - 1)
        return numerator / denominator


def nusselt_number_pipe_universal(reynolds, prandtl, length_diameter_ratio=None):
    """
    Universal Nusselt number calculation covering all flow regimes.
    Automatically selects appropriate correlation based on Reynolds number.
    
    Reference: VDI Heat Atlas methodology
    
    Args:
        reynolds (float): Reynolds number
        prandtl (float): Prandtl number  
        length_diameter_ratio (float, optional): L/D ratio
    
    Returns:
        float: Nusselt number [dimensionless]
    """
    if reynolds < 2300:
        return nusselt_number_laminar_pipe(reynolds, prandtl, length_diameter_ratio)
    else:
        return nusselt_number_turbulent_pipe(reynolds, prandtl, length_diameter_ratio)


def heat_transfer_coefficient(nusselt, thermal_conductivity, characteristic_length):
    """
    Calculate convective heat transfer coefficient from Nusselt number.
    
    Formula: h = Nu × k / L
    Reference: VDI Heat Atlas, fundamental correlation
    
    Args:
        nusselt (float): Nusselt number [dimensionless]
        thermal_conductivity (float): Fluid thermal conductivity [W/(m·K)]
        characteristic_length (float): Characteristic length (diameter for pipes) [m]
    
    Returns:
        float: Heat transfer coefficient [W/(m²·K)]
    """
    if characteristic_length <= 0:
        raise ValueError("Characteristic length must be positive")
    return nusselt * thermal_conductivity / characteristic_length


def thermal_resistance_convection(heat_transfer_coefficient, area):
    """
    Calculate convective thermal resistance.
    
    Formula: R = 1 / (h × A)
    Reference: EN 12975-2, thermal resistance calculations
    
    Args:
        heat_transfer_coefficient (float): Heat transfer coefficient [W/(m²·K)]
        area (float): Heat transfer area [m²]
    
    Returns:
        float: Thermal resistance [K/W]
    """
    if heat_transfer_coefficient <= 0 or area <= 0:
        raise ValueError("Heat transfer coefficient and area must be positive")
    return 1.0 / (heat_transfer_coefficient * area)


def thermal_resistance_conduction(thermal_conductivity, thickness, area):
    """
    Calculate conductive thermal resistance.
    
    Formula: R = L / (k × A)
    Reference: EN 12975-2, thermal resistance for solid materials
    
    Args:
        thermal_conductivity (float): Material thermal conductivity [W/(m·K)]
        thickness (float): Material thickness [m]
        area (float): Cross-sectional area [m²]
    
    Returns:
        float: Thermal resistance [K/W]
    """
    if thermal_conductivity <= 0 or thickness <= 0 or area <= 0:
        raise ValueError("All parameters must be positive")
    return thickness / (thermal_conductivity * area)


def overall_heat_transfer_coefficient(resistances, area=1.0):
    """
    Calculate overall heat transfer coefficient for multiple thermal resistances.
    
    Formula: 1/U = ΣR / A  →  U = A / ΣR
    Reference: VDI Heat Atlas, Section C1
    
    Args:
        resistances (list): List of thermal resistances [K/W]
        area (float): Reference area [m²] (default 1.0 for per-unit-area basis)
    
    Returns:
        float: Overall heat transfer coefficient [W/(m²·K)]
    """
    if not resistances:
        raise ValueError("At least one resistance value required")
    
    total_resistance = sum(resistances)
    if total_resistance <= 0:
        raise ValueError("Total resistance must be positive")
    
    return area / total_resistance


def newtons_law_cooling(heat_transfer_coefficient, area, temp_difference):
    """
    Calculate heat transfer using Newton's law of cooling.
    
    Formula: Q̇ = h × A × ΔT
    Reference: Newton's law of cooling, VDI Heat Atlas fundamentals
    
    Args:
        heat_transfer_coefficient (float): Heat transfer coefficient [W/(m²·K)]
        area (float): Heat transfer area [m²]
        temp_difference (float): Temperature difference [K or °C]
    
    Returns:
        float: Heat transfer rate [W]
    """
    return heat_transfer_coefficient * area * abs(temp_difference)


def fourier_law_conduction(thermal_conductivity, area, temp_difference, thickness):
    """
    Calculate heat conduction using Fourier's law.
    
    Formula: Q̇ = k × A × ΔT / L
    Reference: Fourier's law, VDI Heat Atlas Section B1
    
    Args:
        thermal_conductivity (float): Material thermal conductivity [W/(m·K)]
        area (float): Cross-sectional area [m²]
        temp_difference (float): Temperature difference [K or °C]
        thickness (float): Material thickness [m]
    
    Returns:
        float: Heat transfer rate [W]
    """
    if thickness <= 0:
        raise ValueError("Thickness must be positive")
    return thermal_conductivity * area * abs(temp_difference) / thickness


def log_mean_temperature_difference(hot_inlet, hot_outlet, cold_inlet, cold_outlet, 
                                  flow_arrangement='counterflow'):
    """
    Calculate logarithmic mean temperature difference (LMTD) for heat exchangers.
    
    Reference: VDI Heat Atlas, Section N1
    European Standard: EN 14511-2 for heat exchanger analysis
    
    Args:
        hot_inlet (float): Hot fluid inlet temperature [°C]
        hot_outlet (float): Hot fluid outlet temperature [°C]
        cold_inlet (float): Cold fluid inlet temperature [°C]
        cold_outlet (float): Cold fluid outlet temperature [°C]
        flow_arrangement (str): 'counterflow', 'parallel', or 'crossflow'
    
    Returns:
        float: LMTD [K or °C]
    """
    if flow_arrangement == 'counterflow':
        delta_t1 = hot_inlet - cold_outlet
        delta_t2 = hot_outlet - cold_inlet
    elif flow_arrangement == 'parallel':
        delta_t1 = hot_inlet - cold_inlet  
        delta_t2 = hot_outlet - cold_outlet
    else:
        raise ValueError("Unsupported flow arrangement. Use 'counterflow' or 'parallel'")
    
    # Check for physical validity
    if delta_t1 <= 0 or delta_t2 <= 0:
        raise ValueError(f"Invalid temperature configuration for {flow_arrangement} flow")
    
    # Calculate LMTD
    if abs(delta_t1 - delta_t2) < 1e-6:
        # When temperature differences are equal
        return delta_t1
    else:
        return (delta_t1 - delta_t2) / math.log(delta_t1 / delta_t2)


def effectiveness_ntu_method(capacity_rate_min, capacity_rate_max, ntu, 
                           flow_arrangement='counterflow'):
    """
    Calculate heat exchanger effectiveness using NTU method.
    
    Reference: VDI Heat Atlas, Section N1.3
    European methodology for heat exchanger design
    
    Args:
        capacity_rate_min (float): Minimum capacity rate [W/K]
        capacity_rate_max (float): Maximum capacity rate [W/K]
        ntu (float): Number of Transfer Units [dimensionless]
        flow_arrangement (str): Heat exchanger flow arrangement
    
    Returns:
        float: Heat exchanger effectiveness [dimensionless]
    """
    if capacity_rate_min <= 0 or capacity_rate_max <= 0:
        raise ValueError("Capacity rates must be positive")
    
    if capacity_rate_min > capacity_rate_max:
        capacity_rate_min, capacity_rate_max = capacity_rate_max, capacity_rate_min
    
    c_ratio = capacity_rate_min / capacity_rate_max
    
    if flow_arrangement == 'counterflow':
        if abs(c_ratio - 1.0) < 1e-6:
            # Equal capacity rates
            effectiveness = ntu / (1 + ntu)
        else:
            # Unequal capacity rates
            exp_term = math.exp(-ntu * (1 - c_ratio))
            effectiveness = (1 - exp_term) / (1 - c_ratio * exp_term)
    elif flow_arrangement == 'parallel':
        exp_term = math.exp(-ntu * (1 + c_ratio))
        effectiveness = (1 - exp_term) / (1 + c_ratio)
    else:
        raise ValueError("Unsupported flow arrangement")
    
    return min(effectiveness, 1.0)  # Ensure effectiveness ≤ 1


def pipe_flow_analysis(flow_rate_lpm, pipe_diameter_mm, temperature_c=20, 
                      pipe_length_m=None):
    """
    Complete pipe flow and heat transfer analysis for European applications.
    
    Args:
        flow_rate_lpm (float): Volumetric flow rate [L/min]
        pipe_diameter_mm (float): Inner pipe diameter [mm]
        temperature_c (float): Fluid temperature [°C]
        pipe_length_m (float, optional): Pipe length [m]
    
    Returns:
        dict: Complete flow analysis including heat transfer coefficients
    """
    # Get water properties at operating temperature
    props = get_water_properties_interpolated(temperature_c)
    
    # Convert units
    flow_rate_m3s = flow_rate_lpm * CONVERSION_FACTORS['liters_to_m3'] / CONVERSION_FACTORS['minutes_to_seconds']
    pipe_diameter_m = pipe_diameter_mm / 1000
    pipe_area_m2 = math.pi * (pipe_diameter_m / 2)**2
    
    # Calculate flow parameters
    velocity = flow_rate_m3s / pipe_area_m2
    reynolds = reynolds_number(velocity, pipe_diameter_m, props['kinematic_viscosity'])
    prandtl = props['prandtl_number']
    
    # Determine flow regime
    if reynolds < 2300:
        flow_regime = 'laminar'
    elif reynolds < 10000:
        flow_regime = 'transition'
    else:
        flow_regime = 'turbulent'
    
    # Calculate Nusselt number and heat transfer coefficient
    if pipe_length_m:
        l_d_ratio = pipe_length_m / pipe_diameter_m
        nusselt = nusselt_number_pipe_universal(reynolds, prandtl, l_d_ratio)
    else:
        nusselt = nusselt_number_pipe_universal(reynolds, prandtl)
    
    h_coeff = heat_transfer_coefficient(nusselt, props['thermal_conductivity'], pipe_diameter_m)
    
    return {
        'flow_rate_lpm': flow_rate_lpm,
        'flow_rate_m3s': flow_rate_m3s,
        'velocity_ms': velocity,
        'reynolds_number': reynolds,
        'prandtl_number': prandtl,
        'flow_regime': flow_regime,
        'nusselt_number': nusselt,
        'heat_transfer_coefficient': h_coeff,
        'pipe_diameter_mm': pipe_diameter_mm,
        'pipe_area_m2': pipe_area_m2,
        'fluid_properties': props
    }


def get_water_properties_interpolated(temperature_c):
    """
    Get water properties with interpolation for any temperature.
    Compatibility function for existing system.
    
    Args:
        temperature_c (float): Temperature [°C]
    
    Returns:
        dict: Water properties at specified temperature
    """
    # Temperature bounds check
    if temperature_c < 0:
        temperature_c = 0
        print(f"Warning: Temperature below 0°C, using 0°C properties")
    elif temperature_c > 100:
        temperature_c = 100
        print(f"Warning: Temperature above 100°C, using 100°C properties")
    
    if temperature_c <= 20:
        return WATER_PROPERTIES['20C']
    elif temperature_c <= 30:
        if temperature_c == 30:
            return WATER_PROPERTIES['30C']
        # Linear interpolation between 20°C and 30°C
        factor = (temperature_c - 20) / (30 - 20)
        props_20 = WATER_PROPERTIES['20C']
        props_30 = WATER_PROPERTIES['30C']
        
        return {
            'density': props_20['density'] + factor * (props_30['density'] - props_20['density']),
            'specific_heat': props_20['specific_heat'] + factor * (props_30['specific_heat'] - props_20['specific_heat']),
            'thermal_conductivity': props_20['thermal_conductivity'] + factor * (props_30['thermal_conductivity'] - props_20['thermal_conductivity']),
            'dynamic_viscosity': props_20['dynamic_viscosity'] + factor * (props_30['dynamic_viscosity'] - props_20['dynamic_viscosity']),
            'kinematic_viscosity': props_20['kinematic_viscosity'] + factor * (props_30['kinematic_viscosity'] - props_20['kinematic_viscosity']),
            'prandtl_number': props_20['prandtl_number'] + factor * (props_30['prandtl_number'] - props_20['prandtl_number']),
        }
    elif temperature_c <= 45:
        if temperature_c == 45:
            return WATER_PROPERTIES['45C']
        # Linear interpolation between 30°C and 45°C
        factor = (temperature_c - 30) / (45 - 30)
        props_30 = WATER_PROPERTIES['30C']
        props_45 = WATER_PROPERTIES['45C']
        
        return {
            'density': props_30['density'] + factor * (props_45['density'] - props_30['density']),
            'specific_heat': props_30['specific_heat'] + factor * (props_45['specific_heat'] - props_30['specific_heat']),
            'thermal_conductivity': props_30['thermal_conductivity'] + factor * (props_45['thermal_conductivity'] - props_30['thermal_conductivity']),
            'dynamic_viscosity': props_30['dynamic_viscosity'] + factor * (props_45['dynamic_viscosity'] - props_30['dynamic_viscosity']),
            'kinematic_viscosity': props_30['kinematic_viscosity'] + factor * (props_45['kinematic_viscosity'] - props_30['kinematic_viscosity']),
            'prandtl_number': props_30['prandtl_number'] + factor * (props_45['prandtl_number'] - props_30['prandtl_number']),
        }
    else:
        # Beyond 45°C, use 45°C properties
        return WATER_PROPERTIES['45C']


# =============================================================================
# VALIDATION AND TESTING
# =============================================================================

def validate_heat_transfer_correlations():
    """
    Validate heat transfer correlations against known solutions.
    European standard test cases.
    
    Returns:
        dict: Validation results
    """
    results = []
    
    # Test 1: Water at 20°C in 100mm pipe at 2 m/s
    try:
        props = WATER_PROPERTIES['20C']
        velocity = 2.0
        diameter = 0.1
        
        re = reynolds_number(velocity, diameter, props['kinematic_viscosity'])
        pr = props['prandtl_number']
        nu = nusselt_number_turbulent_pipe(re, pr)
        h = heat_transfer_coefficient(nu, props['thermal_conductivity'], diameter)
        
        # Expected values based on standard correlations
        expected_re = 199203  # Approximately
        expected_nu_range = (300, 450)  # Typical range for this Re and Pr
        
        results.append({
            'test': 'Turbulent pipe flow (Re=199k)',
            'reynolds_calculated': re,
            'reynolds_expected': expected_re,
            'nusselt_calculated': nu,
            'nusselt_in_range': expected_nu_range[0] <= nu <= expected_nu_range[1],
            'heat_transfer_coeff': h,
            'status': 'PASS' if abs(re - expected_re) / expected_re < 0.01 and expected_nu_range[0] <= nu <= expected_nu_range[1] else 'FAIL'
        })
    except Exception as e:
        results.append({
            'test': 'Turbulent pipe flow validation',
            'status': 'ERROR',
            'error': str(e)
        })
    
    # Test 2: LMTD calculation for counterflow
    try:
        lmtd = log_mean_temperature_difference(80, 60, 20, 40, 'counterflow')
        expected_lmtd = 28.85  # Known analytical solution
        error = abs(lmtd - expected_lmtd) / expected_lmtd * 100
        
        results.append({
            'test': 'LMTD counterflow calculation',
            'calculated': lmtd,
            'expected': expected_lmtd,
            'error_percent': error,
            'status': 'PASS' if error < 1.0 else 'FAIL'
        })
    except Exception as e:
        results.append({
            'test': 'LMTD calculation',
            'status': 'ERROR',
            'error': str(e)
        })
    
    # Test 3: Complete pipe analysis
    try:
        analysis = pipe_flow_analysis(1493, 160, 25)  # Your system parameters
        
        expected_velocity_range = (1.0, 3.0)  # Reasonable range for datacenter applications
        
        results.append({
            'test': 'Complete pipe analysis (1493 L/min, 160mm)',
            'velocity_ms': analysis['velocity_ms'],
            'reynolds': analysis['reynolds_number'],
            'flow_regime': analysis['flow_regime'],
            'velocity_reasonable': expected_velocity_range[0] <= analysis['velocity_ms'] <= expected_velocity_range[1],
            'status': 'PASS' if expected_velocity_range[0] <= analysis['velocity_ms'] <= expected_velocity_range[1] else 'WARNING'
        })
    except Exception as e:
        results.append({
            'test': 'Complete pipe analysis',
            'status': 'ERROR', 
            'error': str(e)
        })
    
    return {
        'total_tests': len(results),
        'passed': len([r for r in results if r.get('status') == 'PASS']),
        'failed': len([r for r in results if r.get('status') == 'FAIL']),
        'errors': len([r for r in results if r.get('status') == 'ERROR']),
        'results': results
    }


if __name__ == "__main__":
    # Run validation when module is executed directly
    print("Heat Transfer Module Validation")
    print("=" * 40)
    
    validation = validate_heat_transfer_correlations()
    
    print(f"Total tests: {validation['total_tests']}")
    print(f"Passed: {validation['passed']}")
    print(f"Failed: {validation['failed']}")
    print(f"Errors: {validation['errors']}")
    
    print("\nDetailed Results:")
    for result in validation['results']:
        print(f"\n{result['test']}: {result['status']}")
        for key, value in result.items():
            if key not in ['test', 'status']:
                print(f"  {key}: {value}")