from socket import *
import threading
from protocol import HXeption, SocketHandlerClient


class DataListener(threading.Thread):
    def __init__(self, socketHandler):
        threading.Thread.__init__(self)
        self.socketHandler = socketHandler
        self.connected = True
    def run(self):
        try:
            while 1:
                packets = self.socketHandler.read()
                if packets:
                    for packet in packets:
                        print packet
        except HXeption as e:
            print e
            self.connected = False

if __name__ == '__main__':
    host = 'localhost'
    port = 1337
    addr = (host, port)
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect(addr)
    socketHandler = SocketHandlerClient(clientsocket, "twat")
    dataListener = DataListener(socketHandler)
    dataListener.daemon = True
    dataListener.start()
    try:
        while dataListener.connected:
            data = raw_input()
            if data:
                socketHandler.writeToChat(data)
    except Exception as e:
        print "Exception: ", e
    finally:
        dataListener.connected = False
        clientsocket.close()
        print "..clean exit.."
