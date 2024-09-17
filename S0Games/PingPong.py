import pygame
import random



pygame.init()
# display screen
width , height = 800, 600
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)


ball_speed  = 7
paddlle_speed = 7

score1 = 0
score2 = 0

player1 = "ALi"
player2 = "MMd"

ball_width = 30
ball_height = 30 
ball = pygame.rect(width//2 - ball_width ,height//2 - ball_height , ball_width,ball_height)

# beggening Cordinates harekat be left or right 
ball_dx = ball_speed * random.choice((-1,1))
ball_dy = ball_speed * random.choice((-1,1))

paddle_width = 10
paddle_height = 120

paddle1 = pygame.rect(50,height//2 - paddle_height//2,paddle_width,paddle_height)
paddle2 = pygame.rect(width - 60,height//2 - paddle_height//2,paddle_width,paddle_height)
paddle1_dy = 0
paddle2_dy = 0
# harekate toop
ball_in_motion = True

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Ping Pong")


def draw_score():
    font = pygame.font.Font(None,36)
    score1_text = font.render(f"Score {player1}:{score1}",True,green)
    score2_text = font.render(f"Score {player2}:{score2}",True,green)
    screen.blit(score1_text,(10,10))
    screen.blit(score2_text,(width-score2_text.get_width()- 10,10))

#  barkhord toop ba paddle
def check_collision(ball,paddle):
    if ball.colliderect(paddle):
        return True
    return False

# after restart
def reset_ball_position():
    side = random.choice('left','right')
    if side == 'left':
        # fasele az chap 50 ta + width paddle + 10 fasele as paddle
        ball.x = 50 + 10 + 10
        ball_dx = ball_speed
    else :
        # fasele az rast 50 ta - width paddle - 10 fasele as paddle - ball width
        ball.y = width - 50 - 10 - 10 - 30 
        ball_dy = -ball_speed  
    ball.y = height//2 - ball_height 
    return ball_dx



    