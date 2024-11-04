from faker import Faker  # type: ignore
import random
import sys, os, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.connectionMongo import connect_mongodb as connect_mongo
from config.connectionRedis import connect_redis as connect_redis

fake = Faker('fr_FR')

def generate_fake_data(num_vols=100000, num_clients=50000, num_reservations=200000):
  vols = []
  clients = []
  reservations = []

  # Générer des vols
  for i in range(1, num_vols + 1):
    vol_id = f"V{i:03d}"  # Format du type 'V001', 'V002', etc.
    vol = {
      '_id': vol_id,
      'VilleD': fake.city(),
      'VilleA': fake.city(),
      'Pilote': {'NomPil': fake.last_name()},
      'DateD': fake.date_time_this_year()  # Renvoie un objet datetime.datetime
    }
    vols.append(vol)

  # Index des vols pour accès rapide
  vols_index = {vol['_id']: vol for vol in vols}

  # Générer des clients
  for i in range(1001, 1001 + num_clients):
    client_id = str(i)
    client = {
      '_id': client_id,
      'NomCl': fake.last_name(),
      'Adresse': {
        'NumRueCl': str(fake.random_int(min=1, max=100)),
        'NomRueCl': fake.street_name(),
        'CodePosteCl': fake.postcode(),
        'VilleCl': fake.city()
      },
      'Email': '',
      'Telephone': ''
    }
    clients.append(client)

  # Index des clients pour accès rapide
  clients_index = {client['_id']: client for client in clients}

  # Générer des réservations
  for i in range(1, num_reservations + 1):
    reservation_id = f"R{i:03d}"
    client_id = random.choice(clients)['_id']
    vol_id = random.choice(vols)['_id']
    reservation = {
      '_id': reservation_id,
      'VolId': vol_id,
      'ClientId': client_id,
      'NbPlaces': str(random.randint(1, 8)),  # NbPlaces comme chaîne
      'Classe': random.choice(['Business', 'Touriste', 'Economique'])
    }
    reservations.append(reservation)

  return vols, clients, reservations

def insert_data_into_mongodb(vols, clients, reservations):
  client = connect_mongo()

  db = client.get_database('BookingSystemDB')

  vols_collection = db['vols']
  clients_collection = db['clients']
  reservations_collection = db['reservations']

  # Supprimer les données existantes pour éviter les duplications
  vols_collection.delete_many({})
  clients_collection.delete_many({})
  reservations_collection.delete_many({})

  # Insérer les nouvelles données
  vols_collection.insert_many(vols)
  clients_collection.insert_many(clients)
  reservations_collection.insert_many(reservations)

def insert_data_into_redis(vols, clients, reservations):
  r = connect_redis()
  r.flushdb()  # Effacer la base de données Redis avant l'insertion

  # Insérer les vols
  for vol in vols:
    key = f"vol:{vol['_id']}"
    r.set(key, json.dumps(vol, default=str))  # Ajouter default=str

  # Insérer les clients
  for client in clients:
    key = f"client:{client['_id']}"
    r.set(key, json.dumps(client, default=str))  # Ajouter default=str

  # Insérer les réservations
  for reservation in reservations:
    key = f"reservation:{reservation['_id']}"
    r.set(key, json.dumps(reservation, default=str))  # Ajouter default=str

if __name__ == "__main__":
  vols, clients, reservations = generate_fake_data()
  insert_data_into_mongodb(vols, clients, reservations)
  insert_data_into_redis(vols, clients, reservations)
