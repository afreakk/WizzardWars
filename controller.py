import pygame

def ControlHero(hero, velocity, rx, ry, color):
    key=pygame.key.get_pressed()
    ControlSpell(hero, rx, ry, color)
    if key[pygame.K_w]:
        hero.translate(0,-velocity)
    elif key[pygame.K_s]:
        hero.translate(0,velocity)
    elif key[pygame.K_d]:
        hero.translate(velocity,0)
    elif key[pygame.K_a]:
        hero.translate(-velocity,0)

spaceReleased = True
def ControlSpell(hero, rx, ry, color):
    global spaceReleased
    key=pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        if spaceReleased:
            hero.castSpell(rx, ry, color)
            spaceReleased = False
    else:
        spaceReleased = True
