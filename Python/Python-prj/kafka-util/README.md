# kafka-util.py script #

This kafka-util.py script that can be executed on OS command line or be set up run automatically. It will
do installation, configuration for multiple zookeeper and multiple kafka in one node or multiple
node. It supports run on Linux or Window kafka environment.


# How to display usage help menu of the script #
From command line type python kafka-util.py -h and return key.

~~~
Example:
> python kafka-util.py -h
or
> python kafka-util.py --help

Usage: kafka-util.py -h
       kafka-util.py -I -s sourceTarFile -d untarTargetDirectory
       kafka-util.py -Z -n numberOfZookeeper -q zookeeperPortNumber -d kafkaHomeDirectory
       kafka-util.py -B -n numberOfBroker -p brokerPortNumber -z numberOfZookeeper -q zookeeperPortNumber -d cofigurationDirectory
       kafka-util.py -T -t topicName -p serverName:portNumber -f replicationFactor -n numberOfPartition  -d kafkaHomeDirectory
       kafka-util.py -S -d kafkaHomeDirectory
       kafka-util.py -L -p zookeeperServer:portNumber -d kafkaHomeDirectory
       kafka-util.py -P -t topicName -p serverName:portNumber -d kafkaHomeDirectory
       kafka-util.py -C -t topicName -p serverName:portNumber -d kafkaHomeDirectory

Options:
  -h      : Display this help message.
  -I      : Install kafka tar file.
  -Z      : Create zookeeper server.properties.
  -B      : Create kafka broker server.
  -T      : Create kafka topic.
  -S      : Create Start/Stop kafka scripts.
  -L      : List all kafka topics.
  -P      : Produce kafka message.
  -C      : Consume kafka message.

---
~~~

# How to install kafka from the script #

From command line type python kafka-util.py -I -s kafka_2.12-2.2.0.tgz -d ./app/kafka and
hit return key.

~~~
Example:
> python kafka-util.py -I -s kafka_2.12-2.2.0.tgz -d /app/kafka
>

~~~
---

# How to create zookeeper server properties configuration from the script #

To run the script with -Z is for creating zookeeper properties configuration file.
~~~
Example:
> python ./kafka-util.py -Z -n 1 -q 2181 -d /app/kafka
>
~~~

---
# How to create broker properties configuration from the script #

To run the script with -B is for create kafka broker properites onfiguration file.
Example:
> python ./kafka-util.py -B -n 1 -p 9093 -z 1 -q 2181 -d /app/kafka
>
~~~

---


