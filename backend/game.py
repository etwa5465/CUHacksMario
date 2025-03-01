import pygame

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
GRAVITY = 1
JUMP_STRENGTH = -15
SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Clone")

# Camera Variables
camera_x = 0  # ✅ Camera follows Mario

# Mario Character (always centered visually)
mario = pygame.Rect(WIDTH // 2, 500, 40, 50)
mario_world_x = WIDTH // 2  # ✅ Mario’s actual world position

# Ground
ground = pygame.Rect(0, 550, WIDTH * 3, 50)  # ✅ Extended ground

# Platforms
platforms = [
    pygame.Rect(300, 450, 150, 20),
    pygame.Rect(600, 350, 150, 20),
    pygame.Rect(900, 250, 150, 20),
    pygame.Rect(1200, 450, 150, 20),
]

# Flagpole (Winning Condition)
flagpole = pygame.Rect(1500, 450, 20, 100)

# Goomba (Enemy)
goomba = pygame.Rect(700, 500, 40, 40)
goomba_direction = -1  # Moving left initially

# Mario Movement Variables
velocity_y = 0
on_ground = False

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # 60 FPS
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get Key Presses
    keys = pygame.key.get_pressed()
    moving_left = keys[pygame.K_LEFT]
    moving_right = keys[pygame.K_RIGHT]

    # ✅ Prevent Mario from moving past world limits
    if moving_left and mario_world_x > 0:
        mario_world_x -= SPEED
    if moving_right and mario_world_x < ground.width - mario.width:
        mario_world_x += SPEED

    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = JUMP_STRENGTH
        on_ground = False

    # Apply Gravity
    velocity_y += GRAVITY
    mario.y += velocity_y

    # ✅ Collision with Ground in World Space
    ground_render = ground.move(-camera_x, 0)
    if mario.colliderect(ground_render):
        mario.y = ground_render.y - mario.height
        velocity_y = 0
        on_ground = True

    # ✅ Collision with Platforms in World Space
    for platform in platforms:
        platform_render = platform.move(-camera_x, 0)
        if mario.colliderect(platform_render) and velocity_y > 0:
            mario.y = platform_render.y - mario.height
            velocity_y = 0
            on_ground = True

    # ✅ Keep Camera Centered on Mario
    camera_x = mario_world_x - WIDTH // 2

    # ✅ Render Objects Based on Camera Position
    mario.x = WIDTH // 2  # ✅ Mario stays in center, world moves
    flagpole_render = flagpole.move(-camera_x, 0)
    goomba_render = goomba.move(-camera_x, 0)

    # ✅ Move Goomba Back and Forth
    goomba.x += goomba_direction * 2
    if goomba.x < 600 or goomba.x > 800:
        goomba_direction *= -1  # Change direction

    # ✅ Check if Mario Reaches Flagpole (Winning Condition)
    if mario_world_x >= flagpole.x:
        print("🎉 Mario Wins!")
        running = False

    # ✅ Check if Mario Touches Goomba (Game Over)
    if mario.colliderect(goomba_render):
        print("💀 Mario Died!")
        running = False

    # Draw Ground & Platforms
    pygame.draw.rect(screen, GREEN, ground_render)
    for platform in platforms:
        pygame.draw.rect(screen, BLUE, platform.move(-camera_x, 0))

    # Draw Flagpole
    pygame.draw.rect(screen, RED, flagpole_render)

    # Draw Goomba
    pygame.draw.rect(screen, BROWN, goomba_render)

    # Draw Mario
    pygame.draw.rect(screen, (255, 0, 0), mario)

    pygame.display.flip()

pygame.quit()
