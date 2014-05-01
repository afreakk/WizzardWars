import pygame

class ChatWindow(object):
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.pos = pygame.Rect(300,200, 0, 0)
        self.textStr = ""
    def draw(self, screen):
        screen.blit(rendertext(self.font, self.textStr), self.pos)
    def appendText(self, text):
        self.textStr += "\n"+text



def rendertext(font, text, pos=(0,0), color=(255,255,255), bg=(0,0,0)):
    lines = text.splitlines()
#first we need to find image size...
    width = height = 0
    for l in lines:
        width = max(width, font.size(l)[0])
        height += font.get_linesize()
#create 8bit image for non-aa text..
    img = pygame.Surface((width, height), 0, 8)
    img.set_palette([bg, color])
#render each line
    height = 0
    for l in lines:
        t = font.render(l, 0, color, bg)
        img.blit(t, (0, height))
        height += font.get_linesize()
    return img
