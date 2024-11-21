import subprocess
import time

# Define the VM name prefix and the number of VMs
VM_NAME_PREFIX = "VM"
VM_COUNT = 1

# Define the name of the network interface to bridge to
BRIDGE_INTERFACE = "eno2"  # network interface (Wi-Fi)

# Function to run a shell command and return the output
def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip(), result.stderr.strip()

# Loop through the number of VMs, stop if running, and configure each VM
for i in range(1, VM_COUNT + 1):
    vm_name = f"{VM_NAME_PREFIX}{i}"

    # Check if the VM is running
    cmd_check_state = ["VBoxManage", "showvminfo", vm_name, "--machinereadable"]
    stdout, stderr = run_command(cmd_check_state)
    if stderr:
        print(f"Error checking state of {vm_name}: {stderr}")
        continue

    vm_state_line = next((line for line in stdout.splitlines() if line.startswith("VMState=")), None)
    vm_state = vm_state_line.split('=')[1].strip('"') if vm_state_line else None

    if vm_state == "running":
        print(f"Stopping {vm_name}...")
        cmd_stop_vm = ["VBoxManage", "controlvm", vm_name, "poweroff"]
        _, stderr = run_command(cmd_stop_vm)
        if stderr:
            print(f"Error stopping {vm_name}: {stderr}")
        time.sleep(2)  # Wait a moment for the VM to shut down

    print(f"Configuring {vm_name} for bridged networking...")
    cmd_configure_vm = [
        "VBoxManage", "modifyvm", vm_name,
        "--nic1", "bridged",
        "--bridgeadapter1", BRIDGE_INTERFACE
    ]
    _, stderr = run_command(cmd_configure_vm)
    if stderr:
        print(f"Error configuring {vm_name}: {stderr}")
    else:
        print(f"{vm_name} configured for bridged networking using {BRIDGE_INTERFACE}.")

print("All VMs have been stopped (if running) and configured for bridged networking.")
