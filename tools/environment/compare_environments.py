# tools/environment/compare_environments.py
# Environment Comparison Tool for Heat Reuse Tool Project

import json
import sys
from pathlib import Path
from datetime import datetime

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_status(message, status="INFO"):
    """Print colored status messages"""
    colors = {
        "MATCH": Colors.GREEN + "✓",
        "DIFF": Colors.YELLOW + "⚠", 
        "MISSING": Colors.RED + "✗",
        "INFO": Colors.BLUE + "ℹ",
        "HEADER": Colors.BOLD
    }
    print(f"{colors.get(status, '')} {message}{Colors.END}")

def load_environment_file(filepath):
    """Load environment JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print_status(f"File not found: {filepath}", "MISSING")
        return None
    except json.JSONDecodeError:
        print_status(f"Invalid JSON file: {filepath}", "MISSING")
        return None
    except Exception as e:
        print_status(f"Error loading {filepath}: {str(e)}", "MISSING")
        return None

def compare_system_info(env1, env2, name1, name2):
    """Compare system information between environments"""
    print_status("System Information Comparison", "HEADER")
    print("=" * 40)
    
    sys1 = env1.get('system_info', {})
    sys2 = env2.get('system_info', {})
    
    comparisons = [
        ('Platform', 'platform'),
        ('Python Version', 'python_version'),
        ('Python Implementation', 'python_implementation'),
        ('System', 'system'),
        ('Machine Architecture', 'machine')
    ]
    
    for display_name, key in comparisons:
        val1 = sys1.get(key, 'Unknown')
        val2 = sys2.get(key, 'Unknown')
        
        if val1 == val2:
            print_status(f"{display_name}: {val1}", "MATCH")
        else:
            print_status(f"{display_name}:", "DIFF")
            print(f"  {name1}: {val1}")
            print(f"  {name2}: {val2}")

def compare_packages(env1, env2, name1, name2):
    """Compare Python packages between environments"""
    print_status("\nPackage Comparison", "HEADER")
    print("=" * 40)
    
    # Get package dictionaries
    packages1 = {}
    packages2 = {}
    
    # Handle both list and dict formats for packages
    pkg_data1 = env1.get('python_packages', [])
    pkg_data2 = env2.get('python_packages', [])
    
    if isinstance(pkg_data1, list):
        packages1 = {pkg['name']: pkg['version'] for pkg in pkg_data1 if isinstance(pkg, dict) and 'name' in pkg}
    elif isinstance(pkg_data1, dict):
        packages1 = pkg_data1
    
    if isinstance(pkg_data2, list):
        packages2 = {pkg['name']: pkg['version'] for pkg in pkg_data2 if isinstance(pkg, dict) and 'name' in pkg}
    elif isinstance(pkg_data2, dict):
        packages2 = pkg_data2
    
    # Critical packages for Heat Reuse Tool
    critical_packages = ['jupyter', 'pandas', 'numpy', 'matplotlib', 'scipy', 'ipywidgets', 'notebook', 'ipython']
    
    print_status("Critical Packages:", "INFO")
    
    for package in critical_packages:
        ver1 = packages1.get(package)
        ver2 = packages2.get(package)
        
        if ver1 and ver2:
            if ver1 == ver2:
                print_status(f"{package}: {ver1}", "MATCH")
            else:
                print_status(f"{package}: Version mismatch", "DIFF")
                print(f"  {name1}: {ver1}")
                print(f"  {name2}: {ver2}")
        elif ver1 and not ver2:
            print_status(f"{package}: Missing on {name2} (has {ver1})", "MISSING")
        elif ver2 and not ver1:
            print_status(f"{package}: Missing on {name1} (has {ver2})", "MISSING")
        else:
            print_status(f"{package}: Missing on both systems", "MISSING")
    
    # Package count comparison
    total1 = len(packages1)
    total2 = len(packages2)
    print_status(f"\nTotal packages: {name1}={total1}, {name2}={total2}", "INFO")
    
    # Packages only in one environment
    only_in_1 = set(packages1.keys()) - set(packages2.keys())
    only_in_2 = set(packages2.keys()) - set(packages1.keys())
    
    if only_in_1:
        print_status(f"\nPackages only in {name1}: {len(only_in_1)}", "DIFF")
        for pkg in sorted(list(only_in_1)[:10]):  # Show first 10
            print(f"  - {pkg} ({packages1[pkg]})")
        if len(only_in_1) > 10:
            print(f"  ... and {len(only_in_1) - 10} more")
    
    if only_in_2:
        print_status(f"\nPackages only in {name2}: {len(only_in_2)}", "DIFF")
        for pkg in sorted(list(only_in_2)[:10]):  # Show first 10
            print(f"  - {pkg} ({packages2[pkg]})")
        if len(only_in_2) > 10:
            print(f"  ... and {len(only_in_2) - 10} more")

def compare_jupyter_info(env1, env2, name1, name2):
    """Compare Jupyter configuration"""
    print_status("\nJupyter Configuration", "HEADER")
    print("=" * 40)
    
    jupyter1 = env1.get('jupyter_info', {})
    jupyter2 = env2.get('jupyter_info', {})
    
    # Jupyter versions
    ver1 = jupyter1.get('version', 'Not found')
    ver2 = jupyter2.get('version', 'Not found')
    
    if ver1 == ver2:
        print_status(f"Jupyter version: {ver1}", "MATCH")
    else:
        print_status("Jupyter version mismatch:", "DIFF")
        print(f"  {name1}: {ver1}")
        print(f"  {name2}: {ver2}")
    
    # Kernels
    kernels1 = set()
    kernels2 = set()
    
    k1 = jupyter1.get('kernels', {})
    if isinstance(k1, dict) and 'kernelspecs' in k1:
        kernels1 = set(k1['kernelspecs'].keys())
    
    k2 = jupyter2.get('kernels', {})
    if isinstance(k2, dict) and 'kernelspecs' in k2:
        kernels2 = set(k2['kernelspecs'].keys())
    
    # Check for Heat Reuse Tool kernel
    heat_reuse_kernels = [k for k in kernels1.union(kernels2) if 'heat-reuse' in k.lower()]
    
    if heat_reuse_kernels:
        for kernel in heat_reuse_kernels:
            if kernel in kernels1 and kernel in kernels2:
                print_status(f"Heat Reuse Tool kernel '{kernel}': Found on both", "MATCH")
            elif kernel in kernels1:
                print_status(f"Heat Reuse Tool kernel '{kernel}': Only on {name1}", "DIFF")
            else:
                print_status(f"Heat Reuse Tool kernel '{kernel}': Only on {name2}", "DIFF")
    else:
        print_status("Heat Reuse Tool kernel: Not found on either system", "MISSING")
    
    # All kernels comparison
    common_kernels = kernels1.intersection(kernels2)
    only_1 = kernels1 - kernels2
    only_2 = kernels2 - kernels1
    
    if common_kernels:
        print_status(f"Common kernels: {', '.join(sorted(common_kernels))}", "MATCH")
    
    if only_1:
        print_status(f"Kernels only on {name1}: {', '.join(sorted(only_1))}", "DIFF")
    
    if only_2:
        print_status(f"Kernels only on {name2}: {', '.join(sorted(only_2))}", "DIFF")

def compare_required_files(env1, env2, name1, name2):
    """Compare required Heat Reuse Tool files"""
    print_status("\nRequired Files Comparison", "HEADER")
    print("=" * 40)
    
    files1 = env1.get('required_files', {})
    files2 = env2.get('required_files', {})
    
    all_files = set(files1.keys()).union(set(files2.keys()))
    
    for filepath in sorted(all_files):
        exists1 = files1.get(filepath, False)
        exists2 = files2.get(filepath, False)
        
        if exists1 and exists2:
            print_status(f"{filepath}: Present on both", "MATCH")
        elif exists1 and not exists2:
            print_status(f"{filepath}: Missing on {name2}", "MISSING")
        elif exists2 and not exists1:
            print_status(f"{filepath}: Missing on {name1}", "MISSING")
        else:
            print_status(f"{filepath}: Missing on both", "MISSING")

def compare_vscode_extensions(env1, env2, name1, name2):
    """Compare VSCode extensions"""
    print_status("\nVSCode Extensions", "HEADER")
    print("=" * 40)
    
    ext1 = set(env1.get('vscode_extensions', []))
    ext2 = set(env2.get('vscode_extensions', []))
    
    # Remove error messages
    ext1 = {ext for ext in ext1 if not ext.startswith('VSCode not found') and not ext.startswith('Error')}
    ext2 = {ext for ext in ext2 if not ext.startswith('VSCode not found') and not ext.startswith('Error')}
    
    # Critical extensions for Python development
    critical_extensions = ['ms-python.python', 'ms-toolsai.jupyter']
    
    print_status("Critical Extensions:", "INFO")
    for ext_pattern in critical_extensions:
        found1 = any(ext_pattern in ext for ext in ext1)
        found2 = any(ext_pattern in ext for ext in ext2)
        
        if found1 and found2:
            print_status(f"{ext_pattern}: Installed on both", "MATCH")
        elif found1:
            print_status(f"{ext_pattern}: Only on {name1}", "DIFF")
        elif found2:
            print_status(f"{ext_pattern}: Only on {name2}", "DIFF")
        else:
            print_status(f"{ext_pattern}: Missing on both", "MISSING")
    
    print_status(f"Total extensions: {name1}={len(ext1)}, {name2}={len(ext2)}", "INFO")

def generate_sync_recommendations(env1, env2, name1, name2):
    """Generate recommendations to sync environments"""
    print_status(f"\nSync Recommendations: Make {name2} match {name1}", "HEADER")
    print("=" * 50)
    
    recommendations = []
    
    # Package recommendations
    pkg_data1 = env1.get('python_packages', [])
    pkg_data2 = env2.get('python_packages', [])
    
    packages1 = {}
    packages2 = {}
    
    if isinstance(pkg_data1, list):
        packages1 = {pkg['name']: pkg['version'] for pkg in pkg_data1 if isinstance(pkg, dict) and 'name' in pkg}
    elif isinstance(pkg_data1, dict):
        packages1 = pkg_data1
    
    if isinstance(pkg_data2, list):
        packages2 = {pkg['name']: pkg['version'] for pkg in pkg_data2 if isinstance(pkg, dict) and 'name' in pkg}
    elif isinstance(pkg_data2, dict):
        packages2 = pkg_data2
    
    # Critical packages that need to match
    critical_packages = ['jupyter', 'pandas', 'numpy', 'matplotlib', 'scipy', 'ipywidgets', 'notebook', 'ipython']
    
    for package in critical_packages:
        ver1 = packages1.get(package)
        ver2 = packages2.get(package)
        
        if ver1 and not ver2:
            recommendations.append(f"pip install {package}=={ver1}")
        elif ver1 and ver2 and ver1 != ver2:
            recommendations.append(f"pip install {package}=={ver1}  # Downgrade/upgrade from {ver2}")
    
    # Jupyter kernel recommendation
    jupyter1 = env1.get('jupyter_info', {})
    jupyter2 = env2.get('jupyter_info', {})
    
    k1 = jupyter1.get('kernels', {})
    k2 = jupyter2.get('kernels', {})
    
    if isinstance(k1, dict) and 'kernelspecs' in k1:
        kernels1 = set(k1['kernelspecs'].keys())
        heat_reuse_kernels = [k for k in kernels1 if 'heat-reuse' in k.lower()]
        
        if heat_reuse_kernels:
            kernels2 = set()
            if isinstance(k2, dict) and 'kernelspecs' in k2:
                kernels2 = set(k2['kernelspecs'].keys())
            
            for kernel in heat_reuse_kernels:
                if kernel not in kernels2:
                    recommendations.append("python -m ipykernel install --user --name=heat-reuse-tool --display-name=\"Heat Reuse Tool\"")
                    break  # Only add once
    
    # VSCode extension recommendations
    ext1 = set(env1.get('vscode_extensions', []))
    ext2 = set(env2.get('vscode_extensions', []))
    
    ext1 = {ext for ext in ext1 if not ext.startswith('VSCode not found') and not ext.startswith('Error')}
    ext2 = {ext for ext in ext2 if not ext.startswith('VSCode not found') and not ext.startswith('Error')}
    
    critical_extensions = ['ms-python.python', 'ms-toolsai.jupyter']
    for ext_pattern in critical_extensions:
        found1 = any(ext_pattern in ext for ext in ext1)
        found2 = any(ext_pattern in ext for ext in ext2)
        
        if found1 and not found2:
            recommendations.append(f"code --install-extension {ext_pattern}")
    
    # File recommendations
    files1 = env1.get('required_files', {})
    files2 = env2.get('required_files', {})
    
    for filepath, exists1 in files1.items():
        exists2 = files2.get(filepath, False)
        if exists1 and not exists2:
            recommendations.append(f"# Ensure file exists: {filepath}")
    
    # Print recommendations
    if recommendations:
        print_status("PowerShell commands to run:", "INFO")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i:2d}. {rec}")
        
        # Save to file
        try:
            exports_dir = Path("tools/environment/exports")
            exports_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sync_file = exports_dir / f"sync_{name1}_to_{name2}_{timestamp}.ps1"
            
            with open(sync_file, 'w', encoding='utf-8') as f:
                f.write("# Heat Reuse Tool - Environment Sync Script\n")
                f.write(f"# Sync {name2} to match {name1}\n")
                f.write(f"# Generated: {datetime.now().isoformat()}\n\n")
                
                f.write("# Ensure virtual environment is activated\n")
                f.write("# .\\.venv\\Scripts\\Activate.ps1\n\n")
                
                for rec in recommendations:
                    if rec.startswith('#'):
                        f.write(f"{rec}\n")
                    else:
                        f.write(f"{rec}\n")
            
            print_status(f"\nSync script saved: {sync_file}", "MATCH")
            
        except Exception as e:
            print_status(f"Could not save sync script: {str(e)}", "MISSING")
    else:
        print_status("No sync recommendations needed - environments are compatible!", "MATCH")

def compare_environments(file1, file2):
    """Main comparison function"""
    env1 = load_environment_file(file1)
    env2 = load_environment_file(file2)
    
    if not env1 or not env2:
        print_status("Could not load one or both environment files", "MISSING")
        return False
    
    name1 = env1.get('machine_name', Path(file1).stem.split('_')[0])
    name2 = env2.get('machine_name', Path(file2).stem.split('_')[0])
    
    print_status(f"Heat Reuse Tool - Environment Comparison", "HEADER")
    print_status(f"Comparing: {name1} vs {name2}", "INFO")
    print_status(f"Files: {Path(file1).name} vs {Path(file2).name}", "INFO")
    print("=" * 60)
    
    # Run all comparisons
    compare_system_info(env1, env2, name1, name2)
    compare_packages(env1, env2, name1, name2)
    compare_jupyter_info(env1, env2, name1, name2)
    compare_required_files(env1, env2, name1, name2)
    compare_vscode_extensions(env1, env2, name1, name2)
    generate_sync_recommendations(env1, env2, name1, name2)
    
    return True

def list_available_exports():
    """List available environment export files"""
    exports_dir = Path("tools/environment/exports")
    
    if not exports_dir.exists():
        print_status("No exports directory found", "MISSING")
        print_status("Run 'python tools/environment/export_environment.py' first", "INFO")
        return []
    
    json_files = list(exports_dir.glob("*_environment_*.json"))
    
    if not json_files:
        print_status("No environment export files found", "MISSING")
        print_status("Run 'python tools/environment/export_environment.py' first", "INFO")
        return []
    
    print_status("Available environment exports:", "INFO")
    for i, file_path in enumerate(sorted(json_files), 1):
        # Extract machine name and timestamp from filename
        parts = file_path.stem.split('_')
        if len(parts) >= 3:
            machine = parts[0]
            timestamp = '_'.join(parts[-2:])
            print(f"{i:2d}. {machine} ({timestamp}) - {file_path.name}")
        else:
            print(f"{i:2d}. {file_path.name}")
    
    return json_files

def main():
    """Main function"""
    if len(sys.argv) == 1:
        # No arguments - list available files
        files = list_available_exports()
        if files:
            print(f"\nUsage:")
            print(f"python tools/environment/compare_environments.py <file1> <file2>")
            print(f"python tools/environment/compare_environments.py dragonraider swiftsetup  # Auto-find latest")
        return
    
    elif len(sys.argv) == 2:
        print_status("Please provide two environment files to compare", "MISSING")
        list_available_exports()
        return
    
    elif len(sys.argv) >= 3:
        file1_arg = sys.argv[1]
        file2_arg = sys.argv[2]
        
        # Check if arguments are machine names (auto-find latest files)
        exports_dir = Path("tools/environment/exports")
        
        # Try to auto-find files by machine name
        if not Path(file1_arg).exists() and exports_dir.exists():
            pattern1 = f"{file1_arg}_environment_*.json"
            matches1 = list(exports_dir.glob(pattern1))
            if matches1:
                file1_arg = str(sorted(matches1)[-1])  # Latest file
                print_status(f"Auto-selected for {sys.argv[1]}: {Path(file1_arg).name}", "INFO")
        
        if not Path(file2_arg).exists() and exports_dir.exists():
            pattern2 = f"{file2_arg}_environment_*.json"
            matches2 = list(exports_dir.glob(pattern2))
            if matches2:
                file2_arg = str(sorted(matches2)[-1])  # Latest file
                print_status(f"Auto-selected for {sys.argv[2]}: {Path(file2_arg).name}", "INFO")
        
        # Verify files exist
        if not Path(file1_arg).exists():
            print_status(f"File not found: {file1_arg}", "MISSING")
            list_available_exports()
            return
        
        if not Path(file2_arg).exists():
            print_status(f"File not found: {file2_arg}", "MISSING")
            list_available_exports()
            return
        
        # Perform comparison
        success = compare_environments(file1_arg, file2_arg)
        
        if not success:
            print_status("Comparison failed", "MISSING")
            sys.exit(1)
        else:
            print_status("\nComparison completed successfully!", "MATCH")

if __name__ == "__main__":
    main()