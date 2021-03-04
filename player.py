import pygame
from super_simple import Font

class Player:
    def __init__(self,cor):
        self.moving_right = False
        self.moving_left = False
        self.movement = [0,0]
        self.vertical_momentum = 0
        self.air_timer = 0
        self.cor = cor
        self.animation_frames = {}
        self.animation_database = {}
        self.action = 'idle'
        self.frame = 0
        self.flip = False
        self.animation_database['run'] = self.load_animation('player_animation/run',[6,6,6,6,6,6])
        self.animation_database['idle'] = self.load_animation('player_animation/idle',[10,10,10,10])
        self.image = self.animation_frames['idle_0']
        self.rect = pygame.Rect(self.cor[0],self.cor[1],self.image.get_width(),self.image.get_height())
        self.inventory = Inventory(['4_platform','5_dad'])
        self.my_font = Font('small_font.png')


    def load_animation(self, path, frame_durations):
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            animation_frame_id = animation_name + '_' + str(n)
            img_loc = path + '/' +animation_frame_id + '.png'
            animation_image = pygame.image.load(img_loc).convert()
            animation_image.set_colorkey((255,255,255))
            self.animation_frames[animation_frame_id] = animation_image.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        return animation_frame_data

    def change_action(self, action_var,frame,new_value):
        if(action_var != new_value):
            action_var = new_value
            frame = 0
        return action_var, frame
    
    def update_animation(self):
        self.frame += 1
        self.frame = self.frame % len(self.animation_database[self.action])
        img_id = self.animation_database[self.action][self.frame]
        self.image = self.animation_frames[img_id]

    def update_movement(self):
        #   ===x_movement===
        self.movement = [0,0]
        if self.moving_right:
            self.movement[0] += 2
        if self.moving_left:
            self.movement[0] -= 2
        
        #   ===gravity===
        self.movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.2
        if(self.vertical_momentum > 3):
            self.vertical_momentum = 3

        if(self.movement[0] > 0): #moving right
            self.action,self.frame = self.change_action(self.action,self.frame,'run')
            self.flip = False
        if(self.movement[0] == 0): #standing
            self.action,self.frame = self.change_action(self.action,self.frame,'idle')
        if(self.movement[0] < 0): #moving left
            self.action,self.frame = self.change_action(self.action,self.frame,'run')
            self.flip = True

    def draw_inventory(self, display):
        for i,name in enumerate(self.inventory.stored):
            compact = pygame.transform.scale(self.inventory.elements[name][1],(8,8))
            display.blit(compact,(display.get_width() - (len(self.inventory.stored) - i)*(compact.get_width()*1.5),10))
            self.my_font.render(display, str(i),(display.get_width() - (len(self.inventory.stored) - i)*(compact.get_width()*1.5),3),8)

class Inventory:
    def __init__(self,e_names):
        self.max_slots = 4
        self.elements = {}
        for name in e_names:
            self.elements[name] = (name[0],pygame.image.load('game_map/tiles/'+name+'.png'))
        self.stored = [] #  ['4_platform',4_platform','heal']

    def add(self, e_name):
        if(len(self.stored) < self.max_slots):
            self.stored.append(e_name)
            return True
        return False

    def use(self, index):
        if(index < len(self.stored)):
            return self.elements[self.stored.pop(index)][0]
        return '-1'
    def collect_item(self,c):
        for e in self.elements:
            if(self.elements[e][0] == c):
                return self.add(e)
        return False