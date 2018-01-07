import socket
import threading

import messages
import struct
import logging

from messages import getUserMessage


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class RemoteMe(metaclass=Singleton):
    pass

    __userMessageListeners=[]



    __socketObj = None
    __ownId = None
    __threadRead = None

    def __init__(self):
        self.__logger = logging.getLogger('remoteMe.RemoteMe')
        self.__logger.info('creating an instance of RemoteMe')

    def __readFromSocket(self):
        while self.__socketObj is not None :
            try:
                header = self.__socketObj.recv(4)
                if (len(header) == 4):
                    [messageType, size] = struct.unpack(">hh", header)
                    messageType = struct.MessageType(messageType)
                    print('PYTHON messageType: {} size: {}'.format(messageType, size))
                    data = self.__socketObj.recv(size)
                    print('PYTHON data size: {} read '.format(len(data)))
                    if (len(data) == size):
                        if (messageType == struct.MessageType.USER_MESSAGE):
                            [userMessageSettings, receiverDeviceId, senderDeviceId, messageId, data] = struct.unpack(
                                ">Bhhh{0}s".format(size - struct.USER_DATA_HEADEARS_SIZE), data)
                            userMessageSettings = struct.UserMessageSettings(userMessageSettings)#for later use

                            if (self.__ownId==receiverDeviceId):
                                self.__onUserMessage(userMessageSettings,senderDeviceId, messageId, data)
                            else:
                                print('PYTHON wrong deviceId :{} '.format(receiverDeviceId))
                        else:
                            print('PYTHON wrong data type {} '.format(messageType))

            except:
                self.__socketObj.close()
                print("PYTHON socke OBJ close")
        print("PYTHON end loop")




    def __toHexString(self,array):
        return (''.join('{:02x} '.format(x) for x in array))

    def __onUserMessage(self,userMessageSettings,senderDeviceId,messageId,data):
        self.__logger.debug("got user sender deviceId:{} datalen:{} data: {} ".format(senderDeviceId , len(data),self.__toHexString(data)))
        for listener in self.__userMessageListeners:
            listener(senderDeviceId,data)

    def __onSyncMessage(self, userMessageSettings, senderDeviceId, messageId, data):
        self.__logger.debug("got user sender deviceId:{} datalen:{} data: {} ".format(senderDeviceId, len(data),
                                                                                    self.__toHexString(data)))
        for listener in self.__userMessageListeners:
            listener(senderDeviceId, data)


    def __send(self,message):
        self.__socketObj.sendall(message)



    def __exit__(self, exc_type, exc_value, traceback):
        self.__logger.info("Exit remoteme python with id {}".format(self.__ownId))
        if self.__socketObj is not None:
            self.__socketObj.close()
            self.__socketObj = None

        if self.__threadRead is not None:
            self.__threadRead.join(1000)


    def startRemoteMe(self,sysargv):
        if (len(sysargv)>=4):
            parentId = int(sysargv[1])
            ownId = int(sysargv[2])
            port = int(sysargv[3])
            name="python script"
            if len(sysargv)==5:
                name=sysargv[4]

            self.startRemoteMe(port,parentId,ownId,name)

        else:
            self.__logger.info("usable parentId ownId port deviceName")
            self.__logger.info("got parameters {} : {}".format(len(sysargv), sysargv))
            exit(1)


    def startRemoteMe(self, port, parentId, ownId,name):
        if self.__socketObj is not None:
            self.__logger.warning("Remote Me already started")
            return


        self.__logger.info("starting remogemeMe port:{} parentId:{} ownId:{} name:{}".format(port, parentId, ownId,name))
        self.__ownId = ownId

        self.__socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socketObj.connect(("localhost", port))

        self.__threadRead = threading.Thread(target=self.__readFromSocket)
        self.__threadRead.daemon = True
        self.__threadRead.start()

        self.__send(messages.getRegisterLeafDeviceMessage(parentId, self.__ownId, name,
                                                          struct.LeafDeviceType.LD_EXTERNAL_SCRIPT))

    def addUserMessageListener(self, function):
        self.__userMessageListeners.append(function)

    def addSyncMessageListener(self, function):
        self.__userMessageListeners.append(function)

    def sendUserMessage(self,receiveDevideId,data):
        self.__send(messages.getUserMessage(struct.UserMessageSettings.NO_RENEWAL,receiveDevideId,self.__ownId,0,data))

    def logServerInfo(self, message):
        self.__send(messages.getLogMessage(struct.LogLevel.INFO,message))

    def logServerWarn(self, message):
        self.__send(messages.getLogMessage(struct.LogLevel.WARN, message))

    def logServerError(self, message):
        self.__send(messages.getLogMessage(struct.LogLevel.ERROR, message))

