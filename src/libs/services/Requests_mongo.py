from pymongo import MongoClient, ASCENDING # type: ignore
from typing import List, Optional, Dict, Callable

class RequestsMongo:
  """
  Cette classe permet de faire des requêtes de données en utilisant MongoDB.

  [Args]
    uri: URI de connexion MongoDB
    db_name: nom de la base de données
  """

  def __init__(self, connect: Callable):
    """
    Initialise une instance de la classe.

    [Args]
      uri: URI de connexion MongoDB
      db_name: nom de la base de données
    """
    self.client = connect()
    self.db = self.client["BookingSystemDB"]
    
    self.vols_collection = self.db['vols']
    self.clients_collection = self.db['clients']
    self.reservations_collection = self.db['reservations']

    # Création des index pour optimiser les performances
    self.create_indexes()

  def create_indexes(self):
    """Crée des index sur les champs fréquemment utilisés pour optimiser les requêtes."""
    # Index pour les vols
    self.vols_collection.create_index([('VilleD', ASCENDING)])
    self.vols_collection.create_index([('VilleA', ASCENDING)])
    self.vols_collection.create_index([('Pilote.NomPil', ASCENDING)])

    # Index pour les réservations
    self.reservations_collection.create_index([('ClientId', ASCENDING)])
    self.reservations_collection.create_index([('VolId', ASCENDING)])

  # Fonctions CRUD pour les vols
  def create_vol(self, vol_data: dict) -> str:
    """
    Crée un nouveau vol.

    [Args]
      vol_data: données du vol à insérer

    [Returns]
      str: l'identifiant du vol créé
    """
    result = self.vols_collection.insert_one(vol_data)
    return str(result.inserted_id)

  def update_vol(self, vol_id: str, update_data: dict) -> int:
    """
    Met à jour un vol existant.

    [Args]
      vol_id: identifiant du vol à mettre à jour
      update_data: données à mettre à jour

    [Returns]
      int: le nombre de documents mis à jour
    """
    result = self.vols_collection.update_one({'_id': vol_id}, {'$set': update_data})
    return result.modified_count

  def delete_vol(self, vol_id: str) -> int:
    """
    Supprime un vol.

    [Args]
      vol_id: identifiant du vol à supprimer

    [Returns]
      int: le nombre de documents supprimés
    """
    result = self.vols_collection.delete_one({'_id': vol_id})
    return result.deleted_count

  # Fonctions CRUD pour les clients
  def create_client(self, client_data: dict) -> str:
    result = self.clients_collection.insert_one(client_data)
    return str(result.inserted_id)

  def update_client(self, client_id: str, update_data: dict) -> int:
    result = self.clients_collection.update_one({'_id': client_id}, {'$set': update_data})
    return result.modified_count

  def delete_client(self, client_id: str) -> int:
    result = self.clients_collection.delete_one({'_id': client_id})
    return result.deleted_count

  # Fonctions CRUD pour les réservations
  def create_reservation(self, reservation_data: dict) -> str:
    result = self.reservations_collection.insert_one(reservation_data)
    return str(result.inserted_id)

  def update_reservation(self, reservation_id: str, update_data: dict) -> int:
    result = self.reservations_collection.update_one({'_id': reservation_id}, {'$set': update_data})
    return result.modified_count

  def delete_reservation(self, reservation_id: str) -> int:
    result = self.reservations_collection.delete_one({'_id': reservation_id})
    return result.deleted_count

  # Fonctions de lecture optimisées
  def get_vols(self, projection: Optional[Dict] = None) -> List[dict]:
    """
    Retourne une liste de tous les vols.

    [Args]
      projection: champs à inclure ou exclure

    [Returns]
      vols: liste de vols
    """
    vols = list(self.vols_collection.find({}, projection))
    return vols

  def get_clients(self, projection: Optional[Dict] = None) -> List[dict]:
    clients = list(self.clients_collection.find({}, projection))
    return clients

  def get_reservations(self, projection: Optional[Dict] = None) -> List[dict]:
    reservations = list(self.reservations_collection.find({}, projection))
    return reservations

  def get_vol_by_id(self, vol_id: str, projection: Optional[Dict] = None) -> Optional[dict]:
    vol = self.vols_collection.find_one({'_id': vol_id}, projection)
    return vol

  def get_client_by_id(self, client_id: str, projection: Optional[Dict] = None) -> Optional[dict]:
    client = self.clients_collection.find_one({'_id': client_id}, projection)
    return client

  def get_reservation_by_id(self, reservation_id: str, projection: Optional[Dict] = None) -> Optional[dict]:
    reservation = self.reservations_collection.find_one({'_id': reservation_id}, projection)
    return reservation

  def get_arrival_cities(self) -> List[str]:
    """
    Retourne une liste de toutes les villes d'arrivée des vols.

    [Returns]
      villes: liste de villes d'arrivée
    """
    pipeline = [
      {'$group': {'_id': '$VilleA', 'count': {'$sum': 1}}},
      {'$sort': {'count': -1}}
    ]
    villes = list(self.vols_collection.aggregate(pipeline))
    return villes

  def get_arrival_city_by_id(self, vol_id: str) -> Optional[str]:
    """
    Retourne la ville d'arrivée d'un vol en fonction de son identifiant.

    [Args]
      vol_id: identifiant du vol

    [Returns]
      ville: ville d'arrivée du vol
    """
    vol = self.get_vol_by_id(vol_id, projection={'VilleA': 1})
    if vol and 'VilleA' in vol:
      return vol['VilleA']
    return None

  def get_pilotes(self) -> List[str]:
    """
    Retourne une liste des noms de tous les pilotes, sans doublons.

    [Returns]
      pilotes: liste de noms de pilotes
    """
    pilotes = self.vols_collection.distinct('Pilote.NomPil')
    return pilotes

  def get_vols_by_departure_city(self, departure_city: str, projection: Optional[Dict] = None) -> List[dict]:
    """
    Retourne une liste des vols au départ d'une ville donnée.

    [Args]
      departure_city: ville de départ

    [Returns]
      vols: liste de vols au départ de la ville
    """
    vols = list(self.vols_collection.find({'VilleD': departure_city}, projection))
    return vols

  # Méthodes optimisées avec pipelines d'agrégation
  def get_reservations_by_client(self, client_id: str) -> List[dict]:
    """
    Retourne la liste des réservations pour un client donné, avec les détails des vols.

    [Args]
      client_id: identifiant du client

    [Returns]
      reservations: liste de réservations pour le client
    """
    pipeline = [
      {'$match': {'ClientId': client_id}},
      {'$lookup': {
        'from': 'vols',
        'localField': 'VolId',
        'foreignField': '_id',
        'as': 'Vol'
      }},
      {'$unwind': '$Vol'}
    ]
    reservations = list(self.reservations_collection.aggregate(pipeline))
    return reservations

  def get_clients_by_flight(self, vol_id: str) -> List[dict]:
    """
    Retourne la liste des clients ayant des réservations sur un vol donné, avec les détails des clients.

    [Args]
      vol_id: identifiant du vol

    [Returns]
      clients: liste de clients
    """
    pipeline = [
      {'$match': {'VolId': vol_id}},
      {'$lookup': {
        'from': 'clients',
        'localField': 'ClientId',
        'foreignField': '_id',
        'as': 'Client'
      }},
      {'$unwind': '$Client'}
    ]
    reservations = list(self.reservations_collection.aggregate(pipeline))
    return reservations

  def get_flights_by_pilot(self, nom_pilote: str, projection: Optional[Dict] = None) -> List[dict]:
    """
    Retourne la liste des vols opérés par un pilote donné.

    [Args]
      nom_pilote: nom du pilote
      projection: champs à inclure ou exclure

    [Returns]
      flights: liste de vols opérés par le pilote
    """
    vols = list(self.vols_collection.find({'Pilote.NomPil': nom_pilote}, projection))
    return vols

  def get_clients_by_pilot(self, nom_pilote: str) -> List[dict]:
    """
    Retourne la liste des clients ayant des réservations sur les vols opérés par un pilote donné.

    [Args]
      nom_pilote: nom du pilote

    [Returns]
      clients: liste de clients
    """
    pipeline = [
      {'$match': {'Pilote.NomPil': nom_pilote}},
      {'$project': {'_id': 1}},
      {'$lookup': {
        'from': 'reservations',
        'localField': '_id',
        'foreignField': 'VolId',
        'as': 'Reservations'
      }},
      {'$unwind': '$Reservations'},
      {'$replaceRoot': {'newRoot': '$Reservations'}},
      {'$lookup': {
        'from': 'clients',
        'localField': 'ClientId',
        'foreignField': '_id',
        'as': 'Client'
      }},
      {'$unwind': '$Client'}
    ]
    clients = list(self.vols_collection.aggregate(pipeline))
    return clients
