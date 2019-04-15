echo "Starting Zookeeper"
../bin/Zookeeper-server-start.sh ../config/Zookeeper.properties &
sleep 20s
echo "Starting Kafka Server"
../bin/Kafka-server-start.sh ../config/server.ssl.properties &

