import pygame, sys, csv # import pygame and sys
from Player import Player
from tiles import *
from load_map import load_map
clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
# from pygame_functions import *
import os, random
pygame.init() # initiate pygame

pygame.display.set_caption('The Fourth Friend') # set the window name
favicon = pygame.image.load("logo.png")
pygame.display.set_icon(favicon)
WINDOW_SIZE = (600,400) # set up window size

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode(WINDOW_SIZE, RESIZABLE) # initiate screen

#images
player_run = [pygame.image.load("player_animations/run/run_0.png"),pygame.image.load("player_animations/run/run_1.png"),pygame.image.load("player_animations/run/run_2.png")]
player_idle = [pygame.image.load("player_animations/idle/idle_2.png"), pygame.image.load("player_animations/idle/idle_1.png"),pygame.image.load("player_animations/idle/idle_2.png")]
grass_image = pygame.image.load("imgs/grass.png")
TILE_SIZE = 32
dirt_image = pygame.image.load("imgs/dirt.png")
stone_image = pygame.image.load("imgs/stone_2.png")
stone_image_2 = pygame.image.load("imgs/stone_3.png")
coin = pygame.image.load("imgs/coin.png")
sword = pygame.image.load("imgs/sword.png")
#images

global animation_frames
animation_frames = {}

# functions

def load_animations(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc)
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

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


# functions


# variables
animation_database = {}
animation_database['run'] = load_animations("player_animations/run", [7,7,7])
animation_database['idle'] = load_animations("player_animations/idle", [7, 7, 40])
player_rect = pygame.Rect(50, 50, 32, 32)
player = Player(50, 50)
game_map = load_map('level1')
true_scroll = [0, 0]
fullscreen = False
stone_image_opt = stone_image.copy()
stone_image_2_opt = stone_image_2.copy()
# variables

# game
running = True
while running: # game loop
    screen.fill((146,0,255))


    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()

    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                screen.blit(stone_image_2, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '2':
                screen.blit(stone_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
           
            x += 1
        y += 1

# movement
    player_movement = [0, 0]
    if player.right:
        player_movement[0] += 3
    if player.left:
        player_movement[0] -= 3        
    player_movement[1] += player.momentum
    player.momentum += 0.2
    if player.momentum > 3:
        player.momentum = 3

    if player_movement[0] > 0:
        player.action, player.frame = change_action(player.action, player.frame, 'run')
        player.flip = False

    if player_movement[0] == 0:
        player.action, player.frame = change_action(player.action, player.frame, 'idle')

    if player_movement[0] < 0:
        player.action, player.frame = change_action(player.action, player.frame, 'run')
        player.flip = True
        
# movement

    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    


    if collisions['bottom']:
        player.momentum = 0
        player.air_timer = 0
    else:
        player.air_timer += 1

    player.frame += 1
    if player.frame >= len(animation_database[player.action]):
        player.frame = 0
    player_img_id = animation_database[player.action][player.frame]
    player_img = animation_frames[player_img_id]
    screen.blit(pygame.transform.flip(player_img, player.flip, False), (player_rect.x-scroll[0], player_rect.y-scroll[1]))


    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            running = False
            pygame.quit() # stop pygame
            sys.exit() # stop script

        if event.type == VIDEORESIZE:
                if not fullscreen:
                    screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)


        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.right = True
            if event.key == K_LEFT:
                player.left = True

            if event.key == K_UP:
                player.walk_count = 0
                if player.air_timer < 8:
                    player.momentum = -7
            
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((monitor_size), FULLSCREEN)
                    pygame.transform.scale(stone_image_opt, (100, 100))
                    pygame.transform.scale(stone_image_2_opt, (100, 100))
                else:
                    screen = pygame.display.set_mode((monitor_size), RESIZABLE)

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player.right = False
            if event.key == K_LEFT:
                player.left = False
    
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps

# game