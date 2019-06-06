echo "Stopping Kafka Server"
../bin/Kafka-Server-stop.sh &
sleep 10s
echo "Stopping Zookeeper"
../bin/Zookeeper-Server-stop.sh &
