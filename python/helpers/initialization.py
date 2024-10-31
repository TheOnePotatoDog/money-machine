import pkg_resources
import subprocess
import sys

def check_dependencies():
    required = {
        'stripe': '7.0.0',
        'python-dotenv': '0.19.0',
        'requests': '2.26.0'
    }
    
    missing = []
    
    for package, version in required.items():
        try:
            pkg_resources.require(f"{package}>={version}")
        except pkg_resources.VersionConflict:
            missing.append(f"{package}>={version}")
        except pkg_resources.DistributionNotFound:
            missing.append(f"{package}>={version}")
    
    if missing:
        print("Missing required packages. Installing...")
        for package in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("All required packages installed successfully!")

def initialize():
    check_dependencies()
    # ... rest of initialization code ... 