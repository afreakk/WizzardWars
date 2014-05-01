def fillCommand(command):
    return "|"+command+"|"
class Commands(object):
    join = "|J|"
    leave = "|L|"
    chat = "|C|"
    nick = "|N|"

class HXeption(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def unifyData(data):
    assert "/" not in data
    return str(data)+"/"

def unifyID(id):
    assert "!" not in id
    return "!"+str(id)+"!"

PCK_DELI = "/"

class SocketHandler(object):
    def __init__(self, sock):
        self.buffer = ""
        self.sock = sock

    def read(self):
        stream = self.sock.recv(1024)
        if len(stream) > 0:
            self.buffer += stream
            if PCK_DELI in stream:
                packetCount = self.buffer.count(PCK_DELI)
                totalPackets = []
                for x in xrange(packetCount):
                    packet, self.buffer = self.buffer.split(PCK_DELI, 1)
                    totalPackets.append(packet)
                return totalPackets
        else:
            print "Disconnected"
            raise HXeption("Disconnected")
        return None

    def close(self):
        self.sock.close()

class SocketHandlerServer(SocketHandler):
    def __init__(self, sock):
        SocketHandler.__init__(self,sock)

    def transmitMessage(self, sender, data):
        data = unifyData(data)
        sender = unifyID(sender)
        packet = sender+data
        print "sending data: |"+packet+"|"
        self.sock.send(packet)

class SocketHandlerClient(SocketHandler):
    def __init__(self, sock, nick):
        SocketHandler.__init__(self, sock)
        self.nick = nick
        self.registerNick(self.nick)

    def writeToChat(self, data):
        data = unifyData(data)
        self.sock.send(Commands.chat+data)

    def registerNick(self, nick):
        nick = unifyData(nick)
        self.sock.send(Commands.nick+nick)

