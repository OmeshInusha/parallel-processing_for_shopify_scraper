import subprocess
import time
import threading
import sys

# Path to your script
script_path = "ssm.py"

# Path to the input file

def fair_data_usage(priority):
    if priority < 1 or priority > 10:
        raise ValueError("Priority must be between 1 and 10.")

    # Map priority to delay in days (1 = 12 days, 10 = 2 days)
    delay_in_days = 12 - (priority - 1)  # 1 -> 12 days, 10 -> 2 days
    delay_in_seconds = delay_in_days * 24 * 60 * 60  # Convert days to seconds
    return int(delay_in_seconds)


# Restart interval (seconds)
restart_interval = 172800


def read_inputs_from_file(file_path):
    """Read single inputs from a text file."""
    try:
        with open(file_path, "r") as f:
            inputs = [line.strip() for line in f if line.strip()]
        return inputs
    except Exception as e:
        print(f"Error reading input file: {e}")
        return []


def start_instance(instance_id, input_value):
    """Start a single instance of the script with one input value."""
    try:
        print(f"Starting instance {instance_id} with input '{input_value}'...")
        process = subprocess.Popen(
            ["python", script_path, input_value],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"Error starting instance {instance_id}: {e}")
        return None


def monitor_instance(instance_id, process, instance_inputs, processes):
    """Monitor an instance's output and restart it if it terminates."""
    while True:
        if process.poll() is None:  # Check if the process is still running
            # Print outputs of the running process
            if process.stdout:
                for line in process.stdout:
                    print(f"[Instance {instance_id} - Output]: {line.strip()}")
            if process.stderr:
                for line in process.stderr:
                    print(f"[Instance {instance_id} - Error]: {line.strip()}")
        else:
            print(f"Instance {instance_id} has stopped. Restarting...")
            input_value = instance_inputs[instance_id]
            new_process = start_instance(instance_id, input_value)
            if new_process:
                processes[instance_id] = new_process
                threading.Thread(
                    target=monitor_instance,
                    args=(instance_id, new_process, instance_inputs, processes),
                    daemon=True
                ).start()
            break  # Exit monitoring loop for this instance to restart it

        time.sleep(10)  # Check the process every second


def manage_instances(input_file, restart_interval):
    """Manage and restart parallel script instances."""
    instance_inputs = read_inputs_from_file(input_file)
    if not instance_inputs:
        print("No inputs to process. Exiting...")
        return

    processes = {}

    # Start all instances with their unique input values
    for i, input_value in enumerate(instance_inputs):
        process = start_instance(i, input_value)
        if process:
            processes[i] = process
            # Start monitoring the instance in a separate thread
            threading.Thread(
                target=monitor_instance,
                args=(i, process, instance_inputs, processes),
                daemon=True
            ).start()

    while True:
        time.sleep(restart_interval)  # Sleep indefinitely to let the threads run in parallel


if __name__ == "__main__":
    input_file = sys.argv[1]
    pr = sys.argv[2]
    manage_instances(input_file, int(pr))
