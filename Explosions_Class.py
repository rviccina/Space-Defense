import sys
import pygame
from spritesheet_functions import SpriteSheet

class Explosion(object):
    def __init__(self, file, screen, rows, cols):
        self.file = file
        self.screen = screen
        self.rows = rows
        self.cols = cols
        self.timer = pygame.time.Clock()
        self.animation_frames = []
        self.image = pygame.image.load(file).convert_alpha()
        self.width, self.height = self.image.get_size()
        self.sprite_width = self.width // cols
        self.sprite_height = self.height // rows
        self.sprite_file = SpriteSheet(self.file)
        
    def loadSprites(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.animation_frames.append(self.sprite_file.get_image(col*self.sprite_height, row*self.sprite_width, 
                                                                                self.sprite_height, self.sprite_width))

    def explode(self, x, y, frame):
        self.screen.blit( self.animation_frames[frame], (x, y))
        pygame.display.flip()