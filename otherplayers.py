

class NetworkHero(object):
    def __init__(self):
        self.gfx = HeroGraphics("female.png", "down")
        self.pos = Position(0,0)
        self.castedSpells = []
    def translate(self, x, y):
        self._setAnimation(x,y)
        self.pos.x += x
        self.pos.y += y
        self.pixelPerFrame = 4
        self.pixelMoveCount = 0
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
            self.pixelMoveCount += 1
            self.gfx.incrementFrame()
