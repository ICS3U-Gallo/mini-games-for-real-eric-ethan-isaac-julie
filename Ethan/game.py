import pygame
import random
import time
import math
import string

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
sword_width = 50
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
looking_left = False
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
dodge_press_duration = 0.2
last_dodge_time = 0
perfect_dodge_time = 0
dodge_left = None
time_scale = 1
perfect_dodge_enemy = None
last_teleport_time = 0
player_angle = 0
sword_rect = pygame.Rect(0, 0, 0, 0)
charged = False

enemies = [
    {"id": 1, "x": 100, "y": HEIGHT - 150, "width": 50, "height": 50, "speed": 2, "health": 100, "attack_start_time": 0, "looking_left": True},
    {"id": 2, "x": 300, "y": HEIGHT - 150, "width": 50, "height": 50, "speed": 3, "health": 100, "attack_start_time": 0, "looking_left": False},
    {"id": 3, "x": 500, "y": HEIGHT - 150, "width": 50, "height": 50, "speed": 4, "health": 100, "attack_start_time": 0, "looking_left": True},
]

enemy_hit = False

font = pygame.font.Font(None, 36)

damage_numbers = []

enemies_in_flash = []

def insert_damage_number(damage, x, y, to_player):
    offset_x = random.randint(-25, 25)
    offset_y = random.randint(-25, 25)
    damage_numbers.append({"damage": damage, "x": x + offset_x, "y": y + offset_y, "timestamp": time.time(), "to_player": to_player})

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
    global player_x, player_y, last_dodge_time, dodge_left, perfect_dodge_time, perfect_dodge_enemy
    if time.time() - last_dodge_time < 0.5:
        return
    dodge_left = None
    if not a_pressed and not d_pressed:
        if looking_left:
            dodge_left = False
        else:
            dodge_left = True
    else:
        if a_pressed:
            dodge_left = True
        if d_pressed:
            dodge_left = False

    start_perfect_dodge = False
    if dodge_left:
        for enemy_id in enemies_in_flash:
            for enemy in enemies:
                if enemy["id"] == enemy_id and enemy["looking_left"]:
                    start_perfect_dodge = True
                    
    else:
        for enemy_id in enemies_in_flash:
            for enemy in enemies:
                if enemy["id"] == enemy_id and not enemy["looking_left"]:
                    start_perfect_dodge = True

    if start_perfect_dodge:
        perfect_dodge_time = time.time()           
        perfect_dodge_enemy = enemy
        for enemy in enemies:
            if enemy["id"] in enemies_in_flash:
                enemy["attack_start_time"] -= 4 * (perfect_dodge_time - enemy["attack_start_time"])
        print("Perfect dodge!")

    if time.time() - perfect_dodge_time > 1:
        if dodge_left:
            player_move_to(player_x - dodge_speed, player_y)
        else:
            player_move_to(player_x + dodge_speed, player_y)

    last_dodge_time = time.time()

def move_enemy_forward(enemy, amount):
    if enemy["looking_left"]:
        enemy["x"] -= amount / time_scale
    else:
        enemy["x"] += amount / time_scale

def random_enemy_id():
    return ''.join(random.choices(string.ascii_letters, k=7))

def draw_player():
    global player_angle, sword_rect
    player_surface = pygame.Surface((player_width + sword_width, player_height), pygame.SRCALPHA)
    # pygame.draw.rect(player_surface, (210, 180, 140), (0, 0, player_width + sword_width, player_height))
    if looking_left:
        pygame.draw.rect(player_surface, (0, 0, 255), (sword_width, 0, player_width, player_height))
        pygame.draw.rect(player_surface, (0, 0, 0), (eye_offset_x + sword_width, eye_offset_y, eye_width, eye_height))
        pygame.draw.rect(player_surface, (0, 0, 0), (eye_offset_x + sword_width + 15, eye_offset_y, eye_width, eye_height))
    else:
        pygame.draw.rect(player_surface, (0, 0, 255), (0, 0, player_width, player_height))
        pygame.draw.rect(player_surface, (0, 0, 0), (player_width - eye_offset_x - eye_width, eye_offset_y, eye_width, eye_height))
        pygame.draw.rect(player_surface, (0, 0, 0), (player_width - eye_offset_x - eye_width - 15, eye_offset_y, eye_width, eye_height))

    if swinging_sword:
        if looking_left:
            sword_x = sword_width - sword_body_width
            sword_y = (player_height // 2) - (sword_body_height // 2)
            pygame.draw.rect(player_surface, (192, 192, 192), (sword_x, sword_y, sword_body_width, sword_body_height))
            pygame.draw.polygon(player_surface, (192, 192, 192), [(sword_width - sword_tip_width, player_height // 2), (sword_x, player_height // 2 - sword_tip_height // 2), (sword_x, player_height // 2 + sword_tip_height // 2)])
        else:
            sword_x = player_width
            sword_y = (player_height // 2) - (sword_body_height // 2)
            pygame.draw.rect(player_surface, (192, 192, 192), (sword_x, sword_y, sword_body_width, sword_body_height))
            pygame.draw.polygon(player_surface, (192, 192, 192), [(player_width + sword_tip_width, player_height // 2), (player_width + sword_body_width, player_height // 2 - sword_tip_height // 2), (player_width + sword_body_width, player_height // 2 + sword_tip_height // 2)])

    rotated_player_surface = pygame.transform.rotate(player_surface, player_angle)
    
    angle_offset = 0
    if looking_left:
        angle_offset = -90
    else:
        angle_offset = +90
    center = (player_x + player_width // 2 + math.sin((player_angle + angle_offset) * math.pi / 180) * player_height // 2, player_y + player_height // 2 + math.cos((player_angle + angle_offset) * math.pi / 180) * player_height // 2)
    
    rotated_rect = rotated_player_surface.get_rect(center=center)
    
    screen.blit(rotated_player_surface, rotated_rect.topleft)
    # pygame.draw.circle(screen, (255, 0, 0), (player_x, player_y), 5)
    # pygame.draw.circle(screen, (255, 0, 0), center, 5)
    sword_rect = rotated_rect
    # print(center)

def player_move_to(x, y, pa=0):
    global player_x, player_y, player_angle
    player_x = x
    player_y = y
    player_angle = pa
    print(f"Player: {player_x}, {player_y}")

def swing(damage=10):
    global enemy_hit

    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy["width"], enemy["height"])
        if sword_rect.colliderect(enemy_rect):
            enemy["health"] -= damage
            if enemy["health"] <= 0:
                enemies.remove(enemy)
            insert_damage_number(damage, enemy["x"], enemy["y"], False)
            enemy_hit = True


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
    if time.time() - perfect_dodge_time > 3:
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
                player_move_to(closest_enemy["x"] + 50 if looking_left else closest_enemy["x"] - 50, player_y)
                # player_move_to(closest_enemy["x"], player_y)
            
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
            if time.time() - shift_start_time > dodge_press_duration:
                current_speed = sprint_speed / time_scale
        else:
            shift_pressed = False
            current_speed = move_speed / time_scale

        if not shift_pressed and not shift_released:
            if time.time() - shift_start_time <= dodge_press_duration:
                dodge()
            shift_released = True

        if a_pressed:
            looking_left = True
            player_move_to(player_x - current_speed, player_y)
            
        if d_pressed:
            looking_left = False
            player_move_to(player_x + current_speed, player_y)

        if swinging_sword and not enemy_hit:
            swing()

        if time_scale != 1:
            time_scale = 1
    else:
        if time.time() - perfect_dodge_time < 1:
            charged = False
            time_scale = 5
            if dodge_left:
                player_move_to(player_x - dodge_speed / 5 / time_scale, player_y)
            else:
                player_move_to(player_x + dodge_speed / 5 / time_scale, player_y)
        elif time.time() - perfect_dodge_time < 2:
            if time.time() - last_teleport_time > 0.25:
                last_teleport_time = time.time()
                enemy_center_x = perfect_dodge_enemy["x"] + perfect_dodge_enemy["width"] // 2
                enemy_center_y = perfect_dodge_enemy["y"] + perfect_dodge_enemy["height"] // 2
                random_angle = random.randint(-90, 0)
                player_center_x = math.sin(random_angle * math.pi / 180) * 60 + enemy_center_x
                player_center_y = -math.cos(random_angle * math.pi / 180) * 60 + enemy_center_y

                looking_left = random_angle > 0
                player_move_to(player_center_x - player_width // 2, player_center_y - player_height // 2, 270 - random_angle)
                swinging_sword = True
                draw_player()
                swing(5)
        else:
            if not charged:
                charged = True
                player_move_to(perfect_dodge_enemy["x"] - 100, HEIGHT - 150)
                last_teleport_time = time.time()
            else:
                if time.time() - last_teleport_time > 0.5:
                    player_move_to(player_x + 10, player_y)
                    if player_x - perfect_dodge_enemy["x"] < 75:
                        swing(2)

    for enemy in enemies:
        if time.time() - enemy["attack_start_time"] > 5 * time_scale and random.randint(0, 300 * time_scale) < enemy["speed"]:
            if enemy["x"] < player_x:
                enemy["looking_left"] = False
            else:
                enemy["looking_left"] = True
            enemy["attack_start_time"] = time.time()

        enemy["time_elapsed"] = time.time() - enemy["attack_start_time"]
        if enemy["time_elapsed"] <= 0.3 * time_scale:
            if enemy["id"] not in enemies_in_flash:
                enemies_in_flash.append(enemy["id"])
        elif 0.3 * time_scale <= enemy["time_elapsed"] <= 0.5 * time_scale:
            if enemy["id"] in enemies_in_flash:
                enemies_in_flash.remove(enemy["id"])
        elif 0.5 * time_scale <= enemy["time_elapsed"] <= 1 * time_scale:
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

            if 0.5 * time_scale <= enemy["time_elapsed"] <= 0.6 * time_scale:
                if abs(player_x - enemy["x"]) > 50:
                    move_enemy_forward(enemy, enemy["speed"])
                enemy_sword_rect = pygame.Rect(enemy["sword_body_x"], enemy["sword_body_y"], enemy_sword_body_width, enemy_sword_body_height)
                if not enemy["hit_player"] and enemy_sword_rect.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                    enemy["hit_player"] = True
                    player_health -= 10
                    insert_damage_number(10, player_x, player_y, True)
        else:
            enemy["hit_player"] = False

    # print(f"{player_x}, {player_y}")
    # # print(pygame.mouse.get_pos())
    # print(player_width)

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # DRAWING
    if player_health > 0:
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

            if enemy["time_elapsed"] < 1 * time_scale:
                if enemy["time_elapsed"] <= 0.3 * time_scale:
                    flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    enemy_left_eye_x += enemy_eye_width // 2
                    enemy_eye_y += enemy_eye_height // 2
                    flash_length = 50 * math.sin(10.471975512 / time_scale * enemy["time_elapsed"]) - 0.15
                    print(f"Progress: {enemy['time_elapsed'] / (0.3 * time_scale)}")
                    pygame.draw.line(flash_surface, (255, 0, 0, 200), (enemy_left_eye_x - flash_length, enemy_eye_y + flash_length * flash_slope), (enemy_left_eye_x + flash_length, enemy_eye_y - flash_length * flash_slope), 5)
                    pygame.draw.line(flash_surface, (255, 0, 0, 200), (enemy_left_eye_x - flash_length / 2, enemy_eye_y + flash_length * -1), (enemy_left_eye_x + flash_length / 2, enemy_eye_y - flash_length * -1), 5)
                    screen.blit(flash_surface, (0, 0))
                elif enemy["time_elapsed"] >= 0.5 * time_scale:
                    pygame.draw.rect(screen, (192, 192, 192), (enemy["sword_body_x"], enemy["sword_body_y"], enemy_sword_body_width, enemy_sword_body_height))
                    pygame.draw.polygon(screen, (192, 192, 192), [enemy["sword_tip"], enemy["sword_base1"], enemy["sword_base2"]])

        # pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, player_width, player_height))
        health_bar_width = player_width * player_health / 100
        pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y - 10, health_bar_width, 5))

        draw_player()

        # if swinging_sword:
        #     pygame.draw.rect(screen, (192, 192, 192), (sword_body_x, sword_body_y, sword_body_width, sword_body_height))
        #     pygame.draw.polygon(screen, (192, 192, 192), [sword_tip, sword_base1, sword_base2])

        damage_numbers = [dn for dn in damage_numbers if time.time() - dn["timestamp"] < 1 * time_scale]
        for dn in damage_numbers:
            text_color = (255, 0, 0) if dn["to_player"] else (255, 255, 255)
            damage_text = font.render(str(dn["damage"]), True, text_color)
            screen.blit(damage_text, (dn["x"], dn["y"]))
    else:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2 - 50))

    # pygame.draw.rect(screen, (0, 0, 0), sword_rect, 2)
        
    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(120)
    #---------------------------


pygame.quit()
