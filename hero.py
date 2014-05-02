import pygame
from heroanimspecifics import getAnimationsHero
from vec2 import Position
from spell import Spell

def vecFromDirection(direction):
    if direction == "left":
        return (-1,0)
    elif direction == "right":
        return (1,0)
    elif direction == "up":
        return (0,-1)
    elif direction == "down":
        return (0,1)

class Hero(object):
    def __init__(self, connection):
        self.gfx = HeroGraphics("female.png", "down")
        self.pos = Position(0,0)
        self.castedSpells = []
        self.connection = connection
    def translate(self, x, y):
        self._setAnimation(x,y)
        self.pos.x += x
        self.pos.y += y
    def castSpell(self, rx, ry, color):
        direction = vecFromDirection( self.getDirection() )
        x,y = (self.pos.x+self.gfx.rect.width/2, self.pos.y+self.gfx.rect.height/2)
        self.castedSpells.append(Spell(x, y, rx, ry, direction, color))
    def updateCastedSpells(self, dt, surface):
        for spell in self.castedSpells:
            spell.update(dt, surface)
    def update(self):
        intPos = self.pos.getIntPos()
        self._animate(intPos)
        self.gfx.rect.x, self.gfx.rect.y = intPos
    def getDirection(self):
        return self.gfx.currentAnim
    def _setAnimation(self, x, y):
        if x != 0:
            if x < 0:
                self.gfx.currentAnim = "left"
            else:
                self.gfx.currentAnim = "right"
        elif y != 0:
            if y < 0:
                self.gfx.currentAnim = "up"
            else:
                self.gfx.currentAnim = "down"

    def _animate(self, intPos):
        if ( self.gfx.rect.x, self.gfx.rect.y ) != intPos:
            self.connection.sendPos(intPos)
            self.gfx.incrementFrame()

class HeroGraphics(pygame.sprite.Sprite):
    def __init__(self, filename, currentAnim):
        pygame.sprite.Sprite.__init__(self)
        fullImage = pygame.image.load(filename).convert()

        self.imageIndex = 0
        self.currentAnim = currentAnim
        self.animations = getAnimationsHero(fullImage)
        self.image = self.animations[self.currentAnim][self.imageIndex]
        self.rect = self.image.get_rect()

    def incrementFrame(self):
        if self.imageIndex < len(self.animations[self.currentAnim]) - 1:
            self.imageIndex += 1
        else:
            self.imageIndex = 0

    def update(self):
        self.image = self.animations[self.currentAnim][self.imageIndex]

