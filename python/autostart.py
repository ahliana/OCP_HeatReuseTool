"""
Heat Reuse Tool - Production Autostart Module
Self-discovering, maintainable function loader
"""

import sys
import os
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional

class FunctionRegistry:
    """
    Auto-discovering function registry that finds and loads functions
    from all modules without manual configuration.
    """
    
    def __init__(self):
        self.functions = {}
        self.modules = {}
        self.load_errors = []
        
    def setup_python_path(self) -> str:
        """Add python directory to sys.path"""
        current_dir = os.getcwd()
        python_dir = os.path.join(current_dir, 'python')
        
        if python_dir not in sys.path:
            sys.path.insert(0, python_dir)
            print(f"✅ Added {python_dir} to Python path")
        
        return python_dir
    
    def discover_modules(self, python_dir: str) -> Dict[str, List[str]]:
        """
        Automatically discover all Python modules and their structure.
        Returns a mapping of module paths to their Python files.
        """
        modules = {}
        python_path = Path(python_dir)
        
        # Walk through all directories
        for root, dirs, files in os.walk(python_path):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if not d.startswith('__pycache__')]
            
            # Find Python files
            py_files = [f for f in files if f.endswith('.py') and not f.startswith('__')]
            
            if py_files:
                # Convert path to module format
                rel_path = os.path.relpath(root, python_path)
                if rel_path == '.':
                    module_prefix = ''
                else:
                    module_prefix = rel_path.replace(os.sep, '.') + '.'
                
                for py_file in py_files:
                    module_name = py_file[:-3]  # Remove .py
                    full_module_path = f"{module_prefix}{module_name}"
                    
                    if full_module_path not in modules:
                        modules[full_module_path] = []
                    modules[full_module_path].append(os.path.join(root, py_file))
        
        return modules
    
    def load_module_functions(self, module_path: str) -> Dict[str, Any]:
        """
        Load all public functions from a module.
        Returns {function_name: function_object}
        """
        try:
            # Import the module
            module = importlib.import_module(module_path)
            self.modules[module_path] = module
            
            functions = {}
            
            # Get all attributes
            for name in dir(module):
                if not name.startswith('_'):  # Skip private/internal
                    attr = getattr(module, name)
                    
                    # Check if it's a callable function (not a class or constant)
                    if (callable(attr) and 
                        inspect.isfunction(attr) and 
                        attr.__module__ == module.__name__):
                        
                        functions[name] = attr
            
            if functions:
                print(f"✅ Loaded {len(functions)} functions from {module_path}")
                for func_name in sorted(functions.keys()):
                    print(f"   • {func_name}")
            
            return functions
            
        except Exception as e:
            error_msg = f"❌ Failed to load {module_path}: {e}"
            print(error_msg)
            self.load_errors.append(error_msg)
            return {}
    
    def load_all_functions(self) -> Dict[str, Any]:
        """
        Discover and load all functions from all modules.
        Handles conflicts by preferring core > physics > data modules.
        """
        print("🔍 Auto-discovering modules...")
        
        python_dir = self.setup_python_path()
        discovered_modules = self.discover_modules(python_dir)
        
        print(f"📦 Found {len(discovered_modules)} modules:")
        for module_path in sorted(discovered_modules.keys()):
            print(f"   • {module_path}")
        
        print("\n🔧 Loading functions...")
        
        # Define loading priority (higher priority = preferred for conflicts)
        priority_order = [
            'data.',      # Priority 1: Data utilities
            'physics.',   # Priority 2: Physics calculations  
            'core.',      # Priority 3: Core business logic (highest)
            'ui.',        # Priority 4: UI functions
        ]
        
        # Sort modules by priority
        def get_priority(module_path):
            for i, prefix in enumerate(priority_order):
                if module_path.startswith(prefix):
                    return len(priority_order) - i  # Higher number = higher priority
            return 0  # Default priority
        
        sorted_modules = sorted(discovered_modules.keys(), key=get_priority)
        
        # Load functions from all modules
        all_functions = {}
        conflicts = {}
        
        for module_path in sorted_modules:
            module_functions = self.load_module_functions(module_path)
            
            for func_name, func_obj in module_functions.items():
                if func_name in all_functions:
                    # Handle conflict - track where functions come from
                    if func_name not in conflicts:
                        conflicts[func_name] = []
                    conflicts[func_name].append(module_path)
                    print(f"⚠️ Conflict: {func_name} found in multiple modules, using {module_path}")
                
                # Always take the latest (highest priority)
                all_functions[func_name] = func_obj
        
        # Report conflicts
        if conflicts:
            print(f"\n⚠️ Function conflicts resolved (using highest priority):")
            for func_name, modules in conflicts.items():
                print(f"   • {func_name}: {' < '.join(modules)}")
        
        self.functions = all_functions
        print(f"\n✅ Total functions loaded: {len(all_functions)}")
        return all_functions
    
    def expose_to_notebook(self) -> bool:
        """Expose all functions to the notebook namespace"""
        if not self.functions:
            print("❌ No functions to expose")
            return False
        
        print("📤 Exposing functions to notebook...")
        
        try:
            import __main__
            
            # Expose all functions
            for name, func in self.functions.items():
                setattr(__main__, name, func)
            
            print(f"✅ Exposed {len(self.functions)} functions to notebook")
            
            # Test critical functions
            self._test_critical_functions()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to expose functions: {e}")
            return False
    
    def _test_critical_functions(self):
        """Test a few critical functions to ensure they work"""
        import __main__
        
        test_cases = [
            ('universal_float_convert', lambda f: f("1,493"), "1,493"),
            ('get_MW', lambda f: f(1493, 20, 30), "1493, 20, 30"),
            ('get_MW_divd', lambda f: f(1493, 20, 30), "1493, 20, 30"),
        ]
        
        for func_name, test_func, test_args in test_cases:
            if hasattr(__main__, func_name):
                try:
                    func = getattr(__main__, func_name)
                    result = test_func(func)
                    print(f"✅ Test {func_name}({test_args}) = {result}")
                except Exception as e:
                    print(f"⚠️ Test failed for {func_name}: {e}")
    
    def create_debug_functions(self):
        """Create debugging and introspection functions"""
        import __main__
        
        def list_all_functions():
            """List all available functions by category"""
            print("📋 Available Functions by Module:")
            print("=" * 50)
            
            # Group functions by their module
            by_module = {}
            for name, func in self.functions.items():
                module_name = func.__module__
                if module_name not in by_module:
                    by_module[module_name] = []
                by_module[module_name].append(name)
            
            for module_name in sorted(by_module.keys()):
                print(f"\n📦 {module_name}:")
                for func_name in sorted(by_module[module_name]):
                    print(f"   • {func_name}")
            
            print(f"\n📊 Total: {len(self.functions)} functions from {len(by_module)} modules")
        
        def search_functions(keyword: str):
            """Search for functions containing a keyword"""
            matches = [name for name in self.functions.keys() if keyword.lower() in name.lower()]
            print(f"🔍 Functions containing '{keyword}':")
            for match in sorted(matches):
                func = self.functions[match]
                print(f"   • {match} (from {func.__module__})")
            print(f"Found {len(matches)} matches")
        
        def function_help(func_name: str):
            """Get help for a specific function"""
            if func_name in self.functions:
                func = self.functions[func_name]
                print(f"📖 Help for {func_name}:")
                print(f"   Module: {func.__module__}")
                if func.__doc__:
                    print(f"   Documentation:\n{func.__doc__}")
                else:
                    print("   No documentation available")
            else:
                print(f"❌ Function {func_name} not found")
        
        # Expose debug functions
        __main__.list_all_functions = list_all_functions
        __main__.search_functions = search_functions  
        __main__.function_help = function_help
        
        print("✅ Debug functions available:")
        print("   • list_all_functions() - Show all available functions")
        print("   • search_functions('keyword') - Search for functions")
        print("   • function_help('function_name') - Get help for a function")

# Global registry instance
_registry = FunctionRegistry()

def main():
    """Main function - auto-discover and load everything"""
    print("🚀 Heat Reuse Tool - Production Autostart")
    print("🤖 Auto-discovering and loading all functions...")
    
    # Load all functions automatically
    functions = _registry.load_all_functions()
    
    if functions:
        # Expose to notebook
        success = _registry.expose_to_notebook()
        
        if success:
            # Create debug functions
            _registry.create_debug_functions()
            
            print("\n🎉 SUCCESS! Heat Reuse Tool is ready!")
            print(f"📊 {len(functions)} functions available")
            print("💡 Type 'list_all_functions()' to see what's available")
            
            if _registry.load_errors:
                print(f"\n⚠️ {len(_registry.load_errors)} modules had loading issues")
                print("💡 Type '_registry.load_errors' to see details")
        else:
            print("❌ Failed to expose functions to notebook")
    else:
        print("❌ No functions loaded")
    
    return _registry

# Auto-run when imported
if __name__ != "__main__":
    main()