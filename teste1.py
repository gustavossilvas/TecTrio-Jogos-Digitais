#code made by 

import pygame, sys, os, time

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

pygame.display.set_caption('Crisis Scape')

window_size = (900,600)

screen = pygame.display.set_mode(window_size,0,32)

display = pygame.Surface((450,300))

#PLAYER
player_image = pygame.image.load('character_malePerson_wide.png')
player_image_transf = pygame.transform.scale(player_image,[40,60])
player_image_transf.set_colorkey((0,0,0))

#MAPA E IMAGENS
lateralesq = pygame.transform.scale(pygame.image.load('lateralesq.png'),[25,25])
lateraldir = pygame.transform.scale(pygame.image.load('lateraldir.png'),[25,25])
meio = pygame.transform.scale(pygame.image.load('meio.png'),[25,25])
meio1 = pygame.transform.scale(pygame.image.load('meio1.png'),[25,25])
meio2 = pygame.transform.scale(pygame.image.load('meio2.png'),[25,25])
portacima = pygame.transform.scale(pygame.image.load('portacima.png'),[25,25])
porta = pygame.transform.scale(pygame.image.load('porta.png'),[25,25])
inferiordir = pygame.transform.scale(pygame.image.load('inferiordir.png'),[25,25])
inferioresq = pygame.transform.scale(pygame.image.load('inferioresq.png'),[25,25])
inferiormeio = pygame.transform.scale(pygame.image.load('inferiormeio.png'),[25,25])
moeda = pygame.transform.scale(pygame.image.load('coin_0.png'),[15,15])
heart = pygame.transform.scale(pygame.image.load('heart1.png'), [20,20])



#SONS
jump_sound = pygame.mixer.Sound('jump.wav')
walk_sound = pygame.mixer.Sound('jumpconcrete1.wav')
coin_sound = pygame.mixer.Sound('coin.wav')
die_sound = pygame.mixer.Sound('die.mp3')
lose_sound = pygame.mixer.Sound('lose.mp3')
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)
jump_sound.set_volume(0.4)
coin_sound.set_volume(0.5)
die_sound.set_volume(0.8)

#Variaveis
moving_right = False
moving_left = False
running_right = False 
running_left = False
player_y_momentum = 0
air_timer = 0
tile_size = lateralesq.get_width()
coin_size = moeda.get_width() + 10
true_scroll = [0,0]
concrete_sound_timer = 0
points = 0
life = 3 
font = pygame.font.Font('8-BitMadness.ttf', 13)


def load_map(path):
    file = open(path + '.txt', 'r')
    data = file.read()
    file.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('map')

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list
def collision_coin(rect,coins):
    points =0
    collect_list = []
    for coin in coins:
        coin_rect = pygame.Rect((coin[0],coin[1],coin_size,coin_size))
        if rect.colliderect(coin_rect):
            collect_list.append(coin)
            coin_list.remove(coin)
            coin_sound.play()
            points+=1
        display.blit(moeda,(coin[0] - scroll[0], coin[1] - scroll[1]))
    return points

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
            
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True    
    
    return rect, collision_types

global animation_frames
animation_frames= {}



def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image_transf = pygame.transform.scale(animation_image,[40,60])
        animation_image_transf.set_colorkey((0,0,0))
        animation_frames[animation_frame_id] = animation_image_transf.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n+=1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame=0
    return action_var,frame

animation_database = {}

animation_database['walk'] = load_animation('player_animations/walk',[7,7,7,7,7,7,7,7])
animation_database['jump'] = load_animation('player_animations/jump',[7,7])
animation_database['idle'] = load_animation('player_animations/idle',[7,7,40])
animation_database['fall'] = load_animation('player_animations/fall',[7,7])

player_action = 'idle'
player_frame = 0
player_flip = False
u=0
coin_list = []
for line in game_map:
    o=0
    for coin in line:
        if coin == 'd':
            coin_list.append([o*coin_size,u*coin_size])
        o+=1
    u+=1

    

player_rect = pygame.Rect(50,50, player_image_transf.get_width(), player_image_transf.get_height())
background = pygame.image.load('cidade2.jpeg')
bg_transf = pygame.transform.scale(background,[450,300])

while True:
    display.fill((146,244,255))

    if concrete_sound_timer > 0:
        concrete_sound_timer -= 1
    true_scroll[0] += (player_rect.x-true_scroll[0] - 130)/20
    true_scroll[1] += (player_rect.y-true_scroll[1] - 150)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    tile_rects = []
    y=0
    

    
    
    display.blit(bg_transf,(0,0))

               
    for row in game_map:
        x=0
        for tile in row:
            if tile =='1':
                display.blit(meio,(x * tile_size - scroll[0], y * tile_size - scroll[1]))
                

            if tile == '2':
                display.blit(meio1,(x * tile_size - scroll[0], y * tile_size - scroll[1]))

            if tile == '3':
                display.blit(meio2,(x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == '4':
                display.blit(lateralesq,(x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == '5':
                display.blit(pygame.transform.flip(lateralesq,True,False),(x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == '6':
                display.blit(portacima,(x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == '7':
                display.blit(porta,(x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == '8':
                display.blit(pygame.transform.flip(inferiormeio,False,True),(x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == '9':
                display.blit(pygame.transform.flip(inferioresq,False,True),(x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == 'a':
                display.blit(pygame.transform.flip(inferiordir,False,True),(x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == 'b':
                display.blit(inferiormeio,(x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == 'c':
                display.blit(inferioresq,(x * tile_size - scroll[0], y * tile_size - scroll[1]))


            if tile != '0' and tile != 'd':
                tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            x+=1
            
            
        y+=1
            
    
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    if player_movement[0] > 0:
        player_action,player_frame = change_action(player_action,player_frame,'walk')
        player_flip = False

    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
        player_flip = False
    
    if player_movement[0] < 0:
        player_action,player_frame = change_action(player_action,player_frame,'walk')
        player_flip = True
    
    if player_movement[1] < 3 and player_movement[0] > 0:
        player_action,player_frame = change_action(player_action,player_frame,'jump')
        player_flip = False
        
    if player_rect.y > 90 and (player_rect.x > 1740 or player_rect.x < 0):
        player_action,player_frame = change_action(player_action,player_frame,'fall')
        player_flip = True

    if  player_rect.y > 300 and (player_rect.x > 1740 or player_rect.x < 0):
        pygame.mixer.music.pause()
        die_sound.play()
        time.sleep(4)
        player_rect.x = 50
        player_rect.y = 30
        pygame.mixer.music.unpause()
        life -=1

        
    if life <0:
        pygame.mixer.music.pause()
        lose_sound.play()
        time.sleep(25)
        
        #mudar tela para mostrar a pontuação
        
    points += collision_coin(player_rect,coin_list)
    player_rect,collisions = move(player_rect, player_movement, tile_rects)
    
    
    
    if collisions['bottom']:
        player_momentum = 0
        air_timer = 0
        if player_movement[0] != 0:
            if concrete_sound_timer == 0:
                concrete_sound_timer = 30
                walk_sound.play()
        
            
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_image_transf  = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_image_transf,player_flip,False),(player_rect.x - scroll[0],player_rect.y - scroll[1]))

     #points
    score_text = font.render('PONTUACAO:  ' + str(points),False,(255,255,255))
    score_rect = score_text.get_rect()
    score_rect.topleft = (10,10)
    display.blit(score_text,score_rect)

    #lifes
    life_text = font.render('VIDAS:  ',False,(255,255,255))
    life_rect = life_text.get_rect()
    life_rect.topleft = (10,25)
    heart_size = heart.get_width()
    display.blit(life_text,life_rect)
    
    for l in range(life):
        display.blit(heart, (45+(l*15),20))
        
    
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_s:
                pygame.mixer.music.pause()
            if event.key == K_p:
                pygame.mixer.music.unpause()
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
                    player_y_momentum = -6
                    
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display,window_size)
    screen.blit(surf, (0,0))
    pygame.display.update()
    clock.tick(60)
