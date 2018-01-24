#from __future__ import division

import logging
import socket


import struct
import ../base/remotemeMessages
import ../base/remoteme
import ../base/remotemeStruct
import ../base/remotemeUtils

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

motors =[[motorAIn1,motorAIn2],[motorBIn1,motorBIn2]]

motorsPWM=[14,15]

def onUserSyncMessage(senderDeviceId,data):
    logger.info("on user SYNC message got from {} of length {}".format(senderDeviceId,len(data)))




def onUserMessage(senderDeviceId,wholeData):
    global pwm

    datas=remotemeUtils.splitMessage(wholeData,4)
    for data in datas :

        logger.info(data)
        data=struct.unpack('>BBBB', data)

        if data[0]==1:
            motorId = data[1]
            mode = data[2]
            speed = data[3]*16

            if mode == 1:
                motorSoftStop(motorId)
            elif mode == 2:
                motorForward(motorId)
            elif mode == 3:
                motorBackward(motorId)

            pwm.set_pwm(motorsPWM[motorId], 0, speed)

        elif data[0] == 2:#camera
            cameraId = data[1]
            position = data[2]*256+data[3]


            pwm.set_pwm(cameraId, 0, position)





def setupPWM():
    global pwm
    pwm= Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(80)


def setupPins():
    global GPIO
    GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme

    for motor in motors:
        for pinId in motor:
            GPIO.setup(pinId, GPIO.OUT)



def motorForward(motorId):
    GPIO.output(motors[motorId][0], GPIO.LOW )
    GPIO.output(motors[motorId][1], GPIO.HIGH)

def motorBackward(motorId):
    GPIO.output(motors[motorId][0], GPIO.HIGH )
    GPIO.output(motors[motorId][1], GPIO.LOW)

def motorSoftStop(motorId):
    GPIO.output(motors[motorId][0], GPIO.LOW )
    GPIO.output(motors[motorId][1], GPIO.LOW)



try:

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d.%m %H:%M',
                        filename="./{}/logs.log".format(sys.argv[2]))

    logger = logging.getLogger('application')

    logger.info(">>> My Python application")

    setupPWM()
    setupPins()

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



