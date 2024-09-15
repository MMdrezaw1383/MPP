import pygame
import random

pygame.init()

# display configs
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Collect Coins Game")

normal_font = pygame.font.Font(None,40)
gameover_font = pygame.font.Font(None,80)
dark_mode = True
score = 0

# RGB
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
yellow = (255,255,0)
light_gray = (120,120,120)
dark_gray = (40,40,40)
silver = (192,192,192)

# Player Coordinates
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 10

# Obstacle Coordinates
obstacle_width = 100
obstacle_height = 20
obstacle_x = random.randit(0,screen_width- obstacle_width)
obstacle_y = -obstacle_height
obstacle_speed = 3
obstacle_speed_increase = 0.2

# Coin Coordinates
coin_radius = random.randit(10,15)
coin_x = random.randit(0,screen_width - coin_radius)
coin_y = -coin_radius
coin_speed = 4
coin_speed_increase = 0.2

# Frame
clock = pygame.time.Clock()
class CollectCoins:
    pass 