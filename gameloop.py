from hero import Hero
from controller import ControlHero
from chatwindow import ChatLog
from cnetwork import Connection, PacketHandler
from otherplayers import OtherPlayersContainer
from heroanimspecifics import getAnimationsHero
import pygame

class Arena(object):
    def __init__(self):
        self.otherPlayers = OtherPlayersContainer()
        self.chatLog = ChatLog()
        self.connection = Connection(('localhost', 1337), "afreak")
        self.packetHandler = PacketHandler(self.otherPlayers, self.chatLog)
        self.thisPlayer = Hero(self.connection)
        self.spriteList = pygame.sprite.Group()
        self.spriteList.add(self.thisPlayer.gfx)
        self.heroImage = pygame.image.load("female.png").convert()
        self.heroGFX = getAnimationsHero(self.heroImage)


    def update(self, screen):
        packets = self.connection.getPackets()
        self.packetHandler.handlePackets(packets)
        ControlHero(self.thisPlayer, 0.1, 10, 10, (255,0,0))
        self.thisPlayer.update()
        self.thisPlayer.updateCastedSpells(0.1, screen)
        self.spriteList.update()
        self.spriteList.draw(screen)
        self.otherPlayers.drawPlayers(self.heroGFX, screen)
        self.chatLog.render(screen)

class LevelManager(object):
    def __init__(self):
        self.lvl = Arena()
    def update(self,screen):
        self.lvl.update(screen)
