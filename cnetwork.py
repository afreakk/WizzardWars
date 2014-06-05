from network.protocol import HXeption, SocketHandlerClient, Commands, fillCommand
from chatwindow import ChatLog
import socket



class PacketHandler(object):
    def __init__(self, otherPlayers, chatLog):
        self.otherPlayers = otherPlayers
        self.chatLog = chatLog
    def handlePackets(self, packets):
        if packets:
            for packet in packets:
                self._handlePacket(packet)
    def _handlePacket(self, packet):
        print "packet |"+packet+"|"
        nick, command, data = packet.split("|",2)
        nick = nick.split("!")[1]
        command = fillCommand(command)

        if command == Commands.join:
            self.otherPlayers.addPlayer(nick)
            self.chatLog.join(nick)
        elif command == Commands.leave:
            self.otherPlayers.removePlayer(nick)
            self.chatLog.part(nick)
        elif command == Commands.chat:
            self.chatLog.chat(nick, data)
        else:
            player = self.otherPlayers.getPlayer(nick)
            if player == None:
                print "ERROR", nick , "is not in DB as a player"
            if command == Commands.nick:
                player.rename(data)
            elif command == Commands.setPos:
                player.setPos(self.socketHandler.parsePos(data))
            elif command == Commands.setFrame:
                player.setFrame(self.socketHandler.parseFrame(data))
            elif command == Commands.setAnim:
                player.setAnim(self.socketHandler.parseAnim(data))
            else:
                print "unkown command: ", command

class Connection(object):
    def __init__(self, addr, nick):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(addr)
        clientsocket.setblocking(0)
        self.socketHandler = SocketHandlerClient(clientsocket, nick)

    def getPackets(self):
        try:
            packets = self.socketHandler.read()
        except socket.error:
            return None
        if packets:
            return packets
        return None

    def sendPos(self, pos):
        self.socketHandler.sendPos(pos)
    def sendFrame(self, frame):
        self.socketHandler.sendFrame(frame)
    def sendAnim(self, anim):
        self.socketHandler.sendAnim(anim)
