import time
from functools import wraps
import csv
from memory_profiler import memory_usage # type: ignore
import psutil
import os
from statistics import mean, median, stdev, StatisticsError
from datetime import datetime

# Global list to store performance results
performance_results = []

# Storage for grouped results
grouped_performance_results = {}

def timing_decorator(method_group=None):
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
            mem_before = memory_usage()[0]
            psutil.cpu_percent(interval=None)  # Reset CPU measurement

            result = func(*args, **kwargs)

            mem_after = memory_usage()[0]
            cpu_after = psutil.cpu_percent(interval=None)
            end_time = time.perf_counter()

            execution_time = end_time - start_time
            memory_used = mem_after - mem_before

            performance_results.append({
                'method_group': method_group,
                'function_name': func.__name__,
                'execution_time': execution_time,
                'memory_used': memory_used,
                'cpu_usage': cpu_after
            })

            # Print the result
            print(f"[{method_group}] Function '{func.__name__}' executed in {execution_time:.6f} seconds, "
                  f"Memory Used: {memory_used:.2f} MB, CPU Usage: {cpu_after:.2f}%")
            
            generate_txt_reports()
            return result
        return wrapper
    return decorator

def write_performance_results_to_csv(filename='./Report/performance_results.csv'):
    """
    Writes the performance results to a CSV file.

    Args:
        filename (str): The name of the CSV file.
    """
    fieldnames = ['method_group', 'function_name', 'execution_time', 'memory_used', 'cpu_usage']
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for res in performance_results:
            writer.writerow(res)
    print(f"Performance results written to '{filename}'")

def generate_txt_reports(output_dir='./report/performance'):
    """
    Generate performance reports in TXT format, grouped by method_group.

    Args:
        output_dir (str): Directory to save the reports.
    """
    os.makedirs(output_dir, exist_ok=True)
    grouped_results = {}
    for result in performance_results:
        group = result['method_group']
        grouped_results.setdefault(group, []).append(result)

    for group, results in grouped_results.items():
        report_path = os.path.join(output_dir, f"{group}_performance_report.txt")
        with open(report_path, 'w') as report_file:
            report_file.write(f"Performance Report for {group}\n")
            report_file.write("=" * 50 + "\n")
            exec_times = [r['execution_time'] for r in results]
            memory_usages = [r['memory_used'] for r in results]
            cpu_usages = [r['cpu_usage'] for r in results]

            report_file.write(f"Total Functions: {len(results)}\n")
            report_file.write(f"Total Execution Time: {sum(exec_times):.6f} seconds\n")
            report_file.write(f"Average Execution Time: {mean(exec_times):.6f} seconds\n")
            report_file.write(f"Median Execution Time: {median(exec_times):.6f} seconds\n")
            try:
                report_file.write(f"Execution Time Std Dev: {stdev(exec_times):.6f}\n")
            except StatisticsError:
                report_file.write(f"Execution Time Std Dev: N/A\n")
            report_file.write(f"Max Execution Time: {max(exec_times):.6f} seconds\n")
            report_file.write(f"Min Execution Time: {min(exec_times):.6f} seconds\n")
            report_file.write(f"Average Memory Used: {mean(memory_usages):.2f} MB\n")
            report_file.write(f"Average CPU Usage: {mean(cpu_usages):.2f}%\n\n")
            report_file.write("=" * 50 + "\n")
            report_file.write("Detailed Results:\n")
            report_file.write("=" * 50 + "\n")
            for res in results:
                report_file.write(
                    f"Function: {res['function_name']}, "
                    f"Execution Time: {res['execution_time']:.6f}s, "
                    f"Memory Used: {res['memory_used']:.2f} MB, "
                    f"CPU Usage: {res['cpu_usage']:.2f}%\n"
                )
        print(f"TXT Report generated for {group}: {report_path}")

# # Example usage
# @timing_decorator(method_group="ExampleGroup")
# def sample_function():
#     time.sleep(1)
#     return "Done"

# if __name__ == "__main__":
#     sample_function()
#     sample_function()
#     write_performance_results_to_csv()
#     generate_txt_reports()
