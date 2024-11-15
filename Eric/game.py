import pygame
import random
import math
pygame.init()

WIDTH = 1100
HEIGHT = 750
SIZE = (WIDTH, HEIGHT)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
easy_button = pygame.Rect(WIDTH // 4 - 50, HEIGHT // 2 - 25, 100, 50)
medium_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
hard_button = pygame.Rect(3 * WIDTH // 4 - 50, HEIGHT // 2 - 25, 100, 50)

difficulty = None
star_count = 100
stars = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT), "size": random.randint(1, 3)} for _ in range(star_count)]


def draw_buttons():
    pygame.draw.rect(screen, GREEN, easy_button)
    pygame.draw.rect(screen, YELLOW, medium_button)
    pygame.draw.rect(screen, RED, hard_button)
    font = pygame.font.Font(None, 36)
    easy_text = font.render("Easy", True, BLACK)
    medium_text = font.render("Medium", True, BLACK)
    hard_text = font.render("Hard", True, BLACK)
    screen.blit(easy_text, (easy_button.x + 20, easy_button.y + 15))
    screen.blit(medium_text, (medium_button.x-5 + 10, medium_button.y + 15))
    screen.blit(hard_text, (hard_button.x + 20, hard_button.y + 15))

# Difficulty selection screen
selecting_difficulty = True
while selecting_difficulty:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if easy_button.collidepoint(event.pos):
                difficulty = 'easy'
                selecting_difficulty = False
            elif medium_button.collidepoint(event.pos):
                difficulty = 'medium'
                selecting_difficulty = False
            elif hard_button.collidepoint(event.pos):
                difficulty = 'hard'
                selecting_difficulty = False

    screen.fill(BLACK)
    draw_buttons()
    pygame.display.flip()
    clock.tick(30)
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
asteroid_speed = 5
pickup_speed = 2  # Slower speed for health and ammo packs
bullets = []
asteroids = []
asteroids2 = []
heals = []
ammos = []
superpowers = []
supercounter = 0
player_angle = 0  # Initial angle facing up
score = 0
bonus_size = 0
# ---------------------------
pygame.display.set_caption('Space Defender')
font = pygame.font.Font('freesansbold.ttf', 15)
fontbonus = pygame.font.Font('freesansbold.ttf', 50)
ENDFONT = pygame.font.Font('freesansbold.ttf', 100)
ENDSCORE = pygame.font.Font('freesansbold.ttf', 50)
running = True
def spawn_superpower():
    x = random.randint(0, WIDTH)
    y = -20
    superpowers.append((x, y))
def spawn_asteroid():
    x = random.randint(0, WIDTH)
    y = -20
    size = random.randint(20, 40)
    asteroids.append((x, y, size))
def spawn_asteroid2():
    x = -20
    y = random.randint(0, HEIGHT)
    size = random.randint(20, 40)
    asteroids2.append((x, y, size))
def draw_asteroid(x, y, size):
    points = [(x + math.cos(math.radians(angle)) * size, y + math.sin(math.radians(angle)) * size)
              for angle in range(0, 360, 60)]
    pygame.draw.polygon(screen, (169, 169, 169), points)
def draw_asteroid2(x, y, size):
    points = [(x + math.sin(math.radians(angle)) * size, y + math.cos(math.radians(angle)) * size)
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
def draw_superpower(x, y):
    pygame.draw.circle(screen, (0, 0, 205), (x, y), 20)
    pygame.draw.polygon(screen,(random.randint(0, 205), random.randint(0, 205), random.randint(0, 205)), [(x, y+10), (x+8, y-8), (x, y), (x-8,y-8)] )
def drawammo(x, y, counter= int(0)):
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
def display_bonus(text, x, y, color=(255, bonus_size, bonus_size)):
    label = fontbonus.render(text, True, color)
    screen.blit(label, (x, y))

while running:
    # EVENT HANDLING
    keys = (pygame.key.get_pressed
            ())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ammo > 0:
                bullets.append((playerx, playery, player_angle))
                ammo -= 1
    fontbonus = pygame.font.Font('freesansbold.ttf', bonus_size)
    # MOVEMENT
    if supercounter <= 0:
        if keys[pygame.K_a]:
            playerx -= move_speed
            player_angle += 10
        if keys[pygame.K_d]:
            playerx += move_speed
            player_angle -= 10
        if keys[pygame.K_w]:
            playery -= move_speed
            player_angle += 10
        if keys[pygame.K_s]:
            playery += move_speed
            player_angle -= 10
    else:
        player_angle += 36
        bullets.append((playerx, playery, player_angle))
        playerx += 7

    # SPAWNING LOGIC
    if difficulty == 'easy':
        if random.random() < 0.006:
            spawn_heal()
        if random.random() < 0.006:
            spawn_ammo()
        if random.random() < 0.03:
            spawn_asteroid()
        if random.random() < 0.02:
            spawn_asteroid2()
        if random.random() < 0.03:
            spawn_superpower()
    elif difficulty == 'medium':
        asteroid_speed = 8
        if random.random() < 0.006:
            spawn_heal()
        if random.random() < 0.006:
            spawn_ammo()
        if random.random() < 0.04:
            spawn_asteroid()
        if random.random() < 0.08:
            spawn_asteroid2()
        if random.random() < 0.005:
            spawn_superpower()
    elif difficulty == 'hard':
        asteroid_speed = 9
        if random.random() < 0.005:
            spawn_heal()
        if random.random() < 0.005:
            spawn_ammo()
        if random.random() < 0.1:
            spawn_asteroid()
        if random.random() < 0.1:
            spawn_asteroid2()
        if random.random() < 0.005:
            spawn_superpower()
    if playerx > WIDTH:
        playerx = -10
    elif playerx < 0:
        playerx = WIDTH + 10
    if playery > HEIGHT:
        playery = -10
    elif playery < 0:
        playery = HEIGHT + 10


    new_bullets = []
    for bx, by, angle in bullets:
        bx += bullet_speed * math.cos(math.radians(angle))
        by -= bullet_speed * math.sin(math.radians(angle))

        bullet_hit = False
        for ax, ay, size in asteroids:
            if check_collision(bx, by, ax, ay, 10, size):
                bullet_hit = True
                asteroids.remove((ax, ay, size))
                score += 200
                if bonus_size<=0:
                    bonus_size = 50
                break
        for ax, ay, size in asteroids2:
            if check_collision(bx, by, ax, ay, 10, size):
                bullet_hit = True
                asteroids2.remove((ax, ay, size))
                score += 200
                if bonus_size <= 0:
                    bonus_size = 50
                break

        if not bullet_hit:
            if 0 <= bx <= WIDTH and 0 <= by <= HEIGHT:
                new_bullets.append((bx, by, angle))

    bullets = new_bullets
    # ASTEROID MOVEMENT AND COLLISION
    new_asteroids = []
    for ax, ay, size in asteroids:
        ay += asteroid_speed
        if check_collision(ax, ay, playerx, playery, size, playerwidth):
            health -= 1
            continue

        if ay < HEIGHT + size:
            new_asteroids.append((ax, ay, size))
    asteroids = new_asteroids

    new_asteroids2 = []
    for ax2, ay2, size2 in asteroids2:
        ax2 += asteroid_speed
        if check_collision(ax2, ay2, playerx, playery, size2, playerwidth):
            health -= 1
            continue
        if ax2 < WIDTH + size2:
            new_asteroids2.append((ax2, ay2, size2))
    asteroids2 = new_asteroids2
    supercounter -= 1

    new_heals = []
    for hx, hy in heals:
        hy += pickup_speed
        if hy < HEIGHT:
            if check_collision(hx, hy, playerx, playery, 20, playerwidth):
                health += 1
            else:
                new_heals.append((hx, hy))
    heals = new_heals
    new_superpowers = []
    for sx, sy in superpowers:
        sy += pickup_speed
        if sy < HEIGHT:
            if check_collision(sx, sy, playerx, playery, 20, playerwidth):
                supercounter = 20
            else:
                new_superpowers.append((sx, sy))
    superpowers = new_superpowers
    # AMMO PACK MOVEMENT AND PICKUP
    new_ammos = []
    for amx, amy in ammos:
        amy += pickup_speed
        if amy < HEIGHT:
            if check_collision(amx, amy, playerx, playery, 10, playerwidth):
                ammo += 5
            else:
                new_ammos.append((amx, amy))
    ammos = new_ammos

    screen.fill((0, 0, 51))
    draw_player()
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (star["x"], star["y"]), 2)
    for bx, by, _ in bullets:
        draw_bullet(bx, by)
    for ax, ay, size in asteroids:
        draw_asteroid(ax, ay, size)
    for ax, ay, size in asteroids2:
        draw_asteroid2(ax, ay, size)
    for hx, hy in heals:
        drawheal(hx, hy)
    for amx, amy in ammos:
        drawammo(amx, amy)
    for sx, sy in superpowers:
        draw_superpower(sx, sy)

    # HUD
    display_text(f'Health: {health}', 10, 10)
    display_text(f'Ammo: {ammo}', 10, 30)
    display_text(f'Score: {score}', 10, 50)
    if bonus_size>0:
        display_bonus('+200', WIDTH/2, HEIGHT/2)
    bonus_size-=2
    score+=1
    if health<=0:
        break
    pygame.display.flip()
    clock.tick(30)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 51))
    ENDTEXT = ENDFONT.render("GAME OVER", True, (255, 0, 0))
    screen.blit(ENDTEXT, (10, 40))
    ENDTEXT = ENDSCORE.render(f"YOUR SCORE: {score}", True, (255, 0, 0))
    screen.blit(ENDTEXT,(10, 200))
    clock.tick(30)
    pygame.display.flip()
