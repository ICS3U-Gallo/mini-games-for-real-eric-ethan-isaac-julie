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
playerx = WIDTH // 2
playery = HEIGHT - 60
playerwidth = 5
playerlength = 20
ammo = 10
health = 3
move_speed = 10
bullet_speed = 15
asteroid_speed = 5
pickup_speed = 2  # Slower speed for health and ammo packs
bullets = []
asteroids = []
heals = []
ammos = []
# ---------------------------
pygame.display.set_caption('Space Defender')
font = pygame.font.Font('freesansbold.ttf', 15)
running = True

def draw_player():
    pygame.draw.rect(screen, (255, 255, 255), (playerx, playery, playerwidth, playerlength))

def draw_bullet(x, y):
    pygame.draw.rect(screen, (255, 255, 0), (x, y, 3, 10))

def draw_asteroid(x, y, size):
    points = [(x + random.randint(-size, size), y + random.randint(-size, size)) for _ in range(6)]
    pygame.draw.polygon(screen, (169, 169, 169), points)

def drawheal(x, y):
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20)
    pygame.draw.polygon(screen, (0, 255, 0), [(x - 5, y - 15), (x + 5, y - 15),
                                              (x + 5, y - 5), (x + 15, y - 5),
                                              (x + 15, y), (x + 5, y),
                                              (x + 5, y + 10), (x - 5, y + 10),
                                              (x - 5, y), (x - 15, y),
                                              (x - 15, y - 5), (x - 5, y - 5)])

def drawammo(x, y):
    pygame.draw.circle(screen, (102, 102, 0), (x, y), 10)
    pygame.draw.rect(screen, (51, 102, 0), (x - 5, y, 10, 20))

def spawn_asteroid():
    x = random.randint(0, WIDTH)
    y = -20
    size = random.randint(20, 50)
    asteroids.append((x, y, size))

def spawn_heal():
    x = random.randint(0, WIDTH)
    y = -20  # start off-screen
    heals.append((x, y))

def spawn_ammo():
    x = random.randint(0, WIDTH)
    y = -20  # start off-screen
    ammos.append((x, y))

def display_text(text, x, y, color=(255, 255, 255)):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

while running:
    # EVENT HANDLING
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ammo > 0:
                bullets.append((playerx + playerwidth // 2, playery))
                ammo -= 1

    # MOVEMENT
    if keys[pygame.K_a] and playerx > 0:
        playerx -= move_speed
    if keys[pygame.K_d] and playerx < WIDTH - playerwidth:
        playerx += move_speed

    # SPAWNING LOGIC
    if random.random() < 0.02:
        spawn_asteroid()
    if random.random() < 0.002:
        spawn_heal()
    if random.random() < 0.002:
        spawn_ammo()

    # BULLET MOVEMENT
    bullets = [(bx, by - bullet_speed) for bx, by in bullets if by > 0]

    # ASTEROID MOVEMENT
    asteroids = [(ax, ay + asteroid_speed, size) for ax, ay, size in asteroids if ay < HEIGHT]

    # HEALTH PACK MOVEMENT
    for i, (hx, hy) in enumerate(heals):
        if hy >= HEIGHT:
            # Respawn at top with random x-position
            heals[i] = (random.randint(0, WIDTH), -20)
        else:
            heals[i] = (hx, hy + pickup_speed)

    # AMMO PACK MOVEMENT
    for i, (amx, amy) in enumerate(ammos):
        if amy >= HEIGHT:
            # Respawn at top with random x-position
            ammos[i] = (random.randint(0, WIDTH), -20)
        else:
            ammos[i] = (amx, amy + pickup_speed)

    # COLLISION DETECTION
    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            bx, by = bullet
            ax, ay, size = asteroid
            if ax - size < bx < ax + size and ay - size < by < ay + size:
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                break

    for asteroid in asteroids[:]:
        ax, ay, size = asteroid
        if ay + size > playery and ax - size < playerx < ax + size:
            health -= 1
            asteroids.remove(asteroid)
            if health <= 0:
                running = False

    # HEALTH PICKUP
    for heal in heals[:]:
        hx, hy = heal
        if abs(hx - playerx) < 20 and abs(hy - playery) < 20:
            health += 1
            heals.remove(heal)

    # AMMO PICKUP
    for am in ammos[:]:
        amx, amy = am
        if abs(amx - playerx) < 20 and abs(amy - playery) < 20:
            ammo += 5
            ammos.remove(am)

    # DRAWING
    screen.fill((0, 0, 51))  # Background color
    draw_player()
    for bx, by in bullets:
        draw_bullet(bx, by)
    for ax, ay, size in asteroids:
        draw_asteroid(ax, ay, size)
    for hx, hy in heals:
        drawheal(hx, hy)
    for amx, amy in ammos:
        drawammo(amx, amy)

    # HUD
    display_text(f'Health: {health}', 10, 10)
    display_text(f'Ammo: {ammo}', 10, 30)

    pygame.display.flip()
    clock.tick(30)
    #---------------------------

pygame.quit()
