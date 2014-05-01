import pygame

def imgAt(rectangle, fullImage, colorkey = None):
    "Loads image from x,y,x+offset,y+offset"
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size).convert()
    image.blit(fullImage, (0, 0), rect)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image

def splitImage(fullImage, rects, colorkey = None):
    return [imgAt(rectangle, fullImage, colorkey) for rectangle in rects]

def load_strip(rect, image_count, colorkey = None):
    "Loads a strip of images and returns them as a list"
    tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
            for x in range(image_count)]
    return imgAt(tups, colorkey)
