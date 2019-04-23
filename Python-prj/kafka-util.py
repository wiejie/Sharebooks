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
import re
import platform

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

#Define global variables
SCRIPTDIR="scripts"
FILENAME="start-kserver.sh"

# Use lambda function to create multiple zookeeper portnumber
zookeeper_ports = lambda n, p : ','.join( [ 'localhost:'+str(p+x) for x in range(n)] )

# Use lambda function to get the right kafka bin dirctory base on OS
KAFKABIN = lambda s, h : h+'bin\\windows\\' if s == "Windows" else h+'bin/'

############################################################################################
# Usage or Help function
############################################################################################
def usage():
      print ("Usage: " + sys.argv[0] + " -h " )
      print ("       " + sys.argv[0] + " -I -s sourceTarFile -d untarTargetDirectory" )
      print ("       " + sys.argv[0] + " -Z -n numberOfZookeeper -q zookeeperPortNumber -d kafkaHomeDirectory" )
      print ("       " + sys.argv[0] + " -B -n numberOfBroker -p brokerPortNumber -z numberOfZookeeper -q zookeeperPortNumber -d cofigurationDirectory" )
      print ("       " + sys.argv[0] + " -T -t topicName -p serverName:portNumber -f replicationFactor -n numberOfPartition  -d kafkaHomeDirectory" )
      print ("       " + sys.argv[0] + " -S -d kafkaHomeDirectory" )
      print ("       " + sys.argv[0] + " -L -p zookeeperServer:portNumber -d kafkaHomeDirectory" )
      print ("       " + sys.argv[0] + " -P -t topicName -p serverName:portNumber -d kafkaHomeDirectory" )
      print ("       " + sys.argv[0] + " -C -t topicName -p serverName:portNumber -d kafkaHomeDirectory" )
      print ("")
      print ("Options:" )
      print ("  -h      : Display this help message.")
      print ("  -I      : Install kafka tar file.")
      print ("  -Z      : Create zookeeper server.properties.")
      print ("  -B      : Create kafka broker server.")
      print ("  -T      : Create kafka topic.")
      print ("  -S      : Create Start/Stop kafka scripts.")
      print ("  -L      : List all kafka topics.")
      print ("  -P      : Produce kafka message.")
      print ("  -C      : Consume kafka message.")

############################################################################################
# functions
############################################################################################
def search_and_replace(file_name, search_text, replace_text ):
    with open(file_name) as f:
        new_text=f.read().replace( search_text, replace_text )

    with open(file_name, "w") as f:
        f.write(new_text)

#Refector / replace with lambda function
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

        KAFKA_LISTENERES="PLAINTEXT://localhost:" + str(PORTNUMBER)
        # Search KAFKA_LISTENERS and replace with environment variable
        search_and_replace(FileName, 'KAFKA_LISTENERES', KAFKA_LISTENERES )

        KAFKA_LOG_DIRS="/data/kafka-logs-" + str(PORTNUMBER)
        # Search KAFKA_LOG_DIRS and replace with environment variable
        search_and_replace(FileName, 'KAFKA_LOG_DIRS', KAFKA_LOG_DIRS )

        KAFKA_ZOOKEEPER_CONNECT = zookeeper_ports(int(NUMBERCOUNTZOO), int(ZPORTNUMBER) )
        #replaced with lambda function
        #KAFKA_ZOOKEEPER_CONNECT =  get_multiple_zookeeper_portnumber(NUMBERCOUNTZOO, ZPORTNUMBER )

        #Search KAFKA_ZOOKEEPER_CONNECT and replace with environment variable
        search_and_replace(FileName, 'KAFKA_ZOOKEEPER_CONNECT', KAFKA_ZOOKEEPER_CONNECT )

        print( "End create Node server.properties...")


def create_kafka_scripts(kafka_dir):

    print("Creating Kafka start/stop scripting.. " )
    dir_kafka = './' + kafka_dir + '/' + SCRIPTDIR
    config_dir = kafka_dir + '/config'
    path_filename = dir_kafka  + '/' + FILENAME

    if ( os.path.exists(dir_kafka) ):
        #os.remove(dir_kafka) # permission isues in window platform
        os.system('rm -rf ' + dir_kafka)

    access_rights = 0o755
    os.mkdir(dir_kafka,access_rights)
    os.system('touch ' + path_filename)

    # Generate the filter for zookeeper-????.properties file
    filter = re.compile('zookeeper-\d*\.properties')
    all_files = [ f for f in os.listdir(config_dir)
                  if filter.match(f) ]

    # Compose the star-zookeeper.sh file
    for f in all_files:

        with open(path_filename, "a") as file:
            file.write('echo "Starting Zookeeper..." \n')
            file.write('../bin/zookeeper-server-start.sh ../config/{}'.format(f) + ' &  \n' )
            file.write('sleep 100s &  \n')
            file.closed

    # Compose the star-kafka.sh file
    filter_server = re.compile('server-\d*\.properties')
    all_server_files = [ f for f in os.listdir(config_dir)
                  if filter_server.match(f) ]
    for f in all_server_files:

        with open(path_filename, "a") as file:
            file.write('echo "Starting kafka Server..." \n')
            file.write('../bin/kafka-server-start.sh ../config/{}'.format(f) + ' &  \n' )
            file.write('sleep 50s &  \n')
            file.closed

    # Change the file mode to executable file.
    os.system('chmod 755 ' + path_filename)

def create_kafka_topic(kafka_home, topic_name, server_name_portnumber, number_replication, number_partition):

    print( "Creating Kafka topic.. " + topic_name )

    #$KAFKAHOME/bin/kafka-topics.sh --create --bootstrap-server $SERVERNAMEPORT --replication-factor $REPFACTOR --partitions $NUMBERCOUNT --topic $TOPICNAME

    KBIN =  KAFKABIN( platform.system(), kafka_home)
    retcode = subprocess.call([os.path.join( KBIN , 'kafka-topics.bat'), '--create', '--bootstrap-server' , server_name_portnumber , '--replication-factor', number_replication,
                             '--partitions', number_partition, '--topic', topic_name ], shell=True)

    if retcode == 0:
        print
        "Create topics successfully"
    else:
        raise IOError('tar exited with code %d' % retcode)

    print( "done. " )


def list_kafka_topics(kafka_home, server_name_port):

    print ("Listing..... " + server_name_port)

    topics = subprocess.check_output([ os.path.join( KAFKABIN( platform.system(),kafka_home),'kafka-topics.bat'),
                                     '--list',
                                     '--zookeeper', '{}'.format(server_name_port)],shell=True)

    print ( '{}'.format( topics ) )


def produce_kafka_message(kafka_home, server_name_port, topic_name):

    print("Produce message of Kafka function..")

    KBIN =  KAFKABIN( platform.system(),kafka_home)
    retcode = subprocess.call([ os.path.join(KBIN,'kafka-console-producer.bat'),
                              '--broker-list', server_name_port,
                              '--topic', topic_name], shell=True )

    #           --producer.config  ../certs/client-ssl.properties

#    cmd = os.path.join(KBIN,'kafka-console-producer.bat') +  ' --broker-list '  +  server_name_port + ' --topic ' + topic_name
#    print( cmd )
#    os.system( cmd )

#    retcode = subprocess.Popen([ os.path.join(KBIN,'kafka-console-producer.bat'),
#                               '--broker-list', server_name_port, '--topic', topic_name ],shell=True)

    if retcode == 0:
        print
        "Produce message successfully"
    else:
        raise IOError('kafka-console-producer exited with code %d' % retcode)

    print( "done. " )

def consume_kafka_message(kafka_home, server_name_port, topic_name):

    print("Produce message of Kafka function..")

#Test the command line
#    KBIN =  KAFKABIN( platform.system(),kafka_home)
#    cmd = os.path.join(KBIN,'kafka-console-consumer.bat') + ' --bootstrap-server '  +  server_name_port + ' --topic ' + topic_name + ' --from-beginning '
#    print( cmd )
#    os.system( cmd )

    KBIN =  KAFKABIN( platform.system(),kafka_home)
    retcode = subprocess.call([ os.path.join(KBIN,'kafka-console-consumer.bat'),
                              '--bootstrap-server', server_name_port,
                              '--topic', topic_name,
                              '--from-beginning'],
                              shell=True )

    #           --producer.config  ../certs/client-ssl.properties

    if retcode == 0:
        print
        "Consume messages successfully"
    else:
        raise IOError('tar exited with code %d' % retcode)


############################################################################################################
def main(argv):

   try:
    opts, args = getopt.getopt(argv, "s:d:n:z:t:p:q:f:k:hIZBTSLPC", ["Install", "Zookeeper", "Broker", "Topic", "topicName=", "source=", "directory=", "brookerPortNumber=", "script=", "listTopics=", "produce=", 'consume='] )
   except getopt.GetoptError:
    usage()
    sys.exit(2)
   for opt, arg in opts:
    if opt == '-h':
        usage()
        sys.exit()
    elif opt in ("-I", "-Z", "-B", "-T", "-S", "-L", "-P", "-C", "--Install", "--Zookeeper", "--Broker", "--topicName"):
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

   try:
       if ACTION in ("-T", "--topicName"):
           # -d kafka home directory
           create_kafka_topic(KAFKAHOME,TOPICNAME, SERVERNAMEPORT,NUMBERCOUNT,REPFACTOR)
   except NameError:
       usage()

   try:
       if ACTION in ("-S", "--script"):
           # -d kafka home directory
           create_kafka_scripts(KAFKAHOME)
   except NameError:
       usage()

   try:
       if ACTION in ("-L", "--listTopics"):
           # -d kafka home directory
           list_kafka_topics(KAFKAHOME,SERVERNAMEPORT)
   except NameError:
       usage()

   try:
       if ACTION in ("-P", "--produce"):
           produce_kafka_message(KAFKAHOME, SERVERNAMEPORT, TOPICNAME)
   except NameError:
       usage()

   try:
       if ACTION in ("-C", "--consume"):
           # -d kafka home directory
           consume_kafka_message(KAFKAHOME, SERVERNAMEPORT, TOPICNAME)
   except NameError:
       usage()

if __name__ == "__main__":
   main(sys.argv[1:])

