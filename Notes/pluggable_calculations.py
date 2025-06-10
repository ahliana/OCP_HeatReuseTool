# python/core/calculations/base.py
"""
Base calculation interface - makes adding new calculations incredibly easy
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import inspect


class BaseCalculation(ABC):
    """
    Base class for all calculations
    
    This makes it trivial to add new calculations:
    1. Inherit from BaseCalculation
    2. Define inputs, outputs, and description
    3. Implement calculate() method
    4. Register in the registry
    """
    
    def __init__(self, name: str, description: str, category: str = "general"):
        self.name = name
        self.description = description
        self.category = category
        self._inputs = {}
        self._outputs = {}
        self._physics_references = []
    
    def add_input(self, name: str, description: str, unit: str, 
                  min_value: Optional[float] = None, max_value: Optional[float] = None,
                  default: Optional[float] = None):
        """Add an input parameter with validation"""
        self._inputs[name] = {
            'description': description,
            'unit': unit,
            'min_value': min_value,
            'max_value': max_value,
            'default': default
        }
    
    def add_output(self, name: str, description: str, unit: str):
        """Add an output parameter"""
        self._outputs[name] = {
            'description': description,
            'unit': unit
        }
    
    def add_physics_reference(self, reference: str):
        """Add a physics/engineering reference for this calculation"""
        self._physics_references.append(reference)
    
    @abstractmethod
    def calculate(self, **kwargs) -> Dict[str, float]:
        """
        Perform the calculation
        
        Args:
            **kwargs: Input parameters
        
        Returns:
            Dict[str, float]: Output parameters
        """
        pass
    
    def validate_inputs(self, **kwargs) -> Dict[str, str]:
        """
        Validate input parameters
        
        Returns:
            Dict[str, str]: Error messages (empty if all valid)
        """
        errors = {}
        
        # Check required inputs
        for input_name, input_config in self._inputs.items():
            if input_name not in kwargs:
                if input_config['default'] is None:
                    errors[input_name] = f"Required input '{input_name}' missing"
                else:
                    kwargs[input_name] = input_config['default']
        
        # Validate ranges
        for input_name, value in kwargs.items():
            if input_name in self._inputs:
                config = self._inputs[input_name]
                if config['min_value'] is not None and value < config['min_value']:
                    errors[input_name] = f"{input_name} ({value}) below minimum {config['min_value']} {config['unit']}"
                if config['max_value'] is not None and value > config['max_value']:
                    errors[input_name] = f"{input_name} ({value}) above maximum {config['max_value']} {config['unit']}"
        
        return errors
    
    def get_info(self) -> Dict[str, Any]:
        """Get complete information about this calculation"""
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'inputs': self._inputs,
            'outputs': self._outputs,
            'physics_references': self._physics_references
        }


# python/core/calculations/heat_transfer.py
"""
Heat Transfer Calculations using standard physics formulas
"""

from .base import BaseCalculation
from python.physics.thermodynamics import sensible_heat_transfer
from python.physics.units import (
    liters_per_minute_to_kg_per_second,
    watts_to_megawatts,
    validate_temperature_range,
    validate_flow_rate
)
from python.physics.constants import WATER_SPECIFIC_HEAT_20C


class HeatTransferCalculation(BaseCalculation):
    """
    Standard sensible heat transfer calculation
    
    Uses the fundamental thermodynamic equation: Q = ṁ × cp × ΔT
    """
    
    def __init__(self):
        super().__init__(
            name="Heat Transfer Rate",
            description="Calculate heat transfer rate using standard thermodynamic formulas",
            category="thermodynamics"
        )
        
        # Define inputs with validation
        self.add_input("flow_rate", "Volumetric flow rate", "L/min", 
                      min_value=1, max_value=50000, default=1000)
        self.add_input("inlet_temperature", "Inlet temperature", "°C", 
                      min_value=-10, max_value=100, default=20)
        self.add_input("outlet_temperature", "Outlet temperature", "°C", 
                      min_value=-10, max_value=100, default=30)
        self.add_input("specific_heat", "Specific heat capacity", "J/(kg·K)", 
                      min_value=1000, max_value=10000, default=WATER_SPECIFIC_HEAT_20C)
        
        # Define outputs
        self.add_output("heat_rate_watts", "Heat transfer rate", "W")
        self.add_output("heat_rate_mw", "Heat transfer rate", "MW")
        self.add_output("delta_temperature", "Temperature difference", "°C")
        self.add_output("mass_flow_rate", "Mass flow rate", "kg/s")
        
        # Add physics references
        self.add_physics_reference("Fundamentals of Heat and Mass Transfer, Incropera & DeWitt, Ch. 1")
        self.add_physics_reference("Heat Transfer, Holman, Ch. 1")
        self.add_physics_reference("Thermodynamics: An Engineering Approach, Cengel & Boles, Ch. 2")
    
    def calculate(self, **kwargs) -> Dict[str, float]:
        """Calculate heat transfer rate"""
        # Validate inputs first
        errors = self.validate_inputs(**kwargs)
        if errors:
            raise ValueError(f"Input validation failed: {errors}")
        
        # Extract parameters
        flow_rate = kwargs['flow_rate']
        inlet_temp = kwargs['inlet_temperature']
        outlet_temp = kwargs['outlet_temperature']
        specific_heat = kwargs.get('specific_heat', WATER_SPECIFIC_HEAT_20C)
        
        # Additional physics validation
        validate_temperature_range(inlet_temp)
        validate_temperature_range(outlet_temp)
        validate_flow_rate(flow_rate)
        
        # Convert units to standard SI
        mass_flow = liters_per_minute_to_kg_per_second(flow_rate)
        delta_t = outlet_temp - inlet_temp
        
        # Calculate using standard physics formula
        heat_watts = sensible_heat_transfer(mass_flow, specific_heat, delta_t)
        heat_mw = watts_to_megawatts(heat_watts)
        
        return {
            'heat_rate_watts': heat_watts,
            'heat_rate_mw': heat_mw,
            'delta_temperature': delta_t,
            'mass_flow_rate': mass_flow
        }


class PipeSizingCalculation(BaseCalculation):
    """
    Pipe sizing based on velocity limits and pressure drop
    """
    
    def __init__(self):
        super().__init__(
            name="Pipe Sizing",
            description="Size pipes based on flow velocity and pressure drop limits",
            category="fluid_mechanics"
        )
        
        self.add_input("flow_rate", "Volumetric flow rate", "L/min", 
                      min_value=1, max_value=50000)
        self.add_input("max_velocity", "Maximum velocity", "m/s", 
                      min_value=0.5, max_value=10, default=2.5)
        self.add_input("pipe_length", "Pipe length", "m", 
                      min_value=1, max_value=1000, default=50)
        
        self.add_output("recommended_diameter", "Recommended pipe diameter", "mm")
        self.add_output("actual_velocity", "Actual velocity", "m/s")
        self.add_output("reynolds_number", "Reynolds number", "dimensionless")
        self.add_output("pressure_drop", "Pressure drop", "Pa")
        
        self.add_physics_reference("Fluid Mechanics, White, Ch. 6")
        self.add_physics_reference("Perry's Chemical Engineers' Handbook, Ch. 6")
    
    def calculate(self, **kwargs) -> Dict[str, float]:
        """Calculate recommended pipe size"""
        import math
        from python.physics.materials import STANDARD_PIPE_SIZES
        from python.physics.thermodynamics import reynolds_number_pipe
        from python.physics.units import liters_per_minute_to_m3_per_second
        from python.physics.constants import WATER_DENSITY_20C, WATER_KINEMATIC_VISCOSITY_20C
        
        errors = self.validate_inputs(**kwargs)
        if errors:
            raise ValueError(f"Input validation failed: {errors}")
        
        flow_rate_lpm = kwargs['flow_rate']
        max_velocity = kwargs['max_velocity']
        pipe_length = kwargs['pipe_length']
        
        # Convert flow rate to m³/s
        flow_rate_m3s = liters_per_minute_to_m3_per_second(flow_rate_lpm)
        
        # Calculate minimum diameter based on velocity constraint
        # Q = A × v = (π × D²/4) × v
        # D = √(4Q / (π × v))
        min_diameter = math.sqrt(4 * flow_rate_m3s / (math.pi * max_velocity))
        min_diameter_mm = min_diameter * 1000
        
        # Find next larger standard pipe size
        available_sizes = sorted(STANDARD_PIPE_SIZES.keys())
        selected_size = None
        for size in available_sizes:
            pipe_info = STANDARD_PIPE_SIZES[size]
            if pipe_info['inner_diameter'] >= min_diameter_mm:
                selected_size = size
                break
        
        if selected_size is None:
            selected_size = available_sizes[-1]  # Use largest available
        
        # Calculate actual performance
        actual_diameter = STANDARD_PIPE_SIZES[selected_size]['inner_diameter'] / 1000  # Convert to m
        actual_area = math.pi * (actual_diameter / 2) ** 2
        actual_velocity = flow_rate_m3s / actual_area
        
        # Calculate Reynolds number
        reynolds = reynolds_number_pipe(actual_velocity, actual_diameter, WATER_KINEMATIC_VISCOSITY_20C)
        
        # Estimate pressure drop (simplified Darcy-Weisbach)
        friction_factor = 0.3164 / (reynolds ** 0.25) if reynolds > 4000 else 64 / reynolds
        pressure_drop = friction_factor * (pipe_length / actual_diameter) * (WATER_DENSITY_20C * actual_velocity ** 2 / 2)
        
        return {
            'recommended_diameter': STANDARD_PIPE_SIZES[selected_size]['inner_diameter'],
            'actual_velocity': actual_velocity,
            'reynolds_number': reynolds,
            'pressure_drop': pressure_drop
        }


# python/core/calculations/registry.py
"""
Calculation Registry - Dynamic management of available calculations
"""

from typing import Dict, List, Type, Optional
from .base import BaseCalculation


class CalculationRegistry:
    """
    Registry for all available calculations
    
    This makes it easy to:
    1. Add new calculations dynamically
    2. List available calculations by category
    3. Get calculation metadata
    4. Validate calculation compatibility
    """
    
    def __init__(self):
        self._calculations: Dict[str, BaseCalculation] = {}
        self._categories: Dict[str, List[str]] = {}
    
    def register(self, calculation: BaseCalculation):
        """Register a new calculation"""
        self._calculations[calculation.name] = calculation
        
        # Add to category
        if calculation.category not in self._categories:
            self._categories[calculation.category] = []
        if calculation.name not in self._categories[calculation.category]:
            self._categories[calculation.category].append(calculation.name)
    
    def register_class(self, calculation_class: Type[BaseCalculation]):
        """Register a calculation class (creates instance automatically)"""
        instance = calculation_class()
        self.register(instance)
    
    def get_calculation(self, name: str) -> Optional[BaseCalculation]:
        """Get a specific calculation by name"""
        return self._calculations.get(name)
    
    def list_calculations(self, category: Optional[str] = None) -> List[str]:
        """List available calculations, optionally filtered by category"""
        if category:
            return self._categories.get(category, [])
        return list(self._calculations.keys())
    
    def list_categories(self) -> List[str]:
        """List all available categories"""
        return list(self._categories.keys())
    
    def get_calculation_info(self, name: str) -> Optional[Dict]:
        """Get detailed information about a calculation"""
        calc = self.get_calculation(name)
        return calc.get_info() if calc else None
    
    def find_calculations_by_input(self, input_name: str) -> List[str]:
        """Find calculations that accept a specific input"""
        matching = []
        for name, calc in self._calculations.items():
            if input_name in calc._inputs:
                matching.append(name)
        return matching
    
    def find_calculations_by_output(self, output_name: str) -> List[str]:
        """Find calculations that produce a specific output"""
        matching = []
        for name, calc in self._calculations.items():
            if output_name in calc._outputs:
                matching.append(name)
        return matching
    
    def validate_calculation_chain(self, calculation_names: List[str]) -> Dict[str, List[str]]:
        """
        Validate that outputs of one calculation can feed inputs of another
        
        Returns:
            Dict with 'valid_chains' and 'missing_connections'
        """
        valid_chains = []
        missing_connections = []
        
        for i in range(len(calculation_names) - 1):
            current_name = calculation_names[i]
            next_name = calculation_names[i + 1]
            
            current_calc = self.get_calculation(current_name)
            next_calc = self.get_calculation(next_name)
            
            if not current_calc or not next_calc:
                continue
            
            # Check if any outputs of current match inputs of next
            current_outputs = set(current_calc._outputs.keys())
            next_inputs = set(next_calc._inputs.keys())
            
            connections = current_outputs.intersection(next_inputs)
            
            if connections:
                valid_chains.append(f"{current_name} → {next_name} ({', '.join(connections)})")
            else:
                missing_connections.append(f"{current_name} → {next_name}")
        
        return {
            'valid_chains': valid_chains,
            'missing_connections': missing_connections
        }


# Global registry instance
calculation_registry = CalculationRegistry()

# Auto-register standard calculations
def register_standard_calculations():
    """Register all standard calculations"""
    from .heat_transfer import HeatTransferCalculation, PipeSizingCalculation
    
    calculation_registry.register_class(HeatTransferCalculation)
    calculation_registry.register_class(PipeSizingCalculation)
    
    # Add more calculations here as they're developed
    # calculation_registry.register_class(CostAnalysisCalculation)
    # calculation_registry.register_class(PumpSizingCalculation)

# Auto-register when module is imported
register_standard_calculations()