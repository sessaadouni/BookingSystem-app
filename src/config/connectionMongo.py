def connect_mongodb():
  from pymongo import MongoClient # type: ignore
  from pymongo.errors import ConnectionFailure # type: ignore
  from dotenv import load_dotenv # type: ignore
  from os import getenv
  
  load_dotenv()
  
  try:
    client = MongoClient(getenv("MONGO_URI"), serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("Vous avez été connecté à MongoDB avec succès !")
  except ConnectionFailure as e:
    print(f"Connexion à MongoDB impossible: {e}")
  except Exception as ex:
    print(f"Une erreur est survenue: {ex}")
  
  return client