#!/bin/sh
# 
# Modification History:
# 03/28/2019      Created by Wie Jie Tjeong
#
#

. ./kafka-functions-util.sh

function usage {
    echo "Usage: $0: -h "
    echo "       $0: -I -s sourceTarFile -d untarTargetDirectory"
    echo "       $0: -Z -n numberOfZookeeper -q zookeeperPortNumber -d kafkaHomeDirectory"
    echo "       $0: -B -n numberOfBroker -p brokerPortNumber -z numberOfZookeeper -q zookeeperPortNumber -d cofigurationDirectory"
    echo "       $0: -T -t topicName -p serverName:portNumber -f replicationFactor -n numberOfPartition  -k kafkaHomeDirectory"
    echo "       $0: -S -d kafkaHomeDirectory"
    echo "       $0: -L -p zookeeperServer:portNumber -d kafkaHomeDirectory"
    echo "       $0: -P -t topicName serverName:portNumber -d kafkaHomeDirectory"
    echo "       $0: -C -t topicName serverName:portNumber -d kafkaHomeDirectory"
    echo ""
    echo "Options:"
    echo "  -h      : Display this help message."
    echo "  -I      : Install kafka tar file."
    echo "  -Z      : Create zookeeper server.properties."
    echo "  -B      : Create kafka broker server"
    echo "  -T      : Create kafka topic."
    echo "  -S      : Create Start/Stop kafka scripts."
    echo "  -L      : List all kafka topics."
    exit 1
}

if [ $# -le 1 ]; then
    usage
fi

#        d) DISTINATION="${OPTARG}";
while getopts "s:d:n:z:t:p:q:f:k:hIZBTSL" name
do 
    case $name in
        h) usage; exit 0;;
        L) ACTION=$name;;
        S) ACTION=$name;;
        T) ACTION=$name;;
        I) ACTION=$name;;
        Z) ACTION=$name;;
        B) ACTION=$name;;
        s) SOURCE="${OPTARG}";;
        d) KAFKAHOME="${OPTARG}";;
        n) NUMBERCOUNT="${OPTARG}";
           NUMBERCOUNTZOO="${OPTARG}";;
        z) NUMBERCOUNTZOO="${OPTARG}";;
        t) TOPICNAME="${OPTARG}";;
        p) SERVERNAMEPORT="${OPTARG}";
           KPORTNUMBER="${OPTARG}";;
        q) ZPORTNUMBER="${OPTARG}";;
        f) REPFACTOR="${OPTARG}";;
        :) echo "Missing argument for option -$OPTARG"; exit 1;;
       \?) echo "Unknown option -$OPTARG"; exit 1;;
        *) error "Invalid options: $1"; usage; exit 1 ;;
    esac
done
shift $((OPTIND-1))
args="$@"

############################################################################################
# Declare variables
SVR_PROP_TEMPLATE="server.properties-template"
SVR_NAME="server"
SVR_PROP=".properties"

ZOO_PROP_TEMPLATE="zookeeper.properties-template"
ZOO_NAME="zookeeper"
ZOO_PROP=".properties"

START_KAFKA_SERVER_SH_TEMPLATE="start-kafka-server.sh"
START_KAFKA_SH_TEMPLATE="start-kafka.sh"
START_ZOOKEEPER_SH_TEMPLATE="start-zookeeper.sh"
STOP_KAFKA_SH_TEMPLATE="stop-kafka.sh"

############################################################################################
# Functions
function install()
{
    echo "Installing..." $KAFKAHOME

    if [[ ! -z $KAFKAHOME ]]; then
#        mkdir -p $KAFKAHOME && tar -xvzf $SOURCE -C $KAFKAHOME
#        tar xvf $SOURCE --one-top-level=$KAFKAHOME --strip-components 1
#        tar xvf $SOURCE --strip-components 1 -C $KAFKAHOME
         mkdir -p $KAFKAHOME && tar -xvzf $SOURCE --strip-components 1 -C $KAFKAHOME
    fi
}

function getMultipleZookeeperPortNumber()
{

    ZPORTNUMBER=${ZPORTNUMBER:=2181}
    ZOOKEEPER_CLIENTPORT=""
    for ((NUM=0; NUM < $NUMBERCOUNTZOO; NUM++)) do
        _PORTNUMBER=$((ZPORTNUMBER+NUM))
        ZOOKEEPER_CLIENTPORT=$ZOOKEEPER_CLIENTPORT"localhost\:$_PORTNUMBER,"
    done 

    #Return
    echo $ZOOKEEPER_CLIENTPORT
}

function createZookeeperProperty()
{
    echo "Begin create zookeeper.properties using "  $ZOO_PROP_TEMPLATE " to " $KAFKAHOME

    # Search and replace the kafka_* properites value
    # . ./.env

    ZPORTNUMBER=${ZPORTNUMBER:=2181}
    for ((NUM=0; NUM < $NUMBERCOUNTZOO; NUM++)) do

         KAFKA_BROKER_ID=$NUM
         PORTNUMBER=$((ZPORTNUMBER+NUM))

         #echo "Creating zookeeper-$NUM.properties file... " 
         echo "Creating zookeeper-$PORTNUMBER.properties file... " 

         #cp ./$ZOO_PROP_TEMPLATE $KAFKAHOME/config/$ZOO_NAME-$NUM$ZOO_PROP
         cp ./$ZOO_PROP_TEMPLATE $KAFKAHOME/config/$ZOO_NAME-$PORTNUMBER$ZOO_PROP

         #ZOOKEEPER_DATADIR="\/tmp\/zookeeper"-$NUM
         ZOOKEEPER_DATADIR="\/tmp\/zookeeper"-$PORTNUMBER
#         ZOOKEEPER_CLIENTPORT="localhost\:"$PORTNUMBER
         ZOOKEEPER_CLIENTPORT=$PORTNUMBER
 
         # sed -i "s/ZOOKEEPER_DATADIR/$ZOOKEEPER_DATADIR/g" $KAFKAHOME/config/$ZOO_NAME-$NUM$ZOO_PROP
         #sed -i "s/ZOOKEEPER_CLIENTPORT/$ZOOKEEPER_CLIENTPORT/g" $KAFKAHOME/config/$ZOO_NAME-$PORTNUMBER$ZOO_PROP
         
         sed -i "s/ZOOKEEPER_DATADIR/$ZOOKEEPER_DATADIR/g" $KAFKAHOME/config/$ZOO_NAME-$PORTNUMBER$ZOO_PROP
         sed -i "s/ZOOKEEPER_CLIENTPORT/$ZOOKEEPER_CLIENTPORT/g" $KAFKAHOME/config/$ZOO_NAME-$PORTNUMBER$ZOO_PROP
    done 

    echo "End create zookeeper.properties..."
}

function createNodeServerProperty()
{
    echo "Begin create Node server.properties using $SVR_PROP_TEMPLATE in $KAFKAHOME/config directory"

    # Search and replace the kafka_* properites value
    # . ./.env

    KPORTNUMBER=${KPORTNUMBER:=9093}
    for ((NUM=0; NUM < $NUMBERCOUNT; NUM++)) do

         #Get the kafka port number and increment by NUM 
         PORTNUMBER=$((KPORTNUMBER+NUM))

         #echo "Creating server-$NUM.properties file... " 
         echo "Creating server-$PORTNUMBER.properties file... " 

         #cp ./$SVR_PROP_TEMPLATE $KAFKAHOME/config/$SVR_NAME-$NUM$SVR_PROP
         cp ./$SVR_PROP_TEMPLATE $KAFKAHOME/config/$SVR_NAME-$PORTNUMBER$SVR_PROP

         KAFKA_BROKER_ID=$NUM
         sed -i "s/KAFKA_BROKER_ID/$KAFKA_BROKER_ID/g" $KAFKAHOME/config/$SVR_NAME-$PORTNUMBER$SVR_PROP
         
         KAFKA_LISTENERES="PLAINTEXT\:\/\/localhost\:"$PORTNUMBER
         #sed -i "s/KAFKA_LISTENERES/$KAFKA_LISTENERES/g" $KAFKAHOME/config/$SVR_NAME-$UM$SVR_PROP
         sed -i "s/KAFKA_LISTENERES/$KAFKA_LISTENERES/g" $KAFKAHOME/config/$SVR_NAME-$PORTNUMBER$SVR_PROP
        
         #KAFKA_LOG_DIRS="\/data\/kafka-logs-"$NUM
         #sed -i "s/KAFKA_LOG_DIRS/$KAFKA_LOG_DIRS/g" $KAFKAHOME/config/$SVR_NAME-$NUM$SVR_PROP
         KAFKA_LOG_DIRS="\/data\/kafka-logs-"$PORTNUMBER
         sed -i "s/KAFKA_LOG_DIRS/$KAFKA_LOG_DIRS/g" $KAFKAHOME/config/$SVR_NAME-$PORTNUMBER$SVR_PROP
         
         #Call getMultipleZookeeper function if implemented multiple zookeeper server 
         KAFKA_ZOOKEEPER_CONNECT=$(getMultipleZookeeperPortNumber)
         #sed -i "s/KAFKA_ZOOKEEPER_CONNECT/$KAFKA_ZOOKEEPER_CONNECT/g" $KAFKAHOME/config/$SVR_NAME-$NUM$SVR_PROP
         sed -i "s/KAFKA_ZOOKEEPER_CONNECT/$KAFKA_ZOOKEEPER_CONNECT/g" $KAFKAHOME/config/$SVR_NAME-$PORTNUMBER$SVR_PROP

         #Remove "," at the end of line
         #sed -i "s/\,$//g" $KAFKAHOME/config/$SVR_NAME-$NUM$SVR_PROP
         sed -i "s/\,$//g" $KAFKAHOME/config/$SVR_NAME-$PORTNUMBER$SVR_PROP
    done 

    echo "End create Node server.properties..."
}

function createKafkaTopics()
{
    echo "Creating Kafka topic.. " 

    $KAFKAHOME/bin/kafka-topics.sh --create --bootstrap-server $SERVERNAMEPORT --replication-factor $REPFACTOR --partitions $NUMBERCOUNT --topic $TOPICNAME

    echo "done. " 
}

function createKafkaScripts()
{

    echo "Creating Kafka start/stop scripting.. " 

#    mkdir $KAFKAHOME/scripts
#    cp ./$START_KAFKA_SERVER_SH_TEMPLATE $KAFKAHOME/scripts
#    cp ./$START_KAFKA_SH_TEMPLATE $KAFKAHOME/scripts
#    cp ./$START_ZOOKEEPER_SH_TEMPLATE $KAFKAHOME/scripts

#    cp ./$STOP_KAFKA_SH_TEMPLATE $KAFKAHOME/scripts

    _createStartZookeeperServer $KAFKAHOME
    _createStartKafkaServer $KAFKAHOME

    echo "done. " 
}

function listKafkaTopics()
{
      $KAFKAHOME/bin/kafka-topics.sh --zookeeper  $SERVERNAMEPORT --list
}
############################################################################################
# Action from command line 
if [[ "$ACTION" == "I" ]] ;then
    if [[ ! -z "$SOURCE" && ! -z "$KAFKAHOME" ]] ;then
        # Need add validation input option
        install
    else
        usage
    fi
fi

if [[ "$ACTION" == "Z" ]] ;then
    # Validation input option
    if [[ ! -z "$NUMBERCOUNTZOO" && ! -z "$ZPORTNUMBER" && ! -z "$KAFKAHOME" ]] ;then
        createZookeeperProperty
    else
        usage
    fi
fi

if [[ "$ACTION" == "B" ]] ;then
    # Validation input option
    if [[ ! -z "$NUMBERCOUNT" && ! -z "$SERVERNAMEPORT" &&  ! -z "$NUMBERCOUNTZOO" && ! -z "$ZPORTNUMBER" && ! -z "$KAFKAHOME" ]] ;then
        createNodeServerProperty
    else
        usage
    fi
fi

if [[ "$ACTION" == "T" ]] ;then
    # Validation input option
#    if [[ ! -z "$TOPICNAME" && ! -z "$SERVERNAMEPORT" &&  ! -z "$REPFACTOR" && ! -z "$NUMBERCOUNT" && ! -z "$KAFKAHOME" ]] ;then
    if [[ ! -z "$TOPICNAME" && ! -z "$SERVERNAMEPORT" &&  ! -z "$REPFACTOR" && ! -z "$NUMBERCOUNT" && ! -z "$KAFKAHOME" ]] ;then
        createKafkaTopics
    else
        usage
    fi
fi

if [[ "$ACTION" == "S" ]] ;then
    # Validation input option
    if [[ ! -z "$KAFKAHOME" ]] ;then
        createKafkaScripts
    else
        usage
    fi
fi

if [[ "$ACTION" == "L" ]] ;then
    # Validation input option
    if [[ ! -z "$KAFKAHOME" && ! -z $SERVERNAMEPORT ]] ;then
     listKafkaTopics
    else
        usage
    fi
fi

