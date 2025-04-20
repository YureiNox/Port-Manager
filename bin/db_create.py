import json
import os
from tools.port import scan_network

db_path = "database/db_port.json"

def check_and_create_db():
    if not os.path.exists(db_path):
        print(f"[+] Le fichier {db_path} n'existe pas. Création...")
        with open(db_path, 'w') as f:
            json.dump({}, f, indent=4)  
        print(f"[+] {db_path} créé avec succès.")
    else:
        print(f"[+] Le fichier {db_path} existe déjà.")

def add_scan_results_to_db(scan_results):
    with open(db_path, "r") as f:
        db_data = json.load(f)

    for result in scan_results:
        ip = result['ip']
        port = result['port']
        service = result['service']

        if ip not in db_data:
            db_data[ip] = {}

        if port not in db_data[ip]:
            db_data[ip][port] = {}

        db_data[ip][port]['service'] = service
        db_data[ip][port]['state'] = result['state']
        db_data[ip][port]['protocol'] = result['proto']

    with open(db_path, "w") as f:
        json.dump(db_data, f, indent=4)
    print("[+] Les résultats ont été ajoutés à db_port.json.")

def scan_and_store_results(target="192.168.55.0/24"):
    print(f"[+] Lancement du scan de {target} sur les ports 1-1024...")
    scan_results = scan_network(target)

    add_scan_results_to_db(scan_results)

if __name__ == "__main__":
    check_and_create_db()
    ip = f"192.168.{input("Enter ip adresse base ex:\n192.168.0.0 or 192.168.5.0.\nIn this exemple the base are 0 and 5\nEnter yours: ")}.0/24"
    input(f"Press enter to start with {ip}...")
    scan_and_store_results(ip)
