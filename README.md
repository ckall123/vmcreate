# Ubuntu

***Install Virturalbox***

run `creat_vm_bridged.py` you need to change the path in the code

run `setting_birdged.py`  you need to change the path in the code

# 1. Apache Hadoop Installation – Preparation

## adduser - ** chose **

`sudo adduser hadoop`

- set password 
- press enter
- enter

su - hadoop

## 1.1 Update the Source List of Ubuntu

`sudo apt-get update`

## 1.2 install openssh-server to All VMs

`sudo apt install openssh-server`

You can ssh to your VM.

If you want to connect to other virtual machines via SSH, your virtual machine also needs to have SSH installed.

`ssh user_name@localhost`

## 1.3 Add all our nodes to /etc/hosts.

**namenode** is your master control, datanode(host name, domain) is your VMs

```
sudo vi /etc/hosts
192.168.0.100 namenode.socal.rr.com

192.168.0.101 datanode1
192.168.0.102 datanode2
192.168.0.103 VM1
```

## 1.4 Setup Passwordless login Between Name Node and all Data Nodes.

```
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat .ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```
Now copy authorized_keys to all data nodes in a cluster. This enables name node to connect to data nodes password less (without prompting for password)

```
scp .ssh/authorized_keys datanode1:/home/{urer_name}/.ssh/authorized_keys
scp .ssh/authorized_keys datanode2:/home/vm/.ssh/authorized_keys
scp .ssh/authorized_keys VM1:/home/vm/.ssh/authorized_keys
```

## 1.5 Install JDK1.8 on all VMs

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
        <value>hdfs://your_namenode_ip:9000</value>
    </property>
</configuration>
```

### 3.3.2 Update hdfs-site.xml

`vi ~/hadoop/etc/hadoop/hdfs-site.xml`

if you are in hadoop user you need to change `<value>/home/vm/hadoop/hdfs/datanode</value>`

```
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>  
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/home/vm/hadoop/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/home/vm/hadoop/hdfs/datanode</value>
    </property>
</configuration>
```

### 3.3.3 Update yarn-site.xml

`vi ~/hadoop/etc/hadoop/yarn-site.xml`

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
       <value>your_namenode_ip</value>
    </property>
</configuration>
```

### 3.3.4 Update mapred-site.xml 

`vi ~/hadoop/etc/hadoop/mapred-site.xml`

```
<configuration>
    <property>
        <name>mapreduce.jobtracker.address</name>
        <value>your_namenode_ip:54311</value>
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
your_namenode_ip
```

## 4.2 Create workers file and add all your data node IP.

`vi ~/hadoop/etc/hadoop/workers`

```
192.168.0.101
192.168.0.102
192.168.0.103
```

# 5 set your datanode
## 5.1 scp hadoop folder to data node

```
scp -r /home/vm/hadoop/ datanode1:"/path/to/remote directory"
scp -r /home/vm/hadoop/ VM1:"/path/to/remote directory"
```

**------------------------------------------------------------------------------**


# 6 Format HDFS and Start Hadoop Cluster

## 6.1 Format HDFS

HDFS needs to be formatted like any classical file system. On Name Node server (namenode), run the following command:

```
hdfs namenode -format
```

## 6.2 Start HDFS Cluster

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

[video 4](https://www.youtube.com/watch?v=zdrZTZbWAZc&list=PLJlKGwy-7Ac6ASmzZPjonzYsV4vPELf0x&index=4&ab_channel=JoshuaHruzik)

## use Hadoop

### How to do use --Reference

[Reference website](https://sparkbyexamples.com/hadoop/apache-hadoop-installation/)

[Reference video](https://www.youtube.com/watch?v=hRtInGQhBxs&list=PLJlKGwy-7Ac6ASmzZPjonzYsV4vPELf0x)
