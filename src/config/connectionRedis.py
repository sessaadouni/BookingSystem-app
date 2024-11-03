def connect_redis():
  from os import getenv
  from redis import Redis # type: ignore
  from dotenv import load_dotenv # type: ignore
  load_dotenv()
  
  try:
    connect = Redis(
      host=getenv("REDIS_HOST"),
      password=getenv("REDIS_PASSWORD"),
      port=getenv("REDIS_PORT"),
      db=0,
      decode_responses=True,
    )
    connect.ping()
    print("Vous avez été connecté à Redis avec succès !")
  except Exception as ex:
    print(f"Connexion à Redis impossible: {ex}")
    
  return connect