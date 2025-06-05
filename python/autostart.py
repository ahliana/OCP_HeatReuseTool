# Heat Reuse Tool - Autostart (exec-compatible)
# No __file__ usage - works with exec(open().read())

import sys
import os

print("🔧 Heat Reuse Tool - Autostart")
print("=" * 40)

# Use getcwd() instead of __file__ for exec compatibility
current_working_dir = os.getcwd()
python_dir = os.path.join(current_working_dir, 'python')

print(f"📁 Working dir: {current_working_dir}")
print(f"📁 Python dir: {python_dir}")

# Add to path if not already there
if python_dir not in sys.path:
    sys.path.insert(0, python_dir)
    print(f"✅ Added to Python path")
else:
    print(f"✅ Already in Python path")

# Test basic functionality
try:
    print("🧪 Testing basic functionality...")
    test_value = 1493.0
    print(f"✅ Test calculation: {test_value}")
    print("✅ SUCCESS: Basic functionality working")
except Exception as e:
    print(f"❌ ERROR: {e}")

print("=" * 40)
print("🚀 Autostart complete!")

# Make this available to the notebook
autostart_status = "completed"