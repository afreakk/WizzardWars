from network.protocol import HXeption, SocketHandlerClient, Commands, fillCommand
from otherplayers import drawNetworkHero
import socket

class NetworkPlayer(object):
    def __init__(self, nick):
        self.nick = nick
        self.pos = (0,0)
        self.spells = []
        self.frame = 0
        self.currentAnim = 'down'
    def rename(self, nick):
        self.nick = nick

    def setPos(self, pos):
        print "got new pos: ", pos
        self.pos = pos
    def setFrame(self, frame):
        self.frame = frame
    def setAnim(self, anim):
        self.currentAnim = anim
    def setSpells(self, spells):
        self.spells = []
        for spell in spells:
            self.spells.append(spells)

    def draw(self, heroGFX, screen, spellRadius, spellColor):
        drawNetworkHero(self.pos, heroGFX, self.frame, self.currentAnim, self.spells, screen, spellRadius, spellColor)


class NetworkData(object):
    def __init__(self, log):
        self.players = []
        self.log  = log
    def drawPlayers(self, heroGFX, screen, spellRadius=10, spellColor=(0,255,0)):
        for player in self.players:
            player.draw(heroGFX, screen, spellRadius, spellColor)

    def addPlayer(self, nick):
        newPlayer = NetworkPlayer(nick)
        self.players.append(newPlayer)
        self.log.join(nick)

    def removePlayer(self, nick):
        player = self.getPlayer(nick)
        self.players.remove(player)
        self.log.part(player.nick)

    def addMessage(self, nick, msg):
        self.log.chat(nick, msg)

    def renamePlayer(self, oldNick, newNick):
        try:
            player = self.getPlayer(oldNick)
            player.rename(newNick)
            self.log.rename(oldNick, newNick)
        except AttributeError as e:
            print e, "[rename]nick error:", oldNick, newNick

    def setPos(self, nick, pos):
        try:
            player = self.getPlayer(nick)
            player.setPos(pos)
        except AttributeError as e:
            print e, "[setPos]nick error:", nick
    def setFrame(self, nick, frame):
        player = self.getPlayer(nick)
        player.setFrame(frame)
    def setAnim(self, nick, anim):
        player = self.getPlayer(nick)
        player.setAnim(anim)
    def setSpells(self, nick, spells):
        player = self.getPlayer(nick)
        player.setSpells(spells)

    def getPlayer(self, nick):
        for player in self.players:
            if player.nick == nick:
                return player
        return None



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
    def __init__(self, addr, nick, networkData):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(addr)
        clientsocket.setblocking(0)
        self.socketHandler = SocketHandlerClient(clientsocket, nick)
        self.networkData = networkData

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

        elif command == Commands.setPos:
            self.networkData.setPos(nick, self.socketHandler.parsePos(data))
        elif command == Commands.setFrame:
            self.networkData.setFrame(nick, self.socketHandler.parseFrame(data))
        elif command == Commands.setAnim:
            self.networkData.setAnim(nick, self.socketHandler.parseAnim(data))
        else:
            print "unkown command: ", command

    def sendPos(self, pos):
        self.socketHandler.sendPos(pos)
    def sendFrame(self, frame):
        self.socketHandler.sendFrame(frame)
    def sendAnim(self, anim):
        self.socketHandler.sendAnim(anim)
