import sys
import random
import json
import time



# SIMULATED LOW-LEVEL OS CALLS
def get_cpu_usage():
    return random.randint(0, 100)


def get_memory_usage():
    return random.randint(2048, 16384)  # MB


def _generate_and_save(raw_data: str, fmt: str, target: str, path: str):
    # Parsing the string
    parts = raw_data.split("|")
    cpu_val = int(parts[0])
    mem_val = int(parts[1])
    status_val = parts[2]
    error_list = parts[3].split(",") if parts[3] else []

    content = ""
    
    if fmt == "text":
        content = f"--- REPORT ---\nStatus: {status_val}\nCPU: {cpu_val}%\nMemory: {mem_val}MB\n"
        if error_list:
            content += "Errors: " + "; ".join(error_list)
    elif fmt == "json":
        data = {
            "status": status_val,
            "metrics": {"cpu": cpu_val, "memory": mem_val},
            "errors": error_list,
            "timestamp": time.time()
        }
        content = json.dumps(data, indent=2)

    if target == "console":
        print(content)
    elif target == "file":
        if not path:
            print("Error: No file path provided")
            return
        with open(path, "w") as f:
            f.write(content)
        print(f"Report saved to {path}")


def run_monitor(args: list[str]):
    # Config
    cpu_threshold = 80
    mem_threshold = 14000

    # Argument parsing
    output_format = "text"
    if "--format=json" in args:
        output_format = "json"
    
    target = "console"
    target_path = ""
    for arg in args:
        if arg.startswith("--file="):
            target = "file"
            target_path = arg.split("=", 1)[1]

    # Gathering data
    cpu = get_cpu_usage()
    mem = get_memory_usage()
   
    status = "OK"
    errors = []
    
    if cpu > cpu_threshold:
        status = "WARNING"
        errors.append(f"CPU load too high: {cpu}%")
        
    if mem > mem_threshold:
        status = "WARNING"
        errors.append(f"Memory usage critical: {mem}MB")

    # One simple string insetad of tuples, objects, etc.
    raw_data_string = f"{cpu}|{mem}|{status}|{','.join(errors)}"

    _generate_and_save(raw_data_string, output_format, target, target_path)


if __name__ == "__main__":
    run_monitor(sys.argv)