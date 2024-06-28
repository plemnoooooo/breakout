import pygame

pygame.init()

# Game variables
SCREEN_COLOR = "black"

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

running = True
dt = 0

# Player variables
PLAYER_BOTTOM_MARGIN = 30
PLAYER_SIZE = (180, 30)
PLAYER_COLOR = "red"
PLAYER_SPEED = (300, 300)

player = pygame.Rect(pygame.Vector2(), PLAYER_SIZE)
player.bottom = int(screen.get_height() - PLAYER_BOTTOM_MARGIN)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(SCREEN_COLOR)
    screen.fill(PLAYER_COLOR, player)

    mouse = pygame.mouse.get_pos()
    player.centerx = int(pygame.math.clamp(mouse[0], 0, screen.get_width() - (PLAYER_SIZE[0] / 2)))
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()