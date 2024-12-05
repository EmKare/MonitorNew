import phonefiles as files
import subprocess
import sys

def install(package:str):
    try: subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception: subprocess.check_call([sys.executable, "-m", "pip3", "install", package])

for package in files.pip_packages:
    try: install(package.strip())
    except Exception: print(f"Error installing --{package}--")
