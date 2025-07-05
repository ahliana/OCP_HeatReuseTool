def compare_ipykernel_info(env1, env2, name1, name2):
    """NEW: Compare ipykernel-specific information - CRITICAL for VSCode notebooks"""
    print_status("\n🎯 IPYKERNEL COMPARISON (Critical for VSCode)", "HEADER")
    print("=" * 50)
    
    ipk1 = env1.get('ipykernel_info', {})
    ipk2 = env2.get('ipykernel_info', {})
    
    # Package installation status
    installed1 = ipk1.get('package_installed', False)
    installed2 = ipk2.get('package_installed', False)
    
    if installed1 and installed2:
        ver1 = ipk1.get('version', 'Unknown')
        ver2 = ipk2.get('version', 'Unknown')
        if ver1 == ver2:
            print_status(f"ipykernel package: v{ver1} on both systems", "MATCH")
        else:
            print_status(f"ipykernel version mismatch:", "DIFF")
            print(f"  {name1}: v{ver1}")
            print(f"  {name2}: v{ver2}")
    elif installed1:
        print_status(f"ipykernel: Installed on {name1} (v{ipk1.get('version', 'Unknown')}) but MISSING on {name2}", "MISSING")
    elif installed2:
        print_status(f"ipykernel: Installed on {name2} (v{ipk2.get('version', 'Unknown')}) but MISSING on {name1}", "MISSING")
    else:
        print_status("ipykernel: NOT INSTALLED on either system - CRITICAL ISSUE!", "MISSING")
    
    # Install command functionality
    cmd1 = ipk1.get('install_command_works', False)
    cmd2 = ipk2.get('install_command_works', False)
    
    if cmd1 and cmd2:
        print_status("ipykernel install command: Works on both systems", "MATCH")
    elif cmd1:
        print_status(f"ipykernel install command: Works on {name1} but not {name2}", "DIFF")
    elif cmd2:
        print_status(f"ipykernel install command: Works on {name2} but not {name1}", "DIFF")
    else:
        print_status("ipykernel install command: NOT WORKING on either system", "MISSING")
    
    # Heat Reuse Tool kernel registration
    kernel1 = ipk1.get('heat_reuse_kernel_registered', False)
    kernel2 = ipk2.get('heat_reuse_kernel_registered', False)
    
    if kernel1 and kernel2:
        print_status("Heat Reuse Tool kernel: Registered on both systems", "MATCH")
    elif kernel1:
        print_status(f"Heat Reuse Tool kernel: Registered on {name1} but NOT on {name2}", "DIFF")
    elif kernel2:
        print_status(f"Heat Reuse Tool kernel: Registered on {name2} but NOT on {name1}", "DIFF")
    else:
        print_status("Heat Reuse Tool kernel: NOT REGISTERED on either system", "MISSING")
    
    # Jupyter availability
    jupyter1 = ipk1.get('jupyter_available', False)
    jupyter2 = ipk2.get('jupyter_available', False)
    
    if jupyter1 and jupyter2:
        print_status("Jupyter kernelspec: Available on both systems", "MATCH")
    elif jupyter1:
        print_status(f"Jupyter kernelspec: Available on {name1} but not {name2}", "DIFF")
    elif jupyter2:
        print_status(f"Jupyter kernelspec: Available on {name2} but not {name1}", "DIFF")
    else:
        print_status("Jupyter kernelspec: NOT AVAILABLE on either system", "MISSING")
    
    # Show errors if any
    errors1 = ipk1.get('errors', [])
    errors2 = ipk2.get('errors', [])
    
    if errors1:
        print_status(f"\nErrors on {name1}:", "DIFF")
        for error in errors1:
            print(f"  - {error}")
    
    if errors2:
        print_status(f"\nErrors on {name2}:", "DIFF")
        for error in errors2:
            print(f"  - {error}")

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
                print_status(f"🎯 Heat Reuse Tool kernel '{kernel}': Found on both", "MATCH")
            elif kernel in kernels1:
                print_status(f"🎯 Heat Reuse Tool kernel '{kernel}': Only on {name1}", "DIFF")
            else:
                print_status(f"🎯 Heat Reuse Tool kernel '{kernel}': Only on {name2}", "DIFF")
    else:
        print_status("🎯 Heat Reuse Tool kernel: Not found on either system", "MISSING")
    
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
    
    # Critical packages that need to match (including ipykernel)
    critical_packages = ['jupyter', 'pandas', 'numpy', 'matplotlib', 'scipy', 'ipywidgets', 'notebook', 'ipython', 'ipykernel']
    
    for package in critical_packages:
        ver1 = packages1.get(package)
        ver2 = packages2.get(package)
        
        if ver1 and not ver2:
            if package == 'ipykernel':
                recommendations.append(f"pip install {package}=={ver1}  # CRITICAL for VSCode notebooks")
            else:
                recommendations.append(f"pip install {package}=={ver1}")
        elif ver1 and ver2 and ver1 != ver2:
            if package == 'ipykernel':
                recommendations.append(f"pip install {package}=={ver1}  # CRITICAL: Upgrade/downgrade ipykernel from {ver2}")
            else:
                recommendations.append(f"pip install {package}=={ver1}  # Downgrade/upgrade from {ver2}")
    
    # ipykernel-specific recommendations (NEW)
    ipk1 = env1.get('ipykernel_info', {})
    ipk2 = env2.get('ipykernel_info', {})
    
    # If Heat Reuse Tool kernel is not registered on system 2
    if ipk1.get('heat_reuse_kernel_registered', False) and not ipk2.get('heat_reuse_kernel_registered', False):
        recommendations.append("# CRITICAL: Register Heat Reuse Tool kernel for VSCode")
        recommendations.append("python -m ipykernel install --user --name=heat-reuse-tool --display-name=\"Heat Reuse Tool\"")
    
    # Jupyter kernel recommendation from kernelspec comparison
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
                    # Only add if not already added above
                    if "python -m ipykernel install --user --name=heat-reuse-tool" not in ' '.join(recommendations):
                        recommendations.append("# Register Heat Reuse Tool kernel")
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
            if rec.startswith('#'):
                print(f"    {rec}")
            else:
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
    compare_ipykernel_info(env1, env2, name1, name2)  # NEW: Detailed ipykernel comparison
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
    main()# tools/environment/compare_environments.py
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
    
    # Critical packages for Heat Reuse Tool (including ipykernel)
    critical_packages = ['jupyter', 'pandas', 'numpy', 'matplotlib', 'scipy', 'ipywidgets', 'notebook', 'ipython', 'ipykernel']
    
    print_status("Critical Packages:", "INFO")
    
    for package in critical_packages:
        ver1 = packages1.get(package)
        ver2 = packages2.get(package)
        
        # Special handling for ipykernel
        if package == 'ipykernel':
            if ver1 and ver2:
                if ver1 == ver2:
                    print_status(f"🎯 {package}: {ver1} (CRITICAL FOR VSCODE NOTEBOOKS)", "MATCH")
                else:
                    print_status(f"🎯 {package}: Version mismatch (CRITICAL FOR VSCODE NOTEBOOKS)", "DIFF")
                    print(f"  {name1}: {ver1}")
                    print(f"  {name2}: {ver2}")
            elif ver1 and not ver2:
                print_status(f"🎯 {package}: MISSING on {name2} (has {ver1}) - CRITICAL!", "MISSING")
            elif ver2 and not ver1:
                print_status(f"🎯 {package}: MISSING on {name1} (has {ver2}) - CRITICAL!", "MISSING")
            else:
                print_status(f"🎯 {package}: MISSING on both systems - CRITICAL!", "MISSING")
        else:
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

def compare_ipykernel_info(env1, env2, name1, name2):
    """Compare ipykernel-specific information - CRITICAL for VSCode notebooks"""
    print_status("\n🎯 IPYKERNEL COMPARISON (Critical for VSCode)", "HEADER")
    print("=" * 50)
    
    ipk1 = env1.get('ipykernel_info', {})
    ipk2 = env2.get('ipykernel_info', {})
    
    # Package installation status
    installed1 = ipk1.get('package_installed', False)
    installed2 = ipk2.get('package_installed', False)
    
    if installed1 and installed2:
        ver1 = ipk1.get('version', 'Unknown')
        ver2 = ipk2.get('version', 'Unknown')
        if ver1 == ver2:
            print_status(f"ipykernel package: v{ver1} on both systems", "MATCH")
        else:
            print_status(f"ipykernel version mismatch:", "DIFF")
            print(f"  {name1}: v{ver1}")
            print(f"  {name2}: v{ver2}")
    elif installed1:
        print_status(f"ipykernel: Installed on {name1} (v{ipk1.get('version', 'Unknown')}) but MISSING on {name2}", "MISSING")
    elif installed2:
        print_status(f"ipykernel: Installed on {name2} (v{ipk2.get('version', 'Unknown')}) but MISSING on {name1}", "MISSING")
    else:
        print_status("ipykernel: NOT INSTALLED on either system - CRITICAL ISSUE!", "MISSING")
    
    # Install command functionality
    cmd1 = ipk1.get('install_command_works', False)
    cmd2 = ipk2.get('install_command_works', False)
    
    if cmd1 and cmd2:
        print_status("ipykernel install command: Works on both systems", "MATCH")
    elif cmd1:
        print_status(f"ipykernel install command: Works on {name1} but not {name2}", "DIFF")
    elif cmd2:
        print_status(f"ipykernel install command: Works on {name2} but not {name1}", "DIFF")
    else:
        print_status("ipykernel install command: NOT WORKING on either system", "MISSING")
    
    # Heat Reuse Tool kernel registration
    kernel1 = ipk1.get('heat_reuse_kernel_registered', False)
    kernel2 = ipk2.get('heat_reuse_kernel_registered', False)
    
    if kernel1 and kernel2:
        print_status("Heat Reuse Tool kernel: Registered on both systems", "MATCH")
    elif kernel1:
        print_status(f"Heat Reuse Tool kernel: Registered on {name1} but NOT on {name2}", "DIFF")
    elif kernel2:
        print_status(f"Heat Reuse Tool kernel: Registered on {name2} but NOT on {name1}", "DIFF")
    else:
        print_status("Heat Reuse Tool kernel: NOT REGISTERED on either system", "MISSING")
    
    # Jupyter availability
    jupyter1 = ipk1.get('jupyter_available', False)
    jupyter2 = ipk2.get('jupyter_available', False)
    
    if jupyter1 and jupyter2:
        print_status("Jupyter kernelspec: Available on both systems", "MATCH")
    elif jupyter1:
        print_status(f"Jupyter kernelspec: Available on {name1} but not {name2}", "DIFF")
    elif jupyter2:
        print_status(f"Jupyter kernelspec: Available on {name2} but not {name1}", "DIFF")
    else:
        print_status("Jupyter kernelspec: NOT AVAILABLE on either system", "MISSING")
    
    # Show errors if any
    errors1 = ipk1.get('errors', [])
    errors2 = ipk2.get('errors', [])
    
    if errors1:
        print_status(f"\nErrors on {name1}:", "DIFF")
        for error in errors1:
            print(f"  - {error}")
    
    if errors2:
        print_status(f"\nErrors on {name2}:", "DIFF")
        for error in errors2:
            print(f"  - {error}")
    
    # Summary assessment
    print_status("\nIPYKERNEL ASSESSMENT:", "INFO")
    
    def assess_ipykernel_health(ipk_info, system_name):
        score = 0
        issues = []
        
        if ipk_info.get('package_installed'):
            score += 1
        else:
            issues.append("Package not installed")
        
        if ipk_info.get('install_command_works'):
            score += 1
        else:
            issues.append("Install command not working")
        
        if ipk_info.get('heat_reuse_kernel_registered'):
            score += 1
        else:
            issues.append("Heat Reuse Tool kernel not registered")
        
        if ipk_info.get('jupyter_available'):
            score += 1
        else:
            issues.append("Jupyter not available")
        
        return score, issues
    
    score1, issues1 = assess_ipykernel_health(ipk1, name1)
    score2, issues2 = assess_ipykernel_health(ipk2, name2)
    
    print(f"  {name1}: {score1}/4 points")
    if issues1:
        for issue in issues1:
            print(f"    ✗ {issue}")
    
    print(f"  {name2}: {score2}/4 points")
    if issues2:
        for issue in issues2:
            print(f"    ✗ {issue}")

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
                print_status(f"🎯 Heat Reuse Tool kernel '{kernel}': Found on both", "MATCH")
            elif kernel in kernels1:
                print_status(f"🎯 Heat Reuse Tool kernel '{kernel}': Only on {name1}", "DIFF")
            else:
                print_status(f"🎯 Heat Reuse Tool kernel '{kernel}': Only on {name2}", "DIFF")
    else:
        print_status("🎯 Heat Reuse Tool kernel: Not found on either system", "MISSING")
    
    # Check Heat Reuse Tool specific kernels from new export format
    heat_kernels1 = jupyter1.get('heat_reuse_tool_kernels', {})
    heat_kernels2 = jupyter2.get('heat_reuse_tool_kernels', {})
    
    if heat_kernels1 or heat_kernels2:
        print_status("\nDetailed Heat Reuse Tool Kernels:", "INFO")
        all_heat_kernels = set(heat_kernels1.keys()).union(set(heat_kernels2.keys()))
        
        for kernel_name in all_heat_kernels:
            if kernel_name in heat_kernels1 and kernel_name in heat_kernels2:
                print_status(f"  {kernel_name}: Present on both", "MATCH")
            elif kernel_name in heat_kernels1:
                print_status(f"  {kernel_name}: Only on {name1}", "DIFF")
                spec1 = heat_kernels1[kernel_name].get('spec', {})
                if 'display_name' in spec1:
                    print(f"    Display Name: {spec1['display_name']}")
            else:
                print_status(f"  {kernel_name}: Only on {name2}", "DIFF")
                spec2 = heat_kernels2[kernel_name].get('spec', {})
                if 'display_name' in spec2:
                    print(f"    Display Name: {spec2['display_name']}")
    
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
    
    # Critical packages that need to match (including ipykernel)
    critical_packages = ['jupyter', 'pandas', 'numpy', 'matplotlib', 'scipy', 'ipywidgets', 'notebook', 'ipython', 'ipykernel']
    
    for package in critical_packages:
        ver1 = packages1.get(package)
        ver2 = packages2.get(package)
        
        if ver1 and not ver2:
            if package == 'ipykernel':
                recommendations.append(f"pip install {package}=={ver1}  # CRITICAL for VSCode notebooks")
            else:
                recommendations.append(f"pip install {package}=={ver1}")
        elif ver1 and ver2 and ver1 != ver2:
            if package == 'ipykernel':
                recommendations.append(f"pip install {package}=={ver1}  # CRITICAL: Upgrade/downgrade ipykernel from {ver2}")
            else:
                recommendations.append(f"pip install {package}=={ver1}  # Downgrade/upgrade from {ver2}")
    
    # ipykernel-specific recommendations
    ipk1 = env1.get('ipykernel_info', {})
    ipk2 = env2.get('ipykernel_info', {})
    
    # If ipykernel is missing or not working on system 2
    if not ipk2.get('package_installed', False) and ipk1.get('package_installed', False):
        recommendations.append("# CRITICAL: Install ipykernel package")
        ipykernel_version = ipk1.get('version', 'latest')
        recommendations.append(f"pip install ipykernel=={ipykernel_version}")
    
    # If Heat Reuse Tool kernel is not registered on system 2
    if ipk1.get('heat_reuse_kernel_registered', False) and not ipk2.get('heat_reuse_kernel_registered', False):
        recommendations.append("# CRITICAL: Register Heat Reuse Tool kernel for VSCode")
        recommendations.append("python -m ipykernel install --user --name=heat-reuse-tool --display-name=\"Heat Reuse Tool\"")
    
    # Jupyter kernel recommendation from kernelspec comparison
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
                    # Only add if not already added above
                    if "python -m ipykernel install --user --name=heat-reuse-tool" not in ' '.join(recommendations):
                        recommendations.append("# Register Heat Reuse Tool kernel")
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
            if rec.startswith('#'):
                print(f"    {rec}")
            else:
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
                
                f.write("# IMPORTANT: Ensure virtual environment is activated first\n")
                f.write("# .\\.venv\\Scripts\\Activate.ps1\n\n")
                
                f.write("# Verify you're in the correct directory\n")
                f.write("# cd C:\\Code\\OCP_HeatReuseTool  # or your project path\n\n")
                
                for rec in recommendations:
                    if rec.startswith('#'):
                        f.write(f"{rec}\n")
                    else:
                        f.write(f"{rec}\n")
                
                f.write("\n# After running these commands:\n")
                f.write("# 1. Restart VSCode\n")
                f.write("# 2. Open Interactive Analysis Tool.ipynb\n")
                f.write("# 3. Select the correct kernel: 'Heat Reuse Tool' or your .venv environment\n")
                f.write("# 4. Run: python tools/setup/verify_setup.py\n")
            
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
    compare_ipykernel_info(env1, env2, name1, name2)  # NEW: Detailed ipykernel comparison
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
            print(f"\nTip: The tool will now check ipykernel status in detail!")
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
            print_status("🎯 Pay special attention to ipykernel status for VSCode notebook functionality!", "INFO")

if __name__ == "__main__":
    main()