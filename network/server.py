import threading
import socket
import struct
from protocol import  SocketHandlerServer, HXeption, Commands, fillCommand, unifyID

def getID(player):
    if player.nick != None:
        return player.nick
    else:
        return player.clientaddr

class Data(object):
    def __init__(self):
        self.players = []
        self.lock = threading.RLock()

    def addPlayer(self, newPlayer):
        self._noticeOfPlayers(newPlayer)
        self.players.append(newPlayer)

    def removePlayer(self, player):
        with self.lock:
            self.players.remove(player)
            self.sendToAll(player, Commands.leave)

    def sendToAll(self, sender, data):
        for player in self.players:
            if player is not sender:
                player.sendData(sender, data)

    def checkNick(self, nick):
        for player in self.players:
            if player.nick == nick:
                return False
        return True

    def _noticeOfPlayers(self, newPlayer):
        self.sendToAll(newPlayer, Commands.join)
        for player in self.players:
            newPlayer.sendData(player, Commands.join)

class Client(threading.Thread):
    def __init__(self, socketHandler, clientaddr, data):
        threading.Thread.__init__(self)
        self.clientaddr = clientaddr
        self.socketHandler = socketHandler
        self.data = data
        self.connected = True
        self.nick = None
        self.newNick = None
        print "Accepted connection from: ", getID(self)

    def run(self):
        self._receiveData()
        self.socketHandler.close()

    def sendData(self,sender, data):
        senderID = getID(sender)
        self.socketHandler.transmitMessage(senderID, data)

    def _receiveData(self):
        try:
            while 1:
                packets = self.socketHandler.read()
                self._handlePackets(packets)
        except Exception as e:
            print e
            self.connected = False
            self.data.removePlayer(self)

    def _handlePackets(self, packets):
        if packets:
            for packet in packets:
                print "received packet: ", packet ," from: ", getID(self)
                packet = self._checkCommand(packet)
                self.data.sendToAll(self, packet)
                if self.newNick is not None:
                    self.nick = self.newNick
                    self.newNick = None

    def _checkCommand(self, packet):
        ip, command, data = packet.split("|",2)
        command = fillCommand(command)
        if command == Commands.nick:
            return ip+command+self._bruteForceNick(data)
        return packet

    def _bruteForceNick(self, nick):
        while not self.data.checkNick(nick):
            nick += "_"
        self.newNick = nick
        return nick

def main():
    data = Data()
    host = 'localhost'
    port = 1337
    addr = (host, port)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(addr)
    serversocket.listen(2)
    while 1:
        clientsocket, clientaddr = serversocket.accept()
        socketHandler = SocketHandlerServer(clientsocket)
        newClient = Client(socketHandler, clientaddr, data)
        newClient.setDaemon(True)
        newClient.start()
        data.addPlayer(newClient)
    serversocket.close()

if __name__ == "__main__":
    main()
