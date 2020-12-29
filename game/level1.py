import pygame, sys # import pygame and sys

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
import os
pygame.init() # initiate pygame

pygame.display.set_caption('Pygame Window') # set the window name

WINDOW_SIZE = (600,400) # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

display = pygame.Surface((300, 200))

#images
player_image = pygame.image.load("player_animations/idle/idle_0.png")
grass_image = pygame.image.load("imgs/grass.png")
TILE_SIZE = grass_image.get_width()
dirt_image = pygame.image.load("imgs/dirt.png")
stone_image = pygame.image.load("imgs/stone_2.png")
stone_image_2 = pygame.image.load("imgs/stone_3.png")
#images

# functions

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))

    return game_map

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

class Inherit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = None
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

class Player(Inherit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = player_image
        self.mask = pygame.mask.from_surface(self.img)
        self.right = False
        self.left = False
        self.momentum = 0
        self.air_timer = 0
        self.walkCount = 0
        self.flip = False


# variables
moving_right = False
moving_left = False
player_y_momentum = 0
air_timer = 0
player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)
player = Player(50, 50)
game_map = load_map('map1')
true_scroll = [0, 0]
# variables

while True: # game loop
    display.fill((146,244,255))

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
                display.blit(stone_image_2, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '2':
                display.blit(stone_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

# movement
    player_movement = [0, 0]
    if player.right:
        player_movement[0] += 2
    if player.left:
        player_movement[0] -= 2
    player_movement[1] += player.momentum
    player.momentum += 0.2
    if player.momentum > 3:
        player.momentum = 3
# movement

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player.momentum = 0
        player.air_timer = 0
    else:
        player.air_timer += 1

    display.blit(player_image, (player_rect.x-scroll[0], player_rect.y-scroll[1]))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.right = True
            if event.key == K_LEFT:
                player.left = True
            if event.key == K_UP:
                if player.air_timer < 6:
                    player.momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player.right = False
            if event.key == K_LEFT:
                player.left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps