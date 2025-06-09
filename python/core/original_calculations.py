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
    """Equivalent to original get_MW function using standard physics."""
    return quick_power_calculation(F1, T2 - T1)


def get_MW_divd(F1: float, T1: float, T2: float) -> float:
    """Equivalent to original get_MW_divd function."""
    return get_MW(F1, T1, T2) / 1_000_000