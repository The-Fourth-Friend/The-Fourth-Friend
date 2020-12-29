import pygame, os, csv

class Tile(pygame.sprite.Sprite):
    def __init__(self, x,image, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.img = spritesheet.parse_sprite(image)
        self.rect = self.img.get_rect()
        self.rectx, self.rect.y = x, y
 
    def draw(self, window):
        window.blit(self.img, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self,surface):
        surface.blit(self.map_surface, (0,0))

    
    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)


    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))

        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '1':
                    tiles.append(Tile('stone_2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size

        return tiles