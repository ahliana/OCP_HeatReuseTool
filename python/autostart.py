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

def load_all_functions():
    """Load all the functions we need from the python modules"""
    print("🔧 Loading functions from python modules...")
    
    all_functions = {}
    
    # Define what we want to import from where
    imports = [
        ('data.converter', ['universal_float_convert']),
        ('physics.thermodynamics', ['get_MW_equivalent', 'get_MW_divd_equivalent']),
        ('core.system_analysis', ['get_complete_system_analysis', 'validate_user_inputs']),
        ('physics.engineering_calculations', ['datacenter_cooling_analysis', 'pipe_sizing_analysis', 'heat_exchanger_analysis']),
    ]
    
    # Try each import
    for module_path, function_names in imports:
        functions = safe_import(module_path, function_names)
        if functions:
            all_functions.update(functions)
    
    # Handle name mappings (if functions have different names in modules)
    if 'get_MW_equivalent' in all_functions:
        all_functions['get_MW'] = all_functions['get_MW_equivalent']
    if 'get_MW_divd_equivalent' in all_functions:
        all_functions['get_MW_divd'] = all_functions['get_MW_divd_equivalent']
    
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
        
        # Test one function to make sure it works
        if 'universal_float_convert' in functions:
            test_result = __main__.universal_float_convert("1,493")
            print(f"✅ Test: universal_float_convert('1,493') = {test_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to expose functions: {e}")
        return False

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
            print(f"Available functions: {', '.join(functions.keys())}")
        else:
            print("❌ Failed to expose functions to notebook")
    else:
        print("❌ No functions loaded")
    
    return functions

# Auto-run when imported
if __name__ != "__main__":
    main()