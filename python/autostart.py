# python/autostart.py - Clean User Interface
"""
Heat Reuse Tool - Automatic Startup

This module automatically loads all data and displays the interface.
"""

import os
import sys
import importlib
import inspect
from pathlib import Path

# Global function registry
_function_registry = {}
_module_registry = {}

# Module discovery configuration
MODULE_PRIORITIES = {
    'data': 1,      # Data utilities (highest priority)
    'physics': 2,   # Physics & engineering
    'core': 3,      # Core business logic
    'ui': 4,        # User interface (lowest priority for function conflicts)
}

# =============================================================================
# CSV DATA LOADING
# =============================================================================

def load_csv_data():
    """Load CSV data files quietly."""
    try:
        from data import load_csv_files, list_loaded_csvs
        
        # Try common data directory locations
        data_directories = ["Data", "../Data", "./Data", "data"]
        
        for data_dir in data_directories:
            if os.path.exists(data_dir) and os.path.isdir(data_dir):
                csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
                if csv_files:
                    try:
                        load_csv_files(data_dir)
                        loaded_files = list_loaded_csvs()
                        if loaded_files:
                            return True
                    except:
                        continue
        return False
        
    except:
        return False

# =============================================================================
# MODULE DISCOVERY
# =============================================================================

def discover_modules():
    """Discover and load all Python modules quietly."""
    global _function_registry, _module_registry
    
    current_dir = Path.cwd()
    python_dir = current_dir / "python"
    
    if not python_dir.exists():
        return False
    
    # Add python directory to path
    python_dir_str = str(python_dir)
    if python_dir_str not in sys.path:
        sys.path.insert(0, python_dir_str)
    
    # Discover modules in priority order
    for module_name in sorted(MODULE_PRIORITIES.keys(), key=lambda x: MODULE_PRIORITIES[x]):
        module_path = python_dir / module_name
        
        if module_path.exists() and module_path.is_dir():
            try:
                # Import the module
                module = importlib.import_module(module_name)
                _module_registry[module_name] = module
                
                # Discover functions in the module
                module_functions = {}
                
                # Check main module
                functions_in_main = discover_functions_in_module(module, f"{module_name}.__init__")
                module_functions.update(functions_in_main)
                
                # Check submodules
                for py_file in module_path.glob("*.py"):
                    if py_file.name.startswith("__"):
                        continue
                    
                    submodule_name = f"{module_name}.{py_file.stem}"
                    try:
                        submodule = importlib.import_module(submodule_name)
                        sub_functions = discover_functions_in_module(submodule, submodule_name)
                        module_functions.update(sub_functions)
                    except:
                        continue
                
                # Register functions with conflict resolution
                priority = MODULE_PRIORITIES[module_name]
                for func_name, func_obj in module_functions.items():
                    register_function_with_priority(func_name, func_obj, module_name, priority)
                
            except:
                continue
    
    return len(_module_registry) > 0

def discover_functions_in_module(module, module_name):
    """Discover all callable functions in a module."""
    functions = {}
    
    try:
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            # Skip private functions and imports from other modules
            if name.startswith('_'):
                continue
            
            # Check if function is defined in this module (not imported)
            if hasattr(obj, '__module__') and obj.__module__.startswith(module_name.split('.')[0]):
                functions[name] = obj
                
    except:
        pass
    
    return functions

def register_function_with_priority(func_name, func_obj, module_name, priority):
    """Register function with conflict resolution based on module priority."""
    global _function_registry
    
    if func_name in _function_registry:
        # Function already exists, check priority
        existing_priority = _function_registry[func_name]['priority']
        
        if priority < existing_priority:  # Lower number = higher priority
            # Replace with higher priority function
            _function_registry[func_name] = {
                'function': func_obj,
                'module': module_name,
                'priority': priority
            }
    else:
        # New function
        _function_registry[func_name] = {
            'function': func_obj,
            'module': module_name,
            'priority': priority
        }

# =============================================================================
# INTERFACE DISPLAY
# =============================================================================

def display_interface():
    """Display the Heat Reuse Tool interface."""
    try:
        from ui import auto_initialize_interface
        return auto_initialize_interface()
    except:
        return None

# =============================================================================
# UTILITY FUNCTIONS FOR ADVANCED USERS
# =============================================================================

def list_all_functions():
    """List all available functions grouped by module."""
    if not _function_registry:
        print("No functions loaded.")
        return {}
    
    by_module = {}
    for func_name, info in _function_registry.items():
        module = info['module']
        if module not in by_module:
            by_module[module] = []
        by_module[module].append(func_name)
    
    print(f"📚 Available Functions ({len(_function_registry)} total):")
    for module in sorted(by_module.keys()):
        functions = sorted(by_module[module])
        print(f"\n🔧 {module} ({len(functions)} functions):")
        for func in functions[:10]:  # Show first 10
            print(f"   • {func}")
        if len(functions) > 10:
            print(f"   ... and {len(functions) - 10} more")
    
    return by_module

def search_functions(keyword):
    """Search for functions containing a keyword."""
    if not _function_registry:
        print("No functions loaded.")
        return []
    
    matches = []
    for func_name, info in _function_registry.items():
        if keyword.lower() in func_name.lower():
            matches.append({
                'name': func_name,
                'module': info['module'],
                'function': info['function']
            })
    
    print(f"🔍 Found {len(matches)} functions matching '{keyword}':")
    for match in matches[:10]:  # Show first 10
        print(f"   • {match['name']} ({match['module']})")
    
    return matches

def function_help(func_name):
    """Get help for a specific function."""
    if func_name in _function_registry:
        func = _function_registry[func_name]['function']
        module = _function_registry[func_name]['module']
        
        print(f"📖 Help for {func_name} (from {module}):")
        print("=" * 50)
        
        # Get docstring
        doc = inspect.getdoc(func)
        if doc:
            print(doc)
        else:
            print("No documentation available.")
        
        # Get signature
        try:
            sig = inspect.signature(func)
            print(f"\nSignature: {func_name}{sig}")
        except:
            print(f"\nSignature: {func_name}(...)")
    else:
        print(f"Function '{func_name}' not found.")

# =============================================================================
# FUNCTION ACCESS
# =============================================================================

def __getattr__(name):
    """Dynamic attribute access to make registered functions available directly."""
    if name in _function_registry:
        return _function_registry[name]['function']
    
    raise AttributeError(f"Function '{name}' not found. Use list_all_functions() to see available functions.")

# =============================================================================
# AUTOMATIC INITIALIZATION
# =============================================================================

# Load data
load_csv_data()

# Discover modules
discover_modules()

# Display interface
display_interface()

# Export utility functions
__all__ = [
    'list_all_functions',
    'search_functions', 
    'function_help',
]