import os
import json
import sys

db_dir = "database"
db_path = os.path.join(db_dir, "db_port.json")
nmap_services_path = os.path.join(db_dir, "nmap-services")

def load_nmap_services():
    services = {}
    if os.path.exists(nmap_services_path):
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
    print(f"\n[+] Ports available for {ip}:")
    port_list = list(ports.keys())
    for i, p in enumerate(port_list, 1):
        entry = ports[p]
        print(f"[{i}] -- {p} -- {entry['service']} -- {entry['protocol']} -- {entry['state']}")
    return port_list

def main():
    db = load_db()
    nmap_services = load_nmap_services()

    ip_list = display_ip_list(db)

    while True:
        ip_input = input("\nEnter the IP number or the IP address to modify a port: ").strip()
        selected_ip = None

        if ip_input.isdigit() and 1 <= int(ip_input) <= len(ip_list):
            selected_ip = ip_list[int(ip_input) - 1]
        elif ip_input in db:
            selected_ip = ip_input

        if selected_ip:
            break
        print("[!] Invalid input. Please try again.")

    port_list = display_ports(selected_ip, db[selected_ip])

    while True:
        port_input = input("\nEnter the port number or port to modify: ").strip()
        selected_port = None

        if port_input.isdigit() and 1 <= int(port_input) <= len(port_list):
            selected_port = port_list[int(port_input) - 1]
        elif port_input in db[selected_ip]:
            selected_port = port_input

        if selected_port:
            break
        print("[!] Invalid input. Please try again.")

    old_entry = db[selected_ip][selected_port]
    old_service = old_entry.get("service", "")
    old_protocol = old_entry.get("protocol", "")
    old_state = old_entry.get("state", "")
    old_port = selected_port

    print(f"\n[+] Current port {old_port} details:")
    print(f"    - Old Service: {old_service}")
    print(f"    - Old Protocol: {old_protocol}")
    print(f"    - Old State: {old_state}")

    new_port = input(f"Enter the new port number (current: {old_port}): ").strip() or old_port

    new_protocol = input(f"Enter the new protocol for port {new_port} (old: {old_protocol}, recommended: {old_protocol}): ").strip() or old_protocol

    recommended_service = nmap_services.get((str(new_port), new_protocol), "unknown")

    new_service = input(f"Enter the new service for port {new_port} (old: {old_service}, recommended: {recommended_service}): ").strip() or recommended_service

    new_state = input(f"Enter the new state for port {new_port} (old: {old_state}, recommended: {old_state}): ").strip() or old_state

    if new_port != old_port:
        del db[selected_ip][old_port]

    db[selected_ip][new_port] = {
        "service": new_service,
        "protocol": new_protocol,
        "state": new_state
    }

    save_db(db)
    print(f"\n[+] Port {old_port} has been successfully modified to {new_port}.")

if __name__ == "__main__":
    main()
