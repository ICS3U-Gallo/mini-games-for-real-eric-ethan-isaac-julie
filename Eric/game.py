import pygame
import random
import math

pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables
playerx = WIDTH // 2
playery = HEIGHT // 2
playerwidth = 20
playerlength = 20
ammo = 10
health = 3
move_speed = 10
bullet_speed = 15
asteroid_speed = 10
pickup_speed = 2  # Slower speed for health and ammo packs
bullets = []
asteroids = []
heals = []
ammos = []
player_angle = 0  # Initial angle facing up

# ---------------------------
pygame.display.set_caption('Space Defender')
font = pygame.font.Font('freesansbold.ttf', 15)
running = True

def spawn_asteroid():
    x = random.randint(0, WIDTH)
    y = -20  # start off-screen
    size = random.randint(20, 50)
    asteroids.append((x, y, size))

def draw_asteroid(x, y, size):
    points = [(x + math.cos(math.radians(angle)) * size, y + math.sin(math.radians(angle)) * size)
              for angle in range(0, 360, 60)]
    pygame.draw.polygon(screen, (169, 169, 169), points)

def draw_player():
    points = [
        (playerx + math.cos(math.radians(player_angle)) * playerlength,
         playery - math.sin(math.radians(player_angle)) * playerlength),
        (playerx + math.cos(math.radians(player_angle + 140)) * playerlength // 2,
         playery - math.sin(math.radians(player_angle + 140)) * playerlength // 2),
        (playerx + math.cos(math.radians(player_angle - 140)) * playerlength // 2,
         playery - math.sin(math.radians(player_angle - 140)) * playerlength // 2)
    ]
    pygame.draw.polygon(screen, (255, 255, 255), points)

def draw_bullet(x, y):
    pygame.draw.rect(screen, (255, 255, 0), (x, y, 3, 10))

def drawheal(x, y):
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20)
    pygame.draw.polygon(screen, (0, 255, 0), [(x - 5, y - 15), (x + 5, y - 15),
                                              (x + 5, y - 5), (x + 15, y - 5),
                                              (x + 15, y), (x + 5, y),
                                              (x + 5, y + 10), (x - 5, y + 10),
                                              (x - 5, y), (x - 15, y),
                                              (x - 15, y - 5), (x - 5, y - 5)])

def drawammo(x, y, counter=0):
    if counter <= 2:
        counter += 1
        pygame.draw.circle(screen, (102, 102, 0), (x + 5, y), 5)
        pygame.draw.rect(screen, (51, 102, 0), (x, y, 10, 30))
        pygame.draw.rect(screen, (0, 0, 0), (x + 10, y, 2, 30))
        # recursion stuff
        drawammo(x + 12, y, counter)
    pygame.draw.circle(screen, (102, 102, 0), (x + 5, y), 5)
    pygame.draw.rect(screen, (51, 102, 0), (x, y, 10, 30))

def spawn_heal():
    x = random.randint(0, WIDTH)
    y = -20  # start off-screen
    heals.append((x, y))

def spawn_ammo():
    x = random.randint(0, WIDTH)
    y = -20  # start off-screen
    ammos.append((x, y))

def check_collision(x1, y1, x2, y2, size1, size2):
    # Check distance between two objects for collision
    distance = math.hypot(x1 - x2, y1 - y2)
    return distance < (size1 + size2)

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
                bullets.append((playerx, playery, player_angle))
                ammo -= 1

    # MOVEMENT
    if keys[pygame.K_a]:
        playerx -= move_speed
        player_angle = 180
    if keys[pygame.K_d]:
        playerx += move_speed
        player_angle = 0
    if keys[pygame.K_w]:
        playery -= move_speed
        player_angle = 90
    if keys[pygame.K_s]:
        playery += move_speed
        player_angle = 270

    # SPAWNING LOGIC
    if random.random() < 0.005:
        spawn_heal()
    if random.random() < 0.005:
        spawn_ammo()
    if random.random() < 0.1:
        spawn_asteroid()

    if playerx > WIDTH:
        playerx = -10
    elif playerx < 0:
        playerx = WIDTH + 10
    if playery > HEIGHT:
        playery = -10
    elif playery < 0:
        playery = HEIGHT + 10

    # BULLET MOVEMENT
    new_bullets = []
    for bx, by, angle in bullets:
        bx += bullet_speed * math.cos(math.radians(angle))
        by -= bullet_speed * math.sin(math.radians(angle))
        if 0 <= bx <= WIDTH and 0 <= by <= HEIGHT:
            new_bullets.append((bx, by, angle))
    bullets = new_bullets

    # ASTEROID MOVEMENT AND COLLISION
    new_asteroids = []
    for ax, ay, size in asteroids:
        ay += asteroid_speed
        if ay < HEIGHT + size:  # Make sure the asteroid stays within screen bounds
            new_asteroids.append((ax, ay, size))
    asteroids = new_asteroids

    # HEALTH PACK MOVEMENT AND PICKUP
    new_heals = []
    for hx, hy in heals:
        hy += pickup_speed
        if hy < HEIGHT:
            if check_collision(hx, hy, playerx, playery, 20, playerwidth):
                health += 1  # Increase health if player picks up
            else:
                new_heals.append((hx, hy))
    heals = new_heals

    # AMMO PACK MOVEMENT AND PICKUP
    new_ammos = []
    for amx, amy in ammos:
        amy += pickup_speed
        if amy < HEIGHT:
            if check_collision(amx, amy, playerx, playery, 10, playerwidth):
                ammo += 5  # Increase ammo if player picks up
            else:
                new_ammos.append((amx, amy))
    ammos = new_ammos

    # DRAWING
    screen.fill((0, 0, 51))  # Background color
    draw_player()
    for bx, by, _ in bullets:
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

pygame.quit()
