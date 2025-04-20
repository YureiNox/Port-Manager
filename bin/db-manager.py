import argparse
import subprocess
import sys

parser = argparse.ArgumentParser(description="Gestion des opérations sur la base de données")

# Ajout d'un groupe d'arguments exclusifs (seul un argument peut être choisi)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--add', action='store_true', help='Add data to database')
group.add_argument('--create', action='store_true', help='Create database')
group.add_argument('--delete', action='store_true', help='Delete data from database')
group.add_argument('--modify', action='store_true', help='Modify data in database')
group.add_argument('--list', action='store_true', help='List data in database')

args = parser.parse_args()

# Vérification de l'option choisie et exécution correspondante
if args.add:
    subprocess.run([sys.executable, "bin/db_add.py"])
elif args.create:
    subprocess.run([sys.executable, "bin/db_create.py"])
elif args.delete:
    subprocess.run([sys.executable, "bin/db_delete.py"])
elif args.modify:
    subprocess.run([sys.executable, "bin/db_modify.py"])
elif args.list:
    subprocess.run([sys.executable, "bin/db_list.py"])
else:
    print("Invalid option. Use --help for more information.")
    sys.exit(1)
