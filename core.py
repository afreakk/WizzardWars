import pygame
import os, sys
from gameloop import LevelManager
width, height = 1152 , 648
screen = pygame.display.set_mode((width, height))
os.environ['SDL_VIDEO_CENTERED'] = '1'
def startCore():
    main = Core(screen, 'Node')
    main.run()

class Core(object):
    def __init__(self, surface, name):
        pygame.init()
        pygame.display.set_caption(name)
        self.screen = surface
        self.lvlMgr = LevelManager()

    def dispatch(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    def run(self):
        while True:
            for event in pygame.event.get():
                self.dispatch(event)
            self.screen.fill([0xFF, 0xFF, 0xFF])
            self.lvlMgr.update(self.screen)
            pygame.display.flip()
