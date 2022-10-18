import pygame
import math
import random
from settings import *

class Tile():
    def __init__(self, index, pos):
        super().__init__()
        self.row_index = index[0]
        self.col_index = index[1]
        self.center_x = pos[0]
        self.center_y = pos[1]
        self.vertices = self.create_hex()
        self.tile_type = None
        self.tile_color = None

    def create_hex(self):
        vert_one = (self.center_x + HEX_SIZE * math.cos(math.pi/2), self.center_y + HEX_SIZE * math.sin(math.pi/2))
        vert_two = (self.center_x + HEX_SIZE * math.cos(math.pi/6), self.center_y + HEX_SIZE * math.sin(math.pi/6))
        vert_three = (self.center_x + HEX_SIZE * math.cos(11 * math.pi/6), self.center_y + HEX_SIZE * math.sin(11 * math.pi/6))
        vert_four = (self.center_x + HEX_SIZE * math.cos(3 * math.pi/2), self.center_y + HEX_SIZE * math.sin(3 * math.pi/2))
        vert_five = (self.center_x + HEX_SIZE * math.cos(7 * math.pi/6), self.center_y + HEX_SIZE * math.sin(7 * math.pi/6))
        vert_six = (self.center_x + HEX_SIZE * math.cos(5 * math.pi/6), self.center_y + HEX_SIZE * math.sin(5 * math.pi/6))
        pos_data = [(self.center_x, self.center_y), vert_one, vert_two, vert_three, vert_four, vert_five, vert_six]
        return pos_data

    def set_tile_type_color(self, noise_val):
        if self.row_index == 0 or self.row_index == ROWS - 1:
            noise_val = ICE
        elif self.row_index == 1 or self.row_index == ROWS - 2:
            r_number = random.randint(1, 4)
            if noise_val >= OCEAN:
                noise_val = ICE
            elif r_number != 4:
                noise_val = ICE
        elif self.row_index == 2 or self.row_index == ROWS - 3:
            r_number = random.randint(1, 3)
            if r_number != 3:
                noise_val = ICE
            
        elif self.col_index <= 0 or self.col_index >= COLS - 1:
            if noise_val >= PLAINS:
                noise_val -= 0.5
        elif self.col_index <= 1 or self.col_index >= COLS - 2:
            if noise_val >= PLAINS:
                noise_val -= 0.25
        elif self.col_index <= 3 or self.col_index >= COLS -4:
            if noise_val >= PLAINS:
                noise_val -= 0.15
        elif self.col_index <= 5 or self.col_index >= COLS -6:
            if noise_val >= PLAINS:
                noise_val -= 0.1

        if noise_val == ICE:
            self.tile_type = "ice"
            self.tile_color = WHITE
        elif noise_val >= H_MOUNTAIN:
            self.tile_type = "high_mountain"
            self.tile_color = HIGH_MOUNTAIN_COLOR
        elif noise_val >= MOUNTAIN:
            self.tile_type = "mountain"
            self.tile_color = HILLS_COLOR
        elif noise_val >= HILLS:
            self.tile_type = "hills"
            self.tile_color = FOREST_COLOR
        elif noise_val >= PLAINS:
            self.tile_type = "plains"
            self.tile_color = PLAINS_COLOR
        elif noise_val >= OCEAN:
            self.tile_type = "ocean"
            self.tile_color = WATER_COLOR
        else:
            self.tile_type = "deep_ocean"
            self.tile_color = DEEP_WATER_COLOR