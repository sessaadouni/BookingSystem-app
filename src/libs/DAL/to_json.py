import json
import os

# Table de correspondance des colonnes
tableCorespondance = {
  "AVIONS.txt": ["NumAv", "NomAv", "CapAv", "VilleAv"],
  "CLIENTS.txt": ["NumCl", "NomCl", "NumRueCl", "NomRueCl", "CodePosteCl", "VilleCl"],
  "DEFCLASSES.txt": ["NumVol", "Classe", "CoeffPrix"],
  "PILOTES.txt": ["NumPil", "NomPil", "NaisPil", "VillePil"],
  "RESERVATIONS.txt": ["NumCl", "NumVol", "Classe", "NbPlaces"],
  "VOLS.txt": ["NumVol", "VilleD", "VilleA", "DateD", "HD", "DateA", "HA", "NumPil", "NumAv"],
}

# Lire les fichiers .txt et les stocker dans un dictionnaire
dictAllJson = {}
for fileName in os.listdir("src/libs/DAL/db/txt"):
  if fileName.endswith(".txt"):
    file_path = os.path.join("src/libs/DAL/db/txt", fileName)
    fields = tableCorespondance[fileName]

    # Vérifier si la première colonne est une clé unique
    if fileName in ["DEFCLASSES.txt", "RESERVATIONS.txt"]:
      # Stocker les données dans une liste pour ces fichiers
      dictAllJson[fileName] = []
      with open(file_path, 'r') as fh:
        for line in fh:
          description = list(line.strip().split("\t"))
          if len(description) < len(fields):
            # Gérer les lignes avec des colonnes manquantes
            continue
          data_entry = {}
          for i, categorie in enumerate(fields):
            data_entry[categorie] = description[i]
          dictAllJson[fileName].append(data_entry)
    else:
      # Utiliser un dictionnaire avec la première colonne comme clé
      dictAllJson[fileName] = {}
      with open(file_path, 'r') as fh:
        for line in fh:
          description = list(line.strip().split("\t"))
          if len(description) < len(fields):
            # Gérer les lignes avec des colonnes manquantes
            continue
          key = description[0]
          data_entry = {}
          for i, categorie in enumerate(fields[1:], start=1):
            data_entry[categorie] = description[i]
          dictAllJson[fileName][key] = data_entry

# Construire la liste des vols
vols_list = []
for vol_id, vol_data in dictAllJson["VOLS.txt"].items():
  vol_dict = {"_id": vol_id}

  # Copier les champs du vol
  vol_fields_mapping = {
    "VilleD": "VilleD",
    "VilleA": "VilleA",
    "DateD": "DateD",
    "HD": "HD",
    "DateA": "DateA",
    "HA": "HA",
  }
  for src_field, dest_field in vol_fields_mapping.items():
    vol_dict[dest_field] = vol_data.get(src_field, "")

  # Ajouter l'avion
  num_av = vol_data.get("NumAv", "")
  avion_data = dictAllJson["AVIONS.txt"].get(num_av, {})
  vol_dict["Avion"] = {
    "NumAv": num_av,
    "NomAv": avion_data.get("NomAv", ""),
    "CapAv": avion_data.get("CapAv", ""),
    "VilleAv": avion_data.get("VilleAv", ""),
  }

  # Ajouter le pilote
  num_pil = vol_data.get("NumPil", "")
  pilote_data = dictAllJson["PILOTES.txt"].get(num_pil, {})
  vol_dict["Pilote"] = {
    "NumPil": num_pil,
    "NomPil": pilote_data.get("NomPil", ""),
    "NaisPil": pilote_data.get("NaisPil", ""),
    "VillePil": pilote_data.get("VillePil", ""),
  }

  # Ajouter les classes
  vol_dict["Classes"] = []
  for classe in dictAllJson["DEFCLASSES.txt"]:
    if classe.get("NumVol") == vol_id:
      vol_dict["Classes"].append({
        "Classe": classe.get("Classe", ""),
        "CoeffPrix": classe.get("CoeffPrix", ""),
      })

  vols_list.append(vol_dict)

# Construire la liste des clients
clients_list = []
for client_id, client_data in dictAllJson["CLIENTS.txt"].items():
  client_dict = {
    "_id": client_id,
    "NomCl": client_data.get("NomCl", ""),
    "Adresse": {
      "NumRueCl": client_data.get("NumRueCl", ""),
      "NomRueCl": client_data.get("NomRueCl", ""),
      "CodePosteCl": client_data.get("CodePosteCl", ""),
      "VilleCl": client_data.get("VilleCl", ""),
    },
    "Email": "",      # Champs supplémentaires à remplir si nécessaire
    "Telephone": "",  # Champs supplémentaires à remplir si nécessaire
  }
  clients_list.append(client_dict)

# Construire la liste des réservations
reservations_list = []
reservation_id_counter = 1
for reservation_data in dictAllJson["RESERVATIONS.txt"]:
  reservation_dict = {
    "_id": f"R{str(reservation_id_counter).zfill(3)}",
    "VolId": reservation_data.get("NumVol", ""),
    "ClientId": reservation_data.get("NumCl", ""),
    "NbPlaces": reservation_data.get("NbPlaces", ""),
    "Classe": reservation_data.get("Classe", ""),
  }
  reservations_list.append(reservation_dict)
  reservation_id_counter += 1

# Écrire les données dans des fichiers JSON séparés
with open("src/libs/DAL/db/json/vols.json", "w") as f:
  json.dump(vols_list, f, indent=2, ensure_ascii=False)

with open("src/libs/DAL/db/json/clients.json", "w") as f:
  json.dump(clients_list, f, indent=2, ensure_ascii=False)

with open("src/libs/DAL/db/json/reservations.json", "w") as f:
  json.dump(reservations_list, f, indent=2, ensure_ascii=False)

print("Données extraites avec succès.")
