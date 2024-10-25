import subprocess
import os

# 設定部分
number_of_vms = 6  # 要創建的 VM 數量
vm_base_name = "VM"
os_type = "Ubuntu_64"  # 根據需要修改操作系統類型
iso_path = "ubuntu-24.04.1-live-server-amd64.iso"  # OS ISO 文件路徑
vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe"
vm_storage_base_path = "C:\\VirtualMachines"  # VM 存儲路徑

def create_vm(vm_name):
    try:
        print(f"正在創建虛擬機：{vm_name}")
        
        # 創建 VM
        subprocess.run([vboxmanage_path, "createvm", "--name", vm_name, "--ostype", os_type, "--register"], check=True)

        # 修改 VM 設置
        subprocess.run([vboxmanage_path, "modifyvm", vm_name, "--memory", "2048", "--vram", "128", "--cpus", "1"], check=True)

        # 創建虛擬硬碟
        hdd_path = os.path.join(vm_storage_base_path, vm_name, f"{vm_name}.vdi")
        os.makedirs(os.path.dirname(hdd_path), exist_ok=True)
        subprocess.run([vboxmanage_path, "createhd", "--filename", hdd_path, "--size", "20000"], check=True)

        # 創建存儲控制器
        subprocess.run([vboxmanage_path, "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--controller", "IntelAhci"], check=True)

        # 附加硬碟
        subprocess.run([
            vboxmanage_path, "storageattach", vm_name,
            "--storagectl", "SATA Controller",
            "--port", "0",
            "--device", "0",
            "--type", "hdd",
            "--medium", hdd_path
        ], check=True)

        # 創建並附加 IDE 控制器及 ISO 文件
        subprocess.run([vboxmanage_path, "storagectl", vm_name, "--name", "IDE Controller", "--add", "ide"], check=True)
        subprocess.run([
            vboxmanage_path, "storageattach", vm_name,
            "--storagectl", "IDE Controller",
            "--port", "0",
            "--device", "0",
            "--type", "dvddrive",
            "--medium", iso_path
        ], check=True)

        # 設定啟動順序
        subprocess.run([
            vboxmanage_path, "modifyvm", vm_name,
            "--boot1", "dvd",
            "--boot2", "disk",
            "--boot3", "none",
            "--boot4", "none"
        ], check=True)

        # 無人值守安裝
        subprocess.run([
            vboxmanage_path, "unattended", "install", vm_name,
            "--user=vm",
            "--password=123",
            "--full-user-name=vm",
            "--iso", iso_path,
            "--time-zone=UTC",
            "--hostname", f"{vm_name}.localdomain"
        ], check=True)

        # 啟動 VM 並改用 GUI 模式
        subprocess.run([vboxmanage_path, "startvm", vm_name, "--type", "gui"], check=True)
        
        print(f"{vm_name} 創建並啟動成功")

    except subprocess.CalledProcessError as e:
        error_message = f"虛擬機 {vm_name} 創建失敗：{e}"
        print(error_message)
        with open(f"{vm_name}_error.log", "w") as log_file:
            log_file.write(error_message)

# 主程序
for i in range(1, number_of_vms + 1):
    vm_name = f"{vm_base_name}{i}"
    create_vm(vm_name)
