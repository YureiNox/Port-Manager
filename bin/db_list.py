import os
import json
import csv
import platform

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def load_db(path="database/db_port.json"):
    if not os.path.exists(path):
        print("[!] Database file not found.")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def view_full_db(db):
    if not db:
        print("[!] Database is empty.")
        return
    print(f"{'IP Address':<18} | {'Port':<6} | {'Service':<20} | {'Protocol':<8} | {'State':<8}")
    print("-" * 70)
    for ip, ports in db.items():
        for port, data in ports.items():
            print(f"{ip:<18} | {port:<6} | {data['service']:<20} | {data['protocol']:<8} | {data['state']:<8}")

def view_by_ip(db):
    if not db:
        print("[!] Database is empty.")
        return
    print("\nAvailable IPs:")
    ip_list = list(db.keys())
    for idx, ip in enumerate(ip_list, 1):
        print(f"[{idx}] -- {ip}")
    choice = input("\nEnter IP number or full IP: ").strip()
    selected_ip = None
    if choice.isdigit() and 1 <= int(choice) <= len(ip_list):
        selected_ip = ip_list[int(choice)-1]
    elif choice in ip_list:
        selected_ip = choice
    else:
        print("[!] Invalid selection.")
        return
    print(f"\n[+] Ports for {selected_ip}:")
    print(f"{'Port':<6} | {'Service':<20} | {'Protocol':<8} | {'State':<8}")
    print("-" * 50)
    for port, data in db[selected_ip].items():
        print(f"{port:<6} | {data['service']:<20} | {data['protocol']:<8} | {data['state']:<8}")

def search_port_or_service(db):
    query = input("Enter port number or service name: ").strip().lower()
    found = False
    for ip, ports in db.items():
        for port, data in ports.items():
            if query == port or query == data["service"].lower():
                if not found:
                    print(f"\n{'IP Address':<18} | {'Port':<6} | {'Service':<20} | {'Protocol':<8} | {'State':<8}")
                    print("-" * 70)
                print(f"{ip:<18} | {port:<6} | {data['service']:<20} | {data['protocol']:<8} | {data['state']:<8}")
                found = True
    if not found:
        print("[!] No matching results found.")

def export_to_csv(db):
    export_path = "export.csv"
    with open(export_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP Address", "Port", "Service", "Protocol", "State"])
        for ip, ports in db.items():
            for port, data in ports.items():
                writer.writerow([ip, port, data["service"], data["protocol"], data["state"]])
    print(f"[+] Exported to '{export_path}'.")

def export_to_json(db):
    export_path = "export.json"
    with open(export_path, mode='w', encoding='utf-8') as jsonfile:
        json.dump(db, jsonfile, indent=4, ensure_ascii=False)
    print(f"[+] Exported to '{export_path}'.")

def export_to_txt(db):
    export_path = "export.txt"
    with open(export_path, mode='w', encoding='utf-8') as txtfile:
        txtfile.write(f"{'IP Address':<18} | {'Port':<6} | {'Service':<20} | {'Protocol':<8} | {'State':<8}\n")
        txtfile.write("-" * 70 + "\n")
        for ip, ports in db.items():
            for port, data in ports.items():
                txtfile.write(f"{ip:<18} | {port:<6} | {data['service']:<20} | {data['protocol']:<8} | {data['state']:<8}\n")
    print(f"[+] Exported to '{export_path}'.")

def main_menu():
    while True:
        clear_screen()
        print("=" * 50)
        print("       DATABASE MANAGEMENT INTERFACE")
        print("=" * 50)
        print("[1] View full database")
        print("[2] View by IP address")
        print("[3] Search by port or service")
        print("[4] Exit")
        print("[5] Export to CSV")
        print("[6] Export to JSON")
        print("[7] Export to TXT")
        print("-" * 50)
        choice = input("Enter your choice: ").strip()

        db = load_db()
        print()

        if choice == "1":
            view_full_db(db)
        elif choice == "2":
            view_by_ip(db)
        elif choice == "3":
            search_port_or_service(db)
        elif choice == "4":
            print("[+] Exiting. Bye!")
            break
        elif choice == "5":
            export_to_csv(db)
        elif choice == "6":
            export_to_json(db)
        elif choice == "7":
            export_to_txt(db)
        else:
            print("[!] Invalid choice. Try again.")

        input("\n[↩] Press Enter to return to menu...")

if __name__ == "__main__":
    main_menu()
