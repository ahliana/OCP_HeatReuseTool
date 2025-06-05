# =============================================================================
# MATERIALS MODULE
# =============================================================================

# python/physics/materials.py
"""
Material Properties for Piping, Heat Exchangers, and Thermal Systems
Reference: VDI Heat Atlas, EN Standards, Engineering Material Handbooks
European standards and specifications prioritized
"""

from .constants import WATER_PROPERTIES, EUROPEAN_PIPE_SIZES

# =============================================================================
# PIPE MATERIALS (European Standards)
# =============================================================================

PIPE_MATERIALS = {
    # European Carbon Steel (EN 10025-2)
    'carbon_steel': {
        'thermal_conductivity': 50.0,        # W/(m·K)
        'density': 7850,                     # kg/m³
        'specific_heat': 460,                # J/(kg·K)
        'roughness': 0.045e-3,               # m (absolute roughness)
        'max_temp': 450,                     # °C
        'cost_factor': 1.0,                  # Relative cost (baseline)
        'corrosion_resistance': 'fair',
        'european_standard': 'EN 10025-2',
        'typical_grades': ['S235JR', 'S275JR', 'S355JR'],
        'thermal_expansion': 12e-6,          # 1/K
        'elastic_modulus': 210e9,            # Pa
        'yield_strength': 235e6,             # Pa (S235 grade)
        'applications': ['general_piping', 'structural', 'low_pressure']
    },
    
    # European Stainless Steel 304 (EN 10088-2: 1.4301)
    'stainless_steel_304': {
        'thermal_conductivity': 16.2,        # W/(m·K)
        'density': 8000,                     # kg/m³
        'specific_heat': 500,                # J/(kg·K)
        'roughness': 0.015e-3,               # m (electropolished)
        'max_temp': 870,                     # °C
        'cost_factor': 3.5,                  # Relative to carbon steel
        'corrosion_resistance': 'excellent',
        'european_standard': 'EN 10088-2',
        'designation': '1.4301',
        'thermal_expansion': 17.3e-6,        # 1/K
        'elastic_modulus': 200e9,            # Pa
        'yield_strength': 205e6,             # Pa (0.2% proof)
        'applications': ['food_grade', 'chemical', 'clean_water']
    },
    
    # European Stainless Steel 316L (EN 10088-2: 1.4404)
    'stainless_steel_316l': {
        'thermal_conductivity': 16.3,        # W/(m·K)
        'density': 8000,                     # kg/m³
        'specific_heat': 500,                # J/(kg·K)
        'roughness': 0.015e-3,               # m
        'max_temp': 925,                     # °C
        'cost_factor': 4.8,                  # Premium grade
        'corrosion_resistance': 'superior',
        'european_standard': 'EN 10088-2',
        'designation': '1.4404',
        'thermal_expansion': 17.8e-6,        # 1/K
        'elastic_modulus': 200e9,            # Pa
        'yield_strength': 220e6,             # Pa
        'applications': ['marine', 'pharmaceutical', 'high_chloride']
    },
    
    # Copper (EN 1057 for water applications)
    'copper': {
        'thermal_conductivity': 401,         # W/(m·K)
        'density': 8960,                     # kg/m³
        'specific_heat': 385,                # J/(kg·K)
        'roughness': 0.0015e-3,              # m (drawn tubing)
        'max_temp': 250,                     # °C (practical limit)
        'cost_factor': 6.0,                  # Expensive but efficient
        'corrosion_resistance': 'good',
        'european_standard': 'EN 1057',
        'thermal_expansion': 16.5e-6,        # 1/K
        'elastic_modulus': 130e9,            # Pa
        'yield_strength': 69e6,              # Pa (soft condition)
        'applications': ['heat_exchangers', 'domestic_water', 'hvac']
    },
    
    # PVC-U (European water pipe standard EN 1452)
    'pvc_u': {
        'thermal_conductivity': 0.19,        # W/(m·K)
        'density': 1380,                     # kg/m³
        'specific_heat': 900,                # J/(kg·K)
        'roughness': 0.0015e-3,              # m (very smooth)
        'max_temp': 60,                      # °C (continuous)
        'cost_factor': 0.4,                  # Very economical
        'corrosion_resistance': 'excellent',
        'european_standard': 'EN 1452',
        'thermal_expansion': 80e-6,          # 1/K (high!)
        'elastic_modulus': 3.2e9,            # Pa
        'yield_strength': 50e6,              # Pa
        'applications': ['cold_water', 'drainage', 'low_temp']
    },
    
    # PE-HD (High Density Polyethylene - EN 12201)
    'pe_hd': {
        'thermal_conductivity': 0.48,        # W/(m·K)
        'density': 960,                      # kg/m³
        'specific_heat': 2300,               # J/(kg·K)
        'roughness': 0.007e-3,               # m
        'max_temp': 80,                      # °C (continuous)
        'cost_factor': 0.6,                  # Economical
        'corrosion_resistance': 'excellent',
        'european_standard': 'EN 12201',
        'thermal_expansion': 200e-6,         # 1/K (very high!)
        'elastic_modulus': 1.1e9,            # Pa
        'yield_strength': 26e6,              # Pa
        'applications': ['district_heating', 'water_distribution', 'underground']
    },
    
    # PPR (Polypropylene Random - European standard EN ISO 15874)
    'ppr': {
        'thermal_conductivity': 0.24,        # W/(m·K)
        'density': 900,                      # kg/m³
        'specific_heat': 1900,               # J/(kg·K)
        'roughness': 0.007e-3,               # m
        'max_temp': 95,                      # °C (short term)
        'cost_factor': 0.8,                  # Moderate cost
        'corrosion_resistance': 'excellent',
        'european_standard': 'EN ISO 15874',
        'thermal_expansion': 150e-6,         # 1/K
        'elastic_modulus': 1.5e9,            # Pa
        'yield_strength': 30e6,              # Pa
        'applications': ['hot_water', 'heating', 'chemical_resistant']
    },
}

# =============================================================================
# INSULATION MATERIALS (European Standards)
# =============================================================================

INSULATION_MATERIALS = {
    # Glass Wool (EN 13162)
    'glass_wool': {
        'thermal_conductivity': 0.036,       # W/(m·K) at 20°C
        'density': 16,                       # kg/m³
        'max_temp': 230,                     # °C
        'cost_factor': 1.0,                  # Baseline
        'european_standard': 'EN 13162',
        'fire_rating': 'A1',                # Non-combustible
        'vapor_permeability': 'high',
        'applications': ['general_insulation', 'hvac_ducts', 'pipes']
    },
    
    # Polyurethane Foam (EN 13165)
    'polyurethane_foam': {
        'thermal_conductivity': 0.026,       # W/(m·K)
        'density': 30,                       # kg/m³
        'max_temp': 100,                     # °C
        'cost_factor': 1.5,
        'european_standard': 'EN 13165',
        'fire_rating': 'E',                 # Combustible
        'vapor_permeability': 'low',
        'applications': ['refrigeration', 'district_heating', 'underground']
    },
    
    # Stone Wool/Mineral Wool (EN 13162)
    'stone_wool': {
        'thermal_conductivity': 0.038,       # W/(m·K)
        'density': 100,                      # kg/m³
        'max_temp': 750,                     # °C
        'cost_factor': 1.2,
        'european_standard': 'EN 13162',
        'fire_rating': 'A1',                # Non-combustible
        'vapor_permeability': 'high',
        'applications': ['high_temp', 'fire_protection', 'industrial']
    },
    
    # Expanded Polystyrene (EN 13163)
    'eps': {
        'thermal_conductivity': 0.040,       # W/(m·K)
        'density': 20,                       # kg/m³
        'max_temp': 75,                      # °C
        'cost_factor': 0.8,                  # Economical
        'european_standard': 'EN 13163',
        'fire_rating': 'E',
        'vapor_permeability': 'medium',
        'applications': ['building_insulation', 'foundations', 'roofs']
    },
    
    # Extruded Polystyrene (EN 13164)
    'xps': {
        'thermal_conductivity': 0.034,       # W/(m·K)
        'density': 35,                       # kg/m³
        'max_temp': 75,                      # °C
        'cost_factor': 1.4,
        'european_standard': 'EN 13164',
        'fire_rating': 'E',
        'vapor_permeability': 'very_low',
        'applications': ['wet_areas', 'underground', 'inverted_roofs']
    },
    
    # Aerogel (Premium insulation)
    'aerogel': {
        'thermal_conductivity': 0.013,       # W/(m·K) - Superior performance
        'density': 150,                      # kg/m³
        'max_temp': 650,                     # °C
        'cost_factor': 20.0,                 # Very expensive
        'european_standard': 'Custom',       # Specialized applications
        'fire_rating': 'A1',
        'vapor_permeability': 'low',
        'applications': ['space_constrained', 'extreme_performance', 'retrofit']
    },
    
    # Elastomeric Foam (European HVAC standard)
    'elastomeric_foam': {
        'thermal_conductivity': 0.040,       # W/(m·K)
        'density': 70,                       # kg/m³
        'max_temp': 105,                     # °C
        'cost_factor': 2.5,
        'european_standard': 'EN 14304',
        'fire_rating': 'BL-s3,d0',
        'vapor_permeability': 'very_low',     # Built-in vapor barrier
        'applications': ['hvac_pipes', 'refrigeration', 'condensation_control']
    },
}

# =============================================================================
# EUROPEAN COOLANT PROPERTIES (Extended Temperature Range)
# =============================================================================

COOLANT_PROPERTIES = {
    'water': WATER_PROPERTIES,  # Reference to your constants
    
    # Ethylene Glycol Solutions (VDI Heat Atlas data)
    'ethylene_glycol_30': {  # 30% by volume
        '20C': {
            'density': 1040,                 # kg/m³
            'specific_heat': 3795,           # J/(kg·K)
            'thermal_conductivity': 0.511,   # W/(m·K)
            'dynamic_viscosity': 1.99e-3,    # Pa·s
            'kinematic_viscosity': 1.91e-6,  # m²/s
            'freezing_point': -13.0,         # °C
            'boiling_point': 103.0,          # °C at 1 bar
        },
        '40C': {
            'density': 1025,
            'specific_heat': 3850,
            'thermal_conductivity': 0.520,
            'dynamic_viscosity': 1.15e-3,
            'kinematic_viscosity': 1.12e-6,
            'freezing_point': -13.0,
            'boiling_point': 103.0,
        },
    },
    
    # Propylene Glycol Solutions (Food-safe, European preference)
    'propylene_glycol_30': {  # 30% by volume
        '20C': {
            'density': 1030,                 # kg/m³
            'specific_heat': 3740,           # J/(kg·K)
            'thermal_conductivity': 0.491,   # W/(m·K)
            'dynamic_viscosity': 2.48e-3,    # Pa·s
            'kinematic_viscosity': 2.41e-6,  # m²/s
            'freezing_point': -12.0,         # °C
            'boiling_point': 102.0,          # °C at 1 bar
        },
        '40C': {
            'density': 1015,
            'specific_heat': 3800,
            'thermal_conductivity': 0.500,
            'dynamic_viscosity': 1.45e-3,
            'kinematic_viscosity': 1.43e-6,
            'freezing_point': -12.0,
            'boiling_point': 102.0,
        },
    },
    
    # Higher Concentration Glycol (for colder climates)
    'ethylene_glycol_50': {  # 50% by volume
        '20C': {
            'density': 1070,
            'specific_heat': 3350,
            'thermal_conductivity': 0.415,
            'dynamic_viscosity': 4.85e-3,
            'kinematic_viscosity': 4.53e-6,
            'freezing_point': -35.0,         # °C
            'boiling_point': 108.0,          # °C
        },
    },
}

# =============================================================================
# MATERIAL SELECTION FUNCTIONS
# =============================================================================

def select_pipe_material(temperature_max, pressure_bar, fluid_type='water', 
                        cost_priority='medium', corrosion_environment='normal'):
    """
    Select appropriate pipe material based on European standards and operating conditions.
    
    Args:
        temperature_max (float): Maximum operating temperature [°C]
        pressure_bar (float): Operating pressure [bar]
        fluid_type (str): Fluid type ('water', 'glycol', 'aggressive')
        cost_priority (str): 'low', 'medium', 'high'
        corrosion_environment (str): 'normal', 'aggressive', 'marine'
    
    Returns:
        dict: Material recommendations with European standards
    """
    suitable_materials = []
    
    for material_name, props in PIPE_MATERIALS.items():
        # Temperature check
        if temperature_max <= props['max_temp']:
            # Basic suitability assessment
            suitable = True
            reasons = []
            
            # Cost assessment
            if cost_priority == 'low' and props['cost_factor'] > 2.0:
                suitable = False
                reasons.append('too_expensive')
            elif cost_priority == 'high' and props['cost_factor'] > 6.0:
                suitable = False
                reasons.append('excessive_cost')
            
            # Corrosion assessment
            if corrosion_environment == 'aggressive':
                if props['corrosion_resistance'] not in ['excellent', 'superior']:
                    suitable = False
                    reasons.append('insufficient_corrosion_resistance')
            elif corrosion_environment == 'marine':
                if material_name not in ['stainless_steel_316l', 'copper']:
                    suitable = False
                    reasons.append('not_marine_grade')
            
            # Fluid compatibility
            if fluid_type == 'aggressive' and props['corrosion_resistance'] == 'fair':
                suitable = False
                reasons.append('poor_chemical_compatibility')
            
            # High temperature plastics check
            if temperature_max > 80 and 'pvc' in material_name or 'pe' in material_name:
                suitable = False
                reasons.append('temperature_limit_exceeded')
            
            if suitable:
                suitable_materials.append({
                    'material': material_name,
                    'properties': props,
                    'suitability_score': _calculate_suitability_score(
                        props, temperature_max, pressure_bar, cost_priority
                    )
                })
            else:
                suitable_materials.append({
                    'material': material_name,
                    'properties': props,
                    'unsuitable_reasons': reasons,
                    'suitability_score': 0
                })
    
    # Sort by suitability score
    suitable_materials.sort(key=lambda x: x.get('suitability_score', 0), reverse=True)
    
    return {
        'operating_conditions': {
            'max_temperature_c': temperature_max,
            'pressure_bar': pressure_bar,
            'fluid_type': fluid_type,
            'cost_priority': cost_priority,
            'corrosion_environment': corrosion_environment
        },
        'suitable_materials': [m for m in suitable_materials if m.get('suitability_score', 0) > 0],
        'unsuitable_materials': [m for m in suitable_materials if m.get('suitability_score', 0) == 0],
        'recommended': suitable_materials[0] if suitable_materials and suitable_materials[0].get('suitability_score', 0) > 0 else None
    }


def _calculate_suitability_score(props, temp_max, pressure_bar, cost_priority):
    """Calculate material suitability score (0-100)."""
    score = 50  # Base score
    
    # Temperature margin bonus
    temp_margin = (props['max_temp'] - temp_max) / props['max_temp']
    score += min(20, temp_margin * 40)
    
    # Cost factor penalty/bonus
    cost_factors = {'low': 2.0, 'medium': 4.0, 'high': 8.0}
    target_cost = cost_factors.get(cost_priority, 4.0)
    
    if props['cost_factor'] <= target_cost:
        score += 15
    else:
        score -= min(25, (props['cost_factor'] - target_cost) * 5)
    
    # Corrosion resistance bonus
    corr_bonus = {'fair': 0, 'good': 10, 'excellent': 20, 'superior': 25}
    score += corr_bonus.get(props['corrosion_resistance'], 0)
    
    # Thermal performance bonus (for heat exchangers)
    if props['thermal_conductivity'] > 100:
        score += 10
    elif props['thermal_conductivity'] > 50:
        score += 5
    
    return max(0, min(100, score))


def select_insulation_material(temperature_max, application='general', 
                             fire_requirements='standard', cost_priority='medium'):
    """
    Select appropriate insulation material based on European standards.
    
    Args:
        temperature_max (float): Maximum operating temperature [°C]
        application (str): Application type
        fire_requirements (str): Fire rating requirements
        cost_priority (str): Cost priority level
    
    Returns:
        dict: Insulation recommendations
    """
    suitable_insulations = []
    
    fire_rating_hierarchy = ['A1', 'A2', 'B', 'C', 'D', 'E', 'F']
    required_fire_level = {'high': 'A1', 'standard': 'B', 'low': 'E'}.get(fire_requirements, 'B')
    
    for insul_name, props in INSULATION_MATERIALS.items():
        if temperature_max <= props['max_temp']:
            # Check fire rating
            material_fire_rating = props.get('fire_rating', 'E')
            fire_suitable = (fire_rating_hierarchy.index(material_fire_rating) <= 
                           fire_rating_hierarchy.index(required_fire_level))
            
            if fire_suitable:
                # Calculate score
                score = 50
                
                # Temperature margin
                temp_margin = (props['max_temp'] - temperature_max) / props['max_temp']
                score += min(25, temp_margin * 50)
                
                # Thermal performance bonus
                if props['thermal_conductivity'] < 0.025:
                    score += 20
                elif props['thermal_conductivity'] < 0.035:
                    score += 10
                
                # Cost consideration
                cost_targets = {'low': 1.5, 'medium': 5.0, 'high': 15.0}
                target_cost = cost_targets.get(cost_priority, 5.0)
                
                if props['cost_factor'] <= target_cost:
                    score += 15
                else:
                    score -= min(20, (props['cost_factor'] - target_cost) * 2)
                
                suitable_insulations.append({
                    'material': insul_name,
                    'properties': props,
                    'suitability_score': max(0, score)
                })
    
    suitable_insulations.sort(key=lambda x: x['suitability_score'], reverse=True)
    
    return {
        'requirements': {
            'max_temperature_c': temperature_max,
            'application': application,
            'fire_requirements': fire_requirements,
            'cost_priority': cost_priority
        },
        'suitable_materials': suitable_insulations,
        'recommended': suitable_insulations[0] if suitable_insulations else None
    }


def get_material_properties(material_name, material_type='pipe'):
    """
    Get complete material properties for a specific material.
    
    Args:
        material_name (str): Material name
        material_type (str): 'pipe' or 'insulation'
    
    Returns:
        dict: Complete material properties
    """
    if material_type == 'pipe':
        return PIPE_MATERIALS.get(material_name)
    elif material_type == 'insulation':
        return INSULATION_MATERIALS.get(material_name)
    else:
        return None


def validate_material_selection():
    """
    Validate material property data for consistency.
    
    Returns:
        list: Validation results
    """
    results = []
    
    # Check pipe materials
    for name, props in PIPE_MATERIALS.items():
        # Check thermal conductivity ranges
        if props['thermal_conductivity'] < 0.1 or props['thermal_conductivity'] > 500:
            results.append({
                'test': f'Thermal conductivity range check - {name}',
                'status': 'WARNING',
                'value': props['thermal_conductivity'],
                'message': 'Unusual thermal conductivity value'
            })
        else:
            results.append({
                'test': f'Thermal conductivity range check - {name}',
                'status': 'PASS'
            })
        
        # Check density ranges
        if props['density'] < 500 or props['density'] > 12000:
            results.append({
                'test': f'Density range check - {name}',
                'status': 'WARNING',
                'value': props['density'],
                'message': 'Unusual density value'
            })
        else:
            results.append({
                'test': f'Density range check - {name}',
                'status': 'PASS'
            })
    
    # Check insulation materials
    for name, props in INSULATION_MATERIALS.items():
        # Insulation should have low thermal conductivity
        if props['thermal_conductivity'] > 0.1:
            results.append({
                'test': f'Insulation performance check - {name}',
                'status': 'WARNING',
                'value': props['thermal_conductivity'],
                'message': 'High thermal conductivity for insulation'
            })
        else:
            results.append({
                'test': f'Insulation performance check - {name}',
                'status': 'PASS'
            })
    
    return results


if __name__ == "__main__":
    print("Materials Module - European Standards")
    print("=" * 40)
    
    # Run validation
    validation_results = validate_material_selection()
    passed = sum(1 for r in validation_results if r['status'] == 'PASS')
    total = len(validation_results)
    print(f"Validation: {passed}/{total} tests passed")
    
    print(f"\nAvailable pipe materials: {list(PIPE_MATERIALS.keys())}")
    print(f"Available insulation materials: {list(INSULATION_MATERIALS.keys())}")
    
    # Example material selection
    print(f"\nExample: Material selection for 60°C water system")
    selection = select_pipe_material(60, 6, 'water', 'medium', 'normal')
    if selection['recommended']:
        rec = selection['recommended']
        print(f"Recommended: {rec['material']}")
        print(f"Standard: {rec['properties']['european_standard']}")
        print(f"Cost factor: {rec['properties']['cost_factor']}")