from typing import List
import pygame

pygame.init()

# Game variables
SCREEN_COLOR = "black"

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

running = True
dt = 0

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
BALL_SPEED = (100, 100)

ball = pygame.Rect(screen.get_width() / 2, screen.get_height() - BALL_BOTTOM, BALL_RADIUS, BALL_RADIUS)
ball_vel = pygame.Vector2(1, 1)

# Functions
def get_side_collisions(rect: pygame.Rect, others: list[pygame.Rect]) -> tuple[list[bool], ...]:
    return tuple(list(map(bool, [
        other.clipline(rect.topleft, rect.topright), # Top
        other.clipline(rect.bottomleft, rect.bottomright), # Bottom
        other.clipline(rect.topleft, rect.bottomleft), # Left
        other.clipline(rect.topright, rect.bottomright) # Right
    ])) for other in others)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(SCREEN_COLOR)
    screen.fill(PLAYER_COLOR, player)
    pygame.draw.circle(screen, BALL_COLOR, ball.center, BALL_RADIUS)

    mouse = pygame.mouse.get_pos()
    player.centerx = int(pygame.math.clamp(mouse[0], 0, screen.get_width() - (PLAYER_SIZE[0] / 2)))

    ball.centerx += int(ball_vel.x * BALL_SPEED[0] * dt)
    ball.centery += int(ball_vel.y * BALL_SPEED[1] * dt)

    collisions = get_side_collisions(ball, [player])

    if any(any(i[:2]) for i in collisions) or ball.top < 0 or ball.bottom > screen.get_height():
        ball_vel.y *= -1
    elif any(any(i[2:]) for i in collisions) or ball.left < 0 or ball.right > screen.get_width():
        ball_vel.x *= -1
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()