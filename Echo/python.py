#from __future__ import division

import logging
import socket


import struct
import sys
import os


os.chdir(sys.argv[1])


import remotemeMessages
import remoteme
import remotemeStruct
import remotemeUtils






logger=None
remoteMe=None


def onUserSyncMessage(senderDeviceId,data):
    logger.info("on user SYNC message got from {} of length {}".format(senderDeviceId,len(data)))

    return "Hello Sync "+remotemeMessages.getStringFromArray(data)


def onUserMessage(senderDeviceId,data):
    global remoteMe;
    logger.info("on onUserMessage from senderId {}  length {}".format(senderDeviceId,len(data)))

    remoteMe.sendUserMessage(senderDeviceId,"Hello  "+remotemeMessages.getStringFromArray(data))






try:

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d.%m %H:%M',
                        filename="logs.log")

    logger = logging.getLogger('application')

    logger.info(">>> My Python application")


    remoteMe = remoteme.RemoteMe()


    remoteMe.setUserMessageListener(onUserMessage)
    remoteMe.setUserSyncMessageListener(onUserSyncMessage)

    remoteMe.startRemoteMe(sys.argv)

    remoteMe.wait()


finally:


    print("PYTHON finished")



