import logging
import socket



import messages
import remoteme
import struct

import threading
import sys
from time import sleep









logger=None
remoteMe=None







def onUserMessage(senderDeviceId,data):
    logger.info("on user message got from {} of length {}".format(senderDeviceId,len(data)))



try:

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d.%m %H:%M')

    logger = logging.getLogger('application')

    logger.info(">>> My Python application")

    remoteMe = remoteme.RemoteMe()
    remoteMe.startRemoteMe(sys.argv)

    remoteMe.addUserMessageListener(onUserMessage)



    #for i in range(0,10000):
    #   socketObj.sendall(getLogMessage(LogLevel.INFO, "pam {}".format(i)))
    #   sleep(0.5)





finally:


    print("PYTHON finished")



