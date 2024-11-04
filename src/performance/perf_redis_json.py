import os, sys

# Ajouter le chemin au module de connexion Redis si nécessaire
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libs.services.Json_Query_Search import Requests_Json
from libs.services.get_data_from_redis import load_vols_from_redis, load_clients_from_redis, load_reservations_from_redis

from decorators.timing import timing_decorator, write_performance_results_to_csv

@timing_decorator('REDIS_JSON')
def load_data_from_redis():
  vols = load_vols_from_redis()
  clients = load_clients_from_redis()
  reservations = load_reservations_from_redis()
  return vols, clients, reservations

if __name__ == "__main__":
  from collections import Counter

  vols, clients, reservations = load_data_from_redis()

  req = Requests_Json(vols, clients, reservations, method_group='REDIS_JSON')

  # Obtenir toutes les villes d'arrivée
  villes_counter = Counter(req.get_arrival_cities())
  # print("Liste des villes d'arrivée :")
  # for ville, count in villes_counter.items():
  #     print(f"{ville}: {count}")

  # print()

  # Obtenir la ville d'arrivée d'un vol
  vol_id_1 = "V519"
  # print(f"Ville d'arrivée du vol {vol_id_1} :", req.get_arrival_city_by_id(vol_id_1))

  # print()

  # Obtenir tous les pilotes et compter le nombre de pilotes
  # print("Liste des pilotes :")
  # for pilote in req.get_pilotes():
  #     print(pilote)
  # print("Nombre de pilotes:", len(req.get_pilotes()))

  # print()

  # Obtenir tous les vols au départ de Marseille
  departure_city = "Marseille"
  # print(f"Vols au départ de {departure_city} :")
  vols_marseille = req.get_vols_by_departure_city(departure_city=departure_city)
  # for vol in vols_marseille:
  #     print(vol["_id"], "->", vol["VilleA"])

  # print()

  # Obtenir toutes les réservations pour un client
  client_id = "1001"
  reservations_client = req.get_reservations_by_client(client_id=client_id)
  # print(f"Réservations pour le client {client_id} :")
  # for res in reservations_client:
  #     print(f"Réservation ID: {res['_id']}, Vol ID: {res['VolId']}, Classe: {res['Classe']}, NbPlaces: {res['NbPlaces']}")
  #     vol = res.get("Vol", {})
  #     print(f"Détails du vol: De {vol.get('VilleD', 'N/A')} à {vol.get('VilleA', 'N/A')} le {vol.get('DateD', 'N/A')}")
  #     print()

  # Obtenir tous les clients sur un vol
  vol_id_2 = "V519"
  clients_on_flight = req.get_clients_by_flight(vol_id=vol_id_2)
  # print(f"Clients sur le vol {vol_id_2} :")
  # for res in clients_on_flight:
  #     client = res.get("Client", {})
  #     print(f"Client ID: {client.get('_id', 'N/A')}, Nom: {client.get('NomCl', 'N/A')}, Réservation ID: {res['_id']}, NbPlaces: {res['NbPlaces']}, Classe: {res['Classe']}")
  #     print()

  # Obtenir tous les vols opérés par un pilote
  nom_pilote = "Leblanc"
  flights_by_pilot = req.get_flights_by_pilot(nom_pilote=nom_pilote)
  # print(f"Vols opérés par le pilote {nom_pilote} :")
  # for vol in flights_by_pilot:
  #     print(f"Vol ID: {vol['_id']}, De {vol['VilleD']} à {vol['VilleA']} le {vol['DateD']}")
  # print()

  # Obtenir tous les clients ayant des réservations sur les vols d'un pilote
  clients_by_pilot = req.get_clients_by_pilot(nom_pilote=nom_pilote)
  # print(f"Clients ayant des réservations sur les vols du pilote {nom_pilote} :")
  # for res in clients_by_pilot:
  #     client = res.get("Client", {})
  #     print(f"Client ID: {client.get('_id', 'N/A')}, Nom: {client.get('NomCl', 'N/A')}, Vol ID: {res['VolId']}, NbPlaces: {res['NbPlaces']}, Classe: {res['Classe']}")
  #     print()

  write_performance_results_to_csv('./Report/performance_results_redis_json.csv')
