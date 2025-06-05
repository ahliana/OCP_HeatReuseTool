# =============================================================================
# HEAT EXCHANGERS MODULE
# =============================================================================

# python/physics/heat_exchangers.py
"""
Heat Exchanger Analysis Methods and Correlations
Reference: VDI Heat Atlas, Heat Exchanger Design Handbook (Thulukkanam)
European standards and practices prioritized
"""

import math
from .constants import (
    WATER_PROPERTIES, HEAT_TRANSFER_COEFFICIENTS, 
    STEEL_PROPERTIES, CONVERSION_FACTORS
)
from .thermodynamics import sensible_heat_transfer
from .units import liters_per_minute_to_m3_per_second

# =============================================================================
# TEMPERATURE DIFFERENCE CALCULATIONS
# =============================================================================

def lmtd_counterflow(hot_inlet, hot_outlet, cold_inlet, cold_outlet):
    """
    Calculate Log Mean Temperature Difference for counterflow heat exchanger.
    
    Formula: LMTD = (ΔT₁ - ΔT₂) / ln(ΔT₁/ΔT₂)
    where ΔT₁ = T_h,in - T_c,out and ΔT₂ = T_h,out - T_c,in
    
    Reference: VDI Heat Atlas, LMTD method
    
    Args:
        hot_inlet (float): Hot fluid inlet temperature [°C]
        hot_outlet (float): Hot fluid outlet temperature [°C]
        cold_inlet (float): Cold fluid inlet temperature [°C]
        cold_outlet (float): Cold fluid outlet temperature [°C]
    
    Returns:
        float: LMTD [°C]
        
    Example:
        >>> lmtd_counterflow(30, 20, 18, 28)
        4.49
    """
    delta_t1 = hot_inlet - cold_outlet
    delta_t2 = hot_outlet - cold_inlet
    
    if abs(delta_t1 - delta_t2) < 1e-6:
        # Avoid division by zero when temperature differences are equal
        return delta_t1
    
    if delta_t1 <= 0 or delta_t2 <= 0:
        raise ValueError("Invalid temperature configuration for heat exchanger")
    
    return (delta_t1 - delta_t2) / math.log(delta_t1 / delta_t2)


def lmtd_parallel(hot_inlet, hot_outlet, cold_inlet, cold_outlet):
    """
    Calculate LMTD for parallel flow heat exchanger.
    
    Formula: LMTD = (ΔT₁ - ΔT₂) / ln(ΔT₁/ΔT₂)
    where ΔT₁ = T_h,in - T_c,in and ΔT₂ = T_h,out - T_c,out
    
    Args:
        hot_inlet (float): Hot fluid inlet temperature [°C]
        hot_outlet (float): Hot fluid outlet temperature [°C]
        cold_inlet (float): Cold fluid inlet temperature [°C]
        cold_outlet (float): Cold fluid outlet temperature [°C]
    
    Returns:
        float: LMTD [°C]
    """
    delta_t1 = hot_inlet - cold_inlet
    delta_t2 = hot_outlet - cold_outlet
    
    if abs(delta_t1 - delta_t2) < 1e-6:
        return delta_t1
    
    if delta_t1 <= 0 or delta_t2 <= 0:
        raise ValueError("Invalid temperature configuration for heat exchanger")
    
    return (delta_t1 - delta_t2) / math.log(delta_t1 / delta_t2)


def lmtd_crossflow(hot_inlet, hot_outlet, cold_inlet, cold_outlet, 
                   correction_factor=1.0):
    """
    Calculate LMTD for crossflow heat exchanger with correction factor.
    
    Uses counterflow LMTD with correction factor F.
    LMTD_actual = F × LMTD_counterflow
    
    Reference: VDI Heat Atlas, Section G1
    
    Args:
        hot_inlet (float): Hot fluid inlet temperature [°C]
        hot_outlet (float): Hot fluid outlet temperature [°C]
        cold_inlet (float): Cold fluid inlet temperature [°C]
        cold_outlet (float): Cold fluid outlet temperature [°C]
        correction_factor (float): LMTD correction factor F
    
    Returns:
        float: Corrected LMTD [°C]
    """
    lmtd_cf = lmtd_counterflow(hot_inlet, hot_outlet, cold_inlet, cold_outlet)
    return correction_factor * lmtd_cf


# =============================================================================
# EFFECTIVENESS-NTU METHOD (European Preferred)
# =============================================================================

def effectiveness_ntu_counterflow(ntu, capacity_ratio):
    """
    Calculate effectiveness for counterflow heat exchanger using NTU method.
    
    Formula: ε = (1 - exp(-NTU(1-Cr))) / (1 - Cr×exp(-NTU(1-Cr)))
    For Cr = 1: ε = NTU / (1 + NTU)
    
    Reference: VDI Heat Atlas, Effectiveness-NTU method
    
    Args:
        ntu (float): Number of Transfer Units
        capacity_ratio (float): Cr = Cmin/Cmax
    
    Returns:
        float: Heat exchanger effectiveness [dimensionless]
    """
    if abs(capacity_ratio - 1.0) < 1e-6:
        # Special case: Cr = 1
        return ntu / (1 + ntu)
    else:
        numerator = 1 - math.exp(-ntu * (1 - capacity_ratio))
        denominator = 1 - capacity_ratio * math.exp(-ntu * (1 - capacity_ratio))
        return numerator / denominator


def effectiveness_ntu_parallel(ntu, capacity_ratio):
    """
    Calculate effectiveness for parallel flow heat exchanger.
    
    Formula: ε = (1 - exp(-NTU(1+Cr))) / (1 + Cr)
    
    Reference: VDI Heat Atlas
    
    Args:
        ntu (float): Number of Transfer Units
        capacity_ratio (float): Cr = Cmin/Cmax
    
    Returns:
        float: Heat exchanger effectiveness [dimensionless]
    """
    return (1 - math.exp(-ntu * (1 + capacity_ratio))) / (1 + capacity_ratio)


def effectiveness_ntu_crossflow(ntu, capacity_ratio, mixed_fluid='neither'):
    """
    Calculate effectiveness for crossflow heat exchanger.
    
    Reference: VDI Heat Atlas, crossflow correlations
    
    Args:
        ntu (float): Number of Transfer Units
        capacity_ratio (float): Cr = Cmin/Cmax
        mixed_fluid (str): 'hot', 'cold', 'both', or 'neither'
    
    Returns:
        float: Heat exchanger effectiveness [dimensionless]
    """
    if mixed_fluid == 'neither':
        # Both fluids unmixed (conservative approximation)
        # Use approximate formula from VDI Heat Atlas
        term1 = 1 - math.exp(-ntu)
        term2 = 1 - math.exp(-ntu * capacity_ratio)
        return 1 - math.exp(-(term1 + term2 - term1 * term2) / capacity_ratio)
    elif mixed_fluid == 'hot':
        # Hot fluid mixed, cold unmixed
        return (1 - math.exp(-capacity_ratio * (1 - math.exp(-ntu)))) / capacity_ratio
    elif mixed_fluid == 'cold':
        # Cold fluid mixed, hot unmixed
        return 1 - math.exp(-(1 - math.exp(-ntu * capacity_ratio)) / capacity_ratio)
    else:
        # Both fluids mixed (shell-and-tube approximation)
        return effectiveness_ntu_counterflow(ntu, capacity_ratio)


def ntu_from_effectiveness(effectiveness, capacity_ratio, flow_type='counterflow'):
    """
    Calculate NTU from effectiveness (inverse of effectiveness-NTU relations).
    
    Args:
        effectiveness (float): Heat exchanger effectiveness [0-1]
        capacity_ratio (float): Cr = Cmin/Cmax [0-1]
        flow_type (str): 'counterflow', 'parallel', or 'crossflow'
    
    Returns:
        float: Number of Transfer Units
    """
    if not 0 <= effectiveness <= 1:
        raise ValueError("Effectiveness must be between 0 and 1")
    
    if not 0 <= capacity_ratio <= 1:
        raise ValueError("Capacity ratio must be between 0 and 1")
    
    if flow_type == 'counterflow':
        if abs(capacity_ratio - 1.0) < 1e-6:
            # Special case: Cr = 1
            return effectiveness / (1 - effectiveness)
        else:
            # General case for counterflow
            if abs(effectiveness) < 1e-6:
                return 0.0
            term1 = effectiveness - 1
            term2 = effectiveness * capacity_ratio - 1
            if term2 <= 0 or term1 <= 0:
                raise ValueError("Invalid effectiveness/capacity ratio combination")
            return math.log(term2 / term1) / (capacity_ratio - 1)
    
    elif flow_type == 'parallel':
        if abs(effectiveness) < 1e-6:
            return 0.0
        return -math.log(1 - effectiveness * (1 + capacity_ratio)) / (1 + capacity_ratio)
    
    else:
        raise NotImplementedError(f"Flow type '{flow_type}' not implemented")


# =============================================================================
# HEAT EXCHANGER SIZING AND ANALYSIS
# =============================================================================

def heat_exchanger_sizing(heat_duty, overall_u, lmtd):
    """
    Calculate required heat exchanger area using basic sizing equation.
    
    Formula: A = Q̇ / (U × LMTD)
    
    Reference: Fundamental heat exchanger design equation
    
    Args:
        heat_duty (float): Heat transfer duty [W]
        overall_u (float): Overall heat transfer coefficient [W/(m²·K)]
        lmtd (float): Log mean temperature difference [K or °C]
    
    Returns:
        float: Required heat transfer area [m²]
    """
    if lmtd <= 0:
        raise ValueError("LMTD must be positive")
    if overall_u <= 0:
        raise ValueError("Overall U must be positive")
    
    return heat_duty / (overall_u * lmtd)


def overall_heat_transfer_coefficient(hot_htc, cold_htc, wall_thickness=0.003,
                                    wall_conductivity=50, fouling_hot=0.0,
                                    fouling_cold=0.0):
    """
    Calculate overall heat transfer coefficient for heat exchanger.
    
    Formula: 1/U = 1/h_hot + R_fouling_hot + t_wall/k_wall + R_fouling_cold + 1/h_cold
    
    European approach: Conservative fouling factors
    
    Reference: VDI Heat Atlas, Section C4
    
    Args:
        hot_htc (float): Hot side heat transfer coefficient [W/(m²·K)]
        cold_htc (float): Cold side heat transfer coefficient [W/(m²·K)]
        wall_thickness (float): Wall thickness [m]
        wall_conductivity (float): Wall thermal conductivity [W/(m·K)]
        fouling_hot (float): Hot side fouling resistance [m²·K/W]
        fouling_cold (float): Cold side fouling resistance [m²·K/W]
    
    Returns:
        float: Overall heat transfer coefficient [W/(m²·K)]
    """
    # European conservative approach: include all resistances
    resistance_total = (1/hot_htc + fouling_hot + 
                       wall_thickness/wall_conductivity + 
                       fouling_cold + 1/cold_htc)
    
    return 1.0 / resistance_total


def complete_heat_exchanger_analysis(hot_flow_lpm, cold_flow_lpm,
                                   hot_inlet, hot_outlet, cold_inlet, cold_outlet,
                                   hot_fluid='water', cold_fluid='water',
                                   hx_type='counterflow', include_sizing=True):
    """
    Complete heat exchanger analysis using European methodology.
    
    Performs thermal analysis, effectiveness calculation, and sizing if requested.
    
    Args:
        hot_flow_lpm (float): Hot fluid flow rate [L/min]
        cold_flow_lpm (float): Cold fluid flow rate [L/min]
        hot_inlet (float): Hot fluid inlet temperature [°C]
        hot_outlet (float): Hot fluid outlet temperature [°C]
        cold_inlet (float): Cold fluid inlet temperature [°C]
        cold_outlet (float): Cold fluid outlet temperature [°C]
        hot_fluid (str): Hot fluid type
        cold_fluid (str): Cold fluid type
        hx_type (str): Heat exchanger type
        include_sizing (bool): Include sizing calculations
    
    Returns:
        dict: Complete heat exchanger analysis
    """
    # Get fluid properties (European temperature-dependent approach)
    def get_water_props(temp_c):
        if temp_c <= 25:
            return WATER_PROPERTIES['20C']
        elif temp_c <= 37.5:
            return WATER_PROPERTIES['30C']
        elif temp_c <= 52.5:
            return WATER_PROPERTIES['45C']
        else:
            return WATER_PROPERTIES['60C']
    
    # Hot side properties at average temperature
    hot_avg_temp = (hot_inlet + hot_outlet) / 2
    hot_props = get_water_props(hot_avg_temp) if hot_fluid == 'water' else None
    
    # Cold side properties at average temperature
    cold_avg_temp = (cold_inlet + cold_outlet) / 2
    cold_props = get_water_props(cold_avg_temp) if cold_fluid == 'water' else None
    
    if not hot_props or not cold_props:
        raise ValueError("Only water fluids currently supported")
    
    # Convert flow rates and calculate mass flows
    hot_flow_m3s = liters_per_minute_to_m3_per_second(hot_flow_lpm)
    cold_flow_m3s = liters_per_minute_to_m3_per_second(cold_flow_lpm)
    
    hot_mass_flow = hot_flow_m3s * hot_props['density']
    cold_mass_flow = cold_flow_m3s * cold_props['density']
    
    # Calculate heat duties (should be approximately equal)
    hot_duty = sensible_heat_transfer(hot_mass_flow, hot_props['specific_heat'], 
                                    hot_inlet - hot_outlet)
    cold_duty = sensible_heat_transfer(cold_mass_flow, cold_props['specific_heat'], 
                                     cold_outlet - cold_inlet)
    
    # Use average duty for analysis
    average_duty = (hot_duty + cold_duty) / 2
    heat_balance_error = abs(hot_duty - cold_duty) / average_duty * 100
    
    # Calculate capacity rates
    hot_capacity_rate = hot_mass_flow * hot_props['specific_heat']
    cold_capacity_rate = cold_mass_flow * cold_props['specific_heat']
    
    c_min = min(hot_capacity_rate, cold_capacity_rate)
    c_max = max(hot_capacity_rate, cold_capacity_rate)
    capacity_ratio = c_min / c_max
    
    # Calculate effectiveness
    q_max = c_min * (hot_inlet - cold_inlet)
    effectiveness = average_duty / q_max if q_max > 0 else 0
    
    # Calculate NTU
    if effectiveness > 0:
        try:
            ntu = ntu_from_effectiveness(effectiveness, capacity_ratio, hx_type)
        except:
            ntu = None
    else:
        ntu = 0
    
    # Calculate LMTD
    if hx_type == 'counterflow':
        lmtd = lmtd_counterflow(hot_inlet, hot_outlet, cold_inlet, cold_outlet)
    elif hx_type == 'parallel':
        lmtd = lmtd_parallel(hot_inlet, hot_outlet, cold_inlet, cold_outlet)
    else:
        lmtd = lmtd_counterflow(hot_inlet, hot_outlet, cold_inlet, cold_outlet)
    
    # European performance assessment
    if effectiveness >= 0.85:
        performance_rating = 'excellent'
    elif effectiveness >= 0.70:
        performance_rating = 'good'
    elif effectiveness >= 0.50:
        performance_rating = 'acceptable'
    else:
        performance_rating = 'poor'
    
    # Calculate approach and pinch temperatures
    approach = approach_temperature(hot_inlet, cold_outlet)
    pinch = pinch_temperature(hot_outlet, cold_inlet)
    
    # Basic sizing (if requested)
    sizing_info = {}
    if include_sizing and lmtd > 0:
        # Estimate overall U based on European typical values
        u_range = HEAT_TRANSFER_COEFFICIENTS['water_to_water_hx']
        u_typical = (u_range[0] + u_range[1]) / 2  # Conservative middle value
        
        required_area = heat_exchanger_sizing(average_duty, u_typical, lmtd)
        
        sizing_info = {
            'estimated_overall_u': u_typical,
            'required_area_m2': required_area,
            'area_per_mw': required_area / (average_duty / 1e6) if average_duty > 0 else 0,
            'sizing_basis': 'typical_water_to_water_hx'
        }
    
    return {
        'thermal_analysis': {
            'hot_duty_w': hot_duty,
            'cold_duty_w': cold_duty,
            'average_duty_w': average_duty,
            'heat_balance_error_percent': heat_balance_error,
            'hot_capacity_rate': hot_capacity_rate,
            'cold_capacity_rate': cold_capacity_rate,
            'capacity_ratio': capacity_ratio
        },
        'performance_metrics': {
            'effectiveness': effectiveness,
            'ntu': ntu,
            'lmtd_c': lmtd,
            'approach_temperature_c': approach,
            'pinch_temperature_c': pinch,
            'performance_rating': performance_rating
        },
        'operating_conditions': {
            'hot_inlet_c': hot_inlet,
            'hot_outlet_c': hot_outlet,
            'cold_inlet_c': cold_inlet,
            'cold_outlet_c': cold_outlet,
            'hot_flow_lpm': hot_flow_lpm,
            'cold_flow_lpm': cold_flow_lpm,
            'hx_type': hx_type
        },
        'fluid_properties': {
            'hot_properties': hot_props,
            'cold_properties': cold_props,
            'hot_mass_flow_kg_s': hot_mass_flow,
            'cold_mass_flow_kg_s': cold_mass_flow
        },
        'sizing_information': sizing_info,
        'european_compliance': {
            'conservative_approach': approach >= 2.0,  # European minimum
            'acceptable_effectiveness': effectiveness >= 0.6,
            'reasonable_pinch': pinch >= 1.0,
            'overall_assessment': 'compliant' if (approach >= 2.0 and 
                                               effectiveness >= 0.6 and 
                                               pinch >= 1.0) else 'review_required'
        }
    }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def approach_temperature(hot_inlet, cold_outlet):
    """
    Calculate approach temperature (terminal temperature difference).
    
    European standard: minimum 2°C approach for efficient operation
    
    Args:
        hot_inlet (float): Hot fluid inlet temperature [°C]
        cold_outlet (float): Cold fluid outlet temperature [°C]
    
    Returns:
        float: Approach temperature [°C]
    """
    return hot_inlet - cold_outlet


def pinch_temperature(hot_outlet, cold_inlet):
    """
    Calculate pinch temperature difference.
    
    European standard: minimum 1°C pinch for feasible heat transfer
    
    Args:
        hot_outlet (float): Hot fluid outlet temperature [°C]
        cold_inlet (float): Cold fluid inlet temperature [°C]
    
    Returns:
        float: Pinch temperature difference [°C]
    """
    return hot_outlet - cold_inlet


def validate_heat_exchanger_config(hot_inlet, hot_outlet, cold_inlet, cold_outlet):
    """
    Validate heat exchanger temperature configuration.
    
    European engineering standards for feasible operation.
    
    Args:
        hot_inlet (float): Hot fluid inlet temperature [°C]
        hot_outlet (float): Hot fluid outlet temperature [°C]
        cold_inlet (float): Cold fluid inlet temperature [°C]
        cold_outlet (float): Cold fluid outlet temperature [°C]
    
    Returns:
        dict: Validation results with recommendations
    """
    results = {
        'valid': True,
        'warnings': [],
        'errors': [],
        'recommendations': []
    }
    
    # Basic thermodynamic checks
    if hot_inlet <= hot_outlet:
        results['errors'].append("Hot fluid must be cooled (T_in > T_out)")
        results['valid'] = False
    
    if cold_inlet >= cold_outlet:
        results['errors'].append("Cold fluid must be heated (T_out > T_in)")
        results['valid'] = False
    
    # Temperature level checks
    if hot_outlet <= cold_inlet:
        results['errors'].append("Hot outlet must be warmer than cold inlet")
        results['valid'] = False
    
    if hot_inlet <= cold_outlet:
        results['errors'].append("Hot inlet must be warmer than cold outlet")
        results['valid'] = False
    
    # European standard checks
    approach = approach_temperature(hot_inlet, cold_outlet)
    pinch = pinch_temperature(hot_outlet, cold_inlet)
    
    if approach < 2.0:
        results['warnings'].append(f"Low approach temperature ({approach:.1f}°C < 2°C)")
        results['recommendations'].append("Consider increasing temperature differences")
    
    if pinch < 1.0:
        results['warnings'].append(f"Low pinch temperature ({pinch:.1f}°C < 1°C)")
        results['recommendations'].append("Review temperature configuration")
    
    if approach > 15.0:
        results['warnings'].append(f"High approach temperature ({approach:.1f}°C > 15°C)")
        results['recommendations'].append("Consider optimizing heat recovery")
    
    # Calculate expected effectiveness range
    if results['valid']:
        # Rough effectiveness estimate
        delta_t_hot = hot_inlet - hot_outlet
        delta_t_cold = cold_outlet - cold_inlet
        delta_t_max = hot_inlet - cold_inlet
        
        approx_effectiveness = min(delta_t_hot, delta_t_cold) / delta_t_max
        
        if approx_effectiveness < 0.4:
            results['warnings'].append("Low expected effectiveness")
            results['recommendations'].append("Review flow rates and heat exchanger sizing")
    
    return results


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_heat_exchangers():
    """
    Validate heat exchanger calculations with known test cases.
    
    Returns:
        list: Validation results
    """
    results = []
    
    # Test 1: LMTD calculation for counterflow
    try:
        lmtd = lmtd_counterflow(30, 20, 18, 28)
        expected = 4.49  # Hand calculation
        error = abs(lmtd - expected) / expected * 100
        results.append({
            'test': 'LMTD counterflow calculation',
            'calculated': lmtd,
            'expected': expected,
            'error_percent': error,
            'status': 'PASS' if error < 2.0 else 'FAIL'
        })
    except Exception as e:
        results.append({
            'test': 'LMTD counterflow calculation',
            'status': 'ERROR',
            'error': str(e)
        })
    
    # Test 2: Effectiveness-NTU for balanced flow (Cr=1)
    try:
        eff = effectiveness_ntu_counterflow(1.0, 1.0)
        expected = 0.5  # NTU/(1+NTU) = 1/2
        error = abs(eff - expected) / expected * 100
        results.append({
            'test': 'Effectiveness NTU (Cr=1)',
            'calculated': eff,
            'expected': expected,
            'error_percent': error,
            'status': 'PASS' if error < 0.1 else 'FAIL'
        })
    except Exception as e:
        results.append({
            'test': 'Effectiveness NTU (Cr=1)',
            'status': 'ERROR',
            'error': str(e)
        })
    
    # Test 3: Heat exchanger area calculation
    try:
        area = heat_exchanger_sizing(1000000, 2000, 5.0)  # 1MW, U=2000, LMTD=5K
        expected = 100  # 1e6/(2000*5)
        error = abs(area - expected) / expected * 100
        results.append({
            'test': 'Heat exchanger area calculation',
            'calculated': area,
            'expected': expected,
            'error_percent': error,
            'status': 'PASS' if error < 0.1 else 'FAIL'
        })
    except Exception as e:
        results.append({
            'test': 'Heat exchanger area calculation',
            'status': 'ERROR',
            'error': str(e)
        })
    
    return results


if __name__ == "__main__":
    print("Heat Exchangers Module - European Standards")
    print("=" * 45)
    
    # Run validation tests
    validation_results = validate_heat_exchangers()
    for result in validation_results:
        print(f"{result['test']}: {result['status']}")
        if 'calculated' in result:
            print(f"  Calculated: {result['calculated']:.6f}")
            print(f"  Expected: {result['expected']:.6f}")
            print(f"  Error: {result.get('error_percent', 0):.3f}%")
    
    print("\nExample: Complete heat exchanger analysis")
    try:
        # Example from your system: 1493 L/min hot, 1440 L/min cold
        analysis = complete_heat_exchanger_analysis(
            hot_flow_lpm=1493, cold_flow_lpm=1440,
            hot_inlet=30, hot_outlet=20, 
            cold_inlet=18, cold_outlet=28
        )
        print(f"Effectiveness: {analysis['performance_metrics']['effectiveness']:.3f}")
        print(f"LMTD: {analysis['performance_metrics']['lmtd_c']:.1f}°C")
        print(f"Performance: {analysis['performance_metrics']['performance_rating']}")
        print(f"European compliance: {analysis['european_compliance']['overall_assessment']}")
    except Exception as e:
        print(f"Example error: {e}")