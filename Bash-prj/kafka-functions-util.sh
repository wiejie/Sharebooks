#!/bin/sh
#
# Modification History:
# 04/05/2019 - created by Wie Jie Tjoeng
#

#Define global variables
SCRIPTDIR="scripts"
FILENAME="start-kserver.sh"

function _createStartZookeeperServer(){

local PARAM1=$1

    echo " Zookeeper Parameter $1 "

    if [[ -f $PARAM1/$SCRIPTDIR/$FILENAME ]]; then 
       rm $PARAM1/$SCRIPTDIR/$FILENAME
    else
       mkdir $PARAM1/$SCRIPTDIR
       touch $PARAM1/$SCRIPTDIR/$FILENAME
    fi

    # Compose the star-kafka.sh file
    echo "echo \"Starting zookeeper\" " >> $PARAM1/$SCRIPTDIR/$FILENAME

    for f in $( ls $1/config/zookeeper-*.properties ) ; do

      echo "../bin/zookeeper-server-start.sh ../config/$(basename "${f}")  &" >> $PARAM1/$SCRIPTDIR/$FILENAME
      echo "sleep 20s" >> $PARAM1/$SCRIPTDIR/$FILENAME

    done

    chmod +x $PARAM1/$SCRIPTDIR/$FILENAME
}

function _createStartKafkaServer(){

local PARAM1=$1

    echo " KafkaServer  Parameter $1 "

    if [[ ! -f $PARAM1/$SCRIPTDIR/$FILENAME ]]; then 
       mkdir $PARAM1/$SCRIPTDIR
       touch $PARAM1/$SCRIPTDIR/$FILENAME
    fi

    # Compose the star-kafka.sh file
    echo "echo \"Starting Kafka Server\" " >> $PARAM1/$SCRIPTDIR/$FILENAME

    for f in $( ls $1/config/server-*.properties ) ; do

      echo "../bin/kafka-server-start.sh ../config/$(basename "${f}")  &" >> $PARAM1/$SCRIPTDIR/$FILENAME
      echo "sleep 20s" >> $PARAM1/$SCRIPTDIR/$FILENAME

    done

    chmod +x $PARAM1/$SCRIPTDIR/$FILENAME
}
