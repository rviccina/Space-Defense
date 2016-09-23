import pygame
import math

BLACK = (0, 0, 0)
screen_width = 1250
screen_height = 800

class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen, start_x, start_y, x_dir, y_dir, angle, file):
        super().__init__()
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.angle = angle
        self.file = file
        self.screen = screen
        self.radius = 9

        #### pygame variables ####
        self.projectile_orig = pygame.image.load(file).convert()
        self.projectile_orig.set_colorkey(BLACK)
        self.projectile = self.projectile_orig.copy()
        self.projectile = pygame.transform.rotate(self.projectile_orig, self.angle)
        self.rect = self.projectile.get_rect()

        self.rect.x = start_x
        self.rect.y = start_y

    def update(self):
        if(self.rect.x < 0 or self.rect.x > screen_width or
           self.rect.y < 0 or self.rect.y > screen_height):
            self.kill()
        else:
            self.rect.x += self.x_dir
            self.rect.y += self.y_dir
            self.projectile_rect = self.projectile.get_rect(center=(self.rect.x, self.rect.y))
            self.screen.blit(self.projectile,self.projectile_rect)

