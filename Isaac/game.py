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
#bullet
bullet_width = 5 
bullet_height = 10 
bullet_color = (225, 0, 0)
bullet_speed = 10
bullets = []

# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.K_DOWN: 
            # Create a new bullet 
            bullet_x = spaceship_x + spaceship_width // 2 - bullet_width // 2 
            bullet_y = spaceship_y 
            bullets.append([bullet_x, bullet_y])

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
    if spaceship_x > 1280:
        spaceship_x = 0
    if spaceship_x < 0:
        spaceship_x = 1280
    if spaceship_y > 960:
        spaceship_y = 0
    if spaceship_y < 0:
        spaceship_y = 960
    #bullets
    for bullet in bullets: 
        bullet[1] -= bullet_speed 
        if bullet[1] < 0: 
            bullets.remove(bullet)

    # All game math and comparisons happen here

    # DRAWING
    screen.fill((0, 0, 0))  # always the first drawing command
    pygame.draw.polygon(screen, (255, 255, 255), [(spaceship_x, spaceship_y), (spaceship_x, spaceship_y + spaceship_height), (spaceship_x + spaceship_width, spaceship_y), (spaceship_x + spaceship_width, spaceship_y + spaceship_height)], 0)
    pygame.draw.polygon(screen, (bullet_color), [(spaceship_width, spaceship_y), (spaceship_x, spaceship_height), (spaceship_x + spaceship_width, spaceship_height)], 0)


    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------
