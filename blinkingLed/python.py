import logging
import socket



import remotemeMessages
import remoteme
import remotemeStruct

import threading
import sys
from time import sleep


logger=None
remoteMe=None


def onUserSyncMessage(senderDeviceId,data):
    logger.info("on user SYNC message got from {} of length {}".format(senderDeviceId,len(data)))
    return [data[0]*2]

def onUserMessage(senderDeviceId,data):
    logger.info("on user message got from {} of length {}".format(senderDeviceId,len(data)))

try:

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d.%m %H:%M',
                        filename="./{}/logs.log".format(sys.argv[2]))

    logger = logging.getLogger('application')

    logger.info(">>> My Python application")

    remoteMe = remoteme.RemoteMe()
    remoteMe.startRemoteMe(sys.argv)

    remoteMe.addUserMessageListener(onUserMessage)
    remoteMe.addUserSyncMessageListener(onUserSyncMessage)


    #for i in range(0,20):
    #   sleep(1)
    #   logger.info(">>> My Python application {}".format(i))

    remoteMe.wait()


finally:


    print("PYTHON finished")



