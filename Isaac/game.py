import pygame


pygame.init()

WIDTH = 1280
HEIGHT = 960
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

circle_x = 200
circle_y = 200
spaceship_width = 40
spaceship_height = 60
#spaceship position
spaceship_x = WIDTH // 2 - spaceship_width // 2
spaceship_y = HEIGHT // 2 - spaceship_height // 2
spaceship_speed = 10

# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # GAME STATE UPDATES
        # Get keys pressed
    keys = pygame.key.get_pressed()

    # Move spaceship
    if keys[pygame.K_a]:
        spaceship_x -= spaceship_speed
    if keys[pygame.K_d]:
        spaceship_x += spaceship_speed
    if keys[pygame.K_w]:
        spaceship_y -= spaceship_speed
    if keys[pygame.K_s]:
        spaceship_y += spaceship_speed

    # All game math and comparisons happen here

    # DRAWING
    screen.fill((0, 0, 0))  # always the first drawing command
    pygame.draw.polygon(screen, (255, 255, 255), [(spaceship_x, spaceship_y), (spaceship_x, spaceship_y + spaceship_height), (spaceship_x + spaceship_width, spaceship_y), (spaceship_x + spaceship_width, spaceship_y + spaceship_height)], 0)


    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------
