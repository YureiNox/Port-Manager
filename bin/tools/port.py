import subprocess
import os
import requests
import xml.etree.ElementTree as ET

def download_nmap_services(filepath="database/nmap-services"):
    if not os.path.exists(filepath):
        url = "https://raw.githubusercontent.com/nmap/nmap/master/nmap-services"
        response = requests.get(url)
        with open(filepath, "w") as f:
            f.write(response.text)

def load_port_db(filepath="database/nmap-services"):
    port_db = {}
    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) >= 2:
                service = parts[0]
                port_proto = parts[1]
                if "/" in port_proto:
                    port, proto = port_proto.split("/")
                    port_db[(port, proto)] = service
    return port_db

def run_nmap_scan(target="192.168.1.0/24", ports="1-1024", output_file="scan_output.xml"):
    cmd = ["nmap", "-p", ports, "-T4", "-oX", output_file, target]
    subprocess.run(cmd, stdout=subprocess.DEVNULL)
    return output_file

def parse_nmap_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    results = []

    for host in root.findall("host"):
        addr_tag = host.find("address")
        if addr_tag is None:
            continue
        addr = addr_tag.get("addr")
        ports = host.find("ports")
        if ports is None:
            continue
        for port in ports.findall("port"):
            port_id = port.get("portid")
            proto = port.get("protocol")
            state_tag = port.find("state")
            state = state_tag.get("state") if state_tag is not None else "unknown"
            results.append({
                "ip": addr,
                "port": port_id,
                "proto": proto,
                "state": state
            })
    return results

def annotate_ports(results, port_db):
    annotated = []
    for r in results:
        key = (r["port"], r["proto"])
        service = port_db.get(key, "unknown")
        annotated.append({
            "ip": r["ip"],
            "port": r["port"],
            "proto": r["proto"],
            "state": r["state"],
            "service": service
        })
    return annotated

# 👇 Fonction principale à appeler depuis l’extérieur
def scan_network(target="192.168.1.0/24", ports="1-1024"):
    download_nmap_services()
    port_db = load_port_db()
    xml_output = run_nmap_scan(target, ports)
    scan_results = parse_nmap_xml(xml_output)
    annotated_results = annotate_ports(scan_results, port_db)
    return annotated_results
