import pygame
from genericUtils import Singleton

class ChatLog(object):
    def __init__(self):
        self.textWindow = ChatWindow()
    def chat(self, nick, msg):
        self.textWindow.appendText(nick+msg)
    def join(self, nick):
        self.textWindow.appendText("join "+nick)
    def part(self, nick):
        self.textWindow.appendText("leave "+nick)
    def rename(self, oldNick, newNick):
        self.textWindow.appendText("rename "+oldNick+"-"+newNick)
    def render(self, screen):
        self.textWindow.draw(screen)

class ChatWindow(object):
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.pos = pygame.Rect(0,200, 0, 0)
        self.textStr = ""
    def draw(self, screen):
        screen.blit(rendertext(self.font, self.textStr), self.pos)
    def appendText(self, text):
        self.textStr += "\n"+text
        print "TOTAL|"+self.textStr+"|"

def rendertext(font, text, pos=(0,0), color=(255,255,255), bg=(0,0,0)):
    lines = text.splitlines()
    width = height = 0
    for l in lines:
        width = max(width, font.size(l)[0])
        height += font.get_linesize()
    img = pygame.Surface((width, height), 0, 8)
    img.set_palette([bg, color])
    height = 0
    for l in lines:
        t = font.render(l, 0, color, bg)
        img.blit(t, (0, height))
        height += font.get_linesize()
    return img
