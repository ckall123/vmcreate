# vmcreate

**if #returned non-zero exit status 1. you can delete VM to this two folder.**

# windows
VM folder

C:\Users\user\VirtualBox VMs

C:\VirtualMachines

# linux
## Change your ip 

```
ip a

sudo vim /etc/netplan/50-cloud-init.yaml
```

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

```
sudo netplan apply

sudo reboot
```

## download Hadoop
[Hadoop URL](https://hadoop.apache.org/)

**Click Download**

**Binary download ->** [binary](https://www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz)

```
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz

tar -xzf hadoop-3.4.1.tar.gz

rm hadoop-3.4.1.tar.gz

cd hadoop-3.4.1
```

## configure Hadoop

### install JAVA
```
sudo apt install openjdk-11-jre-headless

java --version
```

### install ssh
```
sudo apt install openssh-server

ssh user_name@localhost

ssh-keygen -t rsa

cat .ssh/id_rsa.pub >> .ssh/authorized_keys

ssh user_name@localhost
```

 **PREASS** `CTRL + D`

## Editing Hadoop's config files

**Edit the core site xml file**
```
cd hadoop-3.4.1/etc/hadoop/

ls

vim hdfs-site.xml

```

**hdfs-site.xml**
```
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>3</value>  
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/home/hadoop/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/home/hadoop/hdfs/datanode</value>
    </property>
</configuration>
```

```
cd ~

mkdir -p /hdfs/datanode

mkdir -p /hdfs/namenode

```

#### A
`./start-dfs.sh`
## use Hadoop

### How to do use --Reference

[Reference website](https://sparkbyexamples.com/hadoop/apache-hadoop-installation/)

[Reference video](https://www.youtube.com/watch?v=hRtInGQhBxs&list=PLJlKGwy-7Ac6ASmzZPjonzYsV4vPELf0x)
