import pygame
import serial # Used to interface with Arduino
import time   # Used for pygame clock
import math

from threading import Thread
from Spaceship_Class import Spaceship
from Explosions_Class import Explosion
from Cannon_Class import Cannon
from Projectile_Class import Projectile
from Arduino_Controller_Class import Arduino_Controller
from Level_Class import Level

"Colors"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
YELLOW = (255, 255, 0)
 
"Pygame Initial Variables"
pygame.init()
pygame.font.init()
screen_width = 1250
screen_height = 800
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SPACE DEFENSE")
clock = pygame.time.Clock()
    
###### Load game objects from classes ########
"Player 1 Spaceship"
spaceship_image="images/Spaceship.png" # image source : http://millionthvector.blogspot.com/
ship = Spaceship(screen, screen_width, screen_height, spaceship_image)


"Player 2 Space Cannon"
space_cannon_image = "images/spaceCannon.png" # image source : http://newimgbase.com/small-spaceship-sprite.html
init_xPos, init_yPos = ship.get_Ship_Coords()
space_cannon = Cannon(screen, init_xPos, init_yPos, space_cannon_image)

"Player 2 Arduino Controller"
rightUSB_Port = '/dev/cu.usbmodem1421'
leftUSB_Port = '/dev/cu.usbmodem1411'
try:
    cannon_controller = Arduino_Controller(rightUSB_Port)
except: pass

"Game Images"
final_boss_image = "images/final_boss.png" # https://warosu.org/vr/image/E_SlH3geSskpJrlQeC3siQ
red_laser_image = "images/RedLaser.png"# image sourde http://alf-img.com/show/laser-pixel-sprite.html
laser_image = "images/laser.gif" #http://themechanicalmaniacs.com/articles/mmmcmysteries.php?plainText=true
enemy_image = "images/enemy.png"  # image source : http://millionthvector.blogspot.com/
spaceImage = "images/StartScreen.jpg" # image source : http://e2ua.com/group/space-images/
titleImgae = "images/GameTitle.png" # Original Image created using Pixal Art
fire_image = "images/fire.png" # imgage source : http://blenderartists.org/forum/showthread.php?217018-Baking-2D-sprites-fire-smoke-etc-for-games
start_screen_image = pygame.image.load(spaceImage).convert()
game_title_image = pygame.image.load(titleImgae).convert()
game_title_image.set_colorkey(BLACK)

Player_image = pygame.image.load(spaceship_image).convert()
Player_image.set_colorkey(BLACK)

Cannon_image = pygame.image.load(space_cannon_image).convert()
Cannon_image.set_colorkey(BLACK)

fire_spritesheet_rows =  5
fire_spritesheet_cols = 5
fire = Explosion(fire_image, screen, fire_spritesheet_rows, fire_spritesheet_cols)
fire.loadSprites()

"Button Settings"
button_x = screen_width//2 - 80
button_y = screen_height//2
button_width = 170
button_height = 50

"The following functions were taken from (source) in order to create buttons and display text via pygame"
" text_display, button, and get_Text "

"Used to Display Text"
def text_display(info, x, y, size=25, color = WHITE):
    font = pygame.font.SysFont(None, size)
    text = font.render(info, True, color)
    screen.blit(text, (x, y))

"Creating a Button"
def button(msg,x_coord,y_coord,width,height,i_c,a_c,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if(x_coord+width> mouse[0] >x_coord and y_coord+height > mouse[1] > y_coord):
        
        pygame.draw.rect(screen, a_c,(x_coord,y_coord,width,height))
        
        if(click[0] == 1 and action != None):
            action()
    else:    
        pygame.draw.rect(screen, i_c, (x_coord,y_coord,width,height))

    "freesansbold.ttf"
    font = pygame.font.SysFont("monospace", 20, True)
    textSurf, textRect = get_Text(msg, font)
    textRect.center = ((x_coord+(width/2)),(y_coord+(height/2)) )
    screen.blit(textSurf, textRect)

def get_Text(text, font):
    textSurface = font.render( text, True, BLACK)
    return textSurface, textSurface.get_rect()

def Get_User_Settings():
    horizontal_enemies = input("Enter Number of Horizontal Enemies: ")
    vertical_enemies = input("Enter Number of Vertical Enemies: ")
    enemy_speed = input("Enter Enemy Speed: ")
    shot_speed = input("Enter Enemy Shooting Speed: ")
    horizontal_enemies, vertical_enemies, enemy_speed, shot_speed = int(horizontal_enemies), int(vertical_enemies), int(enemy_speed),  int(shot_speed)
    return horizontal_enemies, vertical_enemies, enemy_speed, shot_speed

"Main Menu Display"
def StartScreen():
    start_menu = True
    title_x = screen_width//8
    title_y = -100
    button_spacing = 70
    while start_menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_menu = False

        screen.blit(start_screen_image, [0,0])
        screen.blit(game_title_image, [title_x, title_y])

        button("1 PLAYER MODE",button_x, button_y, button_width, button_height, GOLD, YELLOW, SinglePlayer)
        button("2 PLAYER MODE",button_x, button_y+button_spacing, button_width, button_height, GOLD, YELLOW, TwoPlayer) 
        button("INSTRUCTIONS",button_x, button_y+2*button_spacing, button_width, button_height, GOLD, YELLOW, Instructions)
        button("QUIT",button_x, button_y+3*button_spacing, button_width, button_height, GOLD, YELLOW, pygame.quit)      

        pygame.display.flip()

    pygame.quit()
    quit()

def Instructions():
    instruction_menu = True
    OnePlayer_text = "1 PLAYER CONTROLS"
    TwoPlayer_text = "2 PLAYER CONTROLS"
    Up = "PRESS UP ARROW TO GO FORWARD" 
    Down = "PRESS DOWN ARROW TO GO BACKWARDS" 
    P1_Rotate = "USE LEFT AND RIGHT ARROWS TO ROTATE" 
    P1_Fire = "PRESS SPACE BAR TO FIRE LASER"
    P2_Rotate = "USE POTENTIOMETER TO ROTATE CANNON"
    P2_Fire = "PRESS BUTTON TO FIRE"
    Restart = "PRESS R TO GO BACK TO MAIN MENU"
    player2_movement = "SHIP MOVEMENT SAME AS 1P"

    header_size = 50
    header_x = screen_width//4
    header1_y = screen_height//5
    header2_y = header1_y + 300
    header3_y = header2_y + 230
    player1_image_x = screen_width - screen_width//3
    player1_image_y = screen_height//3
    player2_image_x = screen_width - screen_width//3
    player2_image_y = screen_height - screen_height//3

    start_menu_y = button_y-350
    text_spacing = 50
 
    while instruction_menu:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instruction_menu = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    instruction_menu = False
                    StartScreen()

        screen.blit(start_screen_image, [0,0])
        screen.blit(Player_image, [player1_image_x, player1_image_y])
        screen.blit(Player_image, [player2_image_x, player2_image_y])
        screen.blit(Cannon_image, [player2_image_x+30, player2_image_y])
        button("Start Menu",button_x, start_menu_y, button_width, button_height, GOLD, YELLOW, StartScreen) 
        
        " 1 Player "
        text_display(OnePlayer_text, header_x, header1_y, header_size, GOLD)
        text_display(Up, header_x, header1_y+text_spacing)
        text_display(Down, header_x, header1_y+2*text_spacing)
        text_display(P1_Rotate, header_x, header1_y+3*text_spacing)
        text_display(P1_Fire, header_x, header1_y+4*text_spacing)

        " 2 Players "
        text_display(TwoPlayer_text, header_x, header2_y, header_size, GOLD)
        text_display(player2_movement, header_x, header2_y+text_spacing)
        text_display(P2_Rotate, header_x, header2_y+2*text_spacing)
        text_display(P2_Fire, header_x, header2_y+3*text_spacing)
        "Restart"
        text_display(Restart,header_x, header3_y, header_size, GOLD)
        pygame.display.flip()
    
    pygame.quit()
    quit()

def SinglePlayer():
    
    "Initial Game Variable States"
    GameOver = False 
    wave_1 = True
    wave_2 = False
    wave_2_off = False
    wave_3 = False
    wave_3_off = False
    has_rotate_Top_1 = False
    has_rotate_Top_2 = False
    has_rotated_Bot_1 = False
    has_rotated_Bot_2 = False
    ship_isExploding = False

    Top_Enemies_Are_Displayed = True
    Bot_Enemies_Are_Displayed = False
    Side_Enemies_Are_Displayed = False
    final_boss_isDisplayed = False

    ship_explosionFrame = 0
    ship.start_x = screen_width//2
    ship.start_y = screen_height-100
    shot_time_counter = 0
    alternating_const1 = 0
    alternating_const2 = 0
    alternating_const3 = 0
    alternating_const4 = 0
    #shot_speed = 5

    num_horizontal_enemies, num_vertical_enemies, enemy_speed, shot_speed = Get_User_Settings()


    "Sprite Groups"
    Top_Enemies_On_Screen = pygame.sprite.Group()
    Bot_Enemies_On_Screen = pygame.sprite.Group()
    enemy_shots_fired = pygame.sprite.Group() #shots fired by enemies
    shots_Fired = pygame.sprite.Group() # Shots on Screen by the Player

    "Levels"
    level_1 = Level(screen, screen_width, screen_height, enemy_image)
    Top_Enemies_On_Screen = level_1.load_Top_Vertical_Wave(num_horizontal_enemies, enemy_speed)
    Bot_Enemies_On_Screen = level_1.load_Bot_Vertical_Wave(num_horizontal_enemies, enemy_speed)

    level_2 = Level(screen, screen_width, screen_height, enemy_image)
    Left_Horizontal_Enemies_On_Screen = level_2.load_Left_Horizontal_Wave(num_vertical_enemies, enemy_speed)
    Right_Horizontal_Enemies_On_Screen = level_2.load_Right_Horizontal_Wave(num_vertical_enemies, enemy_speed)

    level_3= Level(screen, screen_width, screen_height, final_boss_image)
    final_boss = level_3.load_Final_Boss(5)
    final_boss_health = 50
    final_boss.health = final_boss_health
    rotate_left = True
    rotate_right = False

    while not GameOver:

        "Ship Coordinates and Direction used for firing shots"
        (ship_xPos, ship_yPos) = ship.get_Ship_Coords()
        (x_dir, y_dir, ship_angle) = ship.get_Ship_Direction()

        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameOver = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ship.moveForward()

                if event.key == pygame.K_DOWN:
                    ship.moveReverse()

                if event.key == pygame.K_LEFT:
                    ship.rotateRight()

                if event.key == pygame.K_RIGHT:
                    ship.rotateLeft()

                if event.key == pygame.K_SPACE:
                    "Fire a shot if space bar is pressed"
                    shots_Fired.add(Projectile(screen, ship_xPos, ship_yPos, x_dir, y_dir, ship_angle, laser_image))

                if event.key == pygame.K_r:
                    GameOver = True
                    ship.reset()
                    final_boss.reset(final_boss_health)
                    StartScreen()

            if event.type == pygame.KEYUP:
                if (   event.key == pygame.K_LEFT 
                    or event.key == pygame.K_RIGHT 
                    or event.key == pygame.K_DOWN 
                    or event.key == pygame.K_UP):
                    ship.stop()
                    
        screen.blit(start_screen_image, [0, 0]) #display background image

        "Ship Functions"
        ship.outOfBounds()
        ship.Update_Position()
        
        "Update Game Content"
        if(shot_time_counter > 500):
            Bot_Enemies_Are_Displayed = True
            Bot_Enemies_On_Screen.update()
        
        if(len(Top_Enemies_On_Screen) == 0 and len(Bot_Enemies_On_Screen) == 0):
            Side_Enemies_Are_Displayed = True
            Left_Horizontal_Enemies_On_Screen.update()
            Right_Horizontal_Enemies_On_Screen.update()
            wave_2 = True

        if(len(Left_Horizontal_Enemies_On_Screen) == 0 and len(Right_Horizontal_Enemies_On_Screen) == 0):
            final_boss_isDisplayed = True   
            final_boss.update()
            final_boss.move_sideways()
            
            if(final_boss.angle<45 and rotate_left):
                final_boss.angle += 1
            else:
                rotate_left = False
                rotate_right = True
            
            if(final_boss.angle > -45 and rotate_right):
                final_boss.angle -= 1
            else:
                rotate_right = False
                rotate_left = True
                
            wave_3 = True

        Top_Enemies_On_Screen.update()
        shots_Fired.update()
        enemy_shots_fired.update()

        "Detects if Shots collided with enemies"
        for shot in shots_Fired:

            if(Top_Enemies_Are_Displayed):
                enemy_collision_list1 = pygame.sprite.spritecollide(shot, Top_Enemies_On_Screen, True)
                for enemy_sprite in enemy_collision_list1:
                    shot.kill()

            if(Bot_Enemies_Are_Displayed):
                enemy_collision_list2 = pygame.sprite.spritecollide(shot, Bot_Enemies_On_Screen, True)
                for enemy_sprite in enemy_collision_list2:
                    shot.kill()

            if(Side_Enemies_Are_Displayed):
                enemy_collision_list3 = pygame.sprite.spritecollide(shot, Left_Horizontal_Enemies_On_Screen, True)
                enemy_collision_list4 = pygame.sprite.spritecollide(shot, Right_Horizontal_Enemies_On_Screen, True)
                for enemy_sprite in enemy_collision_list3:
                    shot.kill()
                for enemy_sprite in enemy_collision_list4:
                    shot.kill()

            if(final_boss_isDisplayed):
                boss_is_hit = pygame.sprite.collide_rect(shot, final_boss)
                if(boss_is_hit):
                    final_boss.health -= 1
                    shot.kill()


        "Player Collision"
        for shot in enemy_shots_fired:
            if(pygame.sprite.collide_circle(ship, shot)):
                shot.kill()     
                ship.health -=1
                ship_isExploding = True

        "Update Enemy movement Top"
        for enemy_sprite in Top_Enemies_On_Screen:
            enemy_sprite.moveVertical_Top()

        "Update Enemy movement Bot"
        for enemy_sprite in Bot_Enemies_On_Screen:
            enemy_sprite.moveVertical_Bot()

        "Update Left Enemies"
        for enemy_sprite in Left_Horizontal_Enemies_On_Screen:
            enemy_sprite.moveHorizontal_Left()

        "Update Right Enemies"
        for enemy_sprite in Right_Horizontal_Enemies_On_Screen:
            enemy_sprite.moveHorizontal_Right()

        "Explosion Functions For Ship"
        if(ship_isExploding == True and ship_explosionFrame < 25):
            fire.explode(ship_xPos-30, ship_yPos-20, ship_explosionFrame)
            ship_explosionFrame +=1
        else:
            ship_isExploding = False
            ship_explosionFrame = 0

        "Enemy shooting Top"
        if(shot_time_counter % 200 == 0):
            for enemy_sprite in Top_Enemies_On_Screen:
                enemy_sprite.angle = level_1.Top_Wave_Angle
                if(alternating_const1% 2 == 0):
                    if(has_rotate_Top_1):
                        enemy_sprite.angle +=45
                    else: enemy_sprite.angle -= 45
                    angle_rads = math.radians(enemy_sprite.angle)
                    x_dir = shot_speed * math.sin(angle_rads) * -1 
                    y_dir = shot_speed * math.cos(angle_rads) * -1
                    enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                alternating_const1 +=1
            has_rotate_Top_1 = not has_rotate_Top_1        
        alternating_const1 = 0

        if(shot_time_counter % 300 == 0):
            for enemy_sprite in Top_Enemies_On_Screen:
                enemy_sprite.angle = level_1.Top_Wave_Angle
                if(alternating_const2%2 != 0):
                    if(has_rotate_Top_2):
                        enemy_sprite.angle -=45
                    else: enemy_sprite.angle += 45
                    angle_rads = math.radians(enemy_sprite.angle)
                    x_dir = shot_speed * math.sin(angle_rads) * -1 
                    y_dir = shot_speed * math.cos(angle_rads) * -1
                    enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                alternating_const2 +=1
            has_rotate_Top_2 = not has_rotate_Top_2        
        alternating_const2 = 0

        if(shot_time_counter>500):
            
            "Enemy shooting Bot"
            if(shot_time_counter % 128 == 0):
                for enemy_sprite in Bot_Enemies_On_Screen:
                    enemy_sprite.angle = level_1.Bot_Wave_Angle
                    if(alternating_const3% 2 == 0):
                        if(has_rotated_Bot_1):
                            enemy_sprite.angle +=45
                        else: enemy_sprite.angle -= 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const3 +=1 
                has_rotated_Bot_1 = not has_rotated_Bot_1
            alternating_const3 = 0

            if(shot_time_counter % 256 == 0):
                for enemy_sprite in Bot_Enemies_On_Screen:
                    enemy_sprite.angle = level_1.Bot_Wave_Angle
                    if(alternating_const4%2 != 0):
                        if(has_rotated_Bot_2):
                            enemy_sprite.angle -=45
                        else: enemy_sprite.angle += 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const4 +=1  
                has_rotated_Bot_2 = not has_rotated_Bot_2    
            alternating_const4 = 0

        if(wave_2):
            "Enemy shooting Left"
            if(shot_time_counter % 128 == 0):
                for enemy_sprite in Left_Horizontal_Enemies_On_Screen:
                    enemy_sprite.angle = level_2.Left_Horizontal_Wave_Angle
                    if(alternating_const1% 2 == 0):
                        if(has_rotated_Bot_1):
                            enemy_sprite.angle -=45
                        else: enemy_sprite.angle += 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const1 +=1 
                has_rotated_Bot_1 = not has_rotated_Bot_1
            alternating_const1 = 0

            if(shot_time_counter % 256 == 0):
                for enemy_sprite in Left_Horizontal_Enemies_On_Screen:
                    enemy_sprite.angle = level_2.Left_Horizontal_Wave_Angle
                    if(alternating_const2%2 != 0):
                        if(has_rotated_Bot_2):
                            enemy_sprite.angle +=45
                        else: enemy_sprite.angle -= 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const2 +=1  
                has_rotated_Bot_2 = not has_rotated_Bot_2    
            alternating_const2 = 0

            "Enemy shooting Right"
            if(shot_time_counter % 128 == 0):
                for enemy_sprite in Right_Horizontal_Enemies_On_Screen:
                    enemy_sprite.angle = level_2.Right_Horizontal_Wave_Angle
                    if(alternating_const3% 2 == 0):
                        if(has_rotated_Bot_1):
                            enemy_sprite.angle -=45
                        else: enemy_sprite.angle += 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const3 +=1 
                has_rotated_Bot_1 = not has_rotated_Bot_1
            alternating_const3 = 0

            if(shot_time_counter % 256 == 0):
                for enemy_sprite in Right_Horizontal_Enemies_On_Screen:
                    enemy_sprite.angle = level_2.Right_Horizontal_Wave_Angle
                    if(alternating_const4%2 != 0):
                        if(has_rotated_Bot_2):
                            enemy_sprite.angle +=45
                        else: enemy_sprite.angle -= 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const4 +=1  
                has_rotated_Bot_2 = not has_rotated_Bot_2    
            alternating_const4 = 0

        if(wave_3):
            text_display("Boss Health: " + str(final_boss.health), 20, 50)
            if(shot_time_counter%15 == 0):
                angle_rads = math.radians(final_boss.angle)
                x_dir = shot_speed * math.sin(angle_rads) * -1 
                y_dir = shot_speed * math.cos(angle_rads) 
                enemy_shots_fired.add(Projectile(screen, final_boss.rect.x, final_boss.rect.y, x_dir, y_dir, final_boss.angle, red_laser_image))


        if(wave_1):
            text_display("WAVE 1", screen_width//2.5, screen_height//2, 100, YELLOW)

        if(wave_2 and not wave_2_off):
            text_display("WAVE 2", screen_width//2.5, screen_height//2, 100, YELLOW)

        if(wave_3 and not wave_3_off):
            text_display("FINAL BOSS", screen_width//3.5, screen_height//2, 100, YELLOW)

        if(ship.health < 1):
            GameOver = True
            ship.reset()
            final_boss.reset(final_boss_health)
            Game_Over()

        if(final_boss.health < 1):
            GameOver = True
            ship.reset()
            final_boss.reset(final_boss_health)
            Won()

        text_display("Current Health: " + str(ship.health), 20, 20)
        shot_time_counter += 1
        pygame.display.flip()
  
        if(wave_1):
            pygame.time.wait(2000)
            wave_1 = False
        if(wave_2 and not wave_2_off):
            pygame.time.wait(2000)
            #wave_2 = False
            wave_2_off = not wave_2_off
        if(wave_3 and not wave_3_off):
            pygame.time.wait(2000)
            wave_3_off = not wave_3_off

        # --- Limit to 60 frames per second
        clock.tick(60)
    # Close the window and quit.
    pygame.quit()
    quit()

def TwoPlayer():
    "Initialize Arduino Thread"
    try:
        get_Cannon_Data = Thread(target = cannon_controller.get_Data)
        get_Cannon_Data.start()
    except:
        StartScreen()
    
    "Initial Game Variable States"

    GameOver = False 
    wave_1 = True
    wave_2 = False
    wave_2_off = False
    wave_3 = False
    wave_3_off = False
    has_rotate_Top_1 = False
    has_rotate_Top_2 = False
    has_rotated_Bot_1 = False
    has_rotated_Bot_2 = False
    ship_isExploding = False

    Top_Enemies_Are_Displayed = True
    Bot_Enemies_Are_Displayed = False
    Side_Enemies_Are_Displayed = False
    final_boss_isDisplayed = False

    ship_explosionFrame = 0
    ship.start_x = screen_width//2
    ship.start_y = screen_height-100
    shot_time_counter = 0
    alternating_const1 = 0
    alternating_const2 = 0
    alternating_const3 = 0
    alternating_const4 = 0

    num_horizontal_enemies, num_vertical_enemies, enemy_speed, shot_speed = Get_User_Settings()

    "Sprite Groups"
    Top_Enemies_On_Screen = pygame.sprite.Group()
    Bot_Enemies_On_Screen = pygame.sprite.Group()
    enemy_shots_fired = pygame.sprite.Group() #shots fired by enemies
    shots_Fired = pygame.sprite.Group() # Shots on Screen by the Player

    "Levels"
    level_1 = Level(screen, screen_width, screen_height, enemy_image)
    Top_Enemies_On_Screen = level_1.load_Top_Vertical_Wave(num_horizontal_enemies, enemy_speed)
    Bot_Enemies_On_Screen = level_1.load_Bot_Vertical_Wave(num_horizontal_enemies, enemy_speed)

    level_2 = Level(screen, screen_width, screen_height, enemy_image)
    Left_Horizontal_Enemies_On_Screen = level_2.load_Left_Horizontal_Wave(num_vertical_enemies, enemy_speed)
    Right_Horizontal_Enemies_On_Screen = level_2.load_Right_Horizontal_Wave(num_vertical_enemies, enemy_speed)

    level_3= Level(screen, screen_width, screen_height, final_boss_image)
    final_boss = level_3.load_Final_Boss(5)
    final_boss_health = 500
    final_boss.health = final_boss_health
    rotate_left = True
    rotate_right = False

    ########################################################################

    while not GameOver:
        "Ship Coordinates and Cannon Direction used for firing shots"
        (ship_xPos, ship_yPos) = ship.get_Ship_Coords()
        (x_dir, y_dir) = space_cannon.get_Cannon_Direction(cannon_controller.angle) 
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameOver = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ship.moveForward()

                if event.key == pygame.K_DOWN:
                    ship.moveReverse()

                if event.key == pygame.K_LEFT:
                    ship.rotateRight()

                if event.key == pygame.K_RIGHT:
                    ship.rotateLeft()

                if event.key == pygame.K_r:
                    GameOver = True
                    ship.reset()
                    final_boss.reset(final_boss_health)
                    StartScreen()

            if event.type == pygame.KEYUP:
                if (   event.key == pygame.K_LEFT 
                    or event.key == pygame.K_RIGHT 
                    or event.key == pygame.K_DOWN 
                    or event.key == pygame.K_UP):
                    ship.stop()
        
        screen.blit(start_screen_image, [0, 0])
        "Ship Functions"
        ship.outOfBounds()
        ship.Update_Position()
        space_cannon.Update(ship_xPos, ship_yPos, cannon_controller.angle)
        
        "Fire a shot if Button is Pressed"
        if(cannon_controller.is_Button_Pressed):
            shots_Fired.add(Projectile(screen, ship_xPos, ship_yPos,x_dir, y_dir, cannon_controller.angle, laser_image))

        ########################################################################
        
        "Update Game Content"
        if(shot_time_counter > 500):
            Bot_Enemies_Are_Displayed = True
            Bot_Enemies_On_Screen.update()
        
        if(len(Top_Enemies_On_Screen) == 0 and len(Bot_Enemies_On_Screen) == 0):
            Side_Enemies_Are_Displayed = True
            Left_Horizontal_Enemies_On_Screen.update()
            Right_Horizontal_Enemies_On_Screen.update()
            wave_2 = True

        if(len(Left_Horizontal_Enemies_On_Screen) == 0 and len(Right_Horizontal_Enemies_On_Screen) == 0):
            final_boss_isDisplayed = True   
            final_boss.update()
            final_boss.move_sideways()
            
            if(final_boss.angle<45 and rotate_left):
                final_boss.angle += 1
            else:
                rotate_left = False
                rotate_right = True
            
            if(final_boss.angle > -45 and rotate_right):
                final_boss.angle -= 1
            else:
                rotate_right = False
                rotate_left = True
                
            wave_3 = True

        Top_Enemies_On_Screen.update()
        shots_Fired.update()
        enemy_shots_fired.update()

        "Detects if Shots collided with enemies"
        for shot in shots_Fired:

            if(Top_Enemies_Are_Displayed):
                enemy_collision_list1 = pygame.sprite.spritecollide(shot, Top_Enemies_On_Screen, True)
                for enemy_sprite in enemy_collision_list1:
                    shot.kill()

            if(Bot_Enemies_Are_Displayed):
                enemy_collision_list2 = pygame.sprite.spritecollide(shot, Bot_Enemies_On_Screen, True)
                for enemy_sprite in enemy_collision_list2:
                    shot.kill()

            if(Side_Enemies_Are_Displayed):
                enemy_collision_list3 = pygame.sprite.spritecollide(shot, Left_Horizontal_Enemies_On_Screen, True)
                enemy_collision_list4 = pygame.sprite.spritecollide(shot, Right_Horizontal_Enemies_On_Screen, True)
                for enemy_sprite in enemy_collision_list3:
                    shot.kill()
                for enemy_sprite in enemy_collision_list4:
                    shot.kill()

            if(final_boss_isDisplayed):
                boss_is_hit = pygame.sprite.collide_rect(shot, final_boss)
                if(boss_is_hit):
                    final_boss.health -= 1
                    shot.kill()


        "Player Collision"
        for shot in enemy_shots_fired:
            if(pygame.sprite.collide_circle(ship, shot)):
                shot.kill()     
                ship.health -=1
                ship_isExploding = True

        "Update Enemy movement Top"
        for enemy_sprite in Top_Enemies_On_Screen:
            enemy_sprite.moveVertical_Top()

        "Update Enemy movement Bot"
        for enemy_sprite in Bot_Enemies_On_Screen:
            enemy_sprite.moveVertical_Bot()

        "Update Left Enemies"
        for enemy_sprite in Left_Horizontal_Enemies_On_Screen:
            enemy_sprite.moveHorizontal_Left()

        "Update Right Enemies"
        for enemy_sprite in Right_Horizontal_Enemies_On_Screen:
            enemy_sprite.moveHorizontal_Right()

        "Explosion Functions For Ship"
        if(ship_isExploding == True and ship_explosionFrame < 25):
            fire.explode(ship_xPos-30, ship_yPos-20, ship_explosionFrame)
            ship_explosionFrame +=1
        else:
            ship_isExploding = False
            ship_explosionFrame = 0

        "Enemy shooting Top"
        if(shot_time_counter % 200 == 0):
            for enemy_sprite in Top_Enemies_On_Screen:
                enemy_sprite.angle = level_1.Top_Wave_Angle
                if(alternating_const1% 2 == 0):
                    if(has_rotate_Top_1):
                        enemy_sprite.angle +=45
                    else: enemy_sprite.angle -= 45
                    angle_rads = math.radians(enemy_sprite.angle)
                    x_dir = shot_speed * math.sin(angle_rads) * -1 
                    y_dir = shot_speed * math.cos(angle_rads) * -1
                    enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                alternating_const1 +=1
            has_rotate_Top_1 = not has_rotate_Top_1        
        alternating_const1 = 0

        if(shot_time_counter % 300 == 0):
            for enemy_sprite in Top_Enemies_On_Screen:
                enemy_sprite.angle = level_1.Top_Wave_Angle
                if(alternating_const2%2 != 0):
                    if(has_rotate_Top_2):
                        enemy_sprite.angle -=45
                    else: enemy_sprite.angle += 45
                    angle_rads = math.radians(enemy_sprite.angle)
                    x_dir = shot_speed * math.sin(angle_rads) * -1 
                    y_dir = shot_speed * math.cos(angle_rads) * -1
                    enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                alternating_const2 +=1
            has_rotate_Top_2 = not has_rotate_Top_2        
        alternating_const2 = 0

        if(shot_time_counter>500):
            
            "Enemy shooting Bot"
            if(shot_time_counter % 128 == 0):
                for enemy_sprite in Bot_Enemies_On_Screen:
                    enemy_sprite.angle = level_1.Bot_Wave_Angle
                    if(alternating_const3% 2 == 0):
                        if(has_rotated_Bot_1):
                            enemy_sprite.angle +=45
                        else: enemy_sprite.angle -= 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const3 +=1 
                has_rotated_Bot_1 = not has_rotated_Bot_1
            alternating_const3 = 0

            if(shot_time_counter % 256 == 0):
                for enemy_sprite in Bot_Enemies_On_Screen:
                    enemy_sprite.angle = level_1.Bot_Wave_Angle
                    if(alternating_const4%2 != 0):
                        if(has_rotated_Bot_2):
                            enemy_sprite.angle -=45
                        else: enemy_sprite.angle += 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const4 +=1  
                has_rotated_Bot_2 = not has_rotated_Bot_2    
            alternating_const4 = 0

        if(wave_2):
            "Enemy shooting Left"
            if(shot_time_counter % 128 == 0):
                for enemy_sprite in Left_Horizontal_Enemies_On_Screen:
                    enemy_sprite.angle = level_2.Left_Horizontal_Wave_Angle
                    if(alternating_const1% 2 == 0):
                        if(has_rotated_Bot_1):
                            enemy_sprite.angle -=45
                        else: enemy_sprite.angle += 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const1 +=1 
                has_rotated_Bot_1 = not has_rotated_Bot_1
            alternating_const1 = 0

            if(shot_time_counter % 256 == 0):
                for enemy_sprite in Left_Horizontal_Enemies_On_Screen:
                    enemy_sprite.angle = level_2.Left_Horizontal_Wave_Angle
                    if(alternating_const2%2 != 0):
                        if(has_rotated_Bot_2):
                            enemy_sprite.angle +=45
                        else: enemy_sprite.angle -= 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const2 +=1  
                has_rotated_Bot_2 = not has_rotated_Bot_2    
            alternating_const2 = 0

            "Enemy shooting Right"
            if(shot_time_counter % 128 == 0):
                for enemy_sprite in Right_Horizontal_Enemies_On_Screen:
                    enemy_sprite.angle = level_2.Right_Horizontal_Wave_Angle
                    if(alternating_const3% 2 == 0):
                        if(has_rotated_Bot_1):
                            enemy_sprite.angle -=45
                        else: enemy_sprite.angle += 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const3 +=1 
                has_rotated_Bot_1 = not has_rotated_Bot_1
            alternating_const3 = 0

            if(shot_time_counter % 256 == 0):
                for enemy_sprite in Right_Horizontal_Enemies_On_Screen:
                    enemy_sprite.angle = level_2.Right_Horizontal_Wave_Angle
                    if(alternating_const4%2 != 0):
                        if(has_rotated_Bot_2):
                            enemy_sprite.angle +=45
                        else: enemy_sprite.angle -= 45
                        angle_rads = math.radians(enemy_sprite.angle)
                        x_dir = shot_speed * math.sin(angle_rads) * -1 
                        y_dir = shot_speed * math.cos(angle_rads) * -1
                        enemy_shots_fired.add(Projectile(screen, enemy_sprite.rect.x, enemy_sprite.rect.y, x_dir, y_dir, enemy_sprite.angle, red_laser_image))
                    alternating_const4 +=1  
                has_rotated_Bot_2 = not has_rotated_Bot_2    
            alternating_const4 = 0

        if(wave_3):
            text_display("Final Boss Health: " +str(final_boss.health), 0, 0)
            if(shot_time_counter%25 == 0):
                angle_rads = math.radians(final_boss.angle)
                x_dir = shot_speed * math.sin(angle_rads) * -1 
                y_dir = shot_speed * math.cos(angle_rads) 
                enemy_shots_fired.add(Projectile(screen, final_boss.rect.x, final_boss.rect.y, x_dir, y_dir, final_boss.angle, red_laser_image))


        if(wave_1):
            text_display("WAVE 1", screen_width//2.5, screen_height//2, 100, YELLOW)

        if(wave_2 and not wave_2_off):
            text_display("WAVE 2", screen_width//2.5, screen_height//2, 100, YELLOW)

        if(wave_3 and not wave_3_off):
            text_display("FINAL BOSS", screen_width//3.5, screen_height//2, 100, YELLOW)

        if(ship.health < 1):
            GameOver = True
            final_boss.reset(final_boss_health)
            ship.reset()
            Game_Over()

        if(final_boss.health < 1):
            GameOver = True
            final_boss.reset(final_boss_health)
            ship.reset()
            Won()

        text_display("Current Health: " + str(ship.health), 20, 20)
        shot_time_counter += 1
        pygame.display.flip()
  
        if(wave_1):
            pygame.time.wait(2000)
            wave_1 = False
        if(wave_2 and not wave_2_off):
            pygame.time.wait(2000)
            #wave_2 = False
            wave_2_off = not wave_2_off
        if(wave_3 and not wave_3_off):
            pygame.time.wait(2000)
            wave_3_off = not wave_3_off

        # --- Limit to 60 frames per second
        clock.tick(60)
    # Close the window and quit.
    pygame.quit()
    quit()

def Game_Over():
    game_over_screen = True
    title_x = screen_width//8
    title_y = -100
    button_spacing = 70
    text_size = 150
    while game_over_screen:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_screen = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    game_over_screen = False
                    StartScreen()

        screen.blit(start_screen_image, [0,0])
        text_display("GAME OVER", button_x-210, button_y-150, text_size, YELLOW)
        
        button("PLAY AGAIN 1P",button_x, button_y+button_spacing, button_width, button_height, GOLD, YELLOW, SinglePlayer)
        button("PLAY AGAIN 2P",button_x, button_y+2*button_spacing, button_width, button_height, GOLD, YELLOW, TwoPlayer)  
        button("QUIT",button_x, button_y+3*button_spacing, button_width, button_height, GOLD, YELLOW, pygame.quit)      

        pygame.display.flip()

    pygame.quit()
    quit()

def Won():
    game_over_screen = True
    title_x = screen_width//8
    title_y = -100
    button_spacing = 70
    text_size = 150
    while game_over_screen:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_screen = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    game_over_screen = False
                    StartScreen()

        screen.blit(start_screen_image, [0,0])
        text_display("YOU WON!", button_x-210, button_y-150, text_size, YELLOW)
        
        button("PLAY AGAIN 1P",button_x, button_y+button_spacing, button_width, button_height, GOLD, YELLOW, SinglePlayer)
        button("PLAY AGAIN 2P",button_x, button_y+2*button_spacing, button_width, button_height, GOLD, YELLOW, TwoPlayer)  
        button("QUIT",button_x, button_y+3*button_spacing, button_width, button_height, GOLD, YELLOW, pygame.quit)      

        pygame.display.flip()

    pygame.quit()
    quit()

StartScreen()
