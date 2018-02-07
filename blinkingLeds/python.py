import logging
import socket


import sys;
import os;
os.chdir(sys.argv[1])

sys.path.append('../base');

import remotemeMessages
import remoteme
import remotemeStruct
import remotemeUtils


import threading

from time import sleep

import Adafruit_PCA9685

import time
import RPi.GPIO as GPIO

outputPins =[26, 19]



logger=None
remoteMe=None


def onUserSyncMessage(senderDeviceId,data):
    logger.info("on user SYNC message got from {} of length {}".format(senderDeviceId,len(data)))




def onUserMessage(senderDeviceId,data):
    logger.info("on user message got from {} of length {}".format(senderDeviceId,len(data)))
    GPIO.output(outputPins[data[0]], GPIO.HIGH if data[1] == 1 else GPIO.LOW)


def setupPins():
    GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
    for pin in outputPins:
        GPIO.setup(pin, GPIO.OUT)  # LED pin set as output




try:

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d.%m %H:%M',
                        filename="logs.log")

    logger = logging.getLogger('application')

    logger.info(">>> My Python application")

    remoteMe = remoteme.RemoteMe()
    remoteMe.startRemoteMe(sys.argv)

    remoteMe.addUserMessageListener(onUserMessage)
    remoteMe.addUserSyncMessageListener(onUserSyncMessage)


    #for i in range(0,20):
    #   sleep(1)
    #   logger.info(">>> My Python application {}".format(i))

    setupPins()
    remoteMe.wait()


finally:

    GPIO.cleanup()
    print("PYTHON finished")



