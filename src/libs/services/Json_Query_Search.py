from typing import List, Optional

class Requests_Json:
  ''' 
  Cette classe permet de faire des requetes de données JSON.
  
  [Args]
    vols: liste des vols
    clients: liste des clients
    reservations: liste des réservations
  '''
  
  def __init__(self, vols: Optional[List[dict]] = None, clients: Optional[List[dict]] = None, reservations: Optional[List[dict]] = None):
    """
    [Summary]
      Initialise une instance de la classe.
      
    [Args]
      vols: liste des vols
      clients: liste des clients
      reservations: liste des réservations
      
    [Details]
      Les arguments sont optionnels, mais il est nécessaire de les passer en paramètres.
      Créer des index pour rendre les recherches plus rapides.
    """
    self.vols = vols
    self.clients = clients
    self.reservations = reservations
    self.vols_index = {vol["_id"]: vol for vol in self.vols} if self.vols is not None else None
    self.clients_index = {client["_id"]: client for client in self.clients} if self.clients is not None else None
    self.reservations_index = {res["_id"]: res for res in self.reservations} if self.reservations is not None else None
    
  def get_vols(self) -> list[dict]:
    """
    [Summary]
      Retourne une liste de tous les vols.
      
    [Returns]
      vols: liste de vols
    """
    return self.vols
  
  def get_clients(self) -> list[dict]:
    """
    [Summary]
      Retourne une liste de tous les clients.
      
    [Returns]
      clients: liste de clients
    """
    return self.clients
  
  def get_reservations(self) -> list[dict]:
    """
    [Summary]
      Retourne une liste de toutes les réservations.
      
    [Returns]
      reservations: liste de réservations
    """
    return self.reservations
  
  def get_vols_by_id(self, vol_id: str) -> dict:
    """
    [Summary]
      Retourne un vol en fonction de son identifiant.
      
    [Args]
      vol_id: identifiant du vol
      
    [Returns]
      vol: vol correspondant à l'identifiant
    """
    for vol in self.vols:
      if vol["_id"] == vol_id:
        return vol
    return None 
  
  def get_client_by_id(self, client_id: str) -> dict:
    """
    [Summary]
      Retourne un client en fonction de son identifiant.
      
    [Args]
      client_id: identifiant du client
      
    [Returns]
      client: client correspondant à l'identifiant
    """
    for client in self.clients:
      if client["_id"] == client_id:
        return client
    return None
  
  def get_reservation_by_id(self, reservation_id: str) -> dict:
    """
    [Summary]
      Retourne un réservation en fonction de son identifiant.
    
    [Args]
      reservation_id: identifiant de la réservation
      
    [Returns]
      réservation: réservation correspondant à l'identifiant
    """
    for reservation in self.reservations:
      if reservation["_id"] == reservation_id:
        return reservation
    return None
  
  def get_arrival_cities(self) -> list:
    """
    [Summary]
      Retourne une liste de toutes les villes d'arrivée des vols.
      
    [Returns]
      villes: liste de villes d'arrivée
    """
    return [vol["VilleA"] for vol in self.vols]
  
  def get_arrival_city_by_id(self, vol_id: str) -> str:
    """
    [Summary]
      Retourne la ville d'arrivée d'un vol en fonction de son identifiant.
      
    [Args]
      vol_id: identifiant du vol
      
    [Returns]
      ville: ville d'arrivée du vol
    """
    for vol in self.vols:
      if vol["_id"] == vol_id:
        return vol["VilleA"]
    return None
  
  def get_pilotes(self) -> list:
    """
    [Summary]
      Retourne une liste des noms de tous les pilotes, sans doublons.
      
    [Returns]
      pilotes: liste de noms de pilotes
    """
    return list(set(vol["Pilote"]["NomPil"] for vol in self.vols if "Pilote" in vol and vol["Pilote"]["NomPil"]))
  
  def get_vols_by_departure_city(self, departure_city: str) -> list[dict]:
    """
    [Summary]
      Retourne une liste des vols au départ d'une ville donnée.
      
    [Args]
      ville_depart: ville d'arrivée
      
    [Returns]
      vols: liste de vols au départ de la ville
    """
    return [vol for vol in self.vols if vol["VilleD"].lower() == departure_city.lower()]
  
  # Jointures
  def get_reservations_by_client(self, client_id: str) -> list[dict]:
    """
    [Summary]
      Retourne la liste des réservations pour un client donné, avec les détails des vols.
      
    [Args]
      client_id: identifiant du client
      
    [Returns]
      reservations: liste de réservations pour le client
    """
    # Filtrer les réservations du client
    client_reservations = [res for res in self.reservations if res["ClientId"] == client_id]
    
    # Ajouter les détails du vol à chaque réservation
    for res in client_reservations:
      vol = self.vols_index.get(res["VolId"], {})
      res["Vol"] = vol  # Ajouter les détails du vol
    return client_reservations

  def get_clients_by_flight(self, vol_id: str) -> list[dict]:
    """
    [Summary]
      Retourne la liste des clients ayant des réservations sur un vol donné, avec les détails des réservations.
      
    [Args]
      vol_id: identifiant du vol
      
    [Returns]
      clients: liste de clients ayant des réservations sur le vol
    """
    # Filtrer les réservations du vol
    flight_reservations = [res for res in self.reservations if res["VolId"] == vol_id]
    
    # Ajouter les détails du client à chaque réservation
    for res in flight_reservations:
      client = self.clients_index.get(res["ClientId"], {})
      res["Client"] = client  # Ajouter les détails du client
    return flight_reservations

  def get_flights_by_pilot(self, nom_pilote: str) -> list[dict]:
    """
    [Summary]
      Retourne la liste des vols opérés par un pilote donné.
      
    [Args]
      nom_pilote: nom du pilote
      
    [Returns]
      flights: liste de vols opérés par le pilote
    """
    return [vol for vol in self.vols if vol["Pilote"]["NomPil"] == nom_pilote]

  def get_clients_by_pilot(self, nom_pilote: str) -> list[dict]:
    """
    [Summary]
      Retourne la liste des clients ayant des réservations sur les vols opérés par un pilote donné.
      
    [Args]
      nom_pilote: nom du pilote
      
    [Returns]
      clients: liste de clients ayant des réservations sur les vols du pilote
    """
    # Obtenir les vols opérés par le pilote
    vols_pilote = self.get_flights_by_pilot(nom_pilote)
    vols_ids = {vol["_id"] for vol in vols_pilote}
    
    # Filtrer les réservations sur ces vols
    reservations_pilote = [res for res in self.reservations if res["VolId"] in vols_ids]
    
    # Ajouter les détails du client à chaque réservation
    for res in reservations_pilote:
      client = self.clients_index.get(res["ClientId"], {})
      res["Client"] = client
    return reservations_pilote