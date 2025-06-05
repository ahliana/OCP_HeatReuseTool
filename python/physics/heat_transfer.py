# =============================================================================
# HEAT TRANSFER MODULE
# =============================================================================

# python/physics/heat_transfer.py
"""
Standard Heat Transfer Correlations and Formulas
Reference: Fundamentals of Heat and Mass Transfer (Incropera, DeWitt, Bergman, Lavine)
"""

import math
from .constants import WATER_PROPERTIES

def prandtl_number(specific_heat, dynamic_viscosity, thermal_conductivity):
    """
    Calculate Prandtl number.
    
    Formula: Pr = (cp × μ) / k
    Reference: Dimensionless numbers in heat transfer
    
    Args:
        specific_heat (float): Specific heat capacity [J/(kg·K)]
        dynamic_viscosity (float): Dynamic viscosity [Pa·s]
        thermal_conductivity (float): Thermal conductivity [W/(m·K)]
    
    Returns:
        float: Prandtl number [dimensionless]
    """
    return (specific_heat * dynamic_viscosity) / thermal_conductivity


def nusselt_number_laminar_pipe(reynolds, prandtl, length_diameter_ratio=None):
    """
    Calculate Nusselt number for laminar flow in pipes.
    
    For fully developed flow: Nu = 4.36 (constant wall heat flux)
    For developing flow: Uses Sieder-Tate correlation
    
    Reference: Incropera & DeWitt, Chapter 8
    
    Args:
        reynolds (float): Reynolds number
        prandtl (float): Prandtl number
        length_diameter_ratio (float, optional): L/D ratio for developing flow
    
    Returns:
        float: Nusselt number [dimensionless]
    """
    if reynolds >= 2300:
        raise ValueError("Use turbulent correlation for Re >= 2300")
    
    if length_diameter_ratio is None or length_diameter_ratio > 60:
        # Fully developed flow
        return 4.36  # For constant wall heat flux
    else:
        # Developing flow - Sieder-Tate correlation
        gz = reynolds * prandtl * (1.0 / length_diameter_ratio)  # Graetz number
        if gz > 100:
            return 1.86 * (gz)**(1/3)
        else:
            return 4.36  # Fully developed limit


def nusselt_number_turbulent_pipe(reynolds, prandtl):
    """
    Calculate Nusselt number for turbulent flow in pipes.
    
    Uses Dittus-Boelter equation: Nu = 0.023 × Re^0.8 × Pr^n
    where n = 0.4 for heating, 0.3 for cooling
    
    Reference: Dittus & Boelter (1930), most widely used correlation
    
    Args:
        reynolds (float): Reynolds number (Re > 2300)
        prandtl (float): Prandtl number
    
    Returns:
        float: Nusselt number [dimensionless]
    """
    if reynolds < 2300:
        raise ValueError("Use laminar correlation for Re < 2300")
    
    # Using n = 0.4 (heating mode, typical for datacenter applications)
    return 0.023 * (reynolds**0.8) * (prandtl**0.4)


def heat_transfer_coefficient(nusselt, thermal_conductivity, characteristic_length):
    """
    Calculate convective heat transfer coefficient from Nusselt number.
    
    Formula: h = Nu × k / L
    
    Args:
        nusselt (float): Nusselt number
        thermal_conductivity (float): Fluid thermal conductivity [W/(m·K)]
        characteristic_length (float): Characteristic length (usually diameter) [m]
    
    Returns:
        float: Heat transfer coefficient [W/(m²·K)]
    """
    return nusselt * thermal_conductivity / characteristic_length


def thermal_resistance_convection(heat_transfer_coefficient, area):
    """
    Calculate convective thermal resistance.
    
    Formula: R = 1 / (h × A)
    
    Args:
        heat_transfer_coefficient (float): Convective heat transfer coefficient [W/(m²·K)]
        area (float): Heat transfer area [m²]
    
    Returns:
        float: Thermal resistance [K/W]
    """
    return 1.0 / (heat_transfer_coefficient * area)


def overall_heat_transfer_coefficient(resistances):
    """
    Calculate overall heat transfer coefficient for multiple thermal resistances.
    
    Formula: 1/U = ΣR = R₁ + R₂ + R₃ + ...
    
    Args:
        resistances (list): List of thermal resistances [K/W]
    
    Returns:
        float: Overall heat transfer coefficient [W/(m²·K)]
    """
    total_resistance = sum(resistances)
    return 1.0 / total_resistance


def newtons_law_cooling(heat_transfer_coefficient, area, temp_difference):
    """
    Calculate heat transfer using Newton's law of cooling.
    
    Formula: Q̇ = h × A × ΔT
    Reference: Newton's law of cooling, convective heat transfer fundamentals
    
    Args:
        heat_transfer_coefficient (float): Heat transfer coefficient [W/(m²·K)]
        area (float): Heat transfer area [m²]
        temp_difference (float): Temperature difference [K or °C]
    
    Returns:
        float: Heat transfer rate [W]
    """
    return heat_transfer_coefficient * area * temp_difference


def fourier_law_conduction(thermal_conductivity, area, temp_gradient, thickness):
    """
    Calculate heat conduction using Fourier's law.
    
    Formula: Q̇ = -k × A × (dT/dx) ≈ k × A × ΔT / Δx
    
    Args:
        thermal_conductivity (float): Material thermal conductivity [W/(m·K)]
        area (float): Cross-sectional area [m²]
        temp_gradient (float): Temperature difference [K or °C]
        thickness (float): Material thickness [m]
    
    Returns:
        float: Heat transfer rate [W]
    """
    return thermal_conductivity * area * temp_gradient / thickness

