import pygame
import random
import time
import math

pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

player_x = WIDTH // 2
player_y = HEIGHT - 150
player_width = 50
player_height = 50
move_speed = 5
sprint_speed = 10
swinging_sword = False
swing_start_time = 0
swing_duration = 0.5
space_released = True
eye_width = 5
eye_height = 5
eye_offset_x = 10
eye_offset_y = 10
left_eye_x = player_x + eye_offset_x
right_eye_x = player_x + eye_offset_x + 15
left_eye_y = player_y + eye_offset_y
right_eye_y = player_y + eye_offset_y
sword_width = 60
sword_height = 30
sword_body_width = 20
sword_body_height = 30
sword_tip_width = 40
sword_tip_height = 30
sword_body_x = None
sword_body_y = None
sword_tip = None
sword_base1 = None
sword_base2 = None
looking_left = None
enemy_eye_width = 5
enemy_eye_height = 5
enemy_eye_offset_x = 10
enemy_eye_offset_y = 10
player_auto_attack_range = 200
enemy_sword_body_width = 20
enemy_sword_body_height = 30
flash_slope = 0.5
player_health = 100
shift_pressed = False
shift_released = True
shift_start_time = 0
current_speed = move_speed
a_pressed = False
d_pressed = False
dodge_speed = 50

enemies = [
    {"x": 100, "y": HEIGHT - 150, "width": 50, "height": 50, "speed": 2, "health": 100, "attack_start_time": 0, "looking_left": True},
    {"x": 300, "y": HEIGHT - 150, "width": 50, "height": 50, "speed": 3, "health": 100, "attack_start_time": 0, "looking_left": False},
    {"x": 500, "y": HEIGHT - 150, "width": 50, "height": 50, "speed": 4, "health": 100, "attack_start_time": 0, "looking_left": True},
]

enemy_hit = False

font = pygame.font.Font(None, 36)

damage_numbers = []

def insert_damage_number(damage, x, y):
    offset_x = random.randint(-20, 20)
    offset_y = random.randint(-20, 20)
    damage_numbers.append({"damage": damage, "x": x + offset_x, "y": y + offset_y, "timestamp": time.time()})

def find_closest_enemy(player_x, enemies):
    closest_enemy = None
    min_distance = float('inf')
    for enemy in enemies:
        distance = abs(player_x - enemy["x"])
        if distance < player_auto_attack_range and distance < min_distance:
            min_distance = distance
            closest_enemy = enemy
    
    if closest_enemy:
        look_left = closest_enemy["x"] < player_x
    else:
        look_left = looking_left

    return look_left, closest_enemy

def dodge():
    global player_x, player_y
    if not a_pressed and not d_pressed:
        if looking_left:
            player_x += dodge_speed
        else:
            player_x -= dodge_speed
    else:
        if a_pressed:
            player_x -= dodge_speed
        if d_pressed:
            player_x += dodge_speed


# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            space_released = True

    keys = pygame.key.get_pressed()
    a_pressed = keys[pygame.K_a]
    d_pressed = keys[pygame.K_d]

    if keys[pygame.K_SPACE] and not swinging_sword and space_released:
        swinging_sword = True
        swing_start_time = time.time()
        space_released = False
        enemy_hit = False

        look_left, closest_enemy = find_closest_enemy(player_x, enemies)
        if closest_enemy:
            looking_left = look_left
            player_x = closest_enemy["x"] + 50 if looking_left else closest_enemy["x"] - 50
            
    elif swinging_sword and time.time() - swing_start_time >= swing_duration:
        swinging_sword = False

    if keys[pygame.K_LSHIFT]:
        if not shift_pressed:
            if not a_pressed and not d_pressed:
                dodge()
            else:
                shift_start_time = time.time()
            shift_pressed = True
            shift_released = False
        if time.time() - shift_start_time > 0.2:
            current_speed = sprint_speed
    else:
        shift_pressed = False
        current_speed = move_speed

    if not shift_pressed and not shift_released:
        if time.time() - shift_start_time <= 0.2:
            dodge()
        shift_released = True

    if a_pressed:
        looking_left = True
        player_x -= current_speed
        
    if d_pressed:
        looking_left = False
        player_x += current_speed

    if looking_left:
        left_eye_x = player_x + eye_offset_x
        right_eye_x = player_x + eye_offset_x + 15
        sword_body_x = player_x - sword_body_width
        sword_body_y = player_y + (player_height // 2) - (sword_body_height // 2)
        sword_tip = (player_x - sword_tip_width, player_y + player_height // 2)
        sword_base1 = (player_x - sword_body_width, player_y + player_height // 2 - sword_tip_height // 2)
        sword_base2 = (player_x - sword_body_width, player_y + player_height // 2 + sword_tip_height // 2)
    else:
        left_eye_x = player_x + player_width - eye_offset_x - eye_width - 15
        right_eye_x = player_x + player_width - eye_offset_x - eye_width
        sword_body_x = player_x + player_width
        sword_body_y = player_y + (player_height // 2) - (sword_body_height // 2)
        sword_tip = (player_x + player_width + sword_tip_width, player_y + player_height // 2)
        sword_base1 = (player_x + player_width + sword_body_width, player_y + player_height // 2 - sword_tip_height // 2)
        sword_base2 = (player_x + player_width + sword_body_width, player_y + player_height // 2 + sword_tip_height // 2)

    for enemy in enemies:
        if random.randint(0, 300) == 0:
            enemy["attack_start_time"] = time.time()

    if swinging_sword and not enemy_hit:
        sword_rect = pygame.Rect(sword_body_x, sword_body_y, sword_body_width, sword_body_height)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy["width"], enemy["height"])
            if sword_rect.colliderect(enemy_rect):
                enemy["health"] -= 10
                if enemy["health"] <= 0:
                    enemies.remove(enemy)
                insert_damage_number(10, enemy["x"], enemy["y"])
                enemy_hit = True

    for enemy in enemies:
        enemy["time_elapsed"] = time.time() - enemy["attack_start_time"]
        if 0.5 <= enemy["time_elapsed"] <= 1:
            if enemy["looking_left"]:
                enemy["sword_body_x"] = enemy["x"] - sword_body_width
                enemy["sword_body_y"] = enemy["y"] + (enemy["height"] // 2) - (sword_body_height // 2)
                enemy["sword_tip"] = (enemy["x"] - sword_tip_width, enemy["y"] + enemy["height"] // 2)
                enemy["sword_base1"] = (enemy["x"] - sword_body_width, enemy["y"] + enemy["height"] // 2 - sword_tip_height // 2)
                enemy["sword_base2"] = (enemy["x"] - sword_body_width, enemy["y"] + enemy["height"] // 2 + sword_tip_height // 2)
            else:
                enemy["sword_body_x"] = enemy["x"] + enemy["width"]
                enemy["sword_body_y"] = enemy["y"] + (enemy["height"] // 2) - (sword_body_height // 2)
                enemy["sword_tip"] = (enemy["x"] + enemy["width"] + sword_tip_width, enemy["y"] + enemy["height"] // 2)
                enemy["sword_base1"] = (enemy["x"] + enemy["width"] + sword_body_width, enemy["y"] + enemy["height"] // 2 - sword_tip_height // 2)
                enemy["sword_base2"] = (enemy["x"] + enemy["width"] + sword_body_width, enemy["y"] + enemy["height"] // 2 + sword_tip_height // 2)

            if 0.5 <= enemy["time_elapsed"] <= 0.6:
                enemy_sword_rect = pygame.Rect(enemy["sword_body_x"], enemy["sword_body_y"], enemy_sword_body_width, enemy_sword_body_height)
                if not enemy["hit_player"] and enemy_sword_rect.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                    enemy["hit_player"] = True
                    player_health -= 10
                    insert_damage_number(10, player_x, player_y)
        else:
            enemy["hit_player"] = False

    print("shift_pressed:", shift_pressed)
    print("shift_released:", shift_released)
    print("current_speed:", current_speed)

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # DRAWING
    screen.fill((0, 128, 128))  # always the first drawing command

    pygame.draw.rect(screen, (210, 180, 140), (0, HEIGHT - 100, WIDTH, 100))

    for enemy in enemies:
        pygame.draw.rect(screen, (0, 255, 0), (enemy["x"], enemy["y"], enemy["width"], enemy["height"]))
        health_bar_width = enemy["width"] * (enemy["health"] / 100)
        pygame.draw.rect(screen, (255, 0, 0), (enemy["x"], enemy["y"] - 10, health_bar_width, 5))
 
        if enemy["looking_left"]:
            enemy_left_eye_x = enemy["x"] + enemy_eye_offset_x
            enemy_right_eye_x = enemy["x"] + enemy_eye_offset_x + 15
            enemy_eye_y = enemy["y"] + enemy_eye_offset_y
        else:
            enemy_left_eye_x = enemy["x"] + enemy["width"] - enemy_eye_offset_x - enemy_eye_width - 15
            enemy_right_eye_x = enemy["x"] + enemy["width"] - enemy_eye_offset_x - enemy_eye_width
            enemy_eye_y = enemy["y"] + enemy_eye_offset_y

        pygame.draw.rect(screen, (0, 0, 0), (enemy_left_eye_x, enemy_eye_y, enemy_eye_width, enemy_eye_height))
        pygame.draw.rect(screen, (0, 0, 0), (enemy_right_eye_x, enemy_eye_y, enemy_eye_width, enemy_eye_height))

        if enemy["time_elapsed"] < 1:
            if enemy["time_elapsed"] <= 0.3:
                flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                enemy_left_eye_x += enemy_eye_width // 2
                enemy_eye_y += enemy_eye_height // 2
                flash_length = 50 * math.sin(10.471975512 * enemy["time_elapsed"] - 0.15)
                pygame.draw.line(flash_surface, (255, 0, 0, 200), (enemy_left_eye_x - flash_length, enemy_eye_y + flash_length * flash_slope), (enemy_left_eye_x + flash_length, enemy_eye_y - flash_length * flash_slope), 5)
                pygame.draw.line(flash_surface, (255, 0, 0, 200), (enemy_left_eye_x - flash_length / 2, enemy_eye_y + flash_length * -1), (enemy_left_eye_x + flash_length / 2, enemy_eye_y - flash_length * -1), 5)
                screen.blit(flash_surface, (0, 0))
            elif enemy["time_elapsed"] >= 0.5:
                pygame.draw.rect(screen, (192, 192, 192), (enemy["sword_body_x"], enemy["sword_body_y"], enemy_sword_body_width, enemy_sword_body_height))
                pygame.draw.polygon(screen, (192, 192, 192), [enemy["sword_tip"], enemy["sword_base1"], enemy["sword_base2"]])

    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height))
    health_bar_width = player_width * player_health / 100
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y - 10, health_bar_width, 5))

    pygame.draw.rect(screen, (0, 0, 0), (left_eye_x, left_eye_y, eye_width, eye_height))
    pygame.draw.rect(screen, (0, 0, 0), (right_eye_x, right_eye_y, eye_width, eye_height))

    if swinging_sword:
        pygame.draw.rect(screen, (192, 192, 192), (sword_body_x, sword_body_y, sword_body_width, sword_body_height))
        pygame.draw.polygon(screen, (192, 192, 192), [sword_tip, sword_base1, sword_base2])

    damage_numbers = [dn for dn in damage_numbers if time.time() - dn["timestamp"] < 1]
    for dn in damage_numbers:
        damage_text = font.render(str(dn["damage"]), True, (255, 255, 255))
        screen.blit(damage_text, (dn["x"], dn["y"]))
        
    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(120)
    #---------------------------


pygame.quit()
