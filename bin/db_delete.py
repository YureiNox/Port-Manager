import os
import json
import sys

db_dir = "database"
db_path = os.path.join(db_dir, "db_port.json")

def load_db():
    if not os.path.exists(db_path):
        print(f"[!] Database file not found at {db_path}")
        sys.exit(1)
    with open(db_path, "r") as f:
        return json.load(f)

def save_db(data):
    with open(db_path, "w") as f:
        json.dump(data, f, indent=4)

def display_ip_list(db):
    print("\nAvailable IP addresses:")
    ip_list = list(db.keys())
    for i, ip in enumerate(ip_list, 1):
        print(f"[{i}] -- {ip} -- {len(db[ip])} PORT(S)")
    return ip_list

def display_ports(ip, ports):
    print(f"\n[+] Ports for {ip}:")
    port_list = list(ports.keys())
    for i, p in enumerate(port_list, 1):
        entry = ports[p]
        print(f"[{i}] -- {p} -- {entry['service']} -- {entry['protocol']} -- {entry['state']}")
    return port_list

def main():
    db = load_db()

    if not db:
        print("[!] The database is empty.")
        return

    ip_list = display_ip_list(db)

    while True:
        ip_input = input("\nEnter the IP number or the IP address to delete from: ").strip()
        selected_ip = None

        if ip_input.isdigit() and 1 <= int(ip_input) <= len(ip_list):
            selected_ip = ip_list[int(ip_input) - 1]
        elif ip_input in db:
            selected_ip = ip_input

        if selected_ip:
            break
        print("[!] Invalid input. Please try again.")

    choice = input(f"\nDo you want to delete ALL ports from {selected_ip}? (y/N): ").strip().lower()
    if choice == "y":
        del db[selected_ip]
        save_db(db)
        print(f"[+] All data for {selected_ip} has been deleted.")
        return

    port_list = display_ports(selected_ip, db[selected_ip])

    while True:
        port_input = input("\nEnter the port number or port name to delete: ").strip()
        selected_port = None

        if port_input.isdigit() and 1 <= int(port_input) <= len(port_list):
            selected_port = port_list[int(port_input) - 1]
        elif port_input in db[selected_ip]:
            selected_port = port_input

        if selected_port:
            break
        print("[!] Invalid port. Please try again.")

    confirm = input(f"\nAre you sure you want to delete port {selected_port} from {selected_ip}? (y/N): ").strip().lower()
    if confirm == "y":
        del db[selected_ip][selected_port]
        print(f"[+] Port {selected_port} has been deleted from {selected_ip}.")
        if not db[selected_ip]: 
            del db[selected_ip]
            print(f"[i] No more ports for {selected_ip}, IP entry removed.")
        save_db(db)
    else:
        print("[i] Deletion cancelled.")

if __name__ == "__main__":
    main()
