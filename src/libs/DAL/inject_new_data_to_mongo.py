import sys, os, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.connectionMongo import connect_mongodb as connect

# Définir le chemin vers le dossier contenant les fichiers JSON
SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(SRC, 'libs', 'DAL', 'db', 'json')

# Charger les données JSON
with open(os.path.join(DATA_DIR, 'vols.json'), 'r', encoding='utf-8') as f: vols = json.load(f)
with open(os.path.join(DATA_DIR, 'clients.json'), 'r', encoding='utf-8') as f: clients = json.load(f)
with open(os.path.join(DATA_DIR, 'reservations.json'), 'r', encoding='utf-8') as f: reservations = json.load(f)

# Se connecter à MongoDB
client = connect()

db = client.get_database('BookingSystemDB')

# Créer ou obtenir les collections
vols_collection = db.get_collection('vols')
clients_collection = db.get_collection('clients')
reservations_collection = db.get_collection('reservations')

# Effacer les collections existantes pour éviter les doublons lors de ré-exécutions
vols_collection.delete_many({})
clients_collection.delete_many({})
reservations_collection.delete_many({})

# Insérer les documents JSON dans chaque collection respective
vols_collection.insert_many(vols)
clients_collection.insert_many(clients)
reservations_collection.insert_many(reservations)

print("Les données ont été insérées avec succès dans MongoDB.")