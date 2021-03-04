import pygame
import os, os.path

class Character:

    def __init__(self,path):
        self.name = path
        self.animation_frames = {}
        self.animation_database = self.load_animation()
        self.frame = 0
        # self.flip = False
        # self.image = self.update_animation()


    def load_animation(self):
        path = self.name
        animation_frame_data = []
        for img in os.listdir(path):
            fd = float(img.partition('-')[2][:-5])*60 # removing the 's.png' at the end, gettin only frame duration
            animation_image = pygame.image.load(path+'/'+img).convert()
            if('background' not in path):
                animation_image.set_colorkey(animation_image.get_at((0,0)))
            self.animation_frames[img] = animation_image.copy()
            for i in range(int(fd)):
                animation_frame_data.append(img)
        return animation_frame_data

    
    def update_animation(self):
        self.frame += 1
        self.frame = self.frame % len(self.animation_database)
        img_id = self.animation_database[self.frame]
        return self.animation_frames[img_id]