from pygame.locals import *
import pygame
import math
from settings import *
from tile import Tile
from perlin_noise import PerlinNoise

class Map:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.map_surface = pygame.Surface((X_SPACER * (COLS + 0.5), Y_SPACER * (ROWS + 0.5)))
        self.map_rect = pygame.Surface.get_rect(self.map_surface)
        self.camera_group = pygame.sprite.Group()
        self.active_tile = None
        self.map_data = self.generate_map()
        self.running = False
        self.grid_check = True
        self.previous_tile = None

    def generate_map(self):
        x_pos = X_SCALE
        y_pos = HEX_SIZE
        noise1 = PerlinNoise(octaves=4)
        noise2 = PerlinNoise(octaves=6)
        noise3 = PerlinNoise(octaves=12)
        #noise4 = PerlinNoise(octaves=24)
        #noise5 = PerlinNoise(octaves=48)
        data = []
        for i in range(ROWS):
            row = []
            if (i % 2 != 0):
                x_pos += X_SCALE
            for j in range(COLS): 
                new_tile = Tile((i, j), (x_pos, y_pos), self.camera_group)
                noise_val = noise1([i/ROWS, j/COLS])
                noise_val += 0.7 * noise2([i/ROWS, j/COLS])
                noise_val += 0.25 * noise3([i/ROWS, j/COLS])
                #noise_val += 0.125 * noise4([i/ROWS, j/COLS])
                #noise_val += 0.0625 * noise5([i/ROWS, j/COLS])
                new_tile.set_tile_type_color_noise(noise_val)
                new_tile.set_group(self.camera_group)
                row.append(new_tile)
                x_pos += X_SPACER
            data.append(row)
            x_pos = X_SCALE
            y_pos += Y_SPACER
        return data
        

    def draw_hexagon(self, current_tile, color, fill):
        vert_one = current_tile[1]
        vert_two = current_tile[2]
        vert_three = current_tile[3]
        vert_four = current_tile[4]
        vert_five = current_tile[5]
        vert_six = current_tile[6]
    
        if(fill == True):
            pygame.draw.polygon(self.map_surface, color, [vert_one, vert_two, 
                                vert_three, vert_four, vert_five, vert_six])
        else:
            pygame.draw.polygon(self.map_surface, color, [vert_one, vert_two, 
                                vert_three, vert_four, vert_five, vert_six], width=2)

    def check_mouse(self, pos):
        mouse_xy = pygame.mouse.get_pos()
        sqx = (mouse_xy[0] - pos[0])**2
        sqy = (mouse_xy[1] - pos[1])**2
        if math.sqrt(sqx + sqy) < X_SCALE:
            return True
        else:
            return False

    def draw_map(self):
        for i in range(ROWS):
            for j in range(COLS + 2):
                if j == 0:
                    current_tile = self.map_data[i][COLS - 1]
                elif j == COLS + 1:
                    current_tile = self.map_data[i][0]
                else:
                    current_tile = self.map_data[i][j - 1]
                fill = True
                color = current_tile.tile_color
                self.draw_hexagon(current_tile.vertices, color, fill)
                if self.grid_check:
                    color = BLACK
                    fill = False
                    self.draw_hexagon(current_tile.vertices, color, fill)

    def run(self):
        if self.running == False:
            self.draw_map()
            pygame.image.save_extended(self.map_surface, "map.png")
            self.running = True
        for i in range(ROWS):
            for j in range(COLS):
                current_tile = self.map_data[i][j]
                if self.check_mouse((current_tile.center_x, current_tile.center_y)):
                    color = WHITE
                    fill = False
                    self.draw_hexagon(current_tile.vertices, color, fill)
                    #print(f"{current_tile.noise_value}, {current_tile.tile_type}")
                    if self.previous_tile != current_tile and self.previous_tile != None:
                        fill = False
                        if self.grid_check:
                            color = BLACK
                            self.draw_hexagon(self.previous_tile.vertices, color, fill)
                        else:
                            self.draw_hexagon(self.previous_tile.vertices, self.previous_tile.tile_color, fill)
                    self.previous_tile = current_tile
        self.display_surface.blit(self.map_surface, self.map_rect)