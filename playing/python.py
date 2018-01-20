#from __future__ import division

import logging
import socket

import struct
import remotemeMessages
import remoteme
import remotemeStruct
import remotemeUtils

import threading
import sys
from time import sleep

import time

logger=None
remoteMe=None


pwm=None;

motorAIn1=25#GPIO25
motorAIn2=8#GPIO8

motorBIn1=24#24
motorBIn2=23#23

motors =[[motorAIn1,motorAIn2],[motorBIn1,motorBIn2]]

motorsPWM=[14,15]









pam=remotemeMessages.getLogMessage(remotemeStruct.LogLevel.INFO,"asdadsasd")

print(bytes(pam))

print(remotemeUtils.splitMessage(pam,4))

print("PYTHON finished")



