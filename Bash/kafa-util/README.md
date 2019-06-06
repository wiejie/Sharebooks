# kafka-util.sh #

This bash kafka-util.sh script that can be executed on OS command line or be set up run automatically. It will
do installation, configuration for multiple zookeeper and multiple kafka in one node or multiple
node. It supports run on Linux or Window kafka environment.


# How to display usage help menu of the script #
From command line type kafka-util.sh -h and return key.

~~~
Example:
> ./kafka-util.sh -h

Usage: ./kafka-util.sh: -h
       ./kafka-util.sh: -I -s sourceTarFile -d untarTargetDirectory
       ./kafka-util.sh: -Z -n numberOfZookeeper -q zookeeperPortNumber -d kafkaHomeDirectory
       ./kafka-util.sh: -B -n numberOfBroker -p brokerPortNumber -z numberOfZookeeper -q zookeeperPortNumber -d cofigurationDirector
y
       ./kafka-util.sh: -T -t topicName -p serverName:portNumber -f replicationFactor -n numberOfPartition  -k kafkaHomeDirectory
       ./kafka-util.sh: -S -d kafkaHomeDirectory
       ./kafka-util.sh: -L -p zookeeperServer:portNumber -d kafkaHomeDirectory
       ./kafka-util.sh: -P -t topicName serverName:portNumber -d kafkaHomeDirectory
       ./kafka-util.sh: -C -t topicName serverName:portNumber -d kafkaHomeDirectory

Options:
  -h      : Display this help message.
  -I      : Install kafka tar file.
  -Z      : Create zookeeper server.properties.
  -B      : Create kafka broker server
  -T      : Create kafka topic.
  -S      : Create Start/Stop kafka scripts.
  -L      : List all kafka topics.

~~~




