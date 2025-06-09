from typing import Dict, Optional, List, Tuple, Union

# =============================================================================
# IMPORT DEPENDENCIES
# =============================================================================
try:
    from physics.constants import WATER_PROPERTIES
    from physics.units import (liters_per_minute_to_m3_per_second, m3_per_second_to_liters_per_minute)
    
except ImportError as e:
    # Don't define functions if imports fail
    raise ImportError(f"Cannot import required physics modules: {e}")


# =============================================================================
# DEFINE FUNCTIONS
# =============================================================================
def quick_power_calculation(flow_lpm: float, temp_rise_c: float, fluid: str = 'water') -> float:
    """Quick power calculation compatible with existing code."""
    if fluid == 'water':
        props = WATER_PROPERTIES['30C']  # Representative properties
        mass_flow = liters_per_minute_to_m3_per_second(flow_lpm) * props['density']
        return mass_flow * props['specific_heat'] * temp_rise_c
    else:
        raise ValueError("Only water implemented")


def get_MW(F1: float, T1: float, T2: float) -> float:
    return quick_power_calculation(F1, T2 - T1)


def get_MW_divd(F1: float, T1: float, T2: float) -> float:
    return get_MW(F1, T1, T2) / 1_000_000

def get_DeltaT_TCS(T1, T2):
    try:
        return float(T2) - float(T1)
    except Exception as e:
        return 0.0
    
def get_DeltaT_FWS(T3, T4):
    try:
        return float(T3) - float(T4)
    except Exception as e:
        return 0.0

def get_Approach(T1, T4):
    """Calculate approach temperature"""
    try:
        return float(T4) - float(T1)
    except Exception as e:
        print(f"❌ Error in get_Approach: {e}")
        return 0.0


