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
ball = pygame.Rect(width//2 - ball_width ,height//2 - ball_height , ball_width,ball_height)

# beggening Cordinates harekat be left or right 
ball_dx = ball_speed * random.choice((-1,1))
ball_dy = ball_speed * random.choice((-1,1))

paddle_width = 10
paddle_height = 120

paddle1 = pygame.Rect(50,height//2 - paddle_height//2,paddle_width,paddle_height)
paddle2 = pygame.Rect(width - 60,height//2 - paddle_height//2,paddle_width,paddle_height)
paddle1_dy = 0
paddle2_dy = 0
# harekate toop
ball_in_motion = True

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Ping Pong")


def draw_score():
    font = pygame.font.Font(None,36)
    center = font.render(".",True,white)
    score1_text = font.render(f"Score {player1}:{score1}",True,green)
    score2_text = font.render(f"Score {player2}:{score2}",True,green)
    screen.blit(score1_text,(10,10))
    screen.blit(score2_text,(width-score2_text.get_width()- 10,10))
    screen.blit(center,(width//2,height//2))

#  barkhord toop ba paddle
def check_collision(ball,paddle):
    if ball.colliderect(paddle):
        return True
    return False

# after restart
def reset_ball_position(side):
    # side = random.choice('left','right')
    if side == 'left':
        # fasele az chap 50 ta + width paddle + 10 fasele as paddle
        ball.x = 50 + 10 + 10
        ball_dx = ball_speed
    else :
        # fasele az rast 50 ta - width paddle - 10 fasele as paddle - ball width
        ball.x = width - 50 - 10 - 10 - 30 
        ball_dx = -ball_speed  
    ball.y = height//2 - ball_height 
    return ball_dx



running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle2_dy = -paddlle_speed
            elif event.key == pygame.K_DOWN:
                paddle2_dy = paddlle_speed
            elif event.key == pygame.K_SPACE:
                ball_in_motion = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                paddle2_dy = 0
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1_dy = -paddlle_speed
    elif keys[pygame.K_s]:
        paddle1_dy = paddlle_speed
    else:
        paddle1_dy = 0
    
    if ball_in_motion:
        ball.x += ball_dx
        ball.y += ball_dy
    
    if ball.top <= 0 or ball.bottom >= height:
        ball_dy *= -1
        
    if check_collision(ball,paddle1) or check_collision(ball,paddle2):
        ball_dx *= -1
     
     
    if ball.left <=0:
        score2 += 1
        if score2 == 5:
            running = False
        else:
            ball_dx = reset_ball_position('right')
            ball_in_motion = False        
    elif ball.right >= width:
        score1 += 1
        if score1 == 5:
            running = False
        else:
            ball_dx = reset_ball_position('left')
            ball_in_motion = False       
            
    paddle1.y += paddle1_dy
    paddle2.y += paddle2_dy

    if paddle1.top <=0 :
        paddle1.top = 0
    if paddle1.bottom >= height:
        paddle1.bottom = height
    if paddle2.top <=0 :
        paddle2.top = 0
    if paddle2.bottom >= height:
        paddle2.bottom = height
    
    screen.fill(black)

    
    pygame.draw.rect(screen,white,paddle1)
    pygame.draw.rect(screen,white,paddle2)
    pygame.draw.ellipse(screen,red,ball)

    draw_score()
    
    pygame.display.flip()
    
    pygame.time.delay(30)

pygame.quit()
