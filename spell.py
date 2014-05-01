import pygame.gfxdraw
class Spell(object):
    def __init__(self, x, y, rx, ry, direction, color):
        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry
        self.direction = direction
        self.color = color
    def update(self, dt, surface):
        self._updatePosition(dt)
        self._draw(surface)

    def _updatePosition(self, dt):
        self.x += self.direction[0]*dt
        self.y += self.direction[1]*dt
    def _draw(self, surface):
        pygame.gfxdraw.aaellipse(surface, int(self.x),int(self.y), self.rx, self.ry, self.color)
