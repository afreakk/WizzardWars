import pygame
import pygame.gfxdraw


class OtherPlayersContainer(object):
    def __init__(self):
        self.players = []
    def drawPlayers(self, heroGFX, screen, spellRadius=10, spellColor=(0,255,0)):
        for player in self.players:
            player.draw(heroGFX, screen, spellRadius, spellColor)

    def addPlayer(self, nick):
        newPlayer = NetworkPlayer(nick)
        self.players.append(newPlayer)

    def removePlayer(self, nick):
        player = self.getPlayer(nick)
        self.players.remove(player)

    def getPlayer(self, nick):
        for player in self.players:
            if player.nick == nick:
                return player
        return None

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


# class for drawing of other players
class NetworkPlayer(object):
    def __init__(self, nick):
        self.nick = nick
        self.pos = (0,0)
        self.spells = []
        self.frame = 0
        self.currentAnim = 'down'
    def rename(self, nick):
        self.nick = nick

    def setPos(self, pos):
        print "got new pos: ", pos
        self.pos = pos
    def setFrame(self, frame):
        self.frame = frame
    def setAnim(self, anim):
        self.currentAnim = anim
    def setSpells(self, spells):
        self.spells = []
        for spell in spells:
            self.spells.append(spells)

    def draw(self, heroGFX, screen, spellRadius, spellColor):
        drawNetworkHero(self.pos, heroGFX, self.frame, self.currentAnim, self.spells, screen, spellRadius, spellColor)
