"""
Heat Reuse Tool - Autostart Module
Clean, simple approach: import functions once, expose to notebook
"""

import sys
import os
from pathlib import Path

def setup_python_path():
    """Add python directory to sys.path so we can import modules"""
    current_dir = os.getcwd()
    python_dir = os.path.join(current_dir, 'python')
    
    if python_dir not in sys.path:
        sys.path.insert(0, python_dir)
        print(f"✅ Added {python_dir} to Python path")
    
    return python_dir

def safe_import(module_path, function_names=None):
    """
    Safely import functions from a module path.
    
    Args:
        module_path: String like 'data.converter' or 'physics.thermodynamics'
        function_names: String or list of function names to import
    
    Returns:
        Dictionary of {function_name: function} or None if failed
    """
    try:
        if isinstance(function_names, str):
            function_names = [function_names]
        
        module = __import__(module_path, fromlist=function_names or [])
        
        if function_names:
            # Import specific functions
            functions = {}
            for func_name in function_names:
                if hasattr(module, func_name):
                    functions[func_name] = getattr(module, func_name)
                    print(f"✅ Imported {func_name} from {module_path}")
                else:
                    print(f"⚠️ Function {func_name} not found in {module_path}")
            return functions
        else:
            # Import entire module
            print(f"✅ Imported module {module_path}")
            return {module_path.split('.')[-1]: module}
    
    except ImportError as e:
        print(f"❌ Could not import {module_path}: {e}")
        return None
    except Exception as e:
        print(f"❌ Error importing {module_path}: {e}")
        return None

# Remove the create_working_functions since we're getting them from engineering_calculations

def load_all_functions():
    """Load all the functions we need from the python modules"""
    print("🔧 Loading functions from python modules...")
    
    all_functions = {}
    
    # Import core data conversion function
    core_functions = safe_import('data.converter', ['universal_float_convert'])
    if core_functions:
        all_functions.update(core_functions)
    
    # Import all functions from engineering_calculations (including get_MW and get_MW_divd)
    engineering_functions = safe_import('physics.engineering_calculations', [
        'datacenter_cooling_analysis', 
        'pipe_sizing_analysis', 
        'heat_exchanger_analysis',
        'get_MW',
        'get_MW_divd'
    ])
    if engineering_functions:
        all_functions.update(engineering_functions)
    
    print(f"📦 Loaded {len(all_functions)} functions total")
    return all_functions

def expose_to_notebook(functions):
    """Expose functions to the notebook namespace"""
    print("📤 Exposing functions to notebook...")
    
    try:
        import __main__
        
        exposed_count = 0
        for name, func in functions.items():
            setattr(__main__, name, func)
            exposed_count += 1
        
        print(f"✅ Exposed {exposed_count} functions to notebook")
        
        # Test key functions to make sure they work
        test_functions = ['universal_float_convert', 'get_MW', 'get_MW_divd']
        for test_func in test_functions:
            if test_func in functions:
                try:
                    if test_func == 'universal_float_convert':
                        test_result = getattr(__main__, test_func)("1,493")
                        print(f"✅ Test: {test_func}('1,493') = {test_result}")
                    elif test_func in ['get_MW', 'get_MW_divd']:
                        test_result = getattr(__main__, test_func)(1493, 20, 30)
                        print(f"✅ Test: {test_func}(1493, 20, 30) = {test_result}")
                except Exception as e:
                    print(f"⚠️ Test failed for {test_func}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to expose functions: {e}")
        return False

def debug_notebook_namespace():
    """Debug function to check what's available in the notebook"""
    import __main__
    
    print("🔍 DEBUG: Notebook Namespace Analysis")
    print("=" * 50)
    
    # Check for target functions
    target_functions = ['universal_float_convert', 'get_MW', 'get_MW_divd']
    
    print(f"Target Function Check:")
    for func_name in target_functions:
        if hasattr(__main__, func_name):
            func = getattr(__main__, func_name)
            print(f"  ✅ {func_name}: {type(func)} (callable: {callable(func)})")
            
            # Test the function if it's callable
            if callable(func):
                try:
                    if func_name == 'universal_float_convert':
                        test_result = func("1,493")
                        print(f"    Test result: {test_result}")
                    elif func_name in ['get_MW', 'get_MW_divd']:
                        test_result = func(1493, 20, 30)
                        print(f"    Test result: {test_result}")
                except Exception as e:
                    print(f"    Test failed: {e}")
        else:
            print(f"  ❌ {func_name}: NOT FOUND")
    
    # Show all available functions
    all_functions = [attr for attr in dir(__main__) 
                    if not attr.startswith('_') and callable(getattr(__main__, attr, None))]
    print(f"\nAll available functions: {', '.join(all_functions)}")
    
    return True

def main():
    """Simple main function - do the work"""
    print("🚀 Heat Reuse Tool - Starting Up...")
    
    # 1. Setup path
    setup_python_path()
    
    # 2. Load functions
    functions = load_all_functions()
    
    # 3. Expose to notebook
    if functions:
        success = expose_to_notebook(functions)
        if success:
            print("🎉 Success! Functions are now available in your notebook.")
            print(f"Available functions: {', '.join(sorted(functions.keys()))}")
        else:
            print("❌ Failed to expose functions to notebook")
    else:
        print("❌ No functions loaded")
    
    # 4. Make debug function available too
    try:
        import __main__
        __main__.debug_notebook_namespace = debug_notebook_namespace
        print("✅ Debug function available as debug_notebook_namespace()")
    except:
        pass
    
    return functions

# Auto-run when imported
if __name__ != "__main__":
    main()