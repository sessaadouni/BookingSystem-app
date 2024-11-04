import time
from functools import wraps
import csv

# Global list to store performance results
performance_results = []

def timing_decorator(method_group = None):
  """
  A decorator to measure execution time of methods and log the results.

  Args:
    method_group (str): The group or class name (e.g., 'MongoDB' or 'JSON').

  Returns:
    function: The decorated function with added timing code.
  """
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      nonlocal method_group
      if method_group is None and args:
        self = args[0]
        method_group = getattr(self, 'method_group', 'Undefined')

      start_time = time.perf_counter()

      result = func(*args, **kwargs)

      end_time = time.perf_counter()

      execution_time = end_time - start_time

      performance_results.append({
        'method_group': method_group,
        'function_name': func.__name__,
        'execution_time': execution_time
      })
      # Print the result
      print(f"[{method_group}] Function '{func.__name__}' executed in {execution_time:.6f} seconds")
      # Return the original function's result
      return result
    return wrapper
  return decorator

def write_performance_results_to_csv(filename='./Report/performance_results.csv'):
  """
  Writes the performance results to a CSV file.

  Args:
    filename (str): The name of the CSV file.
  """
  fieldnames = ['method_group', 'function_name', 'execution_time']
  with open(filename, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for res in performance_results:
      writer.writerow(res)
  print(f"Performance results written to '{filename}'")
