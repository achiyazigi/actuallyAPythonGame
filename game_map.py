import pygame
from PIL import Image
import os, os.path

def load_background(path, background_objects):
    images = []
    for obj in background_objects:
        im=pygame.image.load(path+'/'+obj[-1]+'.png').convert()
        im.set_colorkey((255,255,255))
        images.append([obj,im])
    return images

def load_tiles_images(path):
    res = [None]+[pygame.image.load(path+'/'+img).convert() for img in os.listdir(path)]
    res[3].set_colorkey((255,255,255))
    return res

class Game_map:
    def __init__(self, path, background_objects, foreground_objects):
        # self.background_objects = background_objects
        # self.foreground_objects = foreground_objects
        self.path = path
        self.raw_map = self.load_map(path+'/map.txt')
        self.tiles = []
        self.tiles_images = load_tiles_images(path+'/tiles')
        self.background = load_background(path+'/background',background_objects)
        self.foreground = load_background(path+'/foreground', foreground_objects)

    def add_background(self, obj):
        im=pygame.image.load(self.path+'/background/'+obj[-1]+'.png').convert()
        im.set_colorkey((255,255,255))
        self.background.append([obj,im])

    def load_map(self, path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))
        return game_map
   
    def draw_tiles(self,collectable, elements, locked_doors,scroll,display):
        self.tiles = []
        y = 0
        for layer in self.raw_map:
            x = 0
            for tile in layer:
                to_render = self.tiles_images[int(tile)]
                if(tile == '3'):
                    locked_doors[(x,y)] = pygame.Rect(x * 16 - 1, y * 16 - to_render.get_height() + 16, to_render.get_width() + 2, to_render.get_height())
                for e in elements:
                    if(tile == elements[e][0]):
                        collectable[(x,y)] = pygame.Rect(x * 16 - 1, y * 16 - to_render.get_height() + 16, to_render.get_width() + 2, to_render.get_height())
                if(tile != '0'):
                    display.blit(to_render, (x * 16 - scroll[0], y * 16 - to_render.get_height() + 16 - scroll[1]))
                    self.tiles.append(pygame.Rect(x * 16, y * 16 - to_render.get_height() + 16, to_render.get_width(), to_render.get_height()))
                x += 1
            y += 1
    
    def draw_background(self,scroll,display):
        for img in self.background:
            display.blit(img[1], ((img[0][1]-scroll[0]) * img[0][0], (img[0][2]-scroll[1]) * img[0][0]))
    def draw_foreground(self,scroll,display):
        for img in self.foreground:
            display.blit(img[1], ((img[0][1]-scroll[0]) * img[0][0], (img[0][2]-scroll[1]) * img[0][0]))
