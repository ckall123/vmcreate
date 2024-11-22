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

## 3. Configure Apache Hadoop Cluster

## 3.1 Update hadoop-env.sh

***find your java address***

`ls /usr/lib/jvm/java-8-openjdk-amd64`

**hadoop-env.sh**

`vi ~/hadoop/etc/hadoop/hadoop-env.sh`

***type*** `/` ***to find***  `# export JAVA_HOME=`
```
vi ~/hadoop/etc/hadoop/hadoop-env.sh
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

## 3.2 Create data folder

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

## 3.3 Edit the xml file

### 3.3.1 Update core-site.xml
`vi ~/hadoop/etc/hadoop/core-site.xml`

```
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://your_main_host:9000</value>
    </property>
</configuration>
```

### 3.3.2 Update hdfs-site.xml

`vi ~/hadoop/etc/hadoop/hdfs-site.xml`

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

### 3.3.3 Update yarn-site.xml

`vi ~/hadoop/etc/hadoop/`

```
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
    <property>
       <name>yarn.resourcemanager.hostname</name>
       <value>your_main_host</value>
    </property>
</configuration>
```

### 3.3.4 Update mapred-site.xml 

`vi ~/hadoop/etc/hadoop/mapred-site.xml`

```
<configuration>
    <property>
        <name>mapreduce.jobtracker.address</name>
        <value>your_main_host:54311</value>
    </property>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
```

# 4. Create master and workers files

## 4.1 Create master file and add your name node IP.

`vi ~/hadoop/etc/hadoop/masters`


```
your_main_host
```

## 4.2 Create workers file and add all your data node IP.

`vi ~/hadoop/etc/hadoop/workers`

```
192.168.1.141
192.168.1.113
192.168.1.118
```

# 5 Format HDFS and Start Hadoop Cluster

## 5.1 Format HDFS

HDFS needs to be formatted like any classical file system. On Name Node server (namenode), run the following command:

```
hdfs namenode -format
```

## 5.2 Start HDFS Cluster

Start the HDFS by running the start-dfs.sh script from Name Node Server (namenode)

```
ubuntu@namenode:~$ start-dfs.sh
Starting namenodes on [namenode.socal.rr.com]
Starting datanodes
Starting secondary namenodes [namenode]
ubuntu@namenode:~$
```

Running jps command on namenode should list the following
```
ubuntu@namenode:~$ jps
18978 SecondaryNameNode
19092 Jps
18686 NameNode
```

Running jps command on datanodes should list the following

```
ubuntu@datanode1:~$ jps
14012 Jps
11242 DataNode
```

***Open browser***
*type*  `your_main_host:9870`

```
./stop-all.sh
```


# scp your hadoop to other vms

`scp -r /home/vm/hadoop-3.4.1/ hostname@server_ip:"/path/to/remote directory"`

### start your Hadoop in other VM

#### install java



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
