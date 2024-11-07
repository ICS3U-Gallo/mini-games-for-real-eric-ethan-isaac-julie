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
playery = HEIGHT - 60
playerwidth = 5
playerlength = 20
ammo = 10
health = 3
move_speed = 10
rocks = []
heals = []
ammos = []
# ---------------------------
pygame.display.set_caption('Shooter Game')
font = pygame.font.Font('freesansbold.ttf', 15)
running = True

def drawheal(x, y):
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20)
    #draws the green cross:
    pygame.draw.polygon(screen, (0, 255, 0), [(x - 5, y - 15), (x + 5, y - 15),
                                              (x + 5, y - 5), (x + 15, y - 5),
                                              (x + 15, y), (x + 5, y),
                                              (x + 5, y + 10), (x - 5, y + 10),
                                              (x - 5, y), (x - 15, y),
                                              (x - 15, y - 5), (x - 5, y - 5)])
def drawasteroid(x, y):
    size = random.randint(20, 50)

    points = [
        (x + random.randint(-size, size), y + random.randint(-size, size)) for _ in range(6)
    ]

    pygame.draw.polygon(screen, (169, 169, 169), points)

def drawammo(x, y, counter):
    if counter<=2:
        counter+=1
        pygame.draw.circle(screen, (102, 102, 0),(x+5, y), 5)
        pygame.draw.rect(screen, (51, 102, 0), (x, y, 10, 30) )
        pygame.draw.rect(screen, (0, 0, 0), (x+10, y, 2, 30))
        #recursion stuff
        drawammo(x+12 , y, counter)
    pygame.draw.circle(screen, (102, 102, 0), (x + 5, y), 5)
    pygame.draw.rect(screen, (51, 102, 0), (x, y, 10, 30)) #to get rid of the last black line

def drawrock(rock_x, rock_y, scale_factor):
    rock_points = [
        (rock_x + 20 * scale_factor, rock_y - 10 * scale_factor),
        (rock_x + 40 * scale_factor, rock_y * scale_factor),
        (rock_x + 30 * scale_factor, rock_y + 20 * scale_factor),
        (rock_x + 10 * scale_factor, rock_y + 30 * scale_factor),
        (rock_x - 10 * scale_factor, rock_y + 20 * scale_factor)
    ]

    pygame.draw.polygon(screen, (128, 128, 128), rock_points)

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
        playerx = WIDTH - playerwidth  # Prevent out of bounds
    elif playerx <= 0:
        playerx = 0  # Prevent out of bounds on left

    # DRAWING
    screen.fill((0, 0, 51))  # always the first drawing command
    pygame.draw.rect(screen, (255, 255, 255), (playerx, playery, playerwidth, playerlength))
    drawheal(playerx + playerwidth // 2, playery - 40)  # Positioning heal above player
    drawammo(playerx+playerwidth // 2, playery-40, 0)
    scale_factor = random.uniform(0.5, 1.5)
    drawrock(playerx + playerwidth // 2, playery - 40, scale_factor)
    
    pygame.display.flip()
    clock.tick(30)
    #---------------------------

pygame.quit()
