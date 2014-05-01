from spritetools import splitImage

def getFramePosHero():
    width, height = 32, 48
    frames = []
    for y in xrange(4):
        frames.append([])
        for x in xrange(4):
            frames[y].append((x*width,y*height,width,height))
    return frames

def getAnimationsHero(fullImage):
    colorkey = (255,255,255)
    rects = getFramePosHero()
    animations = {}
    animations['down'] = splitImage(fullImage, rects[0], colorkey);
    animations['left'] = splitImage(fullImage, rects[1], colorkey);
    animations['right']= splitImage(fullImage, rects[2], colorkey);
    animations['up'] = splitImage(fullImage, rects[3], colorkey);
    return animations
