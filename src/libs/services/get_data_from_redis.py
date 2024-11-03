import os, sys, json

# Ajouter le chemin au module de connexion Redis si nécessaire
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.connectionRedis import connect_redis as connect

r = connect()

# def load_vols_from_redis() -> list:
#   """
#   Charge tous les vols depuis Redis et les retourne sous forme de liste.
#   """
#   vols_list = []
#   # Récupérer toutes les clés des vols
#   vol_keys = r.keys('vol:*')
#   for key in vol_keys:
#     vol_data = r.get(key)
#     if vol_data:
#       vol = json.loads(vol_data)
#       vols_list.append(vol)
#   return vols_list

# best performance with scan
def load_vols_from_redis() -> list:
  """
  [Summary]
    Charge tous les vols depuis Redis en utilisant SCAN et les retourne sous forme de liste.
    
  [Returns]
    vols: liste de vols
  """
  vols_list = []
  cursor = 0
  while True:
    cursor, keys = r.scan(cursor=cursor, match='vol:*', count=100)
    for key in keys:
      vol_data = r.get(key)
      if vol_data:
        vol = json.loads(vol_data)
        vols_list.append(vol)
    if cursor == 0: break
  return vols_list

def load_clients_from_redis() -> list:
  """
  [Summary]
    Charge tous les clients depuis Redis et les retourne sous forme de liste.
    
  [Returns]
    clients: liste de clients
  """
  clients_list = []
  cursor = 0
  while True:
    cursor, keys = r.scan(cursor=cursor, match='client:*', count=100)
    for key in keys:
      client_data = r.get(key)
      if client_data:
        client = json.loads(client_data)
        clients_list.append(client)
    if cursor == 0: break
  return clients_list

def load_reservations_from_redis() -> list:
  """
  [Summary]
    Charge toutes les réservations depuis Redis et les retourne sous forme de liste.
    
  [Returns]
    reservations: liste de réservations
  """
  reservations_list = []
  cursor = 0
  while True:
    cursor, keys = r.scan(cursor=cursor, match='reservation:*', count=100)
    for key in keys:
      reservation_data = r.get(key)
      if reservation_data:
        reservation = json.loads(reservation_data)
        reservations_list.append(reservation)
    if cursor == 0: break
  return reservations_list