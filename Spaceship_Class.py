import pygame
import math

BLACK = (0, 0, 0)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen, screen_width, screen_height, file, center_x=None, center_y=None,):
        super().__init__()
        self.screen = screen
        self.start_x = center_x
        self.start_y = center_y
        self.width = screen_width
        self.height = screen_height
        self.ship_width = 50
        self.angle = 0
        self.speed = 10
        self.health = 20
        
        self.change_x = 0
        self.change_y = 0 
        self.change_angle = 0
        " pygame variables "
        self.spaceship_orig = pygame.image.load(file).convert()
        self.spaceship_orig.set_colorkey(BLACK)
        self.spaceship = self.spaceship_orig.copy()
        self.rect = self.spaceship.get_rect()

    def get_Ship_Coords(self):
        return (self.start_x, self.start_y)

    def reset(self):
        self.health = 20
        self.angle = 0

    def get_Ship_Direction(self):
        angle_rads = math.radians(self.angle)
        return (self.speed * math.sin(angle_rads) * -1, 
                self.speed * math.cos(angle_rads) * -1, self.angle)

    def moveForward(self):
        angle_rads = math.radians(self.angle)
        self.change_x = self.speed * math.sin(angle_rads) * -1
        self.change_y = self.speed * math.cos(angle_rads) * -1

    def moveReverse(self):
        angle_rads = math.radians(self.angle)
        self.change_x = self.speed * math.sin(angle_rads)
        self.change_y = self.speed * math.cos(angle_rads)

    def rotateRight(self):
        self.change_angle = 4

    def rotateLeft(self):
        self.change_angle = -4

    def stop(self):
        self.change_x = 0 
        self.change_y = 0
        self.change_angle = 0

    def outOfBounds(self):
        if(    self.start_x+self.change_x - self.ship_width < 0 
            or self.start_x+self.change_x + self.ship_width > self.width 
            or self.start_y+self.change_y - self.ship_width < 0 
            or self.start_y+self.change_y + self.ship_width > self.height):
            self.change_x = 0
            self.change_y = 0
            
    def Update_Position(self):
        self.start_x += self.change_x
        self.start_y += self.change_y
        self.angle += self.change_angle
        self.spaceship = pygame.transform.rotate(self.spaceship_orig, self.angle)
        self.spaceship_rect = self.spaceship.get_rect(center=(self.start_x, self.start_y))
        self.screen.blit(self.spaceship,self.spaceship_rect)
        self.rect.x = self.start_x
        self.rect.y = self.start_y

