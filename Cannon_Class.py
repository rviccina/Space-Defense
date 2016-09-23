import pygame
import math

BLACK = (0, 0, 0)
class Cannon(object):
    def __init__(self, screen, center_x, center_y, file):
        self.screen = screen
        self.start_x = center_x
        self.start_y = center_y
        self.speed = 5

        self.change_x = 0
        self.change_y = 0 
        
        "pygame variables"
        self.cannon_orig = pygame.image.load(file).convert()
        self.cannon_orig.set_colorkey(BLACK)
        self.cannon = self.cannon_orig.copy()

    def get_Cannon_Coords(self):
        return (self.start_x, self.start_y)
 
    def get_Cannon_Direction(self, angle):
        angle_rads = math.radians(angle)
        return (self.speed * math.sin(angle_rads) * -1, 
                self.speed * math.cos(angle_rads) * -1)


    def Update(self, pos_x, pos_y, angle=0):
        angle = float(angle)
        self.cannon = pygame.transform.rotate(self.cannon_orig, angle)
        self.cannon_rect = self.cannon.get_rect(center=(pos_x, pos_y))
        self.screen.blit(self.cannon,self.cannon_rect)


