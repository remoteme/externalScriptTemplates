import os
from enum import Enum
import time


USER_DATA_HEADEARS_SIZE = 7
USER_SYNC_DATA_HEADEARS_SIZE = 12

class UserMessageSettings(Enum):
    NO_RENEWAL = 0
    RENEWAL_IF_FAILED = 1

class MessageType(Enum):
    USER_MESSAGE=100
    USER_MESSAGE_WEBPAGE_TOKEN=108
    USER_MESSAGE_DELIVER_STATUS=101
    USER_SYNC_MESSAGE=102
    USER_SYNC_MESSAGE_WEBPAGE_TOKEN=109
    VARIABLE_CHANGE_MESSAGE=103
    VARIABLE_CHANGE_PROPAGATE_MESSAGE=104
    VARIABLE_CHANGE_PROPAGATE_MESSAGE_WEBPAGE_TOKEN=107
    SEND_PUSH_NOTIFICATION=105
    DECREASE_WEBPAGE_TOKEN_CREDIT=110
    SYNC_MESSAGE=120
    SYNC_MESSAGE_RESPONSE=121
    OBSERVER_REGISTER_MESSAGE=122
    REGISTER_DEVICE=200
    REGISTER_CHILD_DEVICE=201
    ADD_DATA=300
    LOG=20000
    SYSTEM_MESSAGE=20001,
    CONNECTION_CHANGE=30001

class VariableType(Enum):
    BOOLEAN=0
    INTEGER=1
    TEXT=2
    SMALL_INTEGER_3=3
    SMALL_INTEGER_2=4
    INTEGER_BOOLEAN=5
    DOUBLE=6
    TEXT_2=7
    SMALL_INTEGER_2_TEXT_2=8

class LogLevel(Enum):
    INFO = 1
    WARN = 2
    ERROR = 3

class ConnectionState(Enum):
    CONNECTING = 0
    CONNECTED = 1
    DISCONNECTED = 2
    FAILED = 3
    DISCONNECTING = 4
    CHECKING = 5

class AddDataMessageSetting(Enum):
    NO_ROUND = 0
    _1S = 1
    _2S = 2
    _5S = 3
    _10S = 4
    _15S = 5
    _20S = 6
    _30S = 7


class DataSeries:
    seriesId=0
    value=0.0

    def __init__(self, seriesId, value):
        self.seriesId = seriesId
        self.value = value


class LeafDeviceType:
    LD_OTHER = 1
    LD_EXTERNAL_SCRIPT = 2
    LD_SERIAL = 3
    LD_NRF24 = 4
    LD_WEB_SOCKET = 5
    LD_GPIO = 6