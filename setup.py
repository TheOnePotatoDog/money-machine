import subprocess
import sys

def install_dependencies():
    print("Installing required packages...")
    packages = [
        'stripe',
        'python-dotenv',
        'requests'
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    install_dependencies() 