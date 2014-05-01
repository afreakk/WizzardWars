from network.protocol import HXeption, SocketHandlerClient, Commands, fillCommand
import socket

class NetworkPlayer(object):
    def __init__(self, nick):
        self.nick = nick
    def rename(self, nick):
        self.nick = nick

class NetworkData(object):
    def __init__(self, log):
        self.players = []
        self.log  = log

    def addPlayer(self, nick):
        newPlayer = NetworkPlayer(nick)
        self.players.append(newPlayer)
        self.log.join(nick)

    def removePlayer(self, nick):
        for player in self.players:
            if player.nick == nick:
                self.players.remove(player)
                self.log.part(player.nick)
            else:
                print nick, "did not match", player.nick

    def addMessage(self, nick, msg):
        self.log.chat(nick, msg)
    def renamePlayer(self, oldNick, newNick):
        for player in self.players:
            if player.nick == oldNick:
                player.rename(newNick)
                self.log.rename(oldNick, newNick)



class ChatLog(object):
    def __init__(self, txtlog):
        self.textLog = txtlog
        pass
    def chat(self, nick, msg):
        print nick, msg
        self.textLog.appendText(nick+msg)
        pass
    def join(self, nick):
        print "join", nick
        self.textLog.appendText("join "+nick)
        pass
    def part(self, nick):
        print "leave", nick
        self.textLog.appendText("leave "+nick)
        pass
    def rename(self, oldNick, newNick):
        print "rename", oldNick, newNick
        self.textLog.appendText("rename "+oldNick+"-"+newNick)
        pass

def networkDataFactory(chatWindow):
    log = ChatLog(chatWindow)
    networkData = NetworkData(log)
    return networkData

class Connection(object):
    def __init__(self, addr, nick, chatWindow):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(addr)
        clientsocket.setblocking(0)
        self.socketHandler = SocketHandlerClient(clientsocket, nick)
        self.networkData = networkDataFactory(chatWindow)

    def update(self, chatWindow):
        try:
            packets = self.socketHandler.read()
        except socket.error:
            return
        if packets:
            for packet in packets:
                self._dealWithPacket(packet)

    def _dealWithPacket(self, packet):
        print "packet |"+packet+"|"
        nick, command, data = packet.split("|",2)
        nick = nick.split("!")[1]
        print "this is nick|"+nick+"|"
        command = fillCommand(command)
        if command == Commands.nick:
            self.networkData.renamePlayer(nick, data)
        elif command == Commands.join:
            self.networkData.addPlayer(nick)
        elif command == Commands.leave:
            self.networkData.removePlayer(nick)
        elif command == Commands.chat:
            self.networkData.addMessage(nick, data)

