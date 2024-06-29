import math
import pygame

pygame.init()

# Game variables
SCREEN_COLOR = "black"

screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
pygame.display.set_caption("Breakout")

pygame.font.init()
font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()

running = True
game_over = False
dt = 0
time = 0

# Player variables
PLAYER_BOTTOM = 30
PLAYER_SIZE = (180, 30)
PLAYER_COLOR = "red"

player = pygame.Rect(pygame.Vector2(), PLAYER_SIZE)
player.bottom = int(screen.get_height() - PLAYER_BOTTOM)

# Ball variables
BALL_BOTTOM = 90
BALL_RADIUS = 10
BALL_COLOR = "white"
BALL_SPEED = (300, 300)
BALL_MAX_VEL_X = 1.6

ball = pygame.Rect(screen.get_width() / 2, screen.get_height() - BALL_BOTTOM, BALL_RADIUS, BALL_RADIUS)
ball_vel = pygame.Vector2(1, -1)

# Brick variables
BRICKS_X = 6
BRICKS_Y = 3
BRICK_GAP_X = 10
BRICK_GAP_Y = 10
BRICKS_TOP = 60
BRICK_COLOR = "green"
BRICK_WIDTH = (screen.get_width() - (BRICK_GAP_X * (BRICKS_X - 1))) / BRICKS_X
BRICK_HEIGHT = 20

bricks: list[pygame.Rect] = [t for ts in [[pygame.Rect(x * (BRICK_WIDTH + BRICK_GAP_X), (y * (BRICK_HEIGHT + BRICK_GAP_Y)) + BRICKS_TOP, BRICK_WIDTH, BRICK_HEIGHT) for x in range(BRICKS_X)] for y in range(BRICKS_Y)] for t in ts]

TIMER_Y = 5

# Functions
def get_side_collisions(rect: pygame.Rect, others: list[pygame.Rect]) -> tuple[list[bool], ...]:
    return tuple(list(map(bool, [
        other.clipline(rect.topleft, rect.topright), # Top
        other.clipline(rect.bottomleft, rect.bottomright), # Bottom
        other.clipline(rect.topleft, rect.bottomleft), # Left
        other.clipline(rect.topright, rect.bottomright) # Right
    ])) for other in others)

# Game loop
while running:
    dt = clock.tick(60) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            game_over = False
            time = 0

            ball.center = (int(screen.get_width() / 2), screen.get_height() - BALL_BOTTOM)
            ball_vel = pygame.Vector2(1, -1)

            bricks = [t for ts in [[pygame.Rect(x * (BRICK_WIDTH + BRICK_GAP_X), (y * (BRICK_HEIGHT + BRICK_GAP_Y)) + BRICKS_TOP, BRICK_WIDTH, BRICK_HEIGHT) for x in range(BRICKS_X)] for y in range(BRICKS_Y)] for t in ts]

    if game_over:
        continue

    screen.fill(SCREEN_COLOR)
    screen.fill(PLAYER_COLOR, player)
    pygame.draw.circle(screen, BALL_COLOR, ball.center, BALL_RADIUS)

    mouse = pygame.mouse.get_pos()
    player.centerx = int(pygame.math.clamp(mouse[0], 0, screen.get_width() - (PLAYER_SIZE[0] / 2)))

    ball.centerx += int(ball_vel.x * BALL_SPEED[0] * dt)
    ball.centery += int(ball_vel.y * BALL_SPEED[1] * dt)

    for brick in bricks:
        screen.fill(BRICK_COLOR, brick)
        
    collisions = get_side_collisions(ball, [player, *bricks])

    if any(collisions[0][:2]):
        ball_vel.x = (1 + min(abs((ball.centerx - player.centerx) / (PLAYER_SIZE[0] / 2)) * (BALL_MAX_VEL_X - 1), BALL_MAX_VEL_X)) * (-1 if ball_vel.x < 0 else 1)
    if any(any(i[:2]) for i in collisions) or ball.top <= 0:
        ball_vel.y *= -1
    elif any(any(i[2:]) for i in collisions) or ball.left <= 0 or ball.right >= screen.get_width():
        ball_vel.x *= -1

    ball.x = int(pygame.math.clamp(ball.x, 0, screen.get_width() - ball.width))
    ball.y = int(pygame.math.clamp(ball.y, 0, screen.get_height() - ball.height))
    
    if ball.bottom >= screen.get_height():
        game_over = True
        end_text = font.render("Game Over", True, "white")
        end_text_rect = end_text.get_rect()
        screen.blit(end_text, ((screen.get_width() / 2) - end_text_rect.centerx, (screen.get_height() / 2) - end_text.get_rect().centery))

    if len(bricks) == 0:
        game_over = True
        end_text = font.render("You win!", True, "white")
        end_text_rect = end_text.get_rect()
        screen.blit(end_text, ((screen.get_width() / 2) - end_text_rect.centerx, (screen.get_height() / 2) - end_text.get_rect().centery))

    for i in range(len(collisions) - 1):
        if any(collisions[i + 1]):
            bricks.remove(bricks[i])

    timer = font.render(f"{math.floor(time / 60000):02}:{(math.floor(time / 1000) % 60):02}:{(time % 1000):03}", True, "white")
    screen.blit(timer, ((screen.get_width() / 2) - timer.get_rect().centerx, TIMER_Y))
    
    pygame.display.flip()
    time += clock.get_time()

pygame.quit()