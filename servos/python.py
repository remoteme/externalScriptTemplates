#from __future__ import division

import logging
import socket


import struct
import sys
import os
os.chdir(sys.argv[1])

sys.path.append('../base')

import remotemeMessages
import remoteme
import remotemeStruct
import remotemeUtils


import Adafruit_PCA9685




logger=None
remoteMe=None


pwm=None;



def onUserSyncMessage(senderDeviceId,data):
    logger.info("on user SYNC message got from {} of length {}".format(senderDeviceId,len(data)))




def onUserMessage(senderDeviceId,data):
    global pwm
    data=struct.unpack('>Bh', data)

    print("on setting servo {} with value {}".format(data[0],data[1]))
    pwm.set_pwm(data[0], 0,data[1] )



def setupServo():
    global pwm
    pwm= Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(80)





try:

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d.%m %H:%M',
                        filename="logs.log")

    logger = logging.getLogger('application')

    logger.info(">>> My Python application")

    setupServo()

    remoteMe = remoteme.RemoteMe()
    remoteMe.startRemoteMe(sys.argv)

    remoteMe.addUserMessageListener(onUserMessage)
    remoteMe.addUserSyncMessageListener(onUserSyncMessage)



    remoteMe.wait()


finally:


    print("PYTHON finished")



