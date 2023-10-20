import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 288, 512
GROUND_HEIGHT = 100
FPS = 60
BIRD_WIDTH, BIRD_HEIGHT = 34, 24
PIPE_WIDTH = 52
PIPE_SPACING = 150
GRAVITY = 0.25
JUMP = 4

# Colors
WHITE = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Load assets
bg = pygame.image.load("sprites/background-day.png")
bird_images = [pygame.image.load("sprites/shot.png"), pygame.image.load("sprites/beer.png"), pygame.image.load("sprites/ice.png")]
pipe_image = pygame.image.load("sprites/pipe-green.png")
ground = pygame.image.load("sprites/base.png")

# Font
font = pygame.font.Font(None, 36)

# Character selection
characters = ["sprites/shot.png", "sprites/beer.png", "sprites/ice.png"]
selected_character = 0

# Game variables
bird_x = 50
bird_y = (HEIGHT - GROUND_HEIGHT) // 2
bird_vel = 0
pipes = []
score = 0

# Functions
def draw_background():
    screen.blit(bg, (0, 0))

def draw_ground():
    screen.blit(ground, (0, HEIGHT - GROUND_HEIGHT))

def draw_bird():
    bird_img = bird_images[selected_character]
    screen.blit(bird_img, (bird_x, bird_y))

def draw_pipes():
    for pipe_x, pipe_height in pipes:
        screen.blit(pipe_image, (pipe_x, 0))
        pipe_height_bottom = HEIGHT - GROUND_HEIGHT - pipe_height - PIPE_SPACING
        screen.blit(pygame.transform.flip(pipe_image, False, True), (pipe_x, pipe_height_bottom))

def draw_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def collision(pipe_x, pipe_height):
    if bird_x + BIRD_WIDTH > pipe_x and bird_x < pipe_x + PIPE_WIDTH:
        if bird_y < pipe_height or bird_y + BIRD_HEIGHT > pipe_height + PIPE_SPACING:
            return True
    return False

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_vel = -JUMP
            if event.key == pygame.K_LEFT:
                selected_character = (selected_character - 1) % len(characters)
            if event.key == pygame.K_RIGHT:
                selected_character = (selected_character + 1) % len(characters)

    bird_vel += GRAVITY
    bird_y += bird_vel

    if bird_y < 0:
        bird_y = 0

    if bird_y + BIRD_HEIGHT > HEIGHT - GROUND_HEIGHT:
        bird_y = HEIGHT - GROUND_HEIGHT - BIRD_HEIGHT
        bird_vel = 0

    # Generate new pipes
    if pipes and pipes[0][0] + PIPE_WIDTH < 0:
        pipes.pop(0)
        score += 1

    if not pipes or pipes[-1][0] < WIDTH - (WIDTH // 3):
        pipe_height = random.randint(100, HEIGHT - GROUND_HEIGHT - 100 - PIPE_SPACING)
        pipes.append((WIDTH, pipe_height))

    # Check for collisions
    for pipe_x, pipe_height in pipes:
        if collision(pipe_x, pipe_height):
            running = False

    # Update game elements
    draw_background()
    draw_pipes()
    draw_ground()
    draw_bird()
    draw_score()

    pygame.display.update()
    clock.tick(FPS)

# Game over
game_over_font = pygame.font.Font(None, 72)
game_over_text = game_over_font.render("Game Over", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 36))
pygame.display.update()

# Wait for a few seconds before quitting
pygame.time.delay(2000)

# Quit pygame
pygame.quit()
