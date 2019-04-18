#!/usr/bin/python3
#
# Modification History:
# 03/28/2019      Created by Wie Jie Tjeong
#
#
import getopt, sys
import os, tarfile
import subprocess
import shutil
from pathlib import Path

############################################################################################ # Declare global variables ############################################################################################ ACTION = '' SOURCE = '' KAFKAHOME = '' NUMBERCOUNT = ''
NUMBERCOUNTZOO = ''
TOPICNAME = ''
SERVERNAMEPORT = ''
KPORTNUMBER = ''
ZPORTNUMBER = ''
REPFACTOR = ''

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

# Use lambda functint to create multiple zookeeper portnumber
zookeeper_ports = lambda n, p : ','.join( [ 'localhost'+str(p+x) for x in range(n)] )

############################################################################################
# Usage or Help function
############################################################################################
def usage():
      print ("Usage: " + sys.argv[0] + " -h " )
      print ("       " + sys.argv[0] + " -I -s sourceTarFile -d untarTargetDirectory" )
      print ("       " + sys.argv[0] + " -Z -n numberOfZookeeper -q zookeeperPortNumber -d kafkaHomeDirectory" )
      print ("       " + sys.argv[0] + " -B -n numberOfBroker -p brokerPortNumber -z numberOfZookeeper -q zookeeperPortNumber -d cofigurationDirectory" )
      print ("       " + sys.argv[0] + " -T -t topicName -p serverName:portNumber -f replicationFactor -n numberOfPartition  -k kafkaHomeDirectory" )
      print ("       " + sys.argv[0] + " -S -d kafkaHomeDirectory" )
      print ("       " + sys.argv[0] + " -L -p zookeeperServer:portNumber -d kafkaHomeDirectory" )
      print ("       " + sys.argv[0] + " -P -t topicName serverName:portNumber -d kafkaHomeDirectory" )
      print ("       " + sys.argv[0] + " -C -t topicName serverName:portNumber -d kafkaHomeDirectory" )
      print ("")
      print ("Options:" )
      print ("  -h      : Display this help message.")
      print ("  -I      : Install kafka tar file.")
      print ("  -Z      : Create zookeeper server.properties.")
      print ("  -B      : Create kafka broker server.")
      print ("  -T      : Create kafka topic.")
      print ("  -S      : Create Start/Stop kafka scripts.")
      print ("  -L      : List all kafka topics.")

############################################################################################
# functions
############################################################################################
def search_and_replace(file_name, search_text, replace_text ):
    with open(file_name) as f:
        new_text=f.read().replace( search_text, replace_text )

    with open(file_name, "w") as f:
        f.write(new_text)

def get_multiple_zookeeper_portnumber(n, zoo_portnumber):

    zoo_client_port = ''
    for i in range(int(n)):
        port_number = int(zoo_portnumber) + i
        zoo_client_port += 'localhost:' + str(port_number) + ','

    return  zoo_client_port[:-1]


def install_kafka(source, destination):

    print ("Install..... " + source)
    if not os.path.exists(destination):
        os.makedirs(destination)

    retcode = subprocess.call(['tar', '-xvzf', source, '-C', destination, '--strip-components=1' ])
    if retcode == 0:
        print
        "Extracted successfully"
    else:
        raise IOError('tar exited with code %d' % retcode)


def create_zookeeper_properties(NUMBERCOUNTZOO, ZPORTNUMBER: object, KAFKAHOME):

    print("CreateZookeeperProperty..... ")

    for NUM in range(int(NUMBERCOUNTZOO)):

        KAFKA_BROKER_ID = NUM
        PORTNUMBER = int(ZPORTNUMBER) + NUM

        print( 'Creating zookeeper-{0}.properties file... '.format(PORTNUMBER))

        shutil.copy(ZOO_PROP_TEMPLATE, KAFKAHOME + '/config/' + ZOO_NAME + '-' + str(PORTNUMBER) + ZOO_PROP )

        ZOOKEEPER_DATADIR = '/tmp/zookeeper-' + str(PORTNUMBER)
        ZOOKEEPER_CLIENTPORT = str(PORTNUMBER)

        ZPROPPFILE = KAFKAHOME + '/config/' + ZOO_NAME + '-' + str(PORTNUMBER) + ZOO_PROP
        base_path = Path(__file__).parent
        FileName = (base_path / ZPROPPFILE).resolve()

        # Search ZOOKEEPER_DATADIR and replace with Environment Variable
        search_and_replace(FileName, 'ZOOKEEPER_DATADIR', ZOOKEEPER_DATADIR )

        # Search ZOOKEEPER_CLIENTPORT and replace with Environment Variable
        search_and_replace(FileName, 'ZOOKEEPER_CLIENTPORT', ZOOKEEPER_CLIENTPORT)


def create_node_server_property(NUMBERCOUNT, KPORTNUMBER, NUMBERCOUNTZOO, ZPORTNUMBER, KAFKAHOME ):

    print("Begin create Node server.properties using {0} $SVR_PROP_TEMPLATE in {1} $KAFKAHOME/config directory".format(SVR_PROP_TEMPLATE, KAFKAHOME ))

    for NUM in range( int(NUMBERCOUNT) ):

        #Get the kafka port number and increment by NUM
        PORTNUMBER = int(KPORTNUMBER) + NUM

        print( 'Creating server-{0}.properties file... '.format(PORTNUMBER))

        #cp ./$SVR_PROP_TEMPLATE $KAFKAHOME/config/$SVR_NAME-$NUM$SVR_PROP
        shutil.copy(SVR_PROP_TEMPLATE, KAFKAHOME + '/config/' + SVR_NAME + '-' + str(PORTNUMBER) + SVR_PROP )

        # Get the server.properties file location
        KPROPPFILE = KAFKAHOME + '/config/' + SVR_NAME + '-' + str(PORTNUMBER) + SVR_PROP
        base_path = Path(__file__).parent
        FileName = (base_path / KPROPPFILE).resolve()

        KAFKA_BROKER_ID = NUM
        # Search KAFKA_BROKER_ID and replace with environment variable
        search_and_replace(FileName, 'KAFKA_BROKER_ID', str(KAFKA_BROKER_ID) )

        KAFKA_LISTENERES="PLAINTEXT:localhost:" + str(PORTNUMBER)
        # Search KAFKA_LISTENERS and replace with environment variable
        search_and_replace(FileName, 'KAFKA_LISTENERES', KAFKA_LISTENERES )

        KAFKA_LOG_DIRS="/data/kafka-logs-" + str(PORTNUMBER)
        # Search KAFKA_LOG_DIRS and replace with environment variable
        search_and_replace(FileName, 'KAFKA_LOG_DIRS', KAFKA_LOG_DIRS )

        KAFKA_ZOOKEEPER_CONNECT = zookeeper_ports(int(NUMBERCOUNTZOO), int(ZPORTNUMBER) )

        #KAFKA_ZOOKEEPER_CONNECT =  get_multiple_zookeeper_portnumber(NUMBERCOUNTZOO, ZPORTNUMBER )

        #Search KAFKA_ZOOKEEPER_CONNECT and replace with environment variable
        search_and_replace(FileName, 'KAFKA_ZOOKEEPER_CONNECT', KAFKA_ZOOKEEPER_CONNECT )

        print( "End create Node server.properties...")

############################################################################################################
def main(argv):

   try:
    opts, args = getopt.getopt(argv, "s:d:n:z:t:p:q:f:k:hIZBTSL", ["Install", "Zookeeper", "Broker", "Topic", "topicName=", "source=", "directory=", "brookerPortNumber="] )
   except getopt.GetoptError:
    usage()
    sys.exit(2)
   for opt, arg in opts:
    if opt == '-h':
        usage()
        sys.exit()
    elif opt in ("-I", "-Z", "-B", "-T", "-S" "-L", "--Install", "--Zookeeper", "--Broker", "--topicName"):
        ACTION = opt
        print('Option selection ', ACTION)
    elif opt in ("-s", "--source"):
        print('Option selection opt ', opt)
        SOURCE = arg
    elif opt in ("-d", "--directory"):
        KAFKAHOME = arg
    elif opt in ("-n", "--numberOfZookeeper"):
        NUMBERCOUNTZOO = arg
        NUMBERCOUNT = arg
    elif opt in ("-z", "--zooKeeperCount"):
        NUMBERCOUNTZOO = arg
    elif opt in ("-t", "--topicName"):
        TOPICNAME = arg
    elif opt in ("-p", "--portNumber"):
        SERVERNAMEPORT = arg
        KPORTNUMBER = arg
    elif opt in ("-q", "--zookeeperPortNumber"):
        ZPORTNUMBER = arg
    elif opt in ("-f", "--replicateFactor"):
        REPFACTOR = arg

   #...

   # Action from command line
   try:
    if ACTION in ("-I", "--Install"):
       # SOURCE, KAFKAHOME
       install_kafka(SOURCE, KAFKAHOME)
   except NameError:
       usage()

   try:
    if ACTION in ("-Z", "--Zookeeper"):
       # NUMBERCOUNTZOO, ZPORTNUMBER, KAFKAHOME
       create_zookeeper_properties(NUMBERCOUNTZOO,ZPORTNUMBER,KAFKAHOME)
   except NameError:
       usage()

   try:
    if ACTION in ("-B", "--brokerKafa"):
        # NUMBERCOUNT, KPORTNUMBER,  NUMBERCOUNTZOO, ZPORTNUMBER, KAFKAHOME
        create_node_server_property(NUMBERCOUNT, KPORTNUMBER, NUMBERCOUNTZOO, ZPORTNUMBER, KAFKAHOME )
   except NameError:
        usage()

if __name__ == "__main__":
   main(sys.argv[1:])
