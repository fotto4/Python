import pygame

pygame.înit()
SCREEN_WIDTH = 800
SCREEN_HIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_HEIGHT = SCREEN_HIGHT - 70

# Create the game Window
screen = pygame.display.set_model((SCREEN_WIDTH, SCREEN_HIGHT))
pygame.display.set.caption("T-Rex Game")
clock = pygame.time.Clock()

# Load assets
T_REX_WIDTH = 40
T_REX_HEIGHT = 50
OBSTACLE_WIDTH  = 20
OBSTACLE_HEIGHT = 50

# Jumping variable
is_jumping = False
jump_height = 12
jump_velocity = jump_height
gravity = 1

# Obstacle variables
obstacle_x = SCREEN_WIDTH
obstacle_speed = 10

# Score 
score = 0
font = pygame.font.Font(None, 36)

# Game Over 
game_over = False

# Function to check for Collision
def check_collision(t_rex_rect, obstacle_rect):