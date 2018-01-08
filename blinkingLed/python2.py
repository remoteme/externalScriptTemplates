import logging
import socket

import remotemeMessages
import remoteme
import remotemeStruct

import threading
import sys
from time import sleep


def onPrintCalled(senderDeviceId,data):
    print("was called")


try:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d.%m %H:%M')



    logger = logging.getLogger('application')

    logger.info('pamparampam')

    remoteMe=remoteme.RemoteMe()


    remoteMe.printShort()
    remoteMe.printShort()
    remoteMe.printShort()

    remoteMe2=remoteme.RemoteMe()

    remoteMe.addUserMessageListener(onPrintCalled)


    remoteMe2.printShort()
    remoteMe2.printShort()
    remoteMe2.printShort()

finally:


    print("PYTHON finished")



