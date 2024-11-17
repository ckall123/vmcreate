# vmcreate

**if #returned non-zero exit status 1. you can delete VM to this two folder.**

# windows
VM folder

C:\Users\user\VirtualBox VMs

C:\VirtualMachines

# linux
## Change your ip -chose

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
## adduser - chose 

`sudo adduser hadoop`

- set password 
- press enter
- enter

su - hadoop

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
```
press `Enter` third
```
cat .ssh/id_rsa.pub >> .ssh/authorized_keys

ssh user_name@localhost
```

 **PREASS** `CTRL + D`

## Editing Hadoop's config files

**Edit the core site xml file**
```
cd hadoop-3.4.1/etc/hadoop/

ls
```

`vim core-site.xml`

```
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

`vim hdfs-site.xml`

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

mkdir -p hdfs/datanode

mkdir -p hdfs/namenode

ls

ls hdfs/
```

[15:48](https://www.youtube.com/watch?v=EJj_0o-EY50&list=PLJlKGwy-7Ac6ASmzZPjonzYsV4vPELf0x&index=3&ab_channel=JoshuaHruzik)

***find your java address***

```
cd hadoop-3.4.1/etc/hadoop/

ls /usr/lib/jvm/java-11-openjdk-amd64

ls

vim hadoop-env.sh
```

**hadoop-env.sh**

***find***  `# export JAVA_HOME=`
```
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

```
cd ~/hadoop-3.4.1/

cd bin/

ls

./hdfs namenode -format
```

```
cd ..

cd sbin/

ls

./start-dfs.sh
```

***Open browser***
*type*  `localhost:9870`

```
./stop-all.sh
```

[video 4](https://www.youtube.com/watch?v=zdrZTZbWAZc&list=PLJlKGwy-7Ac6ASmzZPjonzYsV4vPELf0x&index=4&ab_channel=JoshuaHruzik)

## use Hadoop

### How to do use --Reference

[Reference website](https://sparkbyexamples.com/hadoop/apache-hadoop-installation/)

[Reference video](https://www.youtube.com/watch?v=hRtInGQhBxs&list=PLJlKGwy-7Ac6ASmzZPjonzYsV4vPELf0x)
