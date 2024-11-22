# 1. Apache Hadoop Installation – Preparation

## adduser - ** chose **

`sudo adduser hadoop`

- set password 
- press enter
- enter

su - hadoop

## 1.1 Update the Source List of Ubuntu

`sudo apt-get update`

## 1.2 install openssh-server

`sudo apt install openssh-server`

You can ssh to your VM.

If you want to connect to other virtual machines via SSH, your virtual machine also needs to have SSH installed.

`ssh user_name@localhost`

## 1.3 Add all our nodes to /etc/hosts.

**namenode** is your master control, datanode(host name, domain) is your VMs

```
sudo vi /etc/hosts
192.168.1.100 namenode.socal.rr.com

192.168.1.141 datanode1
192.168.1.113 VM123
192.168.1.118 datanode3.socal.rr.com
```

## 1.4 Setup Passwordless login Between Name Node and all Data Nodes.

```
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat .ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```
Now copy authorized_keys to all data nodes in a cluster. This enables name node to connect to data nodes password less (without prompting for password)

```
scp .ssh/authorized_keys datanode1:/home/ubuntu/.ssh/authorized_keys
scp .ssh/authorized_keys datanode2:/home/ubuntu/.ssh/authorized_keys
scp .ssh/authorized_keys datanode3:/home/ubuntu/.ssh/authorized_keys
```

## 1.5 Install JDK1.8 on all 4 nodes

`sudo apt-get -y install openjdk-8-jdk-headless`

`java --version`

# 2 Download and Install Apache Hadoop

## Hadoop Installation

[Hadoop URL](https://hadoop.apache.org/)

**Click Download**

**Binary download ->** [binary](https://www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz)

```
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz
tar -xzf hadoop-3.4.1.tar.gz
mv hadoop-3.4.1 hadoop
rm hadoop-3.4.1.tar.gz
```

## 2.2 Apache Hadoop configuration – Setup environment variables.

```
vi ~/.bashrc
export HADOOP_HOME=/home/vm/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/sbin
export HADOOP_MAPRED_HOME=${HADOOP_HOME}
export HADOOP_COMMON_HOME=${HADOOP_HOME}
export HADOOP_HDFS_HOME=${HADOOP_HOME}
export YARN_HOME=${HADOOP_HOME}
```

`source ~/.bashrc`

## Editing Hadoop's config files

***find your java address***


`ls /usr/lib/jvm/java-8-openjdk-amd64`

**hadoop-env.sh**

`vi ~/hadoop/etc/hadoop/hadoop-env.sh`

***type*** `/` ***to find***  `# export JAVA_HOME=`
```
vi ~/hadoop/etc/hadoop/hadoop-env.sh
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

**Edit the core site xml file**

`vi ~/hadoop/etc/hadoop/core-site.xml`

```
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://your_main_host:9000</value>
    </property>
</configuration>
```

`vim hdfs-site.xml`

if you are in hadoop user you need to change `<value>/home/your_user_name/hadoop/hdfs/datanode</value>`

```
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>  
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/home/hadoop/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/home/vm/hadoop/hdfs/datanode</value>
    </property>
</configuration>
```

`cd ~`

```
mkdir -p hadoop/hdfs/datanode
mkdir -p hadoop/hdfs/namenode
```

```
chmod 755 /home/vm/hadoop/hdfs/datanode/
chmod 755 /home/vm/hadoop/hdfs/namenode/
```

`ls -l hadoop/hdfs/`

**--------------------------------------------------**

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
### scp to other vms

`scp -r /home/vm/hadoop-3.4.1/ hostname@server_ip:"/path/to/remote directory"`

### start your Hadoop in other VM

#### install java

`sudo apt install openjdk-11-jre-headless`

#### Set up a passwordless SSH login

`cd`

`ssh-keygen -t rsa`

press `Enter` third

`cat .ssh/id_rsa.pub >> .ssh/authorized_keys`

#### start Hadoop

```
cd /home/your_user_name/hadoop-3.4.1/bin

./hdfs namenode -format

cd ..

cd sbin/

./start-dfs.sh
```

```
cd
scp .ssh/authorized_keys datanode1:/home/vm/.ssh/authorized_keys


```
[video 4](https://www.youtube.com/watch?v=zdrZTZbWAZc&list=PLJlKGwy-7Ac6ASmzZPjonzYsV4vPELf0x&index=4&ab_channel=JoshuaHruzik)

## use Hadoop

### How to do use --Reference

[Reference website](https://sparkbyexamples.com/hadoop/apache-hadoop-installation/)

[Reference video](https://www.youtube.com/watch?v=hRtInGQhBxs&list=PLJlKGwy-7Ac6ASmzZPjonzYsV4vPELf0x)
