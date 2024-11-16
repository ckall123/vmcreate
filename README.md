# vmcreate

**if #returned non-zero exit status 1. you can delete VM to this two folder.**

# windows
VM folder

C:\Users\user\VirtualBox VMs

C:\VirtualMachines

# linux
## Change your ip 

`ip a`

`sudo vim /etc/netplan/50-cloud-init.yaml`

cloud-init.yaml **example**
```
network:
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
        - 192.168.0.200/24  # your ip
  renderer: networkd
  version:2
```

`sudo netplan apply`

`sudo reboot`

## download Hadoop
[Hadoop URL](https://hadoop.apache.org/)

**Click Download**

**Binary download ->** [binary](https://www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz)

`wget https://dlcdn.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz`

`tar -xzf hadoop-3.4.1.tar.gz`

`rm hadoop-3.4.1.tar.gz`

`cd hadoop-3.4.1.tar.gz`

`./start-dfs.sh`
## use Hadoop

### How to do use --Reference

[Reference website](https://sparkbyexamples.com/hadoop/apache-hadoop-installation/)

[Reference video](https://www.youtube.com/watch?v=hRtInGQhBxs&list=PLJlKGwy-7Ac6ASmzZPjonzYsV4vPELf0x)
