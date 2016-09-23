import pygame
BLACK = (0,0,0)

class Enemy_Sprite(pygame.sprite.Sprite):
    def __init__(self, screen, file, screen_width, screen_height, speed, angle):
        super().__init__()
        self.screen = screen 
        self.file = file
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed
        self.angle = angle 
        self.isMovingDown = True
        self.isMovingUp = True
        self.isMovingLeft = True
        self.isMovingRight = True
        " pygame variables "
        self.enemy_orig = pygame.image.load(file).convert()
        self.enemy_orig.set_colorkey(BLACK)
        self.enemy = self.enemy_orig.copy()
        self.rect = self.enemy.get_rect()
        
    def update(self):
        self.enemy = pygame.transform.rotate(self.enemy_orig, self.angle)
        self.enemy_rect = self.enemy.get_rect(center=(self.rect.x, self.rect.y))
        self.screen.blit(self.enemy, self.enemy_rect)

    def moveVertical_Top(self):
        if(self.isMovingDown):
            if(self.rect.y > self.screen_height//3):
                self.isMovingDown = False
            else:
                self.rect.y += self.speed
        else:
            if(self.rect.y < 0):
                self.isMovingDown = True
            else:
                self.rect.y -= self.speed

    def moveVertical_Bot(self):
        if(self.isMovingUp):
            if(self.rect.y < 2*self.screen_height//3):
                self.isMovingUp = False
            else:
                self.rect.y -= self.speed
        else:
            if(self.rect.y > self.screen_height):
                self.isMovingUp = True
            else:
                self.rect.y += self.speed

    def moveHorizontal_Left(self):
        if(self.isMovingRight):
            if(self.rect.x > self.screen_width//5):
                self.isMovingRight = False
            else:
                self.rect.x += self.speed
        else:
            if(self.rect.x < 0):
                self.isMovingRight = True
            else:
                self.rect.x -= self.speed

    def moveHorizontal_Right(self):
        if(self.isMovingLeft):
            if(self.rect.x < 4*(self.screen_width//5) ):
                self.isMovingLeft = False
            else:
                self.rect.x -= self.speed
        else:
            if(self.rect.x > self.screen_width):
                self.isMovingLeft = True
            else:
                self.rect.x += self.speed


class Final_Boss_Sprite(Enemy_Sprite):
    def __init__(self, screen, file, screen_width, screen_height, speed, angle):
        super().__init__(screen, file, screen_width, screen_height, speed, angle)
        self.radius = 20
        self.angle = 0
        self.health = None

    def reset(self, health= 50):
        self.health = health
        self.angle = 0
        self.rect.x = self.screen_width//2
        self.rect.y = self.screen_height//7 
    
    def move_sideways(self):
        if(self.isMovingLeft):
            if(self.rect.x < self.screen_width//5):
                self.isMovingLeft = False
            else:
                self.rect.x -= self.speed
        else:
            if(self.rect.x > 4*self.screen_width//5):
                self.isMovingLeft = True
            else:
                self.rect.x += self.speed
      