import json
import sys, os

# Définir le chemin 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Définir le chemin vers le dossier contenant les fichiers JSON
SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(SRC, 'libs', 'DAL', 'db', 'json')

from config.connectionRedis import connect_redis as connect

# Charger les données JSON
with open(os.path.join(DATA_DIR, 'vols.json'), 'r', encoding='utf-8') as f: vols = json.load(f)
with open(os.path.join(DATA_DIR, 'clients.json'), 'r', encoding='utf-8') as f: clients = json.load(f)
with open(os.path.join(DATA_DIR, 'reservations.json'), 'r', encoding='utf-8') as f: reservations = json.load(f)

r = connect()

def clear_redis_database():
  r.flushdb()
  
clear_redis_database()

# Insérer les vols dans Redis
for vol in vols:
  vol_id = vol['_id']
  # Stocker le vol sous la clé 'vol:{vol_id}'
  r.set(f'vol:{vol_id}', json.dumps(vol))

# Insérer les clients dans Redis
for client in clients:
  client_id = client['_id']
  # Stocker le client sous la clé 'client:{client_id}'
  r.set(f'client:{client_id}', json.dumps(client))

# Insérer les réservations dans Redis
for reservation in reservations:
  reservation_id = reservation['_id']
  # Stocker la réservation sous la clé 'reservation:{reservation_id}'
  r.set(f'reservation:{reservation_id}', json.dumps(reservation))

print("Données insérées avec succès dans Redis.")