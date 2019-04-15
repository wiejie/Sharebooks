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


def installKafa(source, destination):

    print ("Install..... " + source)
    if not os.path.exists(destination):
        os.makedirs(destination)

    # with t.open(source, 'r') as t:
    #     t.extractall(destination)
    # print(os.listdir(destination))

    retcode = subprocess.call(['tar', '-xvzf', source, '-C', destination, '--strip-components=1' ])
    if retcode == 0:
        print
        "Extracted successfully"
    else:
        raise IOError('tar exited with code %d' % retcode)

def createZookeeperProperty(NUMBERCOUNTZOO, ZPORTNUMBER: object, KAFKAHOME):

    print("CreateZookeeperProperty..... ")

#    for NUM in range(NUMBERCOUNTZOO):
    for NUM in range(int(NUMBERCOUNTZOO)):

        KAFKA_BROKER_ID = NUM
        PORTNUMBER = int(ZPORTNUMBER) + NUM

        #echo "Creating zookeeper-$NUM.properties file... "
        print( 'Creating zookeeper-{0}.properties file... '.format(PORTNUMBER))

        shutil.copy(ZOO_PROP_TEMPLATE, KAFKAHOME + '/config/' + ZOO_NAME + '-' + str(PORTNUMBER) + ZOO_PROP )

        ZOOKEEPER_DATADIR = '/tmp/zookeeper-' + str(PORTNUMBER)
        ZOOKEEPER_CLIENTPORT = str(PORTNUMBER)

        ZPROPPFILE = KAFKAHOME + '/config/' + ZOO_NAME + '-' + str(PORTNUMBER) + ZOO_PROP
        base_path = Path(__file__).parent
        FileName = (base_path / ZPROPPFILE).resolve()

        # Search ZOOKEEPER_DATADIR and replace with Environment Variable
        with open(FileName) as f:
            newText=f.read().replace('ZOOKEEPER_DATADIR', ZOOKEEPER_DATADIR)

        with open(FileName, "w") as f:
            f.write(newText)

        # Search ZOOKEEPER_CLIENTPORT and replace with Environment Variable
        with open(FileName) as f:
            newText=f.read().replace('ZOOKEEPER_CLIENTPORT', ZOOKEEPER_CLIENTPORT)

        with open(FileName, "w") as f:
            f.write(newText)



############################################################################################################
def main(argv):

   ACTION = ''
   SOURCE = ''
   KAFKAHOME = ''
   NUMBERCOUNT = ''
   NUMBERCOUNTZOO = ''
   TOPICNAME = ''
   SERVERNAMEPORT = ''
   KPORTNUMBE = ''
   ZPORTNUMBER = ''
   REPFACTOR = ''

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
    elif opt in ("-q", "--brokerPortNumber"):
        ZPORTNUMBER = arg
    elif opt in ("-p", "--brokerPortNumber"):
        KPORTNUMBER = arg
   #...

   # Action from command line
   if ACTION in ("-I", "--Install"):
       print('ACTION : ', ACTION)
       print('SOURCE : ', SOURCE)
       print('KAFKA HOME : ', KAFKAHOME)
       installKafa(SOURCE, KAFKAHOME)

   if ACTION in ("-Z", "--Zookeeper"):
       print('ACTION : ', ACTION)
       print('NUMBERCOUNTZOO : ', NUMBERCOUNTZOO)
       print('zookeeperPortNumber : ', ZPORTNUMBER)
       print('KAFKA HOME : ', KAFKAHOME)
       createZookeeperProperty(NUMBERCOUNTZOO,ZPORTNUMBER,KAFKAHOME)

if __name__ == "__main__":
   main(sys.argv[1:])
