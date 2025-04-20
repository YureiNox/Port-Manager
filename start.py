import subprocess
import sys
import os
from time import sleep

modules = ["requests"]

for module in modules:
    try:
        __import__(module)
    except ImportError:
        print(f"Module {module} is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        print(f"Module {module} installed successfully.")

print("Starting the program...")
sleep(1.5)
print("Please wait...")
sleep(2)
os.system("cls" if os.name == "nt" else "clear")
subprocess.run([sys.executable, "menu.py"])
print("Program finished.")
print("Exiting...")
print("Bye!")

