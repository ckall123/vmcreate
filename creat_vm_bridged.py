import subprocess
import os

# 設定部分
number_of_vms = 1  # 要創建的 VM 數量
vm_base_name = "VM"  # 虛擬機基礎名稱
os_type = "Ubuntu_64"  # 操作系統類型
iso_path = "ubuntu-24.04.1-live-server-amd64.iso"  # ISO 文件的路徑
vboxmanage_path = "VBoxManage"  # VBoxManage 命令
vm_storage_base_path = "VirtualMachines"  # VM 存儲目錄
bridge_adapter_name = "eno2"  # 主機網卡名稱

def validate_paths():
    """檢查必要的路徑是否存在"""
    if not os.path.isfile(iso_path):
        raise FileNotFoundError(f"ISO 文件未找到：{iso_path}")
    if not os.path.isdir(vm_storage_base_path):
        os.makedirs(vm_storage_base_path, exist_ok=True)

def create_vm(vm_name):
    """創建虛擬機"""
    try:
        print(f"正在創建虛擬機：{vm_name}")
        
        # 創建虛擬機
        subprocess.run([vboxmanage_path, "createvm", "--name", vm_name, "--ostype", os_type, "--register"], check=True)

        # 配置虛擬機的內存和 CPU
        subprocess.run([vboxmanage_path, "modifyvm", vm_name, "--memory", "1024", "--cpus", "2"], check=True)

        # 創建並附加虛擬硬碟
        hdd_path = os.path.join(vm_storage_base_path, vm_name, f"{vm_name}.vdi")
        os.makedirs(os.path.dirname(hdd_path), exist_ok=True)
        subprocess.run([vboxmanage_path, "createhd", "--filename", hdd_path, "--size", "10000"], check=True)

        # 配置存儲控制器並附加硬碟
        subprocess.run([vboxmanage_path, "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--controller", "IntelAhci"], check=True)
        subprocess.run([
            vboxmanage_path, "storageattach", vm_name,
            "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", hdd_path
        ], check=True)

        # 附加 ISO 文件
        subprocess.run([vboxmanage_path, "storagectl", vm_name, "--name", "IDE Controller", "--add", "ide"], check=True)
        subprocess.run([
            vboxmanage_path, "storageattach", vm_name,
            "--storagectl", "IDE Controller", "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", iso_path
        ], check=True)

        # 設置橋接網路
        subprocess.run([
            vboxmanage_path, "modifyvm", vm_name,
            "--nic1", "bridged", "--bridgeadapter1", bridge_adapter_name
        ], check=True)

        # 無人值守安裝
        subprocess.run([
            vboxmanage_path, "unattended", "install", vm_name,
            "--user=vm", "--password=123", "--full-user-name=vm", "--iso", iso_path, "--hostname", f"{vm_name}.localdomain"
        ], check=True)

        # 啟動虛擬機
        subprocess.run([vboxmanage_path, "startvm", vm_name, "--type", "gui"], check=True)

        print(f"{vm_name} 創建完成！請手動進入虛擬機內設置靜態 IP。")

    except subprocess.CalledProcessError as e:
        print(f"虛擬機 {vm_name} 創建失敗：{e}")

# 主程序
if __name__ == "__main__":
    validate_paths()
    for i in range(number_of_vms):
        vm_name = f"{vm_base_name}{i+1}"
        create_vm(vm_name)
