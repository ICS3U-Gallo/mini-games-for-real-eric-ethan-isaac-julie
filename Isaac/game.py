import pygame
import random
import math

pygame.init()

WIDTH = 1280
HEIGHT = 960
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# Initialize global variables

placeholder = 0
game_state = "start_menu"


spaceship_width = 10
spaceship_height = 15
spaceship_x = WIDTH // 2 - spaceship_width // 2
spaceship_y = HEIGHT // 2 - spaceship_height // 2
spaceship_speed = 10
bullet_width = 2
bullet_height = 5
bullet_color = (225, 0, 0)
bullet_speed = 50
bullet_speed2 = 15
bullet_speed3 = 40
bullets = [] 
bullets2 = []
bullets3 = []


radius3 = 0.5
counter3 = 0
spaceship_angle = 0 
rotation_speed = 2.5
# enemies
enemy_width = random.randrange(10, 40)
enemy_height = random.randrange(10, 40)
enemy_color = (0, 0, 255)
enemy_bullet_color = (255, 0, 0)
enemy_speed = 2 
enemy_bullet_speed = 10
enemy_bullets = []
enemies = []
enemy_num = 0
enemy_health = 20
width_enemy_health = enemy_width

dmg_bullet1 = width_enemy_health / enemy_health
dmg_bullet2 = (width_enemy_health / enemy_health) * 4
dmg_bullet3 = (width_enemy_health / enemy_health) * 7.5

player_health = 5
health_width = 10



# Function to get random direction
def get_random_direction():
    angle = random.uniform(0, 2 * math.pi)
    return math.cos(angle), math.sin(angle)

# Spawn enemies at random positions with random directions
while enemy_num != 15:
    enemy_x = random.randint(0, WIDTH - enemy_width)
    enemy_y = random.randint(0, HEIGHT // 2)
    direction = get_random_direction()
    enemy_hp = 3  # Assign a health value to each enemy (default: 3 HP)
    enemies.append([enemy_x, enemy_y, direction[0], direction[1], enemy_hp])
    enemy_num += 1


# Bullet class for handling bullet movement
class Bullet:
    def __init__(self, x, y, angle, speed, radius=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.radius = radius

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

running = True
# Main game loop
while running:
    if game_state == "game over":
        pygame.quit()
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:  # Right click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle_to_mouse = math.atan2(mouse_y - spaceship_y, mouse_x - spaceship_x)
            bullet2 = Bullet(spaceship_x, spaceship_y, angle_to_mouse, bullet_speed2)
            bullets2.append(bullet2)
        if event.button == 1:  # Left click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle_to_mouse = math.atan2(mouse_y - spaceship_y, mouse_x - spaceship_x)
            bullet = Bullet(spaceship_x, spaceship_y, angle_to_mouse, bullet_speed)
            bullets.append(bullet)
        if event.button == 2:  # Middle click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle_to_mouse = math.atan2(mouse_y - spaceship_y, mouse_x - spaceship_x)
            bullet3 = Bullet(spaceship_x, spaceship_y, angle_to_mouse, bullet_speed3, radius3)
            bullets3.append(bullet3)
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            spaceship_speed = 25
        if event.key == pygame.K_h:
            pygame.time.delay(1000)
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            spaceship_speed = 10

    # GAME STATE UPDATES
    keys = pygame.key.get_pressed()


    # Move spaceship
    if keys[pygame.K_w]: 
        spaceship_x += spaceship_speed * math.sin(math.radians(spaceship_angle)) 
        spaceship_y -= spaceship_speed * math.cos(math.radians(spaceship_angle)) 
    if keys[pygame.K_s]: 
        spaceship_x -= spaceship_speed * math.sin(math.radians(spaceship_angle)) 
        spaceship_y += spaceship_speed * math.cos(math.radians(spaceship_angle)) 
    if keys[pygame.K_a]: 
        spaceship_x -= spaceship_speed * math.cos(math.radians(spaceship_angle)) 
        spaceship_y -= spaceship_speed * math.sin(math.radians(spaceship_angle)) 
    if keys[pygame.K_d]: 
        spaceship_x += spaceship_speed * math.cos(math.radians(spaceship_angle)) 
        spaceship_y += spaceship_speed * math.sin(math.radians(spaceship_angle))
    # rotate spaceship
    if keys[pygame.K_e]: 
        spaceship_angle += rotation_speed 
    if keys[pygame.K_q]: 
        spaceship_angle -= rotation_speed
    if spaceship_x > 1280:
        spaceship_x = 0
    if spaceship_x < 0:
        spaceship_x = 1280
    if spaceship_y > 960:
        spaceship_y = 0
    if spaceship_y < 0:
        spaceship_y = 960

    # Update bullet positions
    for bullet in bullets:
        bullet.move()
    for bullet in bullets2:
        bullet.move()
    for bullet in bullets3:
        bullet.move()
    # Change radius of bullet
    if radius3 > 0:
        radius3 += 20
    if radius3 > 50:
        radius3 = 1

    # Move enemies and shoot bullets towards the player
    for enemy in enemies[:]:  # Iterate over a copy of the list
        # Move enemy
        enemy[0] += enemy[2] * enemy_speed
        enemy[1] += enemy[3] * enemy_speed
        
        # Bounce off walls
        if enemy[0] < 0 or enemy[0] > WIDTH - enemy_width:
            enemy[2] = -enemy[2]
        if enemy[1] < 0 or enemy[1] > HEIGHT - enemy_height:
            enemy[3] = -enemy[3]
        
        # Check for collision with spaceship
        if (spaceship_x < enemy[0] + enemy_width and
            spaceship_x + spaceship_width > enemy[0] and
            spaceship_y < enemy[1] + enemy_height and
            spaceship_y + spaceship_height > enemy[1]):
            # Remove enemy upon collision
            enemies.remove(enemy)
        
        # Randomly shoot bullets towards the player
        if random.randint(1, 60) == 1:
            angle_to_player = math.atan2(spaceship_y - enemy[1], spaceship_x - enemy[0])
            enemy_bullet_x = enemy[0] + enemy_width // 2
            enemy_bullet_y = enemy[1] + enemy_height // 2
            enemy_bullets.append([enemy_bullet_x, enemy_bullet_y, angle_to_player])

    # Check for bullet collision with enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (bullet.x < enemy[0] + enemy_width and bullet.x > enemy[0] and
                bullet.y < enemy[1] + enemy_height and bullet.y > enemy[1]):
                # Decrease enemy HP
                enemy_health -= 1  
                width_enemy_health -= dmg_bullet1
                bullets.remove(bullet)  # Remove the bullet upon collision
                if width_enemy_health <= 0:  # If enemy HP is 0 or below, remove the enemy
                    enemies.remove(enemy)
    for bullet2 in bullets2[:]:
        for enemy in enemies[:]:
            if (bullet.x < enemy[0] + enemy_width and bullet.x > enemy[0] and
                bullet.y < enemy[1] + enemy_height and bullet.y > enemy[1]):
                # Decrease enemy HP
                enemy_health -= 4
                width_enemy_health -= dmg_bullet2
                bullets2.remove(bullet2)  # Remove the bullet upon collision
                if enemy_health <= 0:  # If enemy HP is 0 or below, remove the enemy
                    enemies.remove(enemy)
    for bullet3 in bullets3[:]:
        for enemy in enemies[:]:
            if (bullet.x < enemy[0] + enemy_width and bullet.x > enemy[0] and
                bullet.y < enemy[1] + enemy_height and bullet.y > enemy[1]):
                # Decrease enemy HP
                enemy_health -= 7.5
                width_enemy_health -= dmg_bullet3
                bullets3.remove(bullet3)  # Remove the bullet upon collision
                if enemy_health <= 0:  # If enemy HP is 0 or below, remove the enemy
                    enemies.remove(enemy)

    # Update enemy bullet positions
    for enemy_bullet in enemy_bullets:
        enemy_bullet[0] += enemy_bullet_speed * math.cos(enemy_bullet[2])
        enemy_bullet[1] += enemy_bullet_speed * math.sin(enemy_bullet[2])
        # Remove bullets that go off the screen
        if enemy_bullet[1] > HEIGHT or enemy_bullet[1] < 0 or enemy_bullet[0] > WIDTH or enemy_bullet[0] < 0:
            enemy_bullets.remove(enemy_bullet)
    # Update enemy bullet positions and check for collision with spaceship
    for enemy_bullet in enemy_bullets[:]:
        enemy_bullet[0] += enemy_bullet_speed * math.cos(enemy_bullet[2])
        enemy_bullet[1] += enemy_bullet_speed * math.sin(enemy_bullet[2])
        
        # Remove bullets that go off the screen
        if enemy_bullet[1] > HEIGHT or enemy_bullet[1] < 0 or enemy_bullet[0] > WIDTH or enemy_bullet[0] < 0:
            enemy_bullets.remove(enemy_bullet)

        # Check for collision with spaceship
        if (spaceship_x < enemy_bullet[0] + bullet_width and
            spaceship_x + spaceship_width > enemy_bullet[0] and
            spaceship_y < enemy_bullet[1] + bullet_height and
            spaceship_y + spaceship_height > enemy_bullet[1]):
            player_health -= 1
            health_width -= 2
            if player_health == 0:
                game_state = "game over"
            

        # DRAWING
    screen.fill((0, 0, 0))  # always the first drawing command
    pygame.draw.polygon(screen, (255, 255, 255), [(spaceship_x, spaceship_y), (spaceship_x, spaceship_y + spaceship_height), (spaceship_x + spaceship_width, spaceship_y), (spaceship_x + spaceship_width, spaceship_y + spaceship_height)], 0)
    pygame.draw.rect(screen, (0, 225, 0), (spaceship_x, spaceship_y, health_width, 5), 0)
    # Player bullet code
    for bullet in bullets:
        pygame.draw.circle(screen, bullet_color, (bullet.x, bullet.y), 3)
    for bullet in bullets2:
        pygame.draw.circle(screen, (0, 0, 255), (bullet.x, bullet.y), 10)
        pygame.draw.rect(screen, (3, 37, 126), (bullet.x - 6, bullet.y - 6, 12, 12), 1)
        pygame.draw.line(screen, (3, 37, 126), (bullet.x + 12, bullet.y + 12), (bullet.x - 12, bullet.y - 12), 3)
        pygame.draw.line(screen, (3, 37, 126), (bullet.x, bullet.y + 12), (bullet.x + 12, bullet.y), 3)

    for bullet in bullets3:
        pygame.draw.circle(screen, (255, 0, 255), (bullet.x, bullet.y), radius3)
        

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, enemy_color, (enemy[0], enemy[1], enemy_width, enemy_height))
        pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1] - 10, width_enemy_health, 5))

    # Draw enemy bullets
    for enemy_bullet in enemy_bullets:
        pygame.draw.rect(screen, enemy_bullet_color, (enemy_bullet[0], enemy_bullet[1], bullet_width, bullet_height))

    # Must be the last two lines of the game loop
    pygame.display.flip()
    clock.tick(30)
        
pygame.quit()
