import subprocess
import os
import json
from concurrent.futures import ThreadPoolExecutor

# 設定部分
number_of_vms = 2  # 要創建的 VM 數量
vm_base_name = "VM11"
os_type = "Ubuntu_64"  # 根據需要修改操作系統類型
iso_path = "ubuntu-24.04.1-live-server-amd64.iso"  # OS ISO 文件路徑
vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe"
vm_storage_base_path = "C:\\VirtualMachines"  # VM 存儲路徑
default_memory = "2048"
default_vram = "128"
default_cpus = "1"
default_password = "123"

# 執行命令並處理錯誤
def run_command(command, log_file=None):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_message = f"Command failed: {command}\nError: {e.stderr}"
        if log_file:
            with open(log_file, "a") as f:
                f.write(error_message + "\n")
        print(error_message)
        return None

# 創建虛擬機的主函數
def create_vm(vm_name):
    print(f"正在創建虛擬機：{vm_name}")
    log_file = f"{vm_name}_error.log"

    # 創建和註冊 VM
    if not run_command([vboxmanage_path, "createvm", "--name", vm_name, "--ostype", os_type, "--register"], log_file):
        return

    # 修改 VM 設置
    run_command([vboxmanage_path, "modifyvm", vm_name, "--memory", default_memory, "--vram", default_vram, "--cpus", default_cpus], log_file)

    # 創建虛擬硬碟
    hdd_path = os.path.join(vm_storage_base_path, vm_name, f"{vm_name}.vdi")
    os.makedirs(os.path.dirname(hdd_path), exist_ok=True)
    run_command([vboxmanage_path, "createhd", "--filename", hdd_path, "--size", "20000"], log_file)

    # 創建和附加存儲控制器
    run_command([vboxmanage_path, "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--controller", "IntelAhci"], log_file)
    run_command([vboxmanage_path, "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", hdd_path], log_file)
    
    run_command([vboxmanage_path, "storagectl", vm_name, "--name", "IDE Controller", "--add", "ide"], log_file)
    run_command([vboxmanage_path, "storageattach", vm_name, "--storagectl", "IDE Controller", "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", iso_path], log_file)

    # 設定啟動順序
    run_command([vboxmanage_path, "modifyvm", vm_name, "--boot1", "dvd", "--boot2", "disk", "--boot3", "none", "--boot4", "none"], log_file)

    # 無人值守安裝
    run_command([
        vboxmanage_path, "unattended", "install", vm_name,
        f"--user=vm", f"--password={default_password}",
        "--full-user-name=vm", "--iso", iso_path,
        "--time-zone=UTC", "--hostname", f"{vm_name}.localdomain"
    ], log_file)

    # 啟動 VM 並改用 GUI 模式
    run_command([vboxmanage_path, "startvm", vm_name, "--type", "gui"], log_file)

    print(f"{vm_name} 創建並啟動成功")

# 主程序 - 並行創建 VMs
def main():
    with ThreadPoolExecutor(max_workers=number_of_vms) as executor:
        vm_names = [f"{vm_base_name}{i}" for i in range(1, number_of_vms + 1)]
        executor.map(create_vm, vm_names)

if __name__ == "__main__":
    main()
