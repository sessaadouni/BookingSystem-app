import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './src/')))

from config.connectionMongo import connect_mongodb as connect

client = connect()

db = client.get_database('BookingSystemDB')

def load_vols_from_mongo() -> list:
  """
  [Summary]
    Charge tous les vols depuis MongoDB et les retourne sous forme de liste.
    
  [Returns]
    vols: liste de vols
  """
  return list(db.get_collection('vols').find())
  

def load_clients_from_mongo() -> list:
  """
  [Summary]
    Charge tous les clients depuis MongoDB et les retourne sous forme de liste.
    
  [Returns]
    clients: liste de clients
  """
  return list(db.get_collection('clients').find())

def load_reservations_from_mongo() -> list:
  """
  [Summary]
    Charge toutes les réservations depuis MongoDB et les retourne sous forme de liste.
    
  [Returns]
    reservations: liste de réservations
  """
  return list(db.get_collection('reservations').find())