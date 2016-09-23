import pygame
from Enemy_Sprites_Class import Enemy_Sprite
from Enemy_Sprites_Class import Final_Boss_Sprite


class Level():
    def __init__(self, screen, screen_width, screen_height, enemy_image):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemy_image = enemy_image
        self.off_set = 30
        
        self.top_low = 20
        self.top_high = -40
        self.bot_low = screen_height - self.off_set
        self.bot_high = screen_height + self.off_set
        self.Top_Wave_Angle = 180
        self.Bot_Wave_Angle = 0
        
        self.Left_Horizontal_Wave_Angle = 270
        self.Right_Horizontal_Wave_Angle = 90
        self.left_xfront = 20
        self.left_xback = 0
        self.right_xfront = screen_width-20
        self.right_xback = screen_width

        self.final_boss_angle = 0

    def load_Top_Vertical_Wave(self, num_enemies, speed):
        vertical_wave = pygame.sprite.Group()
        for enemy in range(num_enemies):
            enemy_sprite = Enemy_Sprite(self.screen, self.enemy_image, self.screen_width, self.screen_height, speed, self.Top_Wave_Angle)
            enemy_sprite.rect.x = (self.screen_width//num_enemies)*enemy + self.off_set
            if(enemy%2==0):
                enemy_sprite.rect.y = self.top_high
            else:
                enemy_sprite.rect.y = self.top_low
            vertical_wave.add(enemy_sprite)
        return vertical_wave

    def load_Bot_Vertical_Wave(self, num_enemies, speed):
        vertical_wave = pygame.sprite.Group()
        for enemy in range(num_enemies):
            enemy_sprite = Enemy_Sprite(self.screen, self.enemy_image, self.screen_width, self.screen_height, speed, self.Bot_Wave_Angle)
            enemy_sprite.rect.x = (self.screen_width//num_enemies)*enemy + self.off_set
            if(enemy%2==0):
                enemy_sprite.rect.y = self.bot_high
            else:
                enemy_sprite.rect.y = self.bot_low
            vertical_wave.add(enemy_sprite)
        return vertical_wave

    def load_Left_Horizontal_Wave(self, num_enemies, speed):
        horizontal_wave = pygame.sprite.Group()
        for enemy in range(num_enemies):
            enemy_sprite = Enemy_Sprite(self.screen, self.enemy_image, self.screen_width, self.screen_height, speed, self.Left_Horizontal_Wave_Angle)
            enemy_sprite.rect.y = (self.screen_height//num_enemies)*enemy + self.off_set
            if(enemy%2==0):
                enemy_sprite.rect.x = self.left_xfront
            else:
                enemy_sprite.rect.x = self.left_xback
            horizontal_wave.add(enemy_sprite)
        return horizontal_wave

    def load_Right_Horizontal_Wave(self, num_enemies, speed):
        horizontal_wave = pygame.sprite.Group()
        for enemy in range(num_enemies):
            enemy_sprite = Enemy_Sprite(self.screen, self.enemy_image, self.screen_width, self.screen_height, speed, self.Right_Horizontal_Wave_Angle)
            enemy_sprite.rect.y = (self.screen_height//num_enemies)*enemy + self.off_set
            if(enemy%2==0):
                enemy_sprite.rect.x = self.right_xfront
            else:
                enemy_sprite.rect.x = self.right_xback
            horizontal_wave.add(enemy_sprite)
        return horizontal_wave

    def load_Final_Boss(self, speed):
        final_boss = Final_Boss_Sprite(self.screen, self.enemy_image, self.screen_width, self.screen_height, speed, self.final_boss_angle)
        final_boss.rect.x = self.screen_width//2
        final_boss.rect.y = self.screen_height//7
        return final_boss

