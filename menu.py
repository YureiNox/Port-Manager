import os
import json
from bin.tools.port import scan_network as port_sc

def menu():
    os.system("cls" if os.name == "nt" else "clear")
    print("""
Welcome to the Network Scanner Menu

[1] Scan network
[2] Add data to the database
[3] Delete data from the database
[4] Modify data in the database
[5] List data in the database and export to CSV, JSON, or TXT
[6] Create database from scan results
[7] Exit
""")
    
    choice = input("Please select an option: ")

    if choice == '1':
        ip = f"192.168.{input("Enter ip adresse base ex:\n192.168.0.0 or 192.168.5.0.\nIn this exemple the base are 0 and 5\nEnter yours: ")}.0/24"
        input(f"Press enter to start with {ip}...")
        port_sc(ip)
        os.system("cls" if os.name == "nt" else "clear")
        for result in port_sc(ip):
            print(f"IP: {result['ip']}, Port: {result['port']}, Protocol: {result['proto']}, State: {result['state']}, Service: {result['service']}")
        menu()
    elif choice == '2':
        os.system("cls" if os.name == "nt" else "clear")
        os.system("python bin/db-manager.py --add")
        os.system("cls" if os.name == "nt" else "clear")
        menu()
    elif choice == '3':
        os.system("cls" if os.name == "nt" else "clear")
        os.system("python bin/db-manager.py --delete")
        os.system("cls" if os.name == "nt" else "clear")
        menu()
    elif choice == '4':
        os.system("cls" if os.name == "nt" else "clear")
        os.system("python bin/db-manager.py --modify")
        os.system("cls" if os.name == "nt" else "clear")
        menu()
    elif choice == '5':
        os.system("cls" if os.name == "nt" else "clear")
        os.system("python bin/db-manager.py --list")
        os.system("cls" if os.name == "nt" else "clear")
        menu()
    elif choice == '6':
        os.system("cls" if os.name == "nt" else "clear")
        os.system("python bin/db-manager.py --create")
        os.system("cls" if os.name == "nt" else "clear")
        menu()
    elif choice == '7':
        os.system("cls" if os.name == "nt" else "clear")
        print("Exiting...")
        exit()

menu()