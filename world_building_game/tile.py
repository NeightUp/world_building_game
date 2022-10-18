import pygame
import math
import random
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, index, pos, group):
        super().__init__(group)
        self.row_index = index[0]
        self.col_index = index[1]
        self.center_x = pos[0]
        self.center_y = pos[1]
        self.tile_rect = pygame.Rect((self.center_x - X_SCALE, self.center_y - HEX_SIZE), (X_SCALE * 2, HEX_SIZE * 2))
        self.vertices = self.create_hex()
        self.tile_type = None
        self.tile_color = None
        self.noise_value = None
        self.climate = None

    def create_hex(self):
        vert_one = (self.center_x + HEX_SIZE * math.cos(math.pi/2), self.center_y + HEX_SIZE * math.sin(math.pi/2))
        vert_two = (self.center_x + HEX_SIZE * math.cos(math.pi/6), self.center_y + HEX_SIZE * math.sin(math.pi/6))
        vert_three = (self.center_x + HEX_SIZE * math.cos(11 * math.pi/6), self.center_y + HEX_SIZE * math.sin(11 * math.pi/6))
        vert_four = (self.center_x + HEX_SIZE * math.cos(3 * math.pi/2), self.center_y + HEX_SIZE * math.sin(3 * math.pi/2))
        vert_five = (self.center_x + HEX_SIZE * math.cos(7 * math.pi/6), self.center_y + HEX_SIZE * math.sin(7 * math.pi/6))
        vert_six = (self.center_x + HEX_SIZE * math.cos(5 * math.pi/6), self.center_y + HEX_SIZE * math.sin(5 * math.pi/6))
        pos_data = [(self.center_x, self.center_y), vert_one, vert_two, vert_three, vert_four, vert_five, vert_six]
        return pos_data

    def set_tile_type_color_noise(self, noise_val):
        self.noise_value = noise_val
        ice = 1
        h_mountain = 0.55
        mountain = 0.35
        hill = 0.15
        plain = 0.01
        ocean = -0.05
        if self.row_index == 0 or self.row_index == ROWS - 1:
            self.noise_value = ice
        elif self.row_index == 1 or self.row_index == ROWS - 2:
            r_number = random.randint(1, 4)
            if self.noise_value >= ocean:
                self.noise_value = ice
            elif r_number != 4:
                self.noise_value = ice
        elif self.row_index == 2 or self.row_index == ROWS - 3:
            r_number = random.randint(1, 3)
            if r_number != 3:
                self.noise_value = ice
            
        elif self.col_index <= 0 or self.col_index >= COLS - 1:
            if self.noise_value >= plain:
                self.noise_value -= 0.5
        elif self.col_index <= 1 or self.col_index >= COLS - 2:
            if self.noise_value >= plain:
                self.noise_value -= 0.25
        elif self.col_index <= 3 or self.col_index >= COLS -4:
            if self.noise_value >= plain:
                self.noise_value -= 0.15
        elif self.col_index <= 5 or self.col_index >= COLS -6:
            if self.noise_value >= plain:
                self.noise_value -= 0.1

        if self.noise_value == ice:
            self.tile_type = "ice"
            self.climate = "ice"
            self.tile_color = WHITE
        elif self.noise_value >= h_mountain:
            self.tile_type = "high_mountain"
            self.climate = "cold"
            self.tile_color = HIGH_MOUNTAIN
        elif self.noise_value >= mountain:
            self.tile_type = "mountain"
            self.tile_color = HILLS
            self.climate = self.set_climate()
        elif self.noise_value >= hill:
            self.tile_type = "hills"
            self.tile_color = FOREST
            self.climate = self.set_climate()
        elif self.noise_value >= plain:
            self.tile_type = "plains"
            self.tile_color = PLAINS
            self.climate = self.set_climate()
        elif self.noise_value >= ocean:
            self.tile_type = "ocean"
            self.climate = "ocean"
            self.tile_color = WATER
        else:
            self.tile_type = "deep_ocean"
            self.climate = "ocean"
            self.tile_color = DEEP_WATER
    
    def set_group(self, group):
        self.group = group
    
    def set_climate(self):
        pass