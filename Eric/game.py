import pygame
import random

pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

playerx = 200
playery = HEIGHT-60
playerwidth = 5
playerlength = 20
ammo = 10
health = 3
move_speed = 10
# ---------------------------
pygame.display.set_caption('Shooter Game')
font = pygame.font.Font('freesansbold.ttf', 15)
running = True
while running:
    # EVENT HANDLING
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if keys[pygame.K_a]:
        playerx -= move_speed
    if keys[pygame.K_d]:
        playerx += move_speed
    if playerx >= WIDTH:
        playerx = WIDTH-playerwidth  # Prevent wrapping
    elif playerx <= 0:
        playerx = 0  # Wrap to the right
    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # DRAWING
    screen.fill((0, 0, 51))  # always the first drawing command
    pygame.draw.rect (screen, (255, 255, 255), (playerx, playery, playerwidth, playerlength))

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
