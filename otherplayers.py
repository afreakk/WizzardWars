import pygame
import pygame.gfxdraw


def drawNetworkHero(heroPos, heroGFX, heroFrame, heroCurrentAnim, spellsPos, screen, spellRadius, spellColor):
    heroCurrentGFX = heroGFX[heroCurrentAnim][heroFrame]
    typle = (heroPos[0], heroPos[1])
    try:
        screen.blit(heroCurrentGFX, typle)
    except Exception as e:
        print e
        print typle
    for spellPos in spellsPos:
        pygame.gfxdraw.aaellipse(screen, spellPos[0], spellPos[1], spellRadius, spellRadius, spellColor)

