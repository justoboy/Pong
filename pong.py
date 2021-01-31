#PONG pygame

import random, pygame, sys
import PyGameWindow

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
WIDTH = 1280
HEIGHT = 720       
BALL_RADIUS = 15
PAD_WIDTH = 10
PAD_HEIGHT = 150
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0
score_font = pygame.font.SysFont("Comic Sans MS", 40)

#canvas declaration
window = PyGameWindow.Window(size=(WIDTH,HEIGHT),name="Pong",fps=120)

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH//2,HEIGHT//2]
    horz = random.randrange(3,6)
    vert = random.randrange(2,5)
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT//2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)


#draw function of canvas
def draw():
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
       
    canvas = pygame.Surface((WIDTH,HEIGHT))    
    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], HEIGHT//6, 1)

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel
    if paddle1_pos[1] < HALF_PAD_HEIGHT:
        paddle1_pos[1] = HALF_PAD_HEIGHT
    elif paddle1_pos[1] > HEIGHT-HALF_PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT-HALF_PAD_HEIGHT
    
    paddle2_pos[1] += paddle2_vel
    if paddle2_pos[1] < HALF_PAD_HEIGHT:
        paddle2_pos[1] = HALF_PAD_HEIGHT
    elif paddle2_pos[1] > HEIGHT-HALF_PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT-HALF_PAD_HEIGHT

    #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #draw paddles and ball
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)
        
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)

    #update scores
    
    label1 = score_font.render(str(l_score), 1, (255,255,255))
    canvas.blit(label1, ((WIDTH//2)-(50+label1.get_width()),20))

    label2 = score_font.render(str(r_score), 1, (255,255,255))
    canvas.blit(label2, ((WIDTH//2)+50, 20))
    window.smooth_scaled_blit(canvas) 
    
    
#keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel
    
    if event.key == pygame.K_UP:
        paddle2_vel = -8
    elif event.key == pygame.K_DOWN:
        paddle2_vel = 8
    elif event.key == pygame.K_w:
        paddle1_vel = -8
    elif event.key == pygame.K_s:
        paddle1_vel = 8

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if (event.key == pygame.K_w and paddle1_vel == -8) or (event.key == pygame.K_s and paddle1_vel == 8):
        paddle1_vel = 0
    elif (event.key == pygame.K_UP and paddle2_vel == -8) or (event.key == pygame.K_DOWN and paddle2_vel == 8):
        paddle2_vel = 0

init()


#game loop
is_open = True
while is_open:

    draw()

    for event in window.update():
        if event.type == pygame.KEYDOWN:
            keydown(event)
        elif event.type == pygame.KEYUP:
            keyup(event)
        elif event.type == pygame.QUIT:
            is_open = False