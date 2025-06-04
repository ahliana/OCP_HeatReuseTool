# python/physics/constants.py
"""
Standard Physics Constants
All values from NIST, engineering handbooks, and peer-reviewed sources
"""

# Universal Constants (NIST 2018)
STEFAN_BOLTZMANN = 5.670374419e-8    # W/(m²·K⁴) - Stefan-Boltzmann constant
GAS_CONSTANT = 8.314462618           # J/(mol·K) - Universal gas constant
AVOGADRO = 6.02214076e23            # mol⁻¹ - Avogadro constant

# Water Properties (at standard conditions)
WATER_DENSITY_20C = 998.2            # kg/m³ at 20°C, 1 atm
WATER_SPECIFIC_HEAT_20C = 4182       # J/(kg·K) at 20°C
WATER_KINEMATIC_VISCOSITY_20C = 1.004e-6  # m²/s at 20°C
WATER_THERMAL_CONDUCTIVITY_20C = 0.598    # W/(m·K) at 20°C
WATER_PRANDTL_20C = 7.01             # Prandtl number at 20°C

# Standard Acceleration
GRAVITY = 9.80665                    # m/s² - Standard gravity

# Conversion Factors
LITERS_TO_M3 = 1e-3                 # L to m³
MINUTES_TO_SECONDS = 60             # min to s
WATTS_TO_MEGAWATTS = 1e-6           # W to MW

# Engineering Standards
STANDARD_ATMOSPHERIC_PRESSURE = 101325  # Pa
STANDARD_TEMPERATURE = 273.15       # K (0°C)


# python/physics/thermodynamics.py
"""
Standard Thermodynamic Formulas
References: Fundamentals of Heat and Mass Transfer (Incropera & DeWitt)
"""

import math
from .constants import (
    WATER_SPECIFIC_HEAT_20C, 
    WATER_DENSITY_20C,
    WATER_KINEMATIC_VISCOSITY_20C,
    WATER_PRANDTL_20C
)


def sensible_heat_transfer(mass_flow_rate, specific_heat, delta_temperature):
    """
    Calculate sensible heat transfer rate
    
    Formula: Q = ṁ × cp × ΔT
    Reference: Any thermodynamics textbook, Chapter on Heat Transfer
    
    Args:
        mass_flow_rate (float): Mass flow rate [kg/s]
        specific_heat (float): Specific heat capacity [J/(kg·K)]
        delta_temperature (float): Temperature difference [K or °C]
    
    Returns:
        float: Heat transfer rate [W]
    """
    return mass_flow_rate * specific_heat * delta_temperature


def reynolds_number_pipe(velocity, diameter, kinematic_viscosity=None):
    """
    Calculate Reynolds number for pipe flow
    
    Formula: Re = v × D / ν
    Reference: Fluid Mechanics (White), Chapter 6
    
    Args:
        velocity (float): Average velocity [m/s]
        diameter (float):