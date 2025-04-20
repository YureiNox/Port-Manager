import json
import os
import requests

db_directory = "database"
db_path = os.path.join(db_directory, "db_port.json")
nmap_services_url = "https://raw.githubusercontent.com/nmap/nmap/master/nmap-services"
nmap_services_path = os.path.join(db_directory, "nmap-services")

def check_and_create_db():
    if not os.path.exists(db_directory):
        print(f"[+] Le dossier '{db_directory}' n'existe pas. Création...")
        os.makedirs(db_directory)

    if not os.path.exists(db_path):
        print(f"[+] Le fichier {db_path} n'existe pas. Création...")
        with open(db_path, 'w') as f:
            json.dump({}, f, indent=4)
        print(f"[+] {db_path} créé avec succès.")
    else:
        print(f"[+] Le fichier {db_path} existe déjà.")

def download_nmap_services():
    if not os.path.exists(nmap_services_path):
        print(f"[+] Téléchargement de la liste des services Nmap depuis {nmap_services_url}...")
        response = requests.get(nmap_services_url)
        with open(nmap_services_path, 'w') as f:
            f.write(response.text)
        print(f"[+] Liste des services Nmap téléchargée et enregistrée sous {nmap_services_path}.")
    else:
        print(f"[+] Le fichier des services Nmap existe déjà à {nmap_services_path}.")

    services = {}
    with open(nmap_services_path, 'r') as f:
        for line in f:
            if line and not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 2:
                    port_proto = parts[1]
                    if "/" in port_proto:
                        port, proto = port_proto.split("/")
                        services[(port, proto)] = parts[0]
    return services

def add_port_to_db(ip, port, state, service, protocol):
    with open(db_path, "r") as f:
        db_data = json.load(f)

    if ip not in db_data:
        db_data[ip] = {}

    if port in db_data[ip]:
        print(f"[!] Le port {port} est déjà utilisé par l'IP {ip}. Veuillez en choisir un autre.")
        return False 

    db_data[ip][port] = {
        "service": service,
        "state": state,
        "protocol": protocol
    }

    with open(db_path, "w") as f:
        json.dump(db_data, f, indent=4)
    print(f"[+] Le port {port} a été ajouté à l'IP {ip} avec le service '{service}'.")
    return True  

def get_service_from_nmap(services_db, port, protocol):
    key = (str(port), protocol)
    return services_db.get(key, "unknown")

def main():
    check_and_create_db()

    download_nmap_services()

    services_db = download_nmap_services()

    ip = input("Entrez l'IP de l'appareil : ")
    
    while True:
        port = input("Entrez le port à ajouter : ")

        with open(db_path, "r") as f:
            db_data = json.load(f)
        
        if ip in db_data:
            print(f"\n[+] L'IP {ip} existe déjà dans la base de données.\n")
        else:
            print(f"\n[+] L'IP {ip} n'existe pas dans la base de données. Elle sera ajoutée.\n")

        if ip in db_data and str(port) in db_data[ip]:
            print(f"[!] Le port {port} est déjà utilisé pour l'IP {ip}.")
            continue 

        break 

    default_service = get_service_from_nmap(services_db, port, "tcp")  
    default_protocol = "tcp"  

    service = input(f"Entrez le service [Default:{default_service}] : ") or default_service
    protocol = input(f"Entrez le protocole [Default:{default_protocol}] : ") or default_protocol
    state = input(f"Entrez l'état du port {port} (open/closed) : ").lower()

    if add_port_to_db(ip, port, state, service, protocol):
        print(f"[+] Port {port} ajouté avec succès à l'IP {ip}.")
    else:
        print("[!] L'ajout du port a échoué.")

if __name__ == "__main__":
    main()
