import logging
import socket
import struct

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

logger = None
remoteMe = None

pwm = None;

motorAIn1 = 25  # GPIO25
motorAIn2 = 8  # GPIO8

motorBIn1 = 24  # 24
motorBIn2 = 23  # 23

motors = [[motorAIn1, motorAIn2], [motorBIn1, motorBIn2]]

motorsPWM = [14, 15]


def onUserSyncMessage(senderDeviceId, data):
    logger.info("on user SYNC message got from {} of length {}".format(senderDeviceId, len(data)))


def setMotor(motorId, mode, speed):
    if mode == 1:
        motorSoftStop(motorId)
    elif mode == 2:
        motorForward(motorId)
    elif mode == 3:
        motorBackward(motorId)

    pwm.set_pwm(motorsPWM[motorId], 0, speed)


def onUserMessage(senderDeviceId, data):
    global pwm
    data = struct.unpack('>BhhBBBB', data)

    if data[0] == 1:
        positionX = data[1]
        positionY = data[2]

        motorLeftMode = data[3]
        motorLeftSpeed = data[4] * 16;

        motorRightMode = data[5]
        motorRightSpeed = data[6] * 16;

        pwm.set_pwm(1, 0, positionX)
        pwm.set_pwm(0, 0, positionY)

        setMotor(0, motorLeftMode, motorLeftSpeed)
        setMotor(1, motorRightMode, motorRightSpeed)


def setupPWM():
    global pwm
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(80)


def setupPins():
    global GPIO
    GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme

    for motor in motors:
        for pinId in motor:
            GPIO.setup(pinId, GPIO.OUT)


def motorForward(motorId):
    GPIO.output(motors[motorId][0], GPIO.LOW)
    GPIO.output(motors[motorId][1], GPIO.HIGH)


def motorBackward(motorId):
    GPIO.output(motors[motorId][0], GPIO.HIGH)
    GPIO.output(motors[motorId][1], GPIO.LOW)


def motorSoftStop(motorId):
    GPIO.output(motors[motorId][0], GPIO.LOW)
    GPIO.output(motors[motorId][1], GPIO.LOW)


try:

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d.%m %H:%M',
                        filename="./logs.log")

    logger = logging.getLogger('application')

    logger.info(">>> My Python application")

    setupPWM()
    setupPins()

    remoteMe = remoteme.RemoteMe()
    remoteMe.startRemoteMe(sys.argv)

    remoteMe.setUserMessageListener(onUserMessage)
    remoteMe.setUserSyncMessageListener(onUserSyncMessage)

    # for i in range(0,20):
    #   sleep(1)
    #   logger.info(">>> My Python application {}".format(i))

    remoteMe.wait()


finally:

    print("PYTHON finished")



