# vmcreate

if #returned non-zero exit status 1. you can delete VM to this two folder.

C:\Users\user\VirtualBox VMs

C:\VirtualMachines

## If you are in linux


# How to change your ip 

ip a
sudo vim /etc/netplan/50-cloud-init.yaml
network:
  ethernets:
    enp0s3:
      dhcp4: no
        addresses:
        -your ip
  renderer: networkd
  version:2

sudo netplan apply
sudo reboot
