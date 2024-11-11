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
bullet_speed = 50
bullet_speed2 = 15
bullet_speed3 = 40
bullets = [] 
bullets2 = []
bullets3 = []
radius3 = 1
counter3 = 0
keydowntime = 0
boost_cooldown = []
# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                bullet2 = [spaceship_x + 40, spaceship_y - 5]
                bullets2.append(bullet2)
            if event.key == pygame.K_LEFT: 
                bullet = [spaceship_x, spaceship_y - 5]
                bullets.append(bullet)
            if event.key == pygame.K_UP:
                bullet3 = [spaceship_x + 20, spaceship_y - 5]
                bullets3.append(bullet3)
            if event.key == pygame.K_DOWN:
                spaceship_speed = 50          
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                spaceship_speed = 10

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
    for i in bullets: 
        i[1] -= bullet_speed
    for n in bullets2:
        n[1] -= bullet_speed2
    for g in bullets3:
        g[1] -= bullet_speed3
        radius3 += 20
        counter3 += 1
        if counter3 == 10:
            radius3 = 1
            counter3 = 0


    # All game math and comparisons happen here

    # DRAWING
    screen.fill((0, 0, 0))  # always the first drawing command
    pygame.draw.polygon(screen, (255, 255, 255), [(spaceship_x, spaceship_y), (spaceship_x, spaceship_y + spaceship_height), (spaceship_x + spaceship_width, spaceship_y), (spaceship_x + spaceship_width, spaceship_y + spaceship_height)], 0)
    for i in bullets:
        pygame.draw.circle(screen, (bullet_color), (i[0], i[1]),3)
    for n in bullets2:
        pygame.draw.circle(screen, (0, 0, 255), (n[0], n[1]), 10)
    for g in bullets3:
        pygame.draw.circle(screen, (255, 0, 255), (g[0], g[1]), radius3)


    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------
