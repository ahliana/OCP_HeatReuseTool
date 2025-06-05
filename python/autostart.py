"""
Heat Reuse Tool - Autostart Module
Handles automatic loading of all components in the correct order
"""

import sys
import os
import traceback
from pathlib import Path

# Global state tracking
_loaded_modules = {}
_load_errors = []
_csv_data = {}

def print_status(message, status="info"):
    """Print formatted status messages"""
    icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
    print(f"{icons.get(status, 'ℹ️')} {message}")

def safe_import(module_path, function_name=None):
    """Safely import a module or function with error handling"""
    try:
        if function_name:
            module = __import__(module_path, fromlist=[function_name])
            return getattr(module, function_name)
        else:
            return __import__(module_path)
    except ImportError as e:
        print_status(f"Could not import {module_path}: {e}", "warning")
        return None
    except Exception as e:
        print_status(f"Error importing {module_path}: {e}", "error")
        return None










def load_physics_constants():
    """Load physics constants and base functions"""
    try:
        print_status("Loading physics constants...", "info")
        
        # Import physics modules and make key components available globally
        from . import physics
        from .physics import constants, units, thermodynamics, materials
        
        # Import engineering calculations (high-level functions)
        try:
            from . import engineering_calculations
            globals()['engineering_calculations'] = engineering_calculations
            
            # Make key engineering functions globally available
            globals().update({
                'datacenter_cooling_analysis': getattr(engineering_calculations, 'datacenter_cooling_analysis', None),
                'pipe_sizing_analysis': getattr(engineering_calculations, 'pipe_sizing_analysis', None),
                'heat_exchanger_analysis': getattr(engineering_calculations, 'heat_exchanger_analysis', None),
                'validate_physics_calculations': getattr(engineering_calculations, 'validate_physics_calculations', None),
                'get_water_properties': getattr(engineering_calculations, 'get_water_properties', None),
                'quick_power_calculation': getattr(engineering_calculations, 'quick_power_calculation', None),
                'get_MW': getattr(engineering_calculations, 'get_MW', None),
                'get_MW': getattr(engineering_calculations, 'get_MW_divd', None),
            })
            print_status("  Engineering calculations loaded", "success")
            
        except ImportError:
            print_status("  engineering_calculations.py not found (optional)", "warning")
        
        # Make key constants globally available
        globals().update({
            'WATER_SPECIFIC_HEAT': getattr(constants, 'WATER_SPECIFIC_HEAT', 4186),
            'WATER_DENSITY': getattr(constants, 'WATER_DENSITY', 1000),
            'WATER_PROPERTIES': getattr(materials, 'WATER_PROPERTIES', {}),
        })
        
        _loaded_modules['physics'] = True
        print_status("Physics modules loaded", "success")
        return True
        
    except Exception as e:
        error_msg = f"Failed to load physics modules: {e}"
        print_status(error_msg, "error")
        _load_errors.append(error_msg)
        return False

def load_data_utilities():
    """Load data handling utilities"""
    try:
        print_status("Loading data utilities...", "info")
        
        # Import data modules and specific functions
        from .data.converter import universal_float_convert
        from .data import loader, validator
        
        # Make key functions globally available
        globals().update({
            'universal_float_convert': universal_float_convert,
            'load_csv_files': getattr(loader, 'load_csv_files', None),
            'get_dataframe': getattr(loader, 'get_dataframe', None),
        })
        
        _loaded_modules['data'] = True
        print_status("Data utilities loaded", "success")
        return True
        
    except Exception as e:
        error_msg = f"Failed to load data utilities: {e}"
        print_status(error_msg, "error")
        _load_errors.append(error_msg)
        return False

def load_csv_data():
    """Load all CSV data files"""
    try:
        print_status("Loading CSV data files...", "info")
        
        # Try to get the load_csv_files function
        load_csv_files = globals().get('load_csv_files')
        
        if not load_csv_files:
            # Try direct import if not available globally yet
            try:
                from .data.loader import load_csv_files
            except ImportError:
                print_status("CSV loader not available - using existing notebook data", "warning")
                # Try to use csv_data from the notebook's global scope if available
                import __main__
                if hasattr(__main__, 'csv_data'):
                    _csv_data.update(__main__.csv_data)
                    globals()['csv_data'] = __main__.csv_data
                    print_status(f"Using existing CSV data: {len(__main__.csv_data)} files", "success")
                else:
                    print_status("No CSV data available", "warning")
                _loaded_modules['csv_data'] = True
                return True
        
        # Try to load from default location
        data_dir = Path.cwd() / "Data"
        if not data_dir.exists():
            data_dir = Path.cwd()  # Fallback to current directory
        
        csv_data = load_csv_files(str(data_dir))
        
        if csv_data:
            # Make CSV data globally available
            globals()['csv_data'] = csv_data
            _csv_data.update(csv_data)
            
            print_status(f"Loaded {len(csv_data)} CSV files", "success")
            for name in csv_data.keys():
                print_status(f"  - {name}.csv", "info")
        else:
            print_status("No CSV files found", "warning")
        
        _loaded_modules['csv_data'] = True
        return True
        
    except Exception as e:
        error_msg = f"Failed to load CSV data: {e}"
        print_status(error_msg, "error")
        _load_errors.append(error_msg)
        return False

def load_core_calculations():
    """Load core calculation modules"""
    try:
        print_status("Loading core calculations...", "info")
        
        # Import calculation modules (handle missing modules gracefully)
        calculation_modules = {}
        
        try:
            from .core.calculations import base
            calculation_modules['base'] = base
        except ImportError:
            print_status("  calculations.base not found (optional)", "warning")
        
        try:
            from .core.calculations import heat_transfer
            calculation_modules['heat_transfer'] = heat_transfer
        except ImportError:
            print_status("  calculations.heat_transfer not found (optional)", "warning")
        
        try:
            from .core.calculations import pipe_sizing
            calculation_modules['pipe_sizing'] = pipe_sizing
        except ImportError:
            print_status("  calculations.pipe_sizing not found (optional)", "warning")
        
        try:
            from .core.calculations import cost_analysis
            calculation_modules['cost_analysis'] = cost_analysis
        except ImportError:
            print_status("  calculations.cost_analysis not found (optional)", "warning")
        
        try:
            from .core import lookup
            calculation_modules['lookup'] = lookup
            
            # Make key lookup functions available
            globals().update({
                'lookup_allhx_data': getattr(lookup, 'lookup_allhx_data', None),
                'get_lookup_value': getattr(lookup, 'get_lookup_value', None),
            })
        except ImportError:
            print_status("  core.lookup not found (optional)", "warning")
        
        _loaded_modules['calculations'] = True
        print_status("Core calculations loaded", "success")
        return True
        
    except Exception as e:
        error_msg = f"Failed to load calculations: {e}"
        print_status(error_msg, "error")
        _load_errors.append(error_msg)
        return False

def load_system_analysis():
    """Load system analysis module"""
    try:
        print_status("Loading system analysis...", "info")
        
        from .core.system_analysis import get_complete_system_analysis, validate_user_inputs
        
        # Make key functions globally available
        globals()['get_complete_system_analysis'] = get_complete_system_analysis
        globals()['validate_user_inputs'] = validate_user_inputs
        
        _loaded_modules['system_analysis'] = True
        print_status("System analysis loaded", "success")
        return True
        
    except Exception as e:
        error_msg = f"Failed to load system analysis: {e}"
        print_status(error_msg, "error")
        _load_errors.append(error_msg)
        return False

def load_ui_components():
    """Load UI components"""
    try:
        print_status("Loading UI components...", "info")
        
        # Import UI modules (handle missing modules gracefully)
        ui_modules = {}
        
        try:
            from .ui import interface
            ui_modules['interface'] = interface
            globals()['create_heat_reuse_tool'] = getattr(interface, 'create_heat_reuse_tool', None)
        except ImportError:
            print_status("  ui.interface not found (optional)", "warning")
        
        try:
            from .ui import widgets
            ui_modules['widgets'] = widgets
        except ImportError:
            print_status("  ui.widgets not found (optional)", "warning")
        
        try:
            from .ui import display
            ui_modules['display'] = display
        except ImportError:
            print_status("  ui.display not found (optional)", "warning")
        
        try:
            from .ui import charts
            ui_modules['charts'] = charts
        except ImportError:
            print_status("  ui.charts not found (optional)", "warning")
        
        _loaded_modules['ui'] = True
        print_status("UI components loaded", "success")
        return True
        
    except Exception as e:
        error_msg = f"Failed to load UI components: {e}"
        print_status(error_msg, "error")
        _load_errors.append(error_msg)
        return False

def load_testing_framework():
    """Load testing and validation framework"""
    try:
        print_status("Loading testing framework...", "info")
        
        # Import testing modules (handle missing modules gracefully)
        testing_modules = {}
        
        try:
            from .testing import visual_test_runner
            testing_modules['visual_test_runner'] = visual_test_runner
            globals()['VisualTestRunner'] = getattr(visual_test_runner, 'VisualTestRunner', None)
        except ImportError:
            print_status("  testing.visual_test_runner not found (optional)", "warning")
        
        try:
            from .testing import benchmarks
            testing_modules['benchmarks'] = benchmarks
        except ImportError:
            print_status("  testing.benchmarks not found (optional)", "warning")
        
        try:
            from .testing import validators
            testing_modules['validators'] = validators
        except ImportError:
            print_status("  testing.validators not found (optional)", "warning")
        
        _loaded_modules['testing'] = True
        print_status("Testing framework loaded", "success")
        return True
        
    except Exception as e:
        error_msg = f"Failed to load testing framework: {e}"
        print_status(error_msg, "error")
        _load_errors.append(error_msg)
        return False

def validate_critical_functions():
    """Validate that critical functions are available"""
    try:
        print_status("Validating critical functions...", "info")
        
        critical_functions = [
            'universal_float_convert',
            'get_complete_system_analysis',
        ]
        
        missing_functions = []
        for func_name in critical_functions:
            if func_name not in globals():
                missing_functions.append(func_name)
        
        if missing_functions:
            print_status(f"Missing critical functions: {missing_functions}", "warning")
            return False
        
        print_status("All critical functions available", "success")
        return True
        
    except Exception as e:
        error_msg = f"Validation failed: {e}"
        print_status(error_msg, "error")
        return False

def run_quick_tests():
    """Run quick validation tests"""
    try:
        print_status("Running quick validation tests...", "info")
        
        # Test 1: Data conversion
        if 'universal_float_convert' in globals():
            test_val = universal_float_convert("1,493")
            if test_val == 1493.0:
                print_status("Data conversion test: PASS", "success")
            else:
                print_status(f"Data conversion test: FAIL ({test_val})", "warning")
        
        # Test 2: CSV data availability
        if _csv_data:
            required_csvs = ['ALLHX', 'PIPCOST', 'PIPSZ']
            missing_csvs = [csv for csv in required_csvs if csv not in _csv_data]
            if missing_csvs:
                print_status(f"Missing CSV files: {missing_csvs}", "warning")
            else:
                print_status("Required CSV files: PASS", "success")
        
        # Test 3: System analysis
        if 'get_complete_system_analysis' in globals():
            try:
                # Quick test with default parameters
                analysis = get_complete_system_analysis(1, 20, 10, 2)
                if analysis:
                    print_status("System analysis test: PASS", "success")
                else:
                    print_status("System analysis test: FAIL", "warning")
            except Exception as e:
                print_status(f"System analysis test: ERROR ({e})", "warning")
        
        # Test 4: Engineering calculations validation
        if 'validate_physics_calculations' in globals():
            try:
                validation_results = validate_physics_calculations()
                passed_tests = sum(1 for result in validation_results if result.get('status') == 'PASS')
                total_tests = len(validation_results)
                print_status(f"Physics validation: {passed_tests}/{total_tests} tests PASS", "success")
            except Exception as e:
                print_status(f"Physics validation: ERROR ({e})", "warning")
        
        # Test 5: Engineering functions availability
        engineering_functions = [
            'datacenter_cooling_analysis',
            'pipe_sizing_analysis', 
            'heat_exchanger_analysis',
            'quick_power_calculation'
        ]
        available_eng_functions = [func for func in engineering_functions if func in globals()]
        if available_eng_functions:
            print_status(f"Engineering functions: {len(available_eng_functions)}/{len(engineering_functions)} available", "success")
        
        return True
        
    except Exception as e:
        print_status(f"Quick tests failed: {e}", "error")
        return False

def print_load_summary():
    """Print summary of loading results"""
    print("\n" + "="*50)
    print("🔧 HEAT REUSE TOOL - LOAD SUMMARY")
    print("="*50)
    
    # Show loaded modules
    loaded_count = sum(1 for loaded in _loaded_modules.values() if loaded)
    total_modules = len(_loaded_modules)
    print(f"📦 Modules loaded: {loaded_count}/{total_modules}")
    
    for module, loaded in _loaded_modules.items():
        status = "✅" if loaded else "❌"
        print(f"  {status} {module}")
    
    # Show CSV data
    if _csv_data:
        print(f"📊 CSV files: {len(_csv_data)} loaded")
        for name in sorted(_csv_data.keys()):
            print(f"  📄 {name}")
    
    # Show errors
    if _load_errors:
        print(f"⚠️ Errors: {len(_load_errors)}")
        for error in _load_errors:
            print(f"  ❌ {error}")
    
    # Show available functions
    available_functions = [name for name in globals() if not name.startswith('_') and callable(globals()[name])]
    if available_functions:
        print(f"🔧 Available functions: {len(available_functions)}")
        for func in sorted(available_functions)[:10]:  # Show first 10
            print(f"  🛠️ {func}")
        if len(available_functions) > 10:
            print(f"  ... and {len(available_functions) - 10} more")
    
    print("="*50)
    if loaded_count == total_modules and not _load_errors:
        print("🎉 ALL SYSTEMS READY!")
    elif loaded_count > 0:
        print("⚠️ PARTIAL LOAD - Some features may be limited")
    else:
        print("❌ LOAD FAILED - Check errors above")
    print("="*50)









# =============================================================================
# DEBUG VERSION OF expose_functions_to_main()
# Replace your current function with this debug version
# =============================================================================

def expose_functions_to_main():
    """
    Debug version: Expose key functions to the main/__main__ namespace
    """
    print("\n🔍 DEBUG: Starting expose_functions_to_main()")
    
    try:
        # Step 1: Check if we can import __main__
        print("🔍 Step 1: Importing __main__...")
        import __main__
        print(f"✅ __main__ imported successfully: {type(__main__)}")
        print(f"🔍 __main__ has {len(dir(__main__))} attributes")
        
        # Step 2: Try to import universal_float_convert
        print("\n🔍 Step 2: Importing universal_float_convert...")
        try:
            from .data.converter import universal_float_convert
            print(f"✅ universal_float_convert imported: {type(universal_float_convert)}")
            print(f"🔍 Function location: {universal_float_convert.__module__}")
            
            # Test the function works
            test_result = universal_float_convert("1,493")
            print(f"✅ Function test passed: {test_result}")
            
        except ImportError as e:
            print(f"❌ Failed to import universal_float_convert: {e}")
            return False
        except Exception as e:
            print(f"❌ Error testing universal_float_convert: {e}")
            return False
        
        # Step 3: Try to import other functions
        print("\n🔍 Step 3: Importing other functions...")
        
        try:
            from .core.system_analysis import get_complete_system_analysis, validate_user_inputs
            print(f"✅ System analysis functions imported")
        except ImportError as e:
            print(f"⚠️ Could not import system analysis: {e}")
            get_complete_system_analysis = None
            validate_user_inputs = None
        
        try:
            from .physics.engineering_calculations import get_MW, get_MW_divd
            print(f"✅ Engineering calculations imported")
        except ImportError as e:
            print(f"⚠️ Could not import engineering calculations: {e}")
            get_MW = None
            get_MW_divd = None
        
        # Step 4: Prepare functions to expose
        print("\n🔍 Step 4: Preparing functions to expose...")
        functions_to_expose = {}
        
        if universal_float_convert:
            functions_to_expose['universal_float_convert'] = universal_float_convert
            
        if get_complete_system_analysis:
            functions_to_expose['get_complete_system_analysis'] = get_complete_system_analysis
            
        if validate_user_inputs:
            functions_to_expose['validate_user_inputs'] = validate_user_inputs
            
        if get_MW:
            functions_to_expose['get_MW'] = get_MW
            
        if get_MW_divd:
            functions_to_expose['get_MW_divd'] = get_MW_divd
        
        print(f"🔍 Functions to expose: {list(functions_to_expose.keys())}")
        
        # Step 5: Expose functions to __main__
        print("\n🔍 Step 5: Exposing functions to __main__...")
        
        for name, func in functions_to_expose.items():
            try:
                print(f"🔍 Setting __main__.{name} = {func}")
                setattr(__main__, name, func)
                
                # Verify it was set
                if hasattr(__main__, name):
                    retrieved_func = getattr(__main__, name)
                    print(f"✅ __main__.{name} set successfully: {type(retrieved_func)}")
                    
                    # Test if it's callable
                    if callable(retrieved_func):
                        print(f"✅ __main__.{name} is callable")
                    else:
                        print(f"❌ __main__.{name} is NOT callable")
                else:
                    print(f"❌ __main__.{name} NOT found after setting")
                    
            except Exception as e:
                print(f"❌ Error setting __main__.{name}: {e}")
        
        # Step 6: Final verification
        print("\n🔍 Step 6: Final verification...")
        
        # Check what's actually in __main__ now
        main_functions = [attr for attr in dir(__main__) if not attr.startswith('_')]
        print(f"🔍 Functions now in __main__: {main_functions}")
        
        # Specifically check for our target function
        if hasattr(__main__, 'universal_float_convert'):
            print("✅ universal_float_convert found in __main__")
            try:
                test_func = getattr(__main__, 'universal_float_convert')
                test_result = test_func("1,493")
                print(f"✅ __main__.universal_float_convert test: {test_result}")
            except Exception as e:
                print(f"❌ Error testing __main__.universal_float_convert: {e}")
        else:
            print("❌ universal_float_convert NOT found in __main__")
        
        print(f"\n✅ expose_functions_to_main completed")
        print(f"✅ Exposed {len(functions_to_expose)} functions to notebook")
        
        return True
        
    except Exception as e:
        print(f"❌ Critical error in expose_functions_to_main: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return False

# =============================================================================
# ADDITIONAL DEBUG FUNCTION - ADD THIS TOO
# =============================================================================

def debug_notebook_namespace():
    """
    Debug function to check what's available in the notebook namespace
    Call this from the notebook to see what's available
    """
    import __main__
    
    print("🔍 DEBUG: Notebook Namespace Analysis")
    print("=" * 50)
    
    # Check all attributes
    all_attrs = dir(__main__)
    print(f"Total attributes in __main__: {len(all_attrs)}")
    
    # Filter for functions
    functions = []
    variables = []
    modules = []
    
    for attr_name in all_attrs:
        if not attr_name.startswith('_'):
            try:
                attr_value = getattr(__main__, attr_name)
                if callable(attr_value):
                    if hasattr(attr_value, '__module__'):
                        functions.append(f"{attr_name} (from {attr_value.__module__})")
                    else:
                        functions.append(f"{attr_name} (callable)")
                elif hasattr(attr_value, '__module__'):
                    modules.append(f"{attr_name} (module)")
                else:
                    variables.append(f"{attr_name} = {type(attr_value)}")
            except:
                variables.append(f"{attr_name} (error accessing)")
    
    print(f"\nFunctions ({len(functions)}):")
    for func in functions:
        print(f"  🔧 {func}")
    
    print(f"\nModules ({len(modules)}):")
    for mod in modules:
        print(f"  📦 {mod}")
    
    print(f"\nVariables ({len(variables)}):")
    for var in variables[:10]:  # Show first 10
        print(f"  📊 {var}")
    if len(variables) > 10:
        print(f"  ... and {len(variables) - 10} more")
    
    # Specific checks for our target functions
    target_functions = ['universal_float_convert', 'get_MW', 'get_MW_divd', 'get_complete_system_analysis']
    
    print(f"\nTarget Function Check:")
    for func_name in target_functions:
        if hasattr(__main__, func_name):
            func = getattr(__main__, func_name)
            print(f"  ✅ {func_name}: {type(func)} (callable: {callable(func)})")
        else:
            print(f"  ❌ {func_name}: NOT FOUND")
    
    return {
        'functions': functions,
        'modules': modules, 
        'variables': variables,
        'target_functions_available': [f for f in target_functions if hasattr(__main__, f)]
    }





# # =====================================================================================
# def main():
#     """Main autostart sequence"""
#     print("🚀 Starting Heat Reuse Tool...")
#     print("Loading components in dependency order...\n")
    
#     # Load in dependency order
#     load_physics_constants()
#     load_data_utilities()
#     load_csv_data()
#     load_core_calculations()
#     load_system_analysis()
#     load_ui_components()
#     load_testing_framework()
    
#     # Validation and testing
#     validate_critical_functions()
#     run_quick_tests()
    
#     # Expose functions to notebook namespace
#     expose_functions_to_main()
    
#     # Final setup
#     try:
#         # Call the post-setup function from __init__.py
#         from . import _post_autostart_setup
#         _post_autostart_setup()
#     except:
#         pass  # Not critical if this fails
    
#     # Show summary
#     print_load_summary()
    
#     return {
#         'loaded_modules': _loaded_modules,
#         'csv_data': _csv_data,
#         'errors': _load_errors,
#         'status': 'success' if not _load_errors else 'partial'
#     }

# # Run autostart when this module is imported
# if __name__ == "__main__":
#     main()
# else:
#     # Auto-run when imported
#     main()
# # =====================================================================================

# =============================================================================
# ADD THIS TO THE END OF YOUR autostart.py - TRACE EXECUTION
# =============================================================================

def main():
    """Main autostart sequence - WITH DEBUG TRACING"""
    print("🚀 Starting Heat Reuse Tool...")
    print("Loading components in dependency order...\n")
    
    # Load in dependency order
    print("🔍 DEBUG: About to load physics constants...")
    load_physics_constants()
    
    print("🔍 DEBUG: About to load data utilities...")
    load_data_utilities()
    
    print("🔍 DEBUG: About to load CSV data...")
    load_csv_data()
    
    print("🔍 DEBUG: About to load core calculations...")
    load_core_calculations()
    
    print("🔍 DEBUG: About to load system analysis...")
    load_system_analysis()
    
    print("🔍 DEBUG: About to load UI components...")
    load_ui_components()
    
    print("🔍 DEBUG: About to load testing framework...")
    load_testing_framework()
    
    # Validation and testing
    print("🔍 DEBUG: About to validate critical functions...")
    validate_critical_functions()
    
    print("🔍 DEBUG: About to run quick tests...")
    run_quick_tests()
    
    # *** THE CRITICAL STEP ***
    print("🔍 DEBUG: About to expose functions to main...")
    expose_result = expose_functions_to_main()
    print(f"🔍 DEBUG: expose_functions_to_main returned: {expose_result}")
    
    # Also expose debug_notebook_namespace
    print("🔍 DEBUG: Exposing debug_notebook_namespace...")
    try:
        import __main__
        __main__.debug_notebook_namespace = debug_notebook_namespace
        print("✅ debug_notebook_namespace exposed to notebook")
    except Exception as e:
        print(f"❌ Failed to expose debug_notebook_namespace: {e}")
    
    # Final setup
    print("🔍 DEBUG: About to run post-setup...")
    try:
        from . import _post_autostart_setup
        _post_autostart_setup()
    except Exception as e:
        print(f"🔍 DEBUG: Post-setup failed: {e}")
    
    # Show summary
    print("🔍 DEBUG: About to show load summary...")
    print_load_summary()
    
    print("🔍 DEBUG: Main function completed")
    
    return {
        'loaded_modules': _loaded_modules,
        'csv_data': _csv_data,
        'errors': _load_errors,
        'status': 'success' if not _load_errors else 'partial'
    }

# =============================================================================
# ALSO UPDATE THE BOTTOM OF THE FILE
# =============================================================================

# Run autostart when this module is imported
if __name__ == "__main__":
    print("🔍 DEBUG: Running as __main__")
    main()
else:
    print("🔍 DEBUG: Running as imported module")
    # Auto-run when imported
    result = main()
    print(f"🔍 DEBUG: Import execution completed with result: {result}")

    
    