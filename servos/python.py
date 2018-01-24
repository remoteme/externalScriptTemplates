#from __future__ import division

import logging
import socket


import struct

import sys; sys.path.append('./base');

import remotemeMessages
import remoteme
import remotemeStruct
import remotemeUtils

import threading
import sys
from time import sleep

import time

import RPi.GPIO as GPIO

import Adafruit_PCA9685

logger=None
remoteMe=None


pwm=None;

motorAIn1=25#GPIO25
motorAIn2=8#GPIO8

motorBIn1=24#24
motorBIn2=23#23

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


def setupPins():
    GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme

    GPIO.setup(motorAIn1, GPIO.OUT)
    GPIO.setup(motorAIn2, GPIO.OUT)
    GPIO.setup(motorBIn1, GPIO.OUT)
    GPIO.setup(motorBIn2, GPIO.OUT)


def motorBForward():
    GPIO.output(motorBIn1, GPIO.LOW )
    GPIO.output(motorBIn2, GPIO.HIGH)

def motorBBackward():
    GPIO.output(motorBIn1, GPIO.HIGH)
    GPIO.output(motorBIn2, GPIO.LOW)



try:

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d.%m %H:%M',
                        filename="./{}/logs.log".format(sys.argv[2]))

    logger = logging.getLogger('application')

    logger.info(">>> My Python application")

    setupServo()
    setupPins()
    motorBForward()
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



