"""
Original calculation functions for heat reuse system analysis.

This module contains the core calculation functions that were originally
in the Jupyter notebook.
"""


# =============================================================================
# IMPORT DEPENDENCIES
# =============================================================================
try:
    from typing import Dict, Optional, List, Tuple, Union

    from physics.constants import WATER_PROPERTIES
    from physics.units import (liters_per_minute_to_m3_per_second, m3_per_second_to_liters_per_minute)

    # Import data access functions
    from data.loader import get_csv_data, is_csv_loaded
    from data.converter import universal_float_convert

    # Import lookup functions - now in separate module
    from .lookup import lookup_allhx_data, get_lookup_value
    
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


# =============================================================================
# DEFINE FUNCTIONS WITH LOOKUPS
# =============================================================================


def get_PipeSize_Suggested(F1):
    """
    Get suggested pipe size using CEILING lookup (engineering safe)
    Returns the SMALLEST pipe size that can handle the flow (size >= required)
    """
    try:
        F1_float = float(F1)
        
        # Check if PIPSZ data exists
        if 'PIPSZ' not in csv_data:
            print("❌ PIPSZ CSV not found")
            return 0  # Default fallback
        
        # Get and examine PIPSZ data
        pipsz_df = csv_data['PIPSZ'].copy()
        # print(f"📊 PIPSZ data shape: {pipsz_df.shape}")
        
        # Convert columns to numeric
        pipsz_df.iloc[:, 0] = pipsz_df.iloc[:, 0].apply(universal_float_convert)  # Flow capacity
        pipsz_df.iloc[:, 1] = pipsz_df.iloc[:, 1].apply(universal_float_convert)  # Pipe size
        
        # Remove invalid rows
        valid_rows = pipsz_df.dropna()
        
        # Sort by flow capacity to ensure we find the smallest adequate size
        valid_rows = valid_rows.sort_values(by=valid_rows.columns[0])
        
        flow_values = valid_rows.iloc[:, 0]
        print(f"📊 Available flow capacities: min={flow_values.min()}, max={flow_values.max()}")
        print(f"📊 First few flow/size pairs: {list(zip(flow_values.head(), valid_rows.iloc[:, 1].head()))}")
        
        # CEILING LOOKUP: Find the SMALLEST flow capacity that is >= F1
        # This ensures the pipe can safely handle the required flow
        candidates = valid_rows[valid_rows.iloc[:, 0] >= F1_float]
        
        if not candidates.empty:
            # Get the smallest adequate pipe (first row after sorting)
            selected_flow = candidates.iloc[0, 0]
            selected_size = candidates.iloc[0, 1]
            # print(f"✅ CEILING match found: Flow capacity {selected_flow} >= {F1_float} → Pipe Size {selected_size}")
            # print(f"🔧 Engineering validation: Pipe can handle {selected_flow} l/m >= required {F1_float} l/m ✓")
            return float(selected_size)
        else:
            # If even the largest pipe is too small, use the largest available
            max_flow_row = valid_rows.loc[valid_rows.iloc[:, 0].idxmax()]
            max_flow = max_flow_row.iloc[0]
            max_size = max_flow_row.iloc[1]
            print(f"⚠️ Required flow {F1_float} exceeds largest available capacity {max_flow}")
            print(f"⚠️ Using largest available pipe size: {max_size} (ENGINEERING REVIEW NEEDED)")
            return float(max_size)
        
    except Exception as e:
        print(f"❌ Error in get_PipeSize_Suggested: {e}")
        return 100  # Default fallback



def get_PipeLength(F1, T1, T2):
    """
    Calculate pipe length using CEILING lookup for room size
    Uses the SMALLEST room that can accommodate the power requirement
    """
    try:
        # print(f"🔍 CEILING lookup for pipe length: F1={F1}, T1={T1}, T2={T2}")
        
        # Get MW value
        mw = get_MW_divd(F1, T1, T2)
        # print(f"🔍 Calculated power requirement: {mw} MW")
        
        if mw <= 0:
            print("⚠️ Power is 0 or negative, using default length")
            return 37.5  # Default reasonable length
        
        # Check ROOM data
        if 'ROOM' not in csv_data:
            print("❌ ROOM CSV not found, using default length")
            return 37.5
        
        # Get room data
        room_df = csv_data['ROOM'].copy()
        print(f"📊 ROOM data shape: {room_df.shape}")
        
        # Convert to numeric
        room_df.iloc[:, 0] = room_df.iloc[:, 0].apply(universal_float_convert)  # Power capacity
        room_df.iloc[:, 1] = room_df.iloc[:, 1].apply(universal_float_convert)  # Room length
        
        # Remove invalid rows and sort by power capacity
        valid_rooms = room_df.dropna().sort_values(by=room_df.columns[0])
        
        power_values = valid_rooms.iloc[:, 0]
        print(f"📊 Available room power capacities: {list(power_values)}")
        
        # CEILING LOOKUP: Find the SMALLEST room that can accommodate the power
        adequate_rooms = valid_rooms[valid_rooms.iloc[:, 0] >= mw]
        
        if not adequate_rooms.empty:
            selected_power = adequate_rooms.iloc[0, 0]
            selected_length = adequate_rooms.iloc[0, 1]
            print(f"✅ CEILING match: Room capacity {selected_power} MW >= required {mw} MW → Length {selected_length} m")
            print(f"🔧 Engineering validation: Room can handle {selected_power} MW >= required {mw} MW ✓")
            return float(selected_length)
        else:
            # Use the largest available room
            max_power_row = valid_rooms.loc[valid_rooms.iloc[:, 0].idxmax()]
            max_power = max_power_row.iloc[0]
            max_length = max_power_row.iloc[1]
            print(f"⚠️ Required power {mw} MW exceeds largest room capacity {max_power} MW")
            print(f"⚠️ Using largest available room: {max_length} m (ENGINEERING REVIEW NEEDED)")
            return float(max_length)
        
    except Exception as e:
        print(f"❌ Error in get_PipeLength: {e}")
        return 37.5  # Default fallback

def get_PipeCost_perMeter(F1, pipetype="sched40"):
    """
    Calculate pipe cost per meter using CEILING lookup for pipe size
    Uses the cost for the SMALLEST pipe size that can handle the flow
    """
    try:
        print(f"🔍 CEILING lookup for pipe cost: F1={F1}, type={pipetype}")
        
        # Get pipe size using corrected ceiling lookup
        pipe_size = get_PipeSize_Suggested(F1)
        print(f"🔍 Determined pipe size (ceiling lookup): {pipe_size}")
        
        if pipe_size is None:
            print("❌ get_PipeSize_Suggested returned None")
            return 100.0  # Default cost
        
        # Get column index for pipe type
        column_index = get_pipetype_enum(pipetype)
        print(f"🔍 Pipe type column index: {column_index}")
        
        # Check PIPCOST data
        if 'PIPCOST' not in csv_data:
            print("❌ PIPCOST CSV not found")
            return 100.0
        
        pipcost_df = csv_data['PIPCOST'].copy()
        print(f"📊 PIPCOST data shape: {pipcost_df.shape}")
        
        # Convert to numeric
        pipcost_df.iloc[:, 0] = pipcost_df.iloc[:, 0].apply(universal_float_convert)  # Size
        pipcost_df.iloc[:, column_index] = pipcost_df.iloc[:, column_index].apply(universal_float_convert)  # Cost
        
        # Remove invalid rows and sort by size
        valid_costs = pipcost_df.dropna().sort_values(by=pipcost_df.columns[0])
        
        size_values = valid_costs.iloc[:, 0]
        print(f"📊 Available pipe sizes: {sorted(list(size_values))}")
        
        # CEILING LOOKUP: Find the SMALLEST size that is >= required pipe size
        adequate_sizes = valid_costs[valid_costs.iloc[:, 0] >= pipe_size]
        
        if not adequate_sizes.empty:
            selected_size = adequate_sizes.iloc[0, 0]
            selected_cost = adequate_sizes.iloc[0, column_index]
            print(f"✅ CEILING match: Size {selected_size} >= required {pipe_size} → Cost {selected_cost}")
            print(f"🔧 Engineering validation: Using size {selected_size} >= required {pipe_size} ✓")
            return float(selected_cost)
        else:
            # Use the largest available size
            max_size_row = valid_costs.loc[valid_costs.iloc[:, 0].idxmax()]
            max_size = max_size_row.iloc[0]
            max_cost = max_size_row.iloc[column_index]
            print(f"⚠️ Required size {pipe_size} exceeds largest available {max_size}")
            print(f"⚠️ Using largest available size: {max_size} → Cost {max_cost} (ENGINEERING REVIEW NEEDED)")
            return float(max_cost)
        
    except Exception as e:
        print(f"❌ Error in get_PipeCost_perMeter: {e}")
        return 100.0

def get_PipeCost_Total(F1, T1, T2, pipetype="sched40"):
    """Calculate total pipe cost"""
    try:
        print(f"🔍 Calculating total pipe cost for F1={F1}, T1={T1}, T2={T2}, type={pipetype}")
        
        # Get cost per meter (uses ceiling lookup)
        cost_per_meter = get_PipeCost_perMeter(F1, pipetype)
        print(f"🔍 Cost per meter (ceiling lookup): {cost_per_meter}")
        
        # Get pipe length (uses ceiling lookup)
        pipe_length = get_PipeLength(F1, T1, T2)
        print(f"🔍 Pipe length (ceiling lookup): {pipe_length}")
        
        # Validate both values
        if cost_per_meter is None:
            print("⚠️ Cost per meter is None, using default")
            cost_per_meter = 100.0
        
        if pipe_length is None:
            print("⚠️ Pipe length is None, using default")
            pipe_length = 37.5
        
        total_cost = float(cost_per_meter) * float(pipe_length)
        print(f"✅ Total pipe cost: {cost_per_meter} * {pipe_length} = {total_cost}")
        
        return total_cost
        
    except Exception as e:
        print(f"❌ Error in get_PipeCost_Total: {e}")
        return 3750.0  # Default reasonable total

