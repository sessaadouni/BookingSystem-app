import csv

def read_performance_results(filename):
  results = {}
  with open(filename, mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
      function_name = row['function_name']
      execution_time = float(row['execution_time'])
      method_group = row['method_group']
      key = (function_name, method_group)
      results[key] = execution_time
  return results

def compare_performance(mongo_file, mongo_json_file, redis_json_file, output_file='./Report/comparison_results.csv'):
  mongo_results = read_performance_results(mongo_file)
  mongo_json_results = read_performance_results(mongo_json_file)
  redis_json_results = read_performance_results(redis_json_file)
  all_functions = set()
  for result in [mongo_results, mongo_json_results, redis_json_results]:
    all_functions.update([key[0] for key in result.keys()])
  
  # Calculer le temps total pour les méthodes JSON (incluant le temps de chargement)
  total_mongo_json_time = 0
  total_redis_json_time = 0
  total_mongo_time = 0

  # Fonctions à exclure du calcul individuel (par exemple, 'load_data_from_mongo' et 'load_data_from_redis')
  load_functions = {'load_data_from_mongo', 'load_data_from_redis'}

  with open(output_file, mode='w', newline='') as csv_file:
      fieldnames = [
        'function_name',
        'MongoDB_time',
        'MONGO_JSON_time',
        'REDIS_JSON_time',
        'Difference_MONGO_JSON',
        'Difference_REDIS_JSON',
        'Percentage_Diff_MONGO_JSON',
        'Percentage_Diff_REDIS_JSON'
      ]
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      writer.writeheader()
      for func in all_functions:
        mongo_time = mongo_results.get((func, 'MongoDB'), None)
        mongo_json_time = mongo_json_results.get((func, 'MONGO_JSON'), None)
        redis_json_time = redis_json_results.get((func, 'REDIS_JSON'), None)
        difference_mongo_json = None
        percentage_diff_mongo_json = None
        difference_redis_json = None
        percentage_diff_redis_json = None

        # Ajouter les temps pour le calcul des temps totaux, en excluant les fonctions de chargement
        if func not in load_functions:
          if mongo_time is not None:
            total_mongo_time += mongo_time
          if mongo_json_time is not None:
            total_mongo_json_time += mongo_json_time
          if redis_json_time is not None:
            total_redis_json_time += redis_json_time

        # Calculer les différences pour les fonctions individuelles (hors fonctions de chargement)
        if func not in load_functions:
          if mongo_time is not None and mongo_json_time is not None:
            difference_mongo_json = mongo_json_time - mongo_time
            if mongo_time > 0:
              percentage_diff_mongo_json = (difference_mongo_json / mongo_time) * 100
          if mongo_time is not None and redis_json_time is not None:
            difference_redis_json = redis_json_time - mongo_time
            if mongo_time > 0:
              percentage_diff_redis_json = (difference_redis_json / mongo_time) * 100

        writer.writerow({
          'function_name': func,
          'MongoDB_time': f"{mongo_time:.6f}" if mongo_time is not None else 'N/A',
          'MONGO_JSON_time': f"{mongo_json_time:.6f}" if mongo_json_time is not None else 'N/A',
          'REDIS_JSON_time': f"{redis_json_time:.6f}" if redis_json_time is not None else 'N/A',
          'Difference_MONGO_JSON': f"{difference_mongo_json:.6f}" if difference_mongo_json is not None else 'N/A',
          'Difference_REDIS_JSON': f"{difference_redis_json:.6f}" if difference_redis_json is not None else 'N/A',
          'Percentage_Diff_MONGO_JSON': f"{percentage_diff_mongo_json:.2f}%" if percentage_diff_mongo_json is not None else 'N/A',
          'Percentage_Diff_REDIS_JSON': f"{percentage_diff_redis_json:.2f}%" if percentage_diff_redis_json is not None else 'N/A',
        })

      # Ajouter le temps de chargement aux temps totaux pour les méthodes JSON
      load_data_mongo_json_time = mongo_json_results.get(('load_data_from_mongo', 'MONGO_JSON'), 0)
      load_data_redis_json_time = redis_json_results.get(('load_data_from_redis', 'REDIS_JSON'), 0)
      total_mongo_json_time += load_data_mongo_json_time
      total_redis_json_time += load_data_redis_json_time

      # Écrire une ligne pour les temps totaux
      total_difference_mongo_json = total_mongo_json_time - total_mongo_time
      total_percentage_diff_mongo_json = (total_difference_mongo_json / total_mongo_time) * 100 if total_mongo_time > 0 else None

      total_difference_redis_json = total_redis_json_time - total_mongo_time
      total_percentage_diff_redis_json = (total_difference_redis_json / total_mongo_time) * 100 if total_mongo_time > 0 else None

      writer.writerow({
        'function_name': 'Total',
        'MongoDB_time': f"{total_mongo_time:.6f}",
        'MONGO_JSON_time': f"{total_mongo_json_time:.6f}",
        'REDIS_JSON_time': f"{total_redis_json_time:.6f}",
        'Difference_MONGO_JSON': f"{total_difference_mongo_json:.6f}",
        'Difference_REDIS_JSON': f"{total_difference_redis_json:.6f}",
        'Percentage_Diff_MONGO_JSON': f"{total_percentage_diff_mongo_json:.2f}%" if total_percentage_diff_mongo_json is not None else 'N/A',
        'Percentage_Diff_REDIS_JSON': f"{total_percentage_diff_redis_json:.2f}%" if total_percentage_diff_redis_json is not None else 'N/A',
      })

  print(f"Les résultats de comparaison ont été écrits dans '{output_file}'")

if __name__ == "__main__":
  compare_performance(
    './Report/performance_results_mongo.csv',
    './Report/performance_results_mongo_json.csv',
    './Report/performance_results_redis_json.csv'
  )
