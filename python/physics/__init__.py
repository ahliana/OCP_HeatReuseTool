# python/physics/__init__.py
"""
Comprehensive Physics Module for Datacenter Heat Reuse Systems

This module provides standard physics constants, formulas, and correlations
used in thermodynamics, fluid mechanics, and heat transfer applications,
specifically organized for datacenter cooling and heat recovery systems.

All formulas are based on established engineering references and textbooks:
- Fundamentals of Heat and Mass Transfer (Incropera & DeWitt)
- Introduction to Heat Transfer (Bergman et al.)
- Fluid Mechanics (White)
- Heat Exchanger Design Handbook (Thulukkanam)
- ASHRAE Fundamentals Handbook

Author: Heat Reuse Analysis Tool Team
Version: 1.0
"""

from .constants import *
from .thermodynamics import *
from .fluid_mechanics import *
from .heat_transfer import *
from .heat_exchangers import *
from .materials import *
from .units import *

__all__ = [
    # Constants
    'WATER_PROPERTIES', 'STANDARD_CONDITIONS', 'CONVERSION_FACTORS',
    
    # Thermodynamics
    'sensible_heat_transfer', 'latent_heat_transfer', 'enthalpy_change',
    'power_from_heat_flow', 'temperature_approach', 'pinch_point_analysis',
    
    # Fluid Mechanics
    'reynolds_number', 'friction_factor_laminar', 'friction_factor_turbulent',
    'pressure_drop_pipe', 'pump_power_required', 'flow_velocity',
    
    # Heat Transfer
    'nusselt_number_laminar', 'nusselt_number_turbulent', 'prandtl_number',
    'heat_transfer_coefficient', 'thermal_resistance', 'overall_heat_transfer_coefficient',
    'newtons_law_cooling', 'fourier_law_conduction',
    
    # Heat Exchangers
    'lmtd_counterflow', 'lmtd_parallel', 'lmtd_correction_factor',
    'effectiveness_ntu', 'ntu_from_effectiveness', 'heat_exchanger_sizing',
    'approach_temperature', 'pinch_temperature',
    
    # Materials
    'pipe_materials', 'insulation_materials', 'coolant_properties',
    
    # Unit Conversions
    'celsius_to_kelvin', 'fahrenheit_to_celsius', 'liters_per_minute_to_m3_per_second',
    'watts_to_btu_per_hour', 'pressure_conversions'
]