import pygame
import random
import os
import sys
import math

# Disable pygame audio to prevent ALSA errors
os.environ['SDL_AUDIODRIVER'] = 'dummy'

try:
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 400
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 150, 0)
    BLUE = (0, 0, 255)
    GROUND_COLOR = (83, 83, 83)
    SKY_COLOR = (220, 240, 255)
    
    GROUND_HEIGHT = SCREEN_HEIGHT - 70
    
    # Create the game Window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("T-Rex Game")
    clock = pygame.time.Clock()
    
    # Load or create assets
    T_REX_WIDTH = 50
    T_REX_HEIGHT = 60
    T_REX_DUCK_HEIGHT = 30
    
    CACTUS_WIDTH = 30
    CACTUS_HEIGHT = 60
    
    BIRD_WIDTH = 50
    BIRD_HEIGHT = 30
    
    CLOUD_WIDTH = 70
    CLOUD_HEIGHT = 40
    
    # T-Rex variables
    t_rex_x = 50
    t_rex_y = GROUND_HEIGHT - T_REX_HEIGHT
    t_rex_color = (50, 150, 50)  # Green dino
    
    # Animation variables
    animation_counter = 0
    animation_speed = 5
    run_frame = 0
    bird_frame = 0
    
    # Jumping variables
    is_jumping = False
    jump_height = 100
    jump_velocity = jump_height
    gravity = 1
    
    # Ducking variables
    is_ducking = False
    
    # Obstacle variables
    obstacles = []  # List to store multiple obstacles
    obstacle_types = ["cactus", "bird"]
    obstacle_speed = 5
    min_obstacle_distance = 300  # Minimum distance between obstacles
    
    # Cloud variables
    clouds = []
    for i in range(3):
        clouds.append({
            'x': random.randint(0, SCREEN_WIDTH),
            'y': random.randint(50, 150),
            'speed': random.uniform(0.5, 1.5)
        })
    
    # Game variables
    score = 0
    level = 1
    font = pygame.font.Font(None, 36)
    
    # Game Over 
    game_over = False
    
    # Function to check for Collision
    def check_collision(t_rex_rect, obstacle_rect):
        # Make hitbox slightly smaller for better gameplay
        t_rex_hitbox = pygame.Rect(
            t_rex_rect.x + 5,
            t_rex_rect.y + 5,
            t_rex_rect.width - 10,
            t_rex_rect.height - 10
        )
        obstacle_hitbox = pygame.Rect(
            obstacle_rect.x + 5,
            obstacle_rect.y + 5,
            obstacle_rect.width - 10,
            obstacle_rect.height - 10
        )
        return t_rex_hitbox.colliderect(obstacle_hitbox)
    
    # Function to draw the T-Rex
    def draw_t_rex(x, y, is_ducking, run_frame):
        height = T_REX_DUCK_HEIGHT if is_ducking else T_REX_HEIGHT
        
        # Draw body
        pygame.draw.rect(screen, t_rex_color, (x, y, T_REX_WIDTH, height))
        
        # Draw head
        head_height = min(height // 2, 30)
        pygame.draw.rect(screen, t_rex_color, (x + T_REX_WIDTH - 15, y - head_height + 5, 15, head_height))
        
        # Draw eye
        pygame.draw.circle(screen, WHITE, (x + T_REX_WIDTH - 5, y - head_height + 15), 5)
        pygame.draw.circle(screen, BLACK, (x + T_REX_WIDTH - 3, y - head_height + 15), 2)
        
        # Draw legs (animated)
        leg_offset = 5 if run_frame % 2 == 0 else -5
        
        if not is_ducking:
            # Back leg
            pygame.draw.rect(screen, t_rex_color, (x + 5, y + height - 15, 10, 15 + leg_offset))
            # Front leg
            pygame.draw.rect(screen, t_rex_color, (x + T_REX_WIDTH - 15, y + height - 15, 10, 15 - leg_offset))
        else:
            # Legs when ducking
            pygame.draw.rect(screen, t_rex_color, (x + 5, y + height - 10, 10, 10))
            pygame.draw.rect(screen, t_rex_color, (x + T_REX_WIDTH - 15, y + height - 10, 10, 10))
    
    # Function to draw a cactus
    def draw_cactus(x, y, width, height):
        # Main body
        pygame.draw.rect(screen, GREEN, (x, y, width, height))
        
        # Arms (randomly)
        if random.random() > 0.5:
            pygame.draw.rect(screen, GREEN, (x - 10, y + height // 3, 15, 10))
        if random.random() > 0.5:
            pygame.draw.rect(screen, GREEN, (x + width - 5, y + height // 4, 15, 10))
    
    # Function to draw a bird
    def draw_bird(x, y, width, height, frame):
        # Body
        pygame.draw.ellipse(screen, BLUE, (x, y, width, height))
        
        # Wings (animated)
        wing_height = 15 if frame % 2 == 0 else 5
        pygame.draw.ellipse(screen, (100, 100, 255), (x + 10, y - wing_height, width - 20, 20))
        
        # Beak
        pygame.draw.polygon(screen, (255, 200, 0), [(x, y + height // 2), (x - 15, y + height // 3), (x - 15, y + 2 * height // 3)])
        
        # Eye
        pygame.draw.circle(screen, WHITE, (x + 10, y + height // 3), 5)
        pygame.draw.circle(screen, BLACK, (x + 12, y + height // 3), 2)
    
    # Function to draw clouds
    def draw_cloud(x, y, width, height):
        pygame.draw.ellipse(screen, WHITE, (x, y, width, height))
        pygame.draw.ellipse(screen, WHITE, (x + width // 4, y - height // 4, width // 2, height // 2))
        pygame.draw.ellipse(screen, WHITE, (x + width // 2, y, width // 2, height // 2))
    
    # Function to draw the ground
    def draw_ground():
        pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        # Draw ground details
        for i in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(screen, (100, 100, 100), (i, GROUND_HEIGHT), (i + 20, GROUND_HEIGHT), 2)
    
    # Function to add a new obstacle
    def add_obstacle():
        # Determine if we should add a bird or cactus
        obstacle_type = random.choice(obstacle_types) if score > 10 else "cactus"
        
        if obstacle_type == "cactus":
            height = random.randint(30, 60)
            obstacles.append({
                'type': 'cactus',
                'x': SCREEN_WIDTH,
                'y': GROUND_HEIGHT - height,
                'width': CACTUS_WIDTH,
                'height': height
            })
        else:  # Bird
            # Birds can fly at different heights
            height_options = [
                GROUND_HEIGHT - BIRD_HEIGHT - 10,  # Low flying bird (need to duck)
                GROUND_HEIGHT - T_REX_HEIGHT - BIRD_HEIGHT - 10  # High flying bird (need to run under)
            ]
            y = random.choice(height_options)
            obstacles.append({
                'type': 'bird',
                'x': SCREEN_WIDTH,
                'y': y,
                'width': BIRD_WIDTH,
                'height': BIRD_HEIGHT
            })
    
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
                    if event.key == pygame.K_DOWN:
                        is_ducking = True
                    if event.key == pygame.K_r and game_over:
                        # Reset game
                        game_over = False
                        score = 0
                        level = 1
                        obstacles = []
                        t_rex_y = GROUND_HEIGHT - T_REX_HEIGHT
                        obstacle_speed = 5
                        min_obstacle_distance = 300
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        is_ducking = False
    
            if not game_over:
                # Update animation counter
                animation_counter += 1
                if animation_counter >= animation_speed:
                    animation_counter = 0
                    run_frame = (run_frame + 1) % 4
                    bird_frame = (bird_frame + 1) % 4
                
                # T-Rex jumping logic
                if is_jumping:
                    t_rex_y -= jump_velocity
                    jump_velocity -= gravity
                    if t_rex_y >= GROUND_HEIGHT - T_REX_HEIGHT:
                        t_rex_y = GROUND_HEIGHT - T_REX_HEIGHT
                        is_jumping = False
                
                # T-Rex ducking logic
                if is_ducking and not is_jumping:
                    t_rex_y = GROUND_HEIGHT - T_REX_DUCK_HEIGHT
                elif not is_jumping:
                    t_rex_y = GROUND_HEIGHT - T_REX_HEIGHT
                
                # Move clouds
                for cloud in clouds:
                    cloud['x'] -= cloud['speed']
                    if cloud['x'] < -CLOUD_WIDTH:
                        cloud['x'] = SCREEN_WIDTH
                        cloud['y'] = random.randint(50, 150)
                
                # Move obstacles and check for removal
                for obstacle in obstacles[:]:
                    obstacle['x'] -= obstacle_speed
                    if obstacle['x'] < -obstacle['width']:
                        obstacles.remove(obstacle)
                        score += 1
                        
                        # Increase level every 10 points
                        if score % 10 == 0:
                            level += 1
                            obstacle_speed += 0.5
                            
                            # Make game easier after level 20
                            if level >= 20:
                                min_obstacle_distance = 400  # Increase distance between obstacles
                
                # Add new obstacles if needed
                if not obstacles or (obstacles and obstacles[-1]['x'] < SCREEN_WIDTH - min_obstacle_distance):
                    # Add randomness to obstacle placement
                    if random.random() < 0.3:  # 30% chance to add an obstacle when conditions are met
                        add_obstacle()
                
                # Check for collision
                t_rex_height = T_REX_DUCK_HEIGHT if is_ducking else T_REX_HEIGHT
                t_rex_rect = pygame.Rect(t_rex_x, t_rex_y, T_REX_WIDTH, t_rex_height)
                
                for obstacle in obstacles:
                    obstacle_rect = pygame.Rect(
                        obstacle['x'], 
                        obstacle['y'], 
                        obstacle['width'], 
                        obstacle['height']
                    )
                    if check_collision(t_rex_rect, obstacle_rect):
                        game_over = True
    
            # Draw everything
            screen.fill(SKY_COLOR)
            
            # Draw clouds
            for cloud in clouds:
                draw_cloud(cloud['x'], cloud['y'], CLOUD_WIDTH, CLOUD_HEIGHT)
            
            # Draw ground
            draw_ground()
            
            # Draw T-Rex
            draw_t_rex(t_rex_x, t_rex_y, is_ducking, run_frame)
            
            # Draw obstacles
            for obstacle in obstacles:
                if obstacle['type'] == 'cactus':
                    draw_cactus(
                        obstacle['x'], 
                        obstacle['y'], 
                        obstacle['width'], 
                        obstacle['height']
                    )
                else:  # Bird
                    draw_bird(
                        obstacle['x'], 
                        obstacle['y'], 
                        obstacle['width'], 
                        obstacle['height'],
                        bird_frame
                    )
            
            # Draw score and level
            score_text = font.render(f"Score: {score}", True, BLACK)
            level_text = font.render(f"Level: {level}", True, BLACK)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))
            
            # Draw level 20 notification
            if level >= 20:
                level20_text = font.render("Level 20+: Easier Mode", True, (0, 100, 0))
                screen.blit(level20_text, (SCREEN_WIDTH - 250, 10))
    
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