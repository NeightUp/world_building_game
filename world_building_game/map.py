from pygame.locals import *
import pygame
import math
from settings import *
from tile import Tile
from perlin_noise import PerlinNoise

class Map:
    def __init__(self):
        self.camera_group = CameraGroup()                  # see camera group class below
        self.generate_map()

    def generate_map(self):
        # this mostly just creates the noise values that will define the map, and creates each tile
        # this is mostly sample code from the library, it needs further refinement.
        noise1 = PerlinNoise(octaves=3)
        noise2 = PerlinNoise(octaves=6)
        noise3 = PerlinNoise(octaves=12)
        noise4 = PerlinNoise(octaves=24)
        noise5 = PerlinNoise(octaves=48)
        for i in range(ROWS):
            for j in range(COLS):
                val = [i/ROWS, j/COLS]
                noise_val = noise1(val)
                noise_val += 0.5 * noise2(val)
                noise_val += 0.25 * noise3(val)
                noise_val += 0.125 * noise4(val)
                noise_val += 0.0625 * noise5(val)
                Tile((i, j), noise_val, self.camera_group)  # create the tile object
        self.camera_group.draw_full_map()                   # draw the full map to the map surface

    def run(self):
        self.camera_group.custom_draw()                     # see camera group below

class CameraGroup(pygame.sprite.Group):
    # class to control the camera and track the screen location on the map
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface() # get main display surface
        self.offset = pygame.math.Vector2()                 # create variable to store the map offset
        self.grid_image_black = pygame.image.load('.\\tiles\\grid_black.png').convert_alpha()
        self.grid_image_white = pygame.image.load('.\\tiles\\grid_white.png').convert_alpha()
        self.map_size = self.get_full_map_size()            # need the size to create the map surface
        self.map_surface = pygame.Surface((self.map_size[0], self.map_size[1]))  # creates map surface
        self.map_rect = self.map_surface.get_rect()         # create rect the size of the map surface
        self.grid_check = True                              # boolean to turn on and off the black grid
        self.previous_sprite = None                         # varable to store a tile for later
        self.active_pixel = (0, 0)                          # tuple to store the display center pixel                    
        self.border_size = 30                               # size of the border that allows the mouse to move the screen
        camera_rect_size = self.get_camera_rect()           # rect to track the mouse border
        self.camera_rect = pygame.Rect(self.border_size, self.border_size, camera_rect_size[0], camera_rect_size[1])

    def get_full_map_size(self):
        # this function uses the tile border image to calculate the overall size of the map surface
        tile = self.grid_image_black.get_rect()
        width = tile.width * (COLS + 0.5)
        height = (tile.height * 0.75) * (ROWS + 0.5)
        return (width, height)

    def get_camera_rect(self):
        # calculates the overall size of the camera rect
        width = self.display_surface.get_size()[0] - (self.border_size * 2)
        height = self.display_surface.get_size()[1] - (self.border_size * 2)
        return(width, height)

    def draw_full_map(self):
        # draws the map tiles and the black tile borders to the map surface
        # and saves an image of the entire map
        for sprite in self.sprites():
            self.map_surface.blit(sprite.tile_image, sprite.tile_pos)
            if self.grid_check:
                self.map_surface.blit(self.grid_image_black, sprite.tile_pos)
        pygame.image.save(self.map_surface, "full_map.png")

    def camera_pixel_position(self, pos):
        # this function checks and moves the camera position around on the map surface
        # by using the mouse position and a small border inside the display surface.
        # it keeps the map inside the bounds of the screen.
        speed = 5
        if pos[0] < self.camera_rect.left:
            self.camera_rect.left -= speed
            if self.camera_rect.left - self.border_size < self.map_rect.left:
                self.camera_rect.left = self.map_rect.left + self.border_size
        if pos[0] > self.camera_rect.right:
            self.camera_rect.right += speed
            if self.camera_rect.right + self.border_size > self.map_rect.right:
                self.camera_rect.right = self.map_rect.right - self.border_size
        if pos[1] > self.camera_rect.bottom:
            self.camera_rect.bottom += speed
            if self.camera_rect.bottom + self.border_size > self.map_rect.bottom:
                self.camera_rect.bottom = self.map_rect.bottom - self.border_size
        if pos[1] < self.camera_rect.top:
            self.camera_rect.top -= speed
            if self.camera_rect.top - self.border_size < self.map_rect.top:
                self.camera_rect.top = self.map_rect.top + self.border_size
        self.offset.x = self.camera_rect.left - self.border_size
        self.offset.y = self.camera_rect.top - self.border_size

    def check_mouse(self, tile):
        #checks if the mouse is near the center of a tile
        check = False
        mouse_pos = pygame.mouse.get_pos()
        pos = mouse_pos + self.offset
        square = ((pos[0] - tile.tile_image_rect.centerx) ** 2, (pos[1] - tile.tile_image_rect.centery) ** 2)
        if (math.sqrt(square[0]) + math.sqrt(square[1])) <= tile.tile_image_height // 2 + 2:
             check = True
        return check

    def custom_draw(self):
        # function to draw the map to the screen.
        self.camera_pixel_position(pygame.mouse.get_pos() + self.offset)
        for sprite in self.sprites():
            if self.check_mouse(sprite):
                self.map_surface.blit(self.grid_image_white, sprite.tile_pos)
                # check if the mouse has moved and fill in the tiles behind the mouse
                if self.previous_sprite != sprite and self.previous_sprite != None:
                    if self.grid_check:
                        self.map_surface.blit(self.grid_image_black, self.previous_sprite.tile_pos)
                    else:
                        self.map_surface.blit(self.previous_sprite.image, self.previous_sprite.tile_pos)
                self.previous_sprite = sprite
        #calculate the offset and draw the map
        offset_pos = self.map_rect.topleft - self.offset
        self.display_surface.blit(self.map_surface, offset_pos)