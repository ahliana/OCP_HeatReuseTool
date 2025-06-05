# =============================================================================
# UNITS CONVERSION MODULE - EUROPEAN-FIRST DESIGN
# =============================================================================

# python/physics/units.py
"""
Unit Conversion Functions for Heat Reuse Engineering Calculations
European-first design with comprehensive conversions for temperature, flow, 
pressure, power, etc. Optimized for datacenter heat reuse applications.

Key Features:
- European units (°C, L/min, bar, kW) as primary
- American units as secondary conversions
- Pipe sizing using European DN standards + ASME compatibility
- Robust error handling and validation
- Integration with existing heat reuse calculation modules
"""

import math
from typing import Union, Dict, Tuple, Optional

# Import constants from the constants module
try:
    from .constants import CONVERSION_FACTORS, WATER_PROPERTIES
except ImportError:
    # Fallback constants if constants module not available
    CONVERSION_FACTORS = {
        'celsius_to_kelvin': 273.15,
        'fahrenheit_offset': 32.0,
        'fahrenheit_scale': 5.0/9.0,
        'liters_to_m3': 1e-3,
        'minutes_to_seconds': 60.0,
        'gpm_to_m3_per_s': 6.30902e-5,
        'cfm_to_m3_per_s': 4.71947e-4,
        'watts_to_megawatts': 1e-6,
        'watts_to_btu_per_hour': 3.41214,
        'btu_per_hour_to_watts': 0.293071,
        'watts_to_tons_refrigeration': 2.84345e-4,
        'pa_to_psi': 1.45038e-4,
        'psi_to_pa': 6894.76,
        'bar_to_pa': 1e5,
        'mm_to_m': 1e-3,
        'inches_to_m': 0.0254,
        'feet_to_m': 0.3048,
    }

# =============================================================================
# TEMPERATURE CONVERSIONS (EUROPEAN-FIRST)
# =============================================================================

def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin (European standard)."""
    return celsius + CONVERSION_FACTORS['celsius_to_kelvin']

def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    return kelvin - CONVERSION_FACTORS['celsius_to_kelvin']

def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit (for American compatibility)."""
    return celsius * (9.0/5.0) + CONVERSION_FACTORS['fahrenheit_offset']

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - CONVERSION_FACTORS['fahrenheit_offset']) * CONVERSION_FACTORS['fahrenheit_scale']

def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """Convert Fahrenheit to Kelvin."""
    return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))

def temperature_difference_c_to_k(delta_c: float) -> float:
    """Convert temperature difference from Celsius to Kelvin (same magnitude)."""
    return delta_c  # Temperature differences are the same in C and K

# =============================================================================
# FLOW RATE CONVERSIONS (EUROPEAN L/min PRIMARY)
# =============================================================================

def liters_per_minute_to_m3_per_second(lpm: float) -> float:
    """Convert L/min to m³/s (European standard flow conversion)."""
    return lpm * CONVERSION_FACTORS['liters_to_m3'] / CONVERSION_FACTORS['minutes_to_seconds']

def m3_per_second_to_liters_per_minute(m3s: float) -> float:
    """Convert m³/s to L/min."""
    return m3s / CONVERSION_FACTORS['liters_to_m3'] * CONVERSION_FACTORS['minutes_to_seconds']

def liters_per_hour_to_liters_per_minute(lph: float) -> float:
    """Convert L/h to L/min (European industrial standard)."""
    return lph / 60.0

def liters_per_minute_to_liters_per_hour(lpm: float) -> float:
    """Convert L/min to L/h."""
    return lpm * 60.0

def cubic_meters_per_hour_to_liters_per_minute(m3h: float) -> float:
    """Convert m³/h to L/min (common European industrial unit)."""
    return m3h * 1000.0 / 60.0

def liters_per_minute_to_cubic_meters_per_hour(lpm: float) -> float:
    """Convert L/min to m³/h."""
    return lpm * 60.0 / 1000.0

# American flow conversions (secondary)
def gpm_to_liters_per_minute(gpm: float) -> float:
    """Convert US gallons per minute to L/min."""
    return gpm * 3.78541  # 1 US gallon = 3.78541 liters

def liters_per_minute_to_gpm(lpm: float) -> float:
    """Convert L/min to US gallons per minute."""
    return lpm / 3.78541

def gpm_to_m3_per_second(gpm: float) -> float:
    """Convert gallons per minute to m³/s."""
    return gpm * CONVERSION_FACTORS['gpm_to_m3_per_s']

def cfm_to_m3_per_second(cfm: float) -> float:
    """Convert cubic feet per minute to m³/s."""
    return cfm * CONVERSION_FACTORS['cfm_to_m3_per_s']

def liters_per_minute_to_kg_per_second(lpm: float, density: float = 998.2) -> float:
    """
    Convert L/min to kg/s using fluid density.
    Default density is water at 20°C.
    """
    m3s = liters_per_minute_to_m3_per_second(lpm)
    return m3s * density

def kg_per_second_to_liters_per_minute(kg_s: float, density: float = 998.2) -> float:
    """Convert kg/s to L/min using fluid density."""
    m3s = kg_s / density
    return m3_per_second_to_liters_per_minute(m3s)

# =============================================================================
# POWER CONVERSIONS (EUROPEAN kW/MW PRIMARY)
# =============================================================================

def watts_to_kilowatts(watts: float) -> float:
    """Convert watts to kilowatts (European standard)."""
    return watts * 1e-3

def kilowatts_to_watts(kilowatts: float) -> float:
    """Convert kilowatts to watts."""
    return kilowatts * 1e3

def watts_to_megawatts(watts: float) -> float:
    """Convert watts to megawatts."""
    return watts * CONVERSION_FACTORS['watts_to_megawatts']

def megawatts_to_watts(megawatts: float) -> float:
    """Convert megawatts to watts."""
    return megawatts / CONVERSION_FACTORS['watts_to_megawatts']

def kilowatts_to_megawatts(kilowatts: float) -> float:
    """Convert kilowatts to megawatts."""
    return kilowatts * 1e-3

def megawatts_to_kilowatts(megawatts: float) -> float:
    """Convert megawatts to kilowatts."""
    return megawatts * 1e3

# American power conversions (secondary)
def watts_to_btu_per_hour(watts: float) -> float:
    """Convert watts to BTU/hr."""
    return watts * CONVERSION_FACTORS['watts_to_btu_per_hour']

def btu_per_hour_to_watts(btu_hr: float) -> float:
    """Convert BTU/hr to watts."""
    return btu_hr * CONVERSION_FACTORS['btu_per_hour_to_watts']

def watts_to_tons_refrigeration(watts: float) -> float:
    """Convert watts to tons of refrigeration."""
    return watts * CONVERSION_FACTORS['watts_to_tons_refrigeration']

def tons_refrigeration_to_watts(tons: float) -> float:
    """Convert tons of refrigeration to watts."""
    return tons / CONVERSION_FACTORS['watts_to_tons_refrigeration']

def kilowatts_to_btu_per_hour(kilowatts: float) -> float:
    """Convert kW to BTU/hr (for international compatibility)."""
    return watts_to_btu_per_hour(kilowatts_to_watts(kilowatts))

def horsepower_to_kilowatts(hp: float) -> float:
    """Convert mechanical horsepower to kilowatts."""
    return hp * 0.745699

def kilowatts_to_horsepower(kw: float) -> float:
    """Convert kilowatts to mechanical horsepower."""
    return kw / 0.745699

# =============================================================================
# PRESSURE CONVERSIONS (EUROPEAN bar PRIMARY)
# =============================================================================

def pascal_to_bar(pascal: float) -> float:
    """Convert Pascal to bar (European standard)."""
    return pascal / CONVERSION_FACTORS['bar_to_pa']

def bar_to_pascal(bar: float) -> float:
    """Convert bar to Pascal."""
    return bar * CONVERSION_FACTORS['bar_to_pa']

def bar_to_kpa(bar: float) -> float:
    """Convert bar to kPa (common European engineering unit)."""
    return bar * 100.0

def kpa_to_bar(kpa: float) -> float:
    """Convert kPa to bar."""
    return kpa / 100.0

def mbar_to_bar(mbar: float) -> float:
    """Convert millibar to bar."""
    return mbar * 1e-3

def bar_to_mbar(bar: float) -> float:
    """Convert bar to millibar."""
    return bar * 1e3

# American pressure conversions (secondary)
def pascal_to_psi(pascal: float) -> float:
    """Convert Pascal to PSI."""
    return pascal * CONVERSION_FACTORS['pa_to_psi']

def psi_to_pascal(psi: float) -> float:
    """Convert PSI to Pascal."""
    return psi * CONVERSION_FACTORS['psi_to_pa']

def bar_to_psi(bar: float) -> float:
    """Convert bar to PSI."""
    return pascal_to_psi(bar_to_pascal(bar))

def psi_to_bar(psi: float) -> float:
    """Convert PSI to bar."""
    return pascal_to_bar(psi_to_pascal(psi))

# =============================================================================
# LENGTH CONVERSIONS (EUROPEAN mm/m PRIMARY)
# =============================================================================

def millimeters_to_meters(mm: float) -> float:
    """Convert millimeters to meters (European standard)."""
    return mm * CONVERSION_FACTORS['mm_to_m']

def meters_to_millimeters(m: float) -> float:
    """Convert meters to millimeters."""
    return m / CONVERSION_FACTORS['mm_to_m']

def centimeters_to_meters(cm: float) -> float:
    """Convert centimeters to meters."""
    return cm * 1e-2

def meters_to_centimeters(m: float) -> float:
    """Convert meters to centimeters."""
    return m * 1e2

def millimeters_to_centimeters(mm: float) -> float:
    """Convert millimeters to centimeters."""
    return mm * 1e-1

def centimeters_to_millimeters(cm: float) -> float:
    """Convert centimeters to millimeters."""
    return cm * 1e1

# American length conversions (secondary)
def inches_to_meters(inches: float) -> float:
    """Convert inches to meters."""
    return inches * CONVERSION_FACTORS['inches_to_m']

def meters_to_inches(meters: float) -> float:
    """Convert meters to inches."""
    return meters / CONVERSION_FACTORS['inches_to_m']

def feet_to_meters(feet: float) -> float:
    """Convert feet to meters."""
    return feet * CONVERSION_FACTORS['feet_to_m']

def meters_to_feet(meters: float) -> float:
    """Convert meters to feet."""
    return meters / CONVERSION_FACTORS['feet_to_m']

def inches_to_millimeters(inches: float) -> float:
    """Convert inches to millimeters (for pipe sizing)."""
    return meters_to_millimeters(inches_to_meters(inches))

def millimeters_to_inches(mm: float) -> float:
    """Convert millimeters to inches."""
    return meters_to_inches(millimeters_to_meters(mm))

# =============================================================================
# PIPE SIZE CONVERSIONS (EUROPEAN DN + ASME COMPATIBILITY)
# =============================================================================

def european_dn_pipe_sizes() -> Dict[int, float]:
    """
    European DN (Diameter Nominal) pipe sizes to actual inner diameters.
    DN values in mm, inner diameters in mm.
    Reference: EN 10220, DIN 2448 standards
    """
    return {
        # DN Size: Inner Diameter (mm) for Schedule 40 equivalent
        10: 10.3,    # DN10
        15: 15.8,    # DN15 (≈ 1/2")
        20: 20.9,    # DN20 (≈ 3/4")
        25: 26.6,    # DN25 (≈ 1")
        32: 35.1,    # DN32 (≈ 1-1/4")
        40: 40.9,    # DN40 (≈ 1-1/2")
        50: 52.5,    # DN50 (≈ 2")
        65: 62.7,    # DN65 (≈ 2-1/2")
        80: 77.9,    # DN80 (≈ 3")
        100: 102.3,  # DN100 (≈ 4")
        125: 128.2,  # DN125 (≈ 5")
        150: 154.1,  # DN150 (≈ 6")
        200: 202.7,  # DN200 (≈ 8")
        250: 254.5,  # DN250 (≈ 10")
        300: 303.2,  # DN300 (≈ 12")
        350: 333.3,  # DN350 (≈ 14")
        400: 381.0,  # DN400 (≈ 16")
        450: 428.5,  # DN450 (≈ 18")
        500: 477.8,  # DN500 (≈ 20")
        600: 574.6,  # DN600 (≈ 24")
    }

def american_nominal_pipe_sizes() -> Dict[float, float]:
    """
    American nominal pipe sizes to actual inner diameters.
    Reference: ASME/ANSI B36.10 pipe standards
    """
    return {
        # Nominal Size (inches): Inner Diameter (mm)
        0.5: 15.8,    # 1/2"
        0.75: 20.9,   # 3/4"
        1.0: 26.6,    # 1"
        1.25: 35.1,   # 1-1/4"
        1.5: 40.9,    # 1-1/2"
        2.0: 52.5,    # 2"
        2.5: 62.7,    # 2-1/2"
        3.0: 77.9,    # 3"
        4.0: 102.3,   # 4"
        5.0: 128.2,   # 5"
        6.0: 154.1,   # 6"
        8.0: 202.7,   # 8"
        10.0: 254.5,  # 10"
        12.0: 303.2,  # 12"
        14.0: 333.3,  # 14"
        16.0: 381.0,  # 16"
        18.0: 428.5,  # 18"
        20.0: 477.8,  # 20"
        24.0: 574.6,  # 24"
    }

def dn_to_nominal_inches(dn: int) -> Optional[float]:
    """Convert European DN size to approximate American nominal inches."""
    dn_sizes = european_dn_pipe_sizes()
    american_sizes = american_nominal_pipe_sizes()
    
    if dn not in dn_sizes:
        return None
    
    dn_diameter = dn_sizes[dn]
    
    # Find closest American size
    closest_size = None
    min_difference = float('inf')
    
    for nominal, diameter in american_sizes.items():
        difference = abs(diameter - dn_diameter)
        if difference < min_difference:
            min_difference = difference
            closest_size = nominal
    
    return closest_size

def nominal_inches_to_dn(nominal: float) -> Optional[int]:
    """Convert American nominal inches to approximate European DN size."""
    american_sizes = american_nominal_pipe_sizes()
    dn_sizes = european_dn_pipe_sizes()
    
    if nominal not in american_sizes:
        return None
    
    american_diameter = american_sizes[nominal]
    
    # Find closest DN size
    closest_dn = None
    min_difference = float('inf')
    
    for dn, diameter in dn_sizes.items():
        difference = abs(diameter - american_diameter)
        if difference < min_difference:
            min_difference = difference
            closest_dn = dn
    
    return closest_dn

def get_pipe_inner_diameter_mm(size: Union[int, float], standard: str = "DN") -> Optional[float]:
    """
    Get pipe inner diameter in mm for given size and standard.
    
    Args:
        size: Pipe size (DN for European, inches for American)
        standard: "DN" for European, "ASME" for American
    
    Returns:
        Inner diameter in mm, or None if not found
    """
    if standard.upper() == "DN":
        dn_sizes = european_dn_pipe_sizes()
        return dn_sizes.get(int(size))
    elif standard.upper() == "ASME":
        american_sizes = american_nominal_pipe_sizes()
        return american_sizes.get(float(size))
    else:
        raise ValueError("Standard must be 'DN' or 'ASME'")

# =============================================================================
# VELOCITY AND FLOW CALCULATIONS
# =============================================================================

def calculate_velocity_from_flow(flow_lpm: float, diameter_mm: float) -> float:
    """
    Calculate velocity from flow rate and pipe diameter.
    
    Args:
        flow_lpm: Flow rate in L/min
        diameter_mm: Pipe inner diameter in mm
    
    Returns:
        Velocity in m/s
    """
    # Convert units
    flow_m3s = liters_per_minute_to_m3_per_second(flow_lpm)
    diameter_m = millimeters_to_meters(diameter_mm)
    
    # Calculate area and velocity
    area_m2 = math.pi * (diameter_m / 2) ** 2
    velocity_ms = flow_m3s / area_m2
    
    return velocity_ms

def calculate_flow_from_velocity(velocity_ms: float, diameter_mm: float) -> float:
    """
    Calculate flow rate from velocity and pipe diameter.
    
    Args:
        velocity_ms: Velocity in m/s
        diameter_mm: Pipe inner diameter in mm
    
    Returns:
        Flow rate in L/min
    """
    # Convert diameter
    diameter_m = millimeters_to_meters(diameter_mm)
    
    # Calculate area and flow
    area_m2 = math.pi * (diameter_m / 2) ** 2
    flow_m3s = velocity_ms * area_m2
    flow_lpm = m3_per_second_to_liters_per_minute(flow_m3s)
    
    return flow_lpm

def reynolds_number(velocity_ms: float, diameter_mm: float, 
                   kinematic_viscosity: float = 1.004e-6) -> float:
    """
    Calculate Reynolds number.
    
    Args:
        velocity_ms: Velocity in m/s
        diameter_mm: Pipe diameter in mm
        kinematic_viscosity: Kinematic viscosity in m²/s (default: water at 20°C)
    
    Returns:
        Reynolds number (dimensionless)
    """
    diameter_m = millimeters_to_meters(diameter_mm)
    return velocity_ms * diameter_m / kinematic_viscosity

# =============================================================================
# COMPREHENSIVE UNIT CONVERSION UTILITY
# =============================================================================

def auto_unit_conversion(value: float, from_unit: str, to_unit: str) -> float:
    """
    Automatic unit conversion using lookup table.
    Enhanced with European-first conversions.
    
    Args:
        value: Value to convert
        from_unit: Source unit
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Raises:
        ValueError: If conversion not implemented
    """
    # Normalize unit strings
    from_unit = from_unit.replace(" ", "").replace("/", "_").upper()
    to_unit = to_unit.replace(" ", "").replace("/", "_").upper()
    
    # Temperature conversions
    temperature_conversions = {
        ('C', 'K'): celsius_to_kelvin,
        ('K', 'C'): kelvin_to_celsius,
        ('C', 'F'): celsius_to_fahrenheit,
        ('F', 'C'): fahrenheit_to_celsius,
        ('F', 'K'): fahrenheit_to_kelvin,
    }
    
    # Flow conversions (European primary)
    flow_conversions = {
        ('L_MIN', 'M3_S'): liters_per_minute_to_m3_per_second,
        ('M3_S', 'L_MIN'): m3_per_second_to_liters_per_minute,
        ('L_H', 'L_MIN'): liters_per_hour_to_liters_per_minute,
        ('L_MIN', 'L_H'): liters_per_minute_to_liters_per_hour,
        ('M3_H', 'L_MIN'): cubic_meters_per_hour_to_liters_per_minute,
        ('L_MIN', 'M3_H'): liters_per_minute_to_cubic_meters_per_hour,
        ('GPM', 'L_MIN'): gpm_to_liters_per_minute,
        ('L_MIN', 'GPM'): liters_per_minute_to_gpm,
        ('GPM', 'M3_S'): gpm_to_m3_per_second,
        ('CFM', 'M3_S'): cfm_to_m3_per_second,
    }
    
    # Power conversions (European primary)
    power_conversions = {
        ('W', 'KW'): watts_to_kilowatts,
        ('KW', 'W'): kilowatts_to_watts,
        ('W', 'MW'): watts_to_megawatts,
        ('MW', 'W'): megawatts_to_watts,
        ('KW', 'MW'): kilowatts_to_megawatts,
        ('MW', 'KW'): megawatts_to_kilowatts,
        ('W', 'BTU_HR'): watts_to_btu_per_hour,
        ('BTU_HR', 'W'): btu_per_hour_to_watts,
        ('W', 'TONS'): watts_to_tons_refrigeration,
        ('TONS', 'W'): tons_refrigeration_to_watts,
        ('KW', 'BTU_HR'): kilowatts_to_btu_per_hour,
        ('HP', 'KW'): horsepower_to_kilowatts,
        ('KW', 'HP'): kilowatts_to_horsepower,
    }
    
    # Pressure conversions (European primary)
    pressure_conversions = {
        ('PA', 'BAR'): pascal_to_bar,
        ('BAR', 'PA'): bar_to_pascal,
        ('BAR', 'KPA'): bar_to_kpa,
        ('KPA', 'BAR'): kpa_to_bar,
        ('MBAR', 'BAR'): mbar_to_bar,
        ('BAR', 'MBAR'): bar_to_mbar,
        ('PA', 'PSI'): pascal_to_psi,
        ('PSI', 'PA'): psi_to_pascal,
        ('BAR', 'PSI'): bar_to_psi,
        ('PSI', 'BAR'): psi_to_bar,
    }
    
    # Length conversions (European primary)
    length_conversions = {
        ('MM', 'M'): millimeters_to_meters,
        ('M', 'MM'): meters_to_millimeters,
        ('CM', 'M'): centimeters_to_meters,
        ('M', 'CM'): meters_to_centimeters,
        ('MM', 'CM'): millimeters_to_centimeters,
        ('CM', 'MM'): centimeters_to_millimeters,
        ('IN', 'M'): inches_to_meters,
        ('M', 'IN'): meters_to_inches,
        ('FT', 'M'): feet_to_meters,
        ('M', 'FT'): meters_to_feet,
        ('IN', 'MM'): inches_to_millimeters,
        ('MM', 'IN'): millimeters_to_inches,
    }
    
    # Combine all conversion dictionaries
    all_conversions = {
        **temperature_conversions,
        **flow_conversions,
        **power_conversions,
        **pressure_conversions,
        **length_conversions
    }
    
    # Look up and apply conversion
    conversion_key = (from_unit, to_unit)
    if conversion_key in all_conversions:
        return all_conversions[conversion_key](value)
    else:
        raise ValueError(f"Conversion from {from_unit} to {to_unit} not implemented")

# =============================================================================
# VALIDATION AND UTILITY FUNCTIONS
# =============================================================================

def validate_units_module():
    """
    Validate the units module with known conversions.
    Returns test results for verification.
    """
    test_results = []
    
    # Temperature tests
    try:
        result = celsius_to_kelvin(20)
        expected = 293.15
        test_results.append({
            'test': 'Celsius to Kelvin',
            'result': result,
            'expected': expected,
            'status': 'PASS' if abs(result - expected) < 0.01 else 'FAIL'
        })
    except Exception as e:
        test_results.append({'test': 'Celsius to Kelvin', 'status': 'ERROR', 'error': str(e)})
    
    # Flow tests
    try:
        result = liters_per_minute_to_m3_per_second(1000)
        expected = 0.01667  # Approximately
        test_results.append({
            'test': 'L/min to m³/s',
            'result': result,
            'expected': expected,
            'status': 'PASS' if abs(result - expected) < 0.0001 else 'FAIL'
        })
    except Exception as e:
        test_results.append({'test': 'L/min to m³/s', 'status': 'ERROR', 'error': str(e)})
    
    # Power tests
    try:
        result = kilowatts_to_megawatts(1000)
        expected = 1.0
        test_results.append({
            'test': 'kW to MW',
            'result': result,
            'expected': expected,
            'status': 'PASS' if abs(result - expected) < 0.01 else 'FAIL'
        })
    except Exception as e:
        test_results.append({'test': 'kW to MW', 'status': 'ERROR', 'error': str(e)})
    
    # Pipe size tests
    try:
        dn100_diameter = get_pipe_inner_diameter_mm(100, "DN")
        expected = 102.3
        test_results.append({
            'test': 'DN100 diameter',
            'result': dn100_diameter,
            'expected': expected,
            'status': 'PASS' if dn100_diameter == expected else 'FAIL'
        })
    except Exception as e:
        test_results.append({'test': 'DN100 diameter', 'status': 'ERROR', 'error': str(e)})
    
    # Velocity calculation test
    try:
        velocity = calculate_velocity_from_flow(1493, 102.3)  # 1493 L/min through DN100
        # Expected: ~4.8 m/s
        test_results.append({
            'test': 'Velocity calculation',
            'result': velocity,
            'expected': '~4.8',
            'status': 'PASS' if 4.0 <= velocity <= 5.5 else 'FAIL'
        })
    except Exception as e:
        test_results.append({'test': 'Velocity calculation', 'status': 'ERROR', 'error': str(e)})
    
    return test_results

def get_common_units() -> Dict[str, list]:
    """
    Return dictionary of common units by category for UI dropdowns.
    European units listed first.
    """
    return {
        'temperature': ['°C', 'K', '°F'],
        'flow_rate': ['L/min', 'L/h', 'm³/h', 'm³/s', 'GPM', 'CFM'],
        'power': ['kW', 'MW', 'W', 'BTU/hr', 'HP', 'tons'],
        'pressure': ['bar', 'kPa', 'mbar', 'Pa', 'psi'],
        'length': ['mm', 'cm', 'm', 'in', 'ft'],
        'pipe_size': ['DN', 'inches']
    }

def format_unit_value(value: float, unit: str, precision: int = 2) -> str:
    """
    Format a value with its unit using European number formatting.
    
    Args:
        value: Numerical value
        unit: Unit string
        precision: Decimal places
    
    Returns:
        Formatted string with value and unit
    """
    # European number formatting (space as thousands separator, comma as decimal)
    if abs(value) >= 1000:
        # Use space as thousands separator for large numbers
        formatted_value = f"{value:,.{precision}f}".replace(",", " ")
    else:
        formatted_value = f"{value:.{precision}f}"
    
    return f"{formatted_value} {unit}"

# =============================================================================
# HEAT REUSE SPECIFIC CONVERSIONS
# =============================================================================

def datacenter_power_to_heat_load(it_power_kw: float, efficiency: float = 0.95) -> float:
    """
    Convert datacenter IT power to heat load.
    
    Args:
        it_power_kw: IT equipment power in kW
        efficiency: Power supply efficiency (default 0.95)
    
    Returns:
        Heat load in kW
    """
    return it_power_kw / efficiency

def heat_load_to_cooling_flow(heat_load_kw: float, delta_t_c: float, 
                              fluid: str = "water") -> float:
    """
    Calculate required cooling flow rate from heat load.
    
    Args:
        heat_load_kw: Heat load in kW
        delta_t_c: Temperature rise in °C
        fluid: Cooling fluid type
    
    Returns:
        Flow rate in L/min
    """
    if fluid.lower() == "water":
        # Using water specific heat: 4.186 kJ/kg·K
        # Density: ~1000 kg/m³ at typical temperatures
        heat_load_w = kilowatts_to_watts(heat_load_kw)
        mass_flow_kg_s = heat_load_w / (4186 * delta_t_c)
        volume_flow_m3_s = mass_flow_kg_s / 1000  # Assuming water density 1000 kg/m³
        return m3_per_second_to_liters_per_minute(volume_flow_m3_s)
    else:
        raise NotImplementedError("Only water cooling implemented")

def cooling_efficiency_calc(heat_recovered_kw: float, heat_available_kw: float) -> float:
    """
    Calculate heat recovery efficiency as percentage.
    
    Args:
        heat_recovered_kw: Heat successfully recovered in kW
        heat_available_kw: Total heat available in kW
    
    Returns:
        Efficiency as percentage (0-100)
    """
    if heat_available_kw <= 0:
        return 0.0
    return min(100.0, (heat_recovered_kw / heat_available_kw) * 100.0)

def cop_to_efficiency(cop: float) -> float:
    """
    Convert Coefficient of Performance to efficiency percentage.
    
    Args:
        cop: Coefficient of Performance
    
    Returns:
        Efficiency percentage
    """
    return cop * 100.0

def efficiency_to_cop(efficiency_percent: float) -> float:
    """
    Convert efficiency percentage to Coefficient of Performance.
    
    Args:
        efficiency_percent: Efficiency as percentage
    
    Returns:
        Coefficient of Performance
    """
    return efficiency_percent / 100.0

# =============================================================================
# INTEGRATION WITH EXISTING HEAT REUSE MODULES
# =============================================================================

def integrate_with_universal_float_convert(value_with_unit: str) -> Tuple[float, str]:
    """
    Parse a string containing value and unit, compatible with universal_float_convert.
    
    Args:
        value_with_unit: String like "1,493 L/min" or "20°C"
    
    Returns:
        Tuple of (numerical_value, unit_string)
    """
    import re
    
    # Extract number and unit using regex
    pattern = r'([0-9,.\s]+)\s*([a-zA-Z°/\s]+)'
    match = re.match(pattern, value_with_unit.strip())
    
    if match:
        number_str = match.group(1).strip()
        unit_str = match.group(2).strip()
        
        # Use universal_float_convert if available, otherwise basic conversion
        try:
            from ..data.converter import universal_float_convert
            numerical_value = universal_float_convert(number_str)
        except ImportError:
            # Fallback conversion
            cleaned_number = number_str.replace(',', '.').replace(' ', '')
            numerical_value = float(cleaned_number)
        
        return numerical_value, unit_str
    else:
        raise ValueError(f"Cannot parse value and unit from: {value_with_unit}")

def convert_lookup_table_units(lookup_table: dict, from_unit: str, to_unit: str) -> dict:
    """
    Convert all values in a lookup table from one unit to another.
    Useful for converting existing CSV data to different units.
    
    Args:
        lookup_table: Dictionary with numerical values
        from_unit: Source unit
        to_unit: Target unit
    
    Returns:
        New dictionary with converted values
    """
    converted_table = {}
    
    for key, value in lookup_table.items():
        try:
            if isinstance(value, (int, float)):
                converted_value = auto_unit_conversion(float(value), from_unit, to_unit)
                converted_table[key] = converted_value
            else:
                # Keep non-numerical values unchanged
                converted_table[key] = value
        except (ValueError, TypeError):
            # Keep unconvertible values unchanged
            converted_table[key] = value
    
    return converted_table

def standardize_flow_units_for_heat_reuse(flow_value: float, current_unit: str) -> float:
    """
    Standardize flow units to L/min for heat reuse calculations.
    
    Args:
        flow_value: Flow rate value
        current_unit: Current unit of flow_value
    
    Returns:
        Flow rate in L/min
    """
    if current_unit.lower() in ['l/min', 'lpm', 'liters per minute']:
        return flow_value
    elif current_unit.lower() in ['m3/s', 'cubic meters per second']:
        return m3_per_second_to_liters_per_minute(flow_value)
    elif current_unit.lower() in ['l/h', 'liters per hour']:
        return liters_per_hour_to_liters_per_minute(flow_value)
    elif current_unit.lower() in ['m3/h', 'cubic meters per hour']:
        return cubic_meters_per_hour_to_liters_per_minute(flow_value)
    elif current_unit.lower() in ['gpm', 'gallons per minute']:
        return gpm_to_liters_per_minute(flow_value)
    else:
        raise ValueError(f"Unknown flow unit: {current_unit}")

def standardize_temperature_units_for_heat_reuse(temp_value: float, current_unit: str) -> float:
    """
    Standardize temperature units to Celsius for heat reuse calculations.
    
    Args:
        temp_value: Temperature value
        current_unit: Current unit of temp_value
    
    Returns:
        Temperature in Celsius
    """
    if current_unit.lower() in ['c', '°c', 'celsius']:
        return temp_value
    elif current_unit.lower() in ['k', 'kelvin']:
        return kelvin_to_celsius(temp_value)
    elif current_unit.lower() in ['f', '°f', 'fahrenheit']:
        return fahrenheit_to_celsius(temp_value)
    else:
        raise ValueError(f"Unknown temperature unit: {current_unit}")

def standardize_power_units_for_heat_reuse(power_value: float, current_unit: str) -> float:
    """
    Standardize power units to kW for heat reuse calculations.
    
    Args:
        power_value: Power value
        current_unit: Current unit of power_value
    
    Returns:
        Power in kW
    """
    if current_unit.lower() in ['kw', 'kilowatts']:
        return power_value
    elif current_unit.lower() in ['w', 'watts']:
        return watts_to_kilowatts(power_value)
    elif current_unit.lower() in ['mw', 'megawatts']:
        return megawatts_to_kilowatts(power_value)
    elif current_unit.lower() in ['btu/hr', 'btu per hour']:
        return watts_to_kilowatts(btu_per_hour_to_watts(power_value))
    elif current_unit.lower() in ['hp', 'horsepower']:
        return horsepower_to_kilowatts(power_value)
    else:
        raise ValueError(f"Unknown power unit: {current_unit}")

# =============================================================================
# COMPREHENSIVE VALIDATION AND TESTING
# =============================================================================

def comprehensive_units_test():
    """
    Comprehensive test suite for all unit conversions.
    Returns detailed test results.
    """
    test_results = []
    
    # Test categories
    test_categories = {
        'Temperature': [
            (celsius_to_kelvin, 20, 293.15, '20°C to K'),
            (fahrenheit_to_celsius, 68, 20, '68°F to °C'),
            (celsius_to_fahrenheit, 20, 68, '20°C to °F'),
        ],
        'Flow Rate': [
            (liters_per_minute_to_m3_per_second, 1000, 0.01667, '1000 L/min to m³/s'),
            (gpm_to_liters_per_minute, 100, 378.541, '100 GPM to L/min'),
            (cubic_meters_per_hour_to_liters_per_minute, 1, 16.667, '1 m³/h to L/min'),
        ],
        'Power': [
            (kilowatts_to_megawatts, 1000, 1.0, '1000 kW to MW'),
            (watts_to_kilowatts, 5000, 5.0, '5000 W to kW'),
            (horsepower_to_kilowatts, 1, 0.7457, '1 HP to kW'),
        ],
        'Pressure': [
            (bar_to_kpa, 1, 100, '1 bar to kPa'),
            (psi_to_bar, 14.504, 1.0, '14.504 PSI to bar'),
            (pascal_to_bar, 100000, 1.0, '100000 Pa to bar'),
        ],
        'Length': [
            (millimeters_to_meters, 1000, 1.0, '1000 mm to m'),
            (inches_to_millimeters, 1, 25.4, '1 in to mm'),
            (feet_to_meters, 3.28084, 1.0, '3.28084 ft to m'),
        ]
    }
    
    for category, tests in test_categories.items():
        for func, input_val, expected, description in tests:
            try:
                result = func(input_val)
                tolerance = max(0.001, abs(expected * 0.001))  # 0.1% tolerance
                status = 'PASS' if abs(result - expected) <= tolerance else 'FAIL'
                
                test_results.append({
                    'category': category,
                    'test': description,
                    'input': input_val,
                    'result': result,
                    'expected': expected,
                    'status': status,
                    'error_percent': abs(result - expected) / expected * 100 if expected != 0 else 0
                })
            except Exception as e:
                test_results.append({
                    'category': category,
                    'test': description,
                    'status': 'ERROR',
                    'error': str(e)
                })
    
    # Test pipe sizing
    try:
        dn_sizes = european_dn_pipe_sizes()
        american_sizes = american_nominal_pipe_sizes()
        
        # Test DN to inches conversion
        dn100_to_inches = dn_to_nominal_inches(100)
        test_results.append({
            'category': 'Pipe Sizing',
            'test': 'DN100 to inches',
            'result': dn100_to_inches,
            'expected': 4.0,
            'status': 'PASS' if dn100_to_inches == 4.0 else 'FAIL'
        })
        
        # Test velocity calculation
        velocity = calculate_velocity_from_flow(1493, 102.3)
        test_results.append({
            'category': 'Flow Calculation',
            'test': 'Velocity from flow',
            'input': '1493 L/min, DN100',
            'result': velocity,
            'expected': '~4.8 m/s',
            'status': 'PASS' if 4.0 <= velocity <= 5.5 else 'FAIL'
        })
        
    except Exception as e:
        test_results.append({
            'category': 'Pipe Sizing',
            'test': 'Pipe calculations',
            'status': 'ERROR',
            'error': str(e)
        })
    
    # Test auto conversion
    try:
        auto_result = auto_unit_conversion(1000, 'L/min', 'm3/s')
        expected_auto = 0.01667
        test_results.append({
            'category': 'Auto Conversion',
            'test': 'L/min to m³/s auto',
            'result': auto_result,
            'expected': expected_auto,
            'status': 'PASS' if abs(auto_result - expected_auto) <= 0.0001 else 'FAIL'
        })
    except Exception as e:
        test_results.append({
            'category': 'Auto Conversion',
            'test': 'Auto conversion test',
            'status': 'ERROR',
            'error': str(e)
        })
    
    return test_results

# =============================================================================
# MODULE INITIALIZATION AND COMPATIBILITY
# =============================================================================

def initialize_units_module():
    """
    Initialize the units module and verify compatibility with other modules.
    Returns initialization status.
    """
    try:
        # Test basic functionality
        test_results = validate_units_module()
        failed_tests = [t for t in test_results if t.get('status') == 'FAIL']
        
        if failed_tests:
            return {
                'status': 'WARNING',
                'message': f'{len(failed_tests)} validation tests failed',
                'failed_tests': failed_tests
            }
        
        return {
            'status': 'SUCCESS',
            'message': 'Units module initialized successfully',
            'available_conversions': len(get_common_units()),
            'pipe_standards': ['DN (European)', 'ASME (American)']
        }
        
    except Exception as e:
        return {
            'status': 'ERROR',
            'message': f'Failed to initialize units module: {str(e)}',
            'error': str(e)
        }

# Export commonly used functions for easy import
__all__ = [
    # Temperature
    'celsius_to_kelvin', 'kelvin_to_celsius', 'celsius_to_fahrenheit', 'fahrenheit_to_celsius',
    
    # Flow rate (European primary)
    'liters_per_minute_to_m3_per_second', 'm3_per_second_to_liters_per_minute',
    'cubic_meters_per_hour_to_liters_per_minute', 'liters_per_minute_to_cubic_meters_per_hour',
    'gpm_to_liters_per_minute', 'liters_per_minute_to_gpm',
    'liters_per_minute_to_kg_per_second', 'kg_per_second_to_liters_per_minute',
    
    # Power (European primary)
    'watts_to_kilowatts', 'kilowatts_to_watts', 'kilowatts_to_megawatts', 'megawatts_to_kilowatts',
    'watts_to_megawatts', 'megawatts_to_watts',
    
    # Pressure (European primary)
    'pascal_to_bar', 'bar_to_pascal', 'bar_to_kpa', 'kpa_to_bar',
    'bar_to_psi', 'psi_to_bar',
    
    # Length (European primary)
    'millimeters_to_meters', 'meters_to_millimeters', 'centimeters_to_meters', 'meters_to_centimeters',
    
    # Pipe sizing
    'european_dn_pipe_sizes', 'american_nominal_pipe_sizes', 'get_pipe_inner_diameter_mm',
    'dn_to_nominal_inches', 'nominal_inches_to_dn',
    
    # Flow calculations
    'calculate_velocity_from_flow', 'calculate_flow_from_velocity', 'reynolds_number',
    
    # Heat reuse specific
    'datacenter_power_to_heat_load', 'heat_load_to_cooling_flow', 'cooling_efficiency_calc',
    
    # Standardization functions
    'standardize_flow_units_for_heat_reuse', 'standardize_temperature_units_for_heat_reuse',
    'standardize_power_units_for_heat_reuse',
    
    # Utilities
    'auto_unit_conversion', 'format_unit_value', 'get_common_units',
    'validate_units_module', 'comprehensive_units_test', 'initialize_units_module'
]

if __name__ == "__main__":
    # Run comprehensive tests when module is executed directly
    print("Units Module - European-First Heat Reuse Engineering")
    print("=" * 60)
    
    # Initialize module
    init_result = initialize_units_module()
    print(f"Initialization: {init_result['status']} - {init_result['message']}")
    
    if init_result['status'] in ['SUCCESS', 'WARNING']:
        print("\nRunning comprehensive tests...")
        test_results = comprehensive_units_test()
        
        # Summarize results
        categories = {}
        for result in test_results:
            category = result.get('category', 'Unknown')
            if category not in categories:
                categories[category] = {'total': 0, 'passed': 0, 'failed': 0, 'errors': 0}
            
            categories[category]['total'] += 1
            if result.get('status') == 'PASS':
                categories[category]['passed'] += 1
            elif result.get('status') == 'FAIL':
                categories[category]['failed'] += 1
            elif result.get('status') == 'ERROR':
                categories[category]['errors'] += 1
        
        print("\nTest Results Summary:")
        print("-" * 40)
        for category, stats in categories.items():
            print(f"{category}: {stats['passed']}/{stats['total']} passed")
            if stats['failed'] > 0:
                print(f"  ⚠️ {stats['failed']} failed")
            if stats['errors'] > 0:
                print(f"  ❌ {stats['errors']} errors")
        
        # Show common units
        print(f"\nAvailable Units by Category:")
        print("-" * 40)
        common_units = get_common_units()
        for category, units in common_units.items():
            print(f"{category.title()}: {', '.join(units)}")
        
        print(f"\nEuropean DN Pipe Sizes: {len(european_dn_pipe_sizes())} sizes")
        print(f"American Pipe Sizes: {len(american_nominal_pipe_sizes())} sizes")
        
        print(f"\n✅ Units module ready for heat reuse calculations!")
    else:
        print(f"❌ Module initialization failed: {init_result.get('error', 'Unknown error')}")