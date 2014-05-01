
class Position(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def getIntPos(self):
        return (int(self.x), int(self.y))
