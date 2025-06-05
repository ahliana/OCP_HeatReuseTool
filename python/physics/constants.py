# =============================================================================
# CONSTANTS MODULE
# =============================================================================

# python/physics/constants.py
"""
Standard Physics Constants and Properties
All values from NIST, ASHRAE, and engineering handbooks
European/Metric standards prioritized throughout
"""

import math

# =============================================================================
# UNIVERSAL PHYSICAL CONSTANTS (NIST 2018/CODATA 2018)
# =============================================================================

STEFAN_BOLTZMANN = 5.670374419e-8    # W/(m²·K⁴) - Stefan-Boltzmann constant
GAS_CONSTANT = 8.314462618           # J/(mol·K) - Universal gas constant  
AVOGADRO = 6.02214076e23            # mol⁻¹ - Avogadro constant
BOLTZMANN = 1.380649e-23            # J/K - Boltzmann constant
PLANCK = 6.62607015e-34             # J·s - Planck constant

# =============================================================================
# STANDARD CONDITIONS & REFERENCE VALUES (European/ISO Standards)
# =============================================================================

STANDARD_CONDITIONS = {
    'temperature_k': 273.15,         # K (0°C)
    'temperature_c': 20.0,           # °C (ISO 3046-1 reference temperature)
    'pressure_pa': 101325,           # Pa (1 atm = 1013.25 mbar)
    'pressure_bar': 1.01325,         # bar (European standard pressure unit)
    'gravity': 9.80665,              # m/s² - Standard gravity (ISO 80000-3)
}

# =============================================================================
# WATER PROPERTIES (Primary Coolant)
# Reference: NIST Webbook, corrected values from latest data
# =============================================================================

WATER_PROPERTIES = {
    # At 20°C (293.15 K), 1 atm - CORRECTED VALUES
    '20C': {
        'density': 998.2,                    # kg/m³
        'specific_heat': 4182,               # J/(kg·K) 
        'thermal_conductivity': 0.598,       # W/(m·K)
        'dynamic_viscosity': 1.002e-3,       # Pa·s
        'kinematic_viscosity': 1.004e-6,     # m²/s (corrected: μ/ρ)
        'prandtl_number': 7.01,              # dimensionless
        'thermal_expansion': 2.07e-4,        # 1/K
        'bulk_modulus': 2.2e9,               # Pa (for compressibility)
    },
    
    # At 30°C (typical datacenter supply) - CORRECTED VALUES  
    '30C': {
        'density': 995.7,                    # kg/m³
        'specific_heat': 4178,               # J/(kg·K)
        'thermal_conductivity': 0.615,       # W/(m·K)
        'dynamic_viscosity': 7.97e-4,        # Pa·s (corrected)
        'kinematic_viscosity': 8.01e-7,      # m²/s (corrected: μ/ρ)
        'prandtl_number': 5.42,              # dimensionless
        'thermal_expansion': 3.03e-4,        # 1/K
        'bulk_modulus': 2.25e9,              # Pa
    },
    
    # At 45°C (typical return temperature) - CORRECTED VALUES
    '45C': {
        'density': 990.2,                    # kg/m³
        'specific_heat': 4180,               # J/(kg·K)
        'thermal_conductivity': 0.637,       # W/(m·K)
        'dynamic_viscosity': 5.96e-4,        # Pa·s
        'kinematic_viscosity': 6.02e-7,      # m²/s (corrected: μ/ρ)
        'prandtl_number': 3.91,              # dimensionless
        'thermal_expansion': 4.28e-4,        # 1/K
        'bulk_modulus': 2.3e9,               # Pa
    },
    
    # At 60°C (higher temperature operations)
    '60C': {
        'density': 983.2,                    # kg/m³
        'specific_heat': 4184,               # J/(kg·K)
        'thermal_conductivity': 0.654,       # W/(m·K)
        'dynamic_viscosity': 4.66e-4,        # Pa·s
        'kinematic_viscosity': 4.74e-7,      # m²/s
        'prandtl_number': 2.98,              # dimensionless
        'thermal_expansion': 5.18e-4,        # 1/K
        'bulk_modulus': 2.35e9,              # Pa
    },
}

# =============================================================================
# AIR PROPERTIES (Secondary Coolant) - European Conditions
# Reference: VDI Heat Atlas, ASHRAE Fundamentals
# =============================================================================

AIR_PROPERTIES = {
    # At 20°C, 1 bar (European standard conditions)
    '20C': {
        'density': 1.204,                    # kg/m³
        'specific_heat': 1006,               # J/(kg·K)
        'thermal_conductivity': 0.0251,      # W/(m·K)
        'dynamic_viscosity': 1.825e-5,       # Pa·s
        'kinematic_viscosity': 1.516e-5,     # m²/s
        'prandtl_number': 0.730,             # dimensionless
        'gas_constant_specific': 287.1,      # J/(kg·K) for air
    },
    
    # At 35°C (warm datacenter conditions)
    '35C': {
        'density': 1.146,                    # kg/m³
        'specific_heat': 1007,               # J/(kg·K)
        'thermal_conductivity': 0.0268,      # W/(m·K)
        'dynamic_viscosity': 1.895e-5,       # Pa·s
        'kinematic_viscosity': 1.655e-5,     # m²/s
        'prandtl_number': 0.725,             # dimensionless
        'gas_constant_specific': 287.1,      # J/(kg·K)
    },
}

# =============================================================================
# EUROPEAN PIPE SIZING (EN 10220/EN ISO 1127) - DN System
# Reference: EN 10220:2002, EN ISO 1127
# =============================================================================

# DN to Inner Diameter mapping for Schedule 40 equivalent (European standard)
EUROPEAN_PIPE_SIZES = {
    # DN : {'inner_diameter_mm': value, 'outer_diameter_mm': value, 'wall_thickness_mm': value}
    15: {'inner_diameter_mm': 15.8, 'outer_diameter_mm': 21.3, 'wall_thickness_mm': 2.75},
    20: {'inner_diameter_mm': 20.9, 'outer_diameter_mm': 26.9, 'wall_thickness_mm': 3.0},
    25: {'inner_diameter_mm': 26.6, 'outer_diameter_mm': 33.7, 'wall_thickness_mm': 3.55},
    32: {'inner_diameter_mm': 35.1, 'outer_diameter_mm': 42.4, 'wall_thickness_mm': 3.65},
    40: {'inner_diameter_mm': 40.9, 'outer_diameter_mm': 48.3, 'wall_thickness_mm': 3.7},
    50: {'inner_diameter_mm': 52.5, 'outer_diameter_mm': 60.3, 'wall_thickness_mm': 3.9},
    65: {'inner_diameter_mm': 62.7, 'outer_diameter_mm': 73.0, 'wall_thickness_mm': 5.15},
    80: {'inner_diameter_mm': 77.9, 'outer_diameter_mm': 88.9, 'wall_thickness_mm': 5.5},
    100: {'inner_diameter_mm': 102.3, 'outer_diameter_mm': 114.3, 'wall_thickness_mm': 6.0},
    150: {'inner_diameter_mm': 154.1, 'outer_diameter_mm': 168.3, 'wall_thickness_mm': 7.1},
    200: {'inner_diameter_mm': 202.7, 'outer_diameter_mm': 219.1, 'wall_thickness_mm': 8.2},
    250: {'inner_diameter_mm': 254.5, 'outer_diameter_mm': 273.0, 'wall_thickness_mm': 9.25},
    300: {'inner_diameter_mm': 303.2, 'outer_diameter_mm': 323.9, 'wall_thickness_mm': 10.35},
}

# =============================================================================
# DATACENTER SPECIFIC CONSTANTS (European/ISO Standards)
# Reference: EN 50600 series, ASHRAE TC 9.9
# =============================================================================

DATACENTER_STANDARDS = {
    # Temperature standards (European preference for higher supply temps)
    'en50600_recommended_supply_temp': 22.0,     # °C (EN 50600 recommendation)
    'ashrae_recommended_supply_temp': 18.0,      # °C (ASHRAE A1 class)
    'ashrae_allowable_temp_range': (18.0, 27.0), # °C (ASHRAE 2021 allowable)
    'en50600_allowable_temp_range': (20.0, 25.0), # °C (EN 50600 recommended)
    
    # Humidity (European standards more conservative)
    'en50600_recommended_humidity': (45.0, 55.0), # % RH (EN 50600)
    'ashrae_recommended_humidity': (40.0, 60.0),  # % RH (ASHRAE)
    
    # Power and efficiency metrics
    'typical_server_power_density': 5000,         # W/m² (rack level)
    'european_cooling_efficiency_target': 1.15,   # PUE (European Green Deal target)
    'typical_cooling_efficiency': 1.25,           # PUE (current average)
    
    # Fluid velocity standards (European conservative approach)
    'water_velocity_recommended': 1.5,            # m/s (VDI recommendation)
    'water_velocity_max': 2.5,                    # m/s (to minimize erosion)
    'air_velocity_min': 1.0,                      # m/s (minimum for cooling)
    'air_velocity_max': 4.0,                      # m/s (noise considerations)
}

# =============================================================================
# CONVERSION FACTORS (Metric/European First)
# =============================================================================

CONVERSION_FACTORS = {
    # Temperature conversions
    'celsius_to_kelvin': 273.15,
    'fahrenheit_offset': 32.0,
    'fahrenheit_scale': 5.0/9.0,
    'rankine_offset': 459.67,
    
    # Volume and Flow (European units prioritized)
    'liters_to_m3': 1e-3,                        # L → m³
    'm3_to_liters': 1e3,                         # m³ → L
    'liters_per_minute_to_m3_per_second': 1e-3/60, # L/min → m³/s
    'm3_per_hour_to_m3_per_second': 1/3600,      # m³/h → m³/s
    
    # Imperial conversions (for compatibility)
    'gpm_to_m3_per_s': 6.309e-5,                # US gal/min → m³/s
    'cfm_to_m3_per_s': 4.719e-4,                # ft³/min → m³/s
    'imperial_gallon_to_liter': 4.54609,         # UK gallon → L
    'us_gallon_to_liter': 3.78541,              # US gallon → L
    
    # Time
    'minutes_to_seconds': 60,
    'hours_to_seconds': 3600,
    'days_to_seconds': 86400,
    
    # Power (European/SI units prioritized)
    'watts_to_kilowatts': 1e-3,
    'kilowatts_to_megawatts': 1e-3,
    'watts_to_megawatts': 1e-6,
    
    # Imperial power conversions
    'watts_to_btu_per_hour': 3.412141633,
    'watts_to_tons_refrigeration': 3.516853e-4,
    'btu_per_hour_to_watts': 0.293071,
    'tons_refrigeration_to_watts': 3516.853,
    
    # Pressure (European bar/Pa system prioritized)
    'pa_to_kpa': 1e-3,
    'kpa_to_mpa': 1e-3,
    'pa_to_bar': 1e-5,
    'bar_to_pa': 1e5,
    'mbar_to_pa': 1e2,
    
    # Imperial pressure conversions
    'pa_to_psi': 1.450377e-4,
    'psi_to_pa': 6894.76,
    'psi_to_bar': 0.0689476,
    'bar_to_psi': 14.5038,
    
    # Length (Metric prioritized)
    'mm_to_m': 1e-3,
    'm_to_mm': 1e3,
    'cm_to_m': 1e-2,
    'm_to_cm': 1e2,
    
    # Imperial length conversions
    'inches_to_m': 0.0254,
    'feet_to_m': 0.3048,
    'inches_to_mm': 25.4,
    'feet_to_mm': 304.8,
    
    # Area and Volume
    'mm2_to_m2': 1e-6,
    'cm2_to_m2': 1e-4,
    'mm3_to_m3': 1e-9,
    'cm3_to_m3': 1e-6,
    
    # Mass
    'g_to_kg': 1e-3,
    'kg_to_tonnes': 1e-3,
    'tonnes_to_kg': 1e3,
}

# =============================================================================
# MATERIAL PROPERTIES (European Steel Standards)
# Reference: EN 10025 series, VDI Heat Atlas
# =============================================================================

STEEL_PROPERTIES = {
    # Carbon steel (EN 10025-2: S235, S275, S355)
    'carbon_steel': {
        'density': 7850,                     # kg/m³
        'specific_heat': 460,                # J/(kg·K)
        'thermal_conductivity': 50,          # W/(m·K)
        'thermal_expansion': 12e-6,          # 1/K
        'youngs_modulus': 210e9,             # Pa
        'roughness': 0.045e-3,               # m (commercial steel)
    },
    
    # Stainless steel (EN 10088-2: 1.4301/1.4307)
    'stainless_steel_304': {
        'density': 8000,                     # kg/m³
        'specific_heat': 500,                # J/(kg·K)
        'thermal_conductivity': 16.2,        # W/(m·K)
        'thermal_expansion': 17.3e-6,        # 1/K
        'youngs_modulus': 200e9,             # Pa
        'roughness': 0.015e-3,               # m (electropolished)
    },
    
    # Copper (for heat exchangers)
    'copper': {
        'density': 8960,                     # kg/m³
        'specific_heat': 385,                # J/(kg·K)
        'thermal_conductivity': 401,         # W/(m·K)
        'thermal_expansion': 16.5e-6,        # 1/K
        'youngs_modulus': 130e9,             # Pa
        'roughness': 0.0015e-3,              # m (drawn tubing)
    },
}

# =============================================================================
# FLUID VELOCITY LIMITS (European Conservative Standards)
# Reference: VDI 2056, EN 806
# =============================================================================

VELOCITY_LIMITS = {
    'water_systems': {
        'supply_lines': 2.0,                 # m/s (VDI 2056 recommendation)
        'return_lines': 1.5,                 # m/s (lower to reduce pressure drop)
        'suction_lines': 1.0,                # m/s (avoid cavitation)
        'drain_lines': 0.6,                  # m/s (gravity systems)
    },
    'air_systems': {
        'supply_ducts': 8.0,                 # m/s (commercial HVAC)
        'return_ducts': 6.0,                 # m/s (noise considerations)
        'fresh_air_intakes': 3.0,            # m/s (weather protection)
    },
}

# =============================================================================
# HEAT TRANSFER COEFFICIENTS (Typical Values)
# Reference: VDI Heat Atlas, Incropera & DeWitt
# =============================================================================

HEAT_TRANSFER_COEFFICIENTS = {
    # Water convection (W/(m²·K))
    'water_forced_convection': (1000, 20000),   # range for turbulent flow
    'water_natural_convection': (100, 1000),    # range for natural circulation
    
    # Air convection (W/(m²·K))
    'air_forced_convection': (10, 200),         # range for forced air cooling
    'air_natural_convection': (5, 50),          # range for natural convection
    
    # Combined coefficients for heat exchangers
    'water_to_water_hx': (2000, 8000),          # typical range for plate HX
    'water_to_air_hx': (50, 500),               # typical range for finned tube HX
}

# =============================================================================
# VALIDATION CONSTANTS
# =============================================================================

VALIDATION_DATA = {
    # Known test cases for validation
    'water_heating_1mw': {
        'flow_lpm': 1493,
        'temperature_rise_c': 10,
        'expected_power_w': 1041616,         # Theoretical calculation
        'tolerance_percent': 2.0,            # ±2% acceptable error
    },
    
    'reynolds_transition': {
        'critical_re': 2300,                 # laminar to turbulent transition
        'fully_turbulent_re': 4000,          # fully developed turbulent
    },
    
    'pipe_sizing_limits': {
        'max_velocity_water': 2.5,           # m/s (European standard)
        'min_velocity_water': 0.3,           # m/s (avoid stagnation)
        'max_pressure_drop_per_100m': 5000,  # Pa/100m (reasonable limit)
    },
}

# =============================================================================
# MODULE VALIDATION
# =============================================================================

def validate_constants():
    """
    Validate critical constants for consistency and physical reasonableness.
    Returns dict with validation results.
    """
    results = []
    
    # Test water density consistency
    densities = [WATER_PROPERTIES[temp]['density'] for temp in ['20C', '30C', '45C', '60C']]
    if not all(densities[i] > densities[i+1] for i in range(len(densities)-1)):
        results.append({'test': 'Water density decreases with temperature', 'status': 'FAIL'})
    else:
        results.append({'test': 'Water density decreases with temperature', 'status': 'PASS'})
    
    # Test viscosity consistency  
    viscosities = [WATER_PROPERTIES[temp]['dynamic_viscosity'] for temp in ['20C', '30C', '45C', '60C']]
    if not all(viscosities[i] > viscosities[i+1] for i in range(len(viscosities)-1)):
        results.append({'test': 'Water viscosity decreases with temperature', 'status': 'FAIL'})
    else:
        results.append({'test': 'Water viscosity decreases with temperature', 'status': 'PASS'})
    
    # Test conversion factor consistency
    lpm_to_m3s = CONVERSION_FACTORS['liters_per_minute_to_m3_per_second']
    expected = CONVERSION_FACTORS['liters_to_m3'] / CONVERSION_FACTORS['minutes_to_seconds']
    if abs(lpm_to_m3s - expected) / expected > 1e-10:
        results.append({'test': 'Flow conversion consistency', 'status': 'FAIL'})
    else:
        results.append({'test': 'Flow conversion consistency', 'status': 'PASS'})
    
    # Test kinematic viscosity calculation
    for temp in ['20C', '30C', '45C']:
        props = WATER_PROPERTIES[temp]
        calculated_nu = props['dynamic_viscosity'] / props['density']
        stored_nu = props['kinematic_viscosity']
        error = abs(calculated_nu - stored_nu) / stored_nu
        if error > 0.01:  # 1% tolerance
            results.append({'test': f'Kinematic viscosity calculation at {temp}', 'status': 'FAIL'})
        else:
            results.append({'test': f'Kinematic viscosity calculation at {temp}', 'status': 'PASS'})
    
    return results

if __name__ == "__main__":
    print("Physics Constants Module - European/Metric Standards")
    print("=" * 55)
    
    # Run validation
    validation_results = validate_constants()
    for result in validation_results:
        print(f"{result['test']}: {result['status']}")
    
    print(f"\nAvailable water temperatures: {list(WATER_PROPERTIES.keys())}")
    print(f"Available pipe sizes (DN): {list(EUROPEAN_PIPE_SIZES.keys())}")
    print(f"Standard pressure: {STANDARD_CONDITIONS['pressure_bar']:.3f} bar")
    print(f"Standard temperature: {STANDARD_CONDITIONS['temperature_c']}°C")