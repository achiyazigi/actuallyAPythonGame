import pygame, sys, subprocess
from io import StringIO
from super_simple import Font
from player import Player
from game_map import Game_map
from characters import Character
from pygame.locals import *


clock = pygame.time.Clock()


pygame.init()

pygame.display.set_caption('fall')

WINDOW_SIZE = (1200,800)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

display = pygame.Surface((300,200))

def check_events():

    global text, active, color,lines, line,answer
    global current_level
    for event in pygame.event.get():

        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            # print(input_box,event.pos)
            if input_box.collidepoint(event.pos):
                # Toggle the active variable.
                active = not active
            else:
                active = False
            # Change the current color of the input box.
            color = color_active if active else color_inactive
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.moving_right = True
            if event.key == K_LEFT:
                player.moving_left = True
            if event.key == K_UP and player.air_timer < 6:
                player.vertical_momentum = -5
            if active:

                if event.key == pygame.K_F5:
                    #   ===code entered===
                    text.append(line)
                    code = ''.join(text)
                    header = open(f'levels/level_{current_level}/header.txt','r').read()
                    footer = open(f'levels/level_{current_level}/footer.txt','r').read()
                    
                    output = StringIO()
                    sys.stdout = output

                    exec(header)
                    try:
                        exec(code)
                    except:
                        print('didn\'t compile')
                    exec(footer)
                    sys.stdout = sys.__stdout__
                    answer = output.getvalue().strip()
                    output.close()
                    
                    if(answer == levels[current_level]):
                    #   ===level passed!===
                        print('passed level ', current_level)
                        current_level += 1
                    else:
                        #   ===nothing happens just wrong answer appears===
                        print('wrong answer to level ', current_level)
                    #   ===reset text box===
                    text = []
                    line = ''
                    lines = 0
                elif event.key == pygame.K_BACKSPACE:
                    if(len(line) > 0):
                        line = line[:-1]
                    elif(len(text) > 0):
                        line = text.pop()[:-1]
                        lines -= 1

                #   ===new line===
                elif event.key == pygame.K_RETURN:
                    lines += 1
                    text.append(line + event.unicode)
                    line = ''
                else:
                    line += event.unicode
        if(event.type == KEYUP):
            if(event.key == K_RIGHT):
                player.moving_right = False
            if(event.key == K_LEFT):
                player.moving_left = False

def draw_popup(text, font, color, cor, surface):
    for i,row in enumerate(text):
        text_surface = font.render(row, True, color)
        surface.blit(text_surface, (cor[0] * 4, cor[1]*4+i*font.get_linesize()))

def collision_test(rect,tiles):

    hit_list = []
    for tile in tiles:
        if(rect.colliderect(tile)):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles,player):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if(movement[0] > 0):
            rect.right = tile.left
            collision_types['right'] = True
        elif(movement[0] < 0):
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if(movement[1] > 0):
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif(movement[1] < 0):
            rect.top = tile.bottom
            if(player.air_timer > 0):
                player.vertical_momentum
                player.vertical_momentum += (5/player.air_timer)
            collision_types['top'] = True
    return rect,collision_types

def load_background(mult):
    images = []
    for obj in mult:
        im=pygame.image.load('background/'+obj[-1]+'.png').convert()
        im.set_colorkey((255,255,255))
        images.append([obj,im])
    return images

def set_text_box(rect):
    global input_box,lines
    input_box = rect
    # Render the current text.
    txt_surface = font.render(line, True, color)
    # Resize the box if the text is too long.
    max_width = 200
    for row in text:
        temp_size = font.render(row, True, color).get_width()+font_size//3
        if max_width < temp_size:
            max_width = temp_size
    width = max(max_width, txt_surface.get_width()+font_size//3)
    input_box.w = width
    input_box.h = max(font_size,(lines+1) * font_size)
    # Blit the text.

    for i,row in enumerate(text):
        screen.blit(font.render(row, True, color), (input_box.x+5, input_box.y+5 + i * font_size))
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5 + lines * font_size))
    # Blit the input_box rect.
    pygame.draw.rect(screen, color, input_box, 2)
    
def set_output_box(output_text):
    rows = output_text.splitlines()
    txt_surface = font.render(output_text, True, (0,255,0))
    height = max(len(rows) *font_size, font_size)
    width = 200
    for row in rows:
        temp_width = font.render(row, True, (0,255,0)).get_width()+font_size//3
        if(width < temp_width):
            width = temp_width
    output_box = pygame.Rect(10, screen.get_height() - 10 - height, width, height)
    for i, row in enumerate(rows):
        txt_surface = font.render(row, True, (0,255,0))
        screen.blit(txt_surface, (output_box.x+5, output_box.y+5+i*font_size))
    pygame.draw.rect(screen, (0,255,0), output_box, 2)    

def load_levels_text(lst):
    for i in range(len(levels)):
        f = open(f'levels/level_{i}/level_text.txt','r').read()
        lst.append(f.splitlines())
    
def level_flow(popup):
    global been_here
    #   ===level_0===
    while(current_level == 0):
        screen.fill((0,0,0))
    
        # screen.blit(pygame.transform.scale(pirate.update_animation(),(200,200)),(screen.get_width()-220,screen.get_height()-220))
        pirate_image = pirate.update_animation()
        screen.blit(pirate_image,(screen.get_width() - pirate_image.get_width()*0.8, screen.get_height() - pirate_image.get_height()*0.8))

        draw_popup(levels_text[current_level],font,(100,220,140),(10,40), screen)
        check_events()
        set_output_box(answer)
        set_text_box(pygame.Rect(10, 10, 140, font_size))

        pygame.display.update()
        clock.tick(60)
    
    #   ===level 1===
    if(current_level == 1):
        popup[3] = [80*16 - scroll[0], 14*16 - scroll[1]]
    #   ===level 2===
    if(current_level == 2):
        game_map.raw_map[18][98] = '0'
        popup[3] = [106*16 - scroll[0], 11*16 - scroll[1]]
    #   ===level 3===
    if(current_level == 3):
        game_map.raw_map[18][118] = '0'
        popup[3] = [102*16 - scroll[0], 21*16 - scroll[1]]

    #   ===level 4===
    if(current_level == 4):
        game_map.raw_map[26][96] = '0'
        game_map.raw_map[27][96] = '0'
        if(not been_here):
            game_map.raw_map[27][97] = '3'
            been_here = True
        popup[3] = [76*16 - scroll[0], 22*16 - scroll[1]]
    #   ===level 5===
    if(current_level == 5):
        game_map.raw_map[26][70] = '0'
        popup[3] = [58*16 - scroll[0], 22*16 - scroll[1]]
        if(been_here):
            game_map.add_background((1,57*16,26*16,'boxes'))
            been_here = False
    #   ===level 6===
    if(current_level == 6):
        game_map.raw_map[26][56] = '0'

def use(index):
    if('3' != game_map.raw_map[player.rect.y//16][player.rect.x//16]):
        replace = player.inventory.use(index)
        if(replace != '-1'):
            game_map.raw_map[player.rect.y//16][player.rect.x//16] = replace
        else:
            print('No such index:',index) # player entered illegal index
    else:
        print('Cant palce here :(\nTry to unlock the door first') # a door_locked tile in the way!


locked_doors = {}

color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color(48,62,160) # once been 'dodgerblue2'
answer = ''
color = color_inactive
active = False
font_size = 48
input_box = pygame.Rect(0,0,100,font_size)
text = []
line = ''
lines = 0
font = pygame.font.Font(None, font_size)

my_font = Font('small_font.png')
my_big_font = Font('large_font.png')
popup = [[''],font, (255,0,0), (0,0), screen]

# [(mult,x_pos,y_pos,name)]
background_objects = [(0.25,60*16,14 * 16,'mountain'),(0.25,-13*16,14*16,'mountain'),(0.5,4*16,12*16,'poll'),(0.5,39*16,12*16,'poll')]
foreground_objects = [(1.5,10*16,12*16,'poll')]
game_map = Game_map('game_map', background_objects, foreground_objects)

true_scroll = [0,0]

been_here = False

current_level = 0
levels = ['output:\nhello world','passed level 1','passed level 2','coding\nin python\nis cool','passed level 4','passed level 5','unlocked']
levels_text = []
load_levels_text(levels_text)

player = Player([100,100])

pirate = Character('characters/pirate')
# background_animated = Character('characters/background_animated') # not in use yet, maybe for menu?
sky = pygame.image.load('game_map/background/sky.png').convert()

collectable = {}
while True:

    player.update_animation()
    true_scroll[0] += (player.rect.x - true_scroll[0] - display.get_width()//2 - player.image.get_width()//2)/20
    true_scroll[1] += (player.rect.y - true_scroll[1] - display.get_height()//2 - player.image.get_height()//2)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    display.fill((146,244,255)) # refresh
    display.set_colorkey((146,244,255))
    screen.blit(sky,(-4*16-scroll[0] * 0.2,-scroll[1] * 0.2))

    #   ===background draw===
    game_map.draw_background(scroll, display)
    #   ===draw tiles===
    game_map.tiles = []
    
    game_map.draw_tiles(collectable, player.inventory.elements, locked_doors,scroll, display)

    player.update_movement()
 
    player.rect, collisions = move(player.rect,player.movement,game_map.tiles,player)

    #   ===block multiple jumps===
    if(collisions['bottom']):
        player.air_timer = 0
        player.vertical_momentum = 0
    else:
        player.air_timer += 1

    #   ===player animation change===
    display.blit(pygame.transform.flip(player.image,player.flip,False),(player.rect.x - scroll[0], player.rect.y - scroll[1]))

    #   ===foreground draw===
    game_map.draw_foreground(scroll, display)

    level_flow(popup)
    #   ===door interact===
    for key in locked_doors:
        if(player.rect.colliderect(locked_doors[key])):
            temp = current_level
            current_level = len(levels)-1
            door_locked = True
            my_font.render(display,'door_locked = True', [locked_doors[key].x- scroll[0]-25, locked_doors[key].y - scroll[1] - 12],8)

            check_events()
            if(answer == 'unlocked'):
                answer = ''
                game_map.raw_map[key[1]][key[0]] = '0'
                game_map.raw_map[key[1]-1][key[0]] = '0'
                # background_objects += [(1,locked_doors[key].x, locked_doors[key].y,'door')]
                game_map.add_background((1,locked_doors[key].x, locked_doors[key].y,'door'))
                del locked_doors[key]
            current_level = temp
            break

    for key in collectable:
        if(player.rect.colliderect(collectable[key])):
            if(player.inventory.collect_item(game_map.raw_map[key[1]][key[0]])):
                game_map.raw_map[key[1]][key[0]] = '0'
                del collectable[key]
            break
    
    #   ===inventory draw===
    player.draw_inventory(display)

    check_events()
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    set_text_box(pygame.Rect(10, 10, 140, font_size))
    set_output_box(answer)
    popup[0] = levels_text[current_level]

    #   ===level text===
    if(current_level < len(levels)-1):
        draw_popup(popup[0],popup[1],popup[2],popup[3],popup[4])

    #   ===boolean explenation===
    draw_popup(levels_text[-1],font,(40,60,80),[780 - scroll[0], 250 - scroll[1]], screen)

    pygame.display.update()
    #   ===frame rate===
    clock.tick(60)
