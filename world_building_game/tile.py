import pygame
import random
from settings import *

class Tile(pygame.sprite.Sprite):                    
    def __init__(self, index, noise, group):
        super().__init__(group)
        self.row_index = index[0]                  # tile index at the time it was created
        self.col_index = index[1]
        self.noise = noise                         # original noise value from map generation
        self.adj_noise, self.tile_type = self.set_tile_type()  # values to store adjusted noise and tile type
        self.tile_image = self.get_image()         # calls function to determine tile image from tile type
        self.tile_image_width = self.tile_image.get_width()    # get tile width
        self.tile_image_height = self.tile_image.get_height()  # get tile height
        self.tile_pos = self.get_xy()              # get tile position on the map
        self.tile_image_rect = self.tile_image.get_rect(topleft = self.tile_pos)  # create rect of image

    def set_tile_type(self): 
        # uses the column and row index values along with the nosie value to 
        # pre-shape the map edges
        value = 0
        type = ""
        # nudge the edge columns towards being ocean tiles.
        if self.col_index == 0 or self.col_index == COLS - 1:
            if self.noise >= OCEAN:
                self.noise -= 0.4
        elif self.col_index <= 1 or self.col_index >= COLS - 2:
            if self.noise >= OCEAN:
                self.noise -= 0.2
        elif self.col_index <= 2 or self.col_index >= COLS - 3:
            if self.noise >= PLAINS:
                self.noise -= 0.1
        elif self.col_index <= 3 or self.col_index >= COLS - 4:
            if self.noise >= PLAINS:
                self.noise -= 0.05
        elif self.col_index <= 4 or self.col_index >= COLS - 5:
            if self.noise >= PLAINS:
                self.noise -= 0.05
        elif self.col_index <= 5 or self.col_index >= COLS - 6:
            if self.noise >= PLAINS:
                self.noise -= 0.05
        # set the border rows to ice and tundra to create "arctic circles" at the poles
        if self.row_index == 0 or self.row_index == ROWS - 1:
            value = ICE
        elif self.row_index == 1 or self.row_index == ROWS - 2:
            if random.randint(1, 5) != 5:
                value = ICE
            elif self.noise >= PLAINS:
                    value = TUNDRA
            else:
                value = self.noise
        elif self.row_index == 2 or self.row_index == ROWS - 3:
            if random.randint(1, 4) != 4:
                value = ICE
            elif self.noise >= PLAINS:
                value = TUNDRA
            else:
                value = self.noise
        elif self.row_index == 3 or self.row_index == ROWS - 4:
            if self.noise >= PLAINS:
                value = TUNDRA
            else:
                value = self.noise
        elif self.row_index == 4 or self.row_index == ROWS - 5:
            if self.noise >= PLAINS:
                if random.randint(1, 5) != 5:
                    value = TUNDRA
                else:
                    value = self.noise
            else:
                value = self.noise
        elif self.row_index == 5 or self.row_index == ROWS -6:
            if self.noise >= PLAINS:
                if random.randint(1, 2) == 2:
                    value = TUNDRA
                else:
                    value = self.noise
            else:
                value = self.noise
        else:
            value = self.noise
        # uses the noise values set above to set the tile type
        if value == ICE:
            type = "ice"
        elif value == TUNDRA:
            type = "tundra"
        elif value >= H_MOUNTAIN:
            type = "high_mountain"
        elif value >= MOUNTAIN:
            type = "mountain"
        elif value >= HILLS:
            type = "hills"
        elif value >= PLAINS:
            type = "plains"
        elif value >= OCEAN:
            type = "ocean"
        else:
            type = "deep_ocean"
        return value, type

    def get_xy(self):
        # uses the col and row index values to determine the map x and y positions
        x = self.col_index * self.tile_image_width
        if self.row_index % 2 != 0:                      # on odd numbered rows
            x += self.tile_image_width // 2              # move a half tile over to fit in with above and below tiles
        y = self.row_index * int(self.tile_image_height * 0.75)  # move 75% of a tile down for next row
        return(x, y)

    def get_image(self):
        # uses tile type to set the tile image to draw to the map
        if self.tile_type == "ice":
            image = pygame.image.load('.\\tiles\\ice.png').convert_alpha()
        elif self.tile_type == "tundra":
            image = pygame.image.load('.\\tiles\\tundra.png').convert_alpha()
        elif self.tile_type == "high_mountain":
            image = pygame.image.load('.\\tiles\\high_mountain.png').convert_alpha()
        elif self.tile_type == "mountain":
            image = pygame.image.load('.\\tiles\\mountans.png').convert_alpha()
        elif self.tile_type == "hills":
            image = pygame.image.load('.\\tiles\\hills.png').convert_alpha()
        elif self.tile_type == "plains":
            image = pygame.image.load('.\\tiles\\plains.png').convert_alpha()
        elif self.tile_type == "ocean":
            image = pygame.image.load('.\\tiles\\water.png').convert_alpha()
        elif self.tile_type == "deep_ocean":
            image = pygame.image.load('.\\tiles\\deep_water.png').convert_alpha()
        return image