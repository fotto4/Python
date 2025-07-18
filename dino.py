import pygame
import random
import os
import sys

# Disable pygame audio to prevent ALSA errors
os.environ['SDL_AUDIODRIVER'] = 'dummy'

try:
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 400
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GROUND_HEIGHT = SCREEN_HEIGHT - 70
    
    # Create the game Window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("T-Rex Game")
    clock = pygame.time.Clock()
    
    # Load assets
    T_REX_WIDTH = 40
    T_REX_HEIGHT = 50
    OBSTACLE_WIDTH = 20
    OBSTACLE_HEIGHT = 30   # Adjusted height for ground obstacles
    BIRD_WIDTH = 40        # Width of the bird
    BIRD_HEIGHT = 30       # Height of the bird
    
    # T-Rex variables
    t_rex_x = 50
    t_rex_y = GROUND_HEIGHT - T_REX_HEIGHT
    
    # Jumping variables
    is_jumping = False
    jump_height = 17
    jump_velocity = jump_height
    gravity = 1
    
    # Obstacle variables
    obstacle_x = SCREEN_WIDTH
    bird_x = SCREEN_WIDTH + 300  # Position the bird a bit further down the screen
    obstacle_speed = 5
    
    # Score 
    score = 0
    font = pygame.font.Font(None, 36)
    
    # Game Over 
    game_over = False
    
    # Function to check for Collision
    def check_collision(t_rex_rect, obstacle_rect):
        return t_rex_rect.colliderect(obstacle_rect)
    
    # Main game loop
    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not is_jumping and not game_over:
                        is_jumping = True
                        jump_velocity = jump_height
                    if event.key == pygame.K_r and game_over:
                        # Reset game
                        game_over = False
                        score = 0
                        obstacle_x = SCREEN_WIDTH
                        bird_x = SCREEN_WIDTH + 300
                        t_rex_y = GROUND_HEIGHT - T_REX_HEIGHT
                        obstacle_speed = 5
            
            if not game_over:
                # T-Rex jumping logic
                if is_jumping:
                    t_rex_y -= jump_velocity
                    jump_velocity -= gravity
                    if t_rex_y >= GROUND_HEIGHT - T_REX_HEIGHT:
                        t_rex_y = GROUND_HEIGHT - T_REX_HEIGHT
                        is_jumping = False
                
                # Move obstacles
                obstacle_x -= obstacle_speed
                bird_x -= obstacle_speed
                
                if obstacle_x < -OBSTACLE_WIDTH:
                    obstacle_x = SCREEN_WIDTH
                    score += 1
                    obstacle_speed += 0.5
                
                if bird_x < -BIRD_WIDTH:
                    bird_x = SCREEN_WIDTH + random.randint(100, 300)  # Reset bird position
                
                # Check for collision with ground obstacle
                t_rex_rect = pygame.Rect(t_rex_x, t_rex_y, T_REX_WIDTH, T_REX_HEIGHT)
                obstacle_rect = pygame.Rect(obstacle_x, GROUND_HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
                bird_rect = pygame.Rect(bird_x, GROUND_HEIGHT - BIRD_HEIGHT - 40, BIRD_WIDTH, BIRD_HEIGHT)  # Positioned randomly higher
                
                if check_collision(t_rex_rect, obstacle_rect) or check_collision(t_rex_rect, bird_rect):
                    game_over = True
            
            # Draw everything
            screen.fill(WHITE)
            pygame.draw.rect(screen, BLACK, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))  # Ground
            # Draw ground obstacle
            pygame.draw.rect(screen, BLACK, (obstacle_x, GROUND_HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            # Draw bird
            pygame.draw.rect(screen, BLACK, (bird_x, GROUND_HEIGHT - BIRD_HEIGHT - 40, BIRD_WIDTH, BIRD_HEIGHT))  # Adjusted bird height
            
            # Draw T-Rex
            if is_jumping:
                pygame.draw.rect(screen, BLACK, (t_rex_x, t_rex_y, T_REX_WIDTH, T_REX_HEIGHT))
            else:
                pygame.draw.rect(screen, BLACK, (t_rex_x, GROUND_HEIGHT - T_REX_HEIGHT, T_REX_WIDTH, T_REX_HEIGHT))  # T-Rex position on ground
            
            # Draw score
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))
            
            if game_over:
                game_over_text = font.render("Game Over! Press 'R' to restart", True, BLACK)
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 18))
            
            pygame.display.flip()
            clock.tick(60)

        except KeyboardInterrupt:
            print("\nGame terminated by user")
            running = False
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            running = False
            break

finally:
    pygame.quit()
    sys.exit()