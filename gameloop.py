from hero import Hero
from controller import ControlHero
from chatwindow import ChatWindow
from cnetwork import Connection
import pygame

class Arena(object):
    def __init__(self):
        self.thisPlayer = Hero()
        self.spriteList = pygame.sprite.Group()
        self.spriteList.add(self.thisPlayer.gfx)
        self.chatWindow = ChatWindow()
        self.connection = Connection(('localhost', 1337), "afreak", self.chatWindow)
    def update(self, screen):
        self.connection.update(self.chatWindow)
        ControlHero(self.thisPlayer, 0.1, 10, 10, (255,0,0))
        self.thisPlayer.update()
        self.thisPlayer.updateCastedSpells(0.1, screen)
        self.spriteList.update()
        self.spriteList.draw(screen)
        self.chatWindow.draw(screen)

class LevelManager(object):
    def __init__(self):
        self.lvl = Arena()
    def update(self,screen):
        self.lvl.update(screen)
