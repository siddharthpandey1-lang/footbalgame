import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (30, 144, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kick 2 Hard")
clock = pygame.time.Clock()
FPS = 60

# Fonts
font_large = pygame.font.Font(None, 72)
font_small = pygame.font.Font(None, 36)

# Game variables
ball_radius = 20
ball_start_y = HEIGHT - 100
goalkeeper_width = 120
goalkeeper_height = 20
goalkeeper_y = 100
kick_power = 0
kick_charging = False
ball_in_motion = False
ball_vel_y = 0
score = 0
attempts = 5
game_over = False

# Ball position
ball_x = WIDTH // 2
ball_y = ball_start_y

# Goalkeeper position
goalkeeper_x = WIDTH // 2 - goalkeeper_width // 2
goalkeeper_speed = 5

def reset_ball():
    global ball_y, ball_in_motion, ball_vel_y
    ball_y = ball_start_y
    ball_in_motion = False
    ball_vel_y = 0

def draw_text(text, font, color, x, y, center=True):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

def handle_kick():
    global kick_charging, ball_in_motion, ball_vel_y, kick_power
    if kick_charging and not ball_in_motion:
        ball_in_motion = True
        ball_vel_y = -kick_power // 5
        kick_power = 0
        kick_charging = False

def update_goalkeeper():
    global goalkeeper_x, goalkeeper_speed
    goalkeeper_x += goalkeeper_speed
    if goalkeeper_x <= 0 or goalkeeper_x + goalkeeper_width >= WIDTH:
        goalkeeper_speed *= -1

def check_goal():
    global score, attempts, game_over
    if ball_y <= goalkeeper_y + goalkeeper_height:
        if goalkeeper_x < ball_x < goalkeeper_x + goalkeeper_width:
            draw_text("Saved!", font_large, RED, WIDTH // 2, HEIGHT // 2)
        else:
            score += 1
            draw_text("GOAL!", font_large, BLUE, WIDTH // 2, HEIGHT // 2)
        pygame.display.update()
        pygame.time.delay(1000)
        reset_ball()
        attempts -= 1
        if attempts == 0:
            game_over = True

def restart_game():
    global score, attempts, game_over
    score = 0
    attempts = 5
    game_over = False
    reset_ball()

# Main loop
running = True
while running:
    screen.fill(GREEN)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not ball_in_motion:
                    kick_charging = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    handle_kick()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()

    # Kick power charging
    if kick_charging:
        kick_power = min(kick_power + 1, 100)

    # Ball movement
    if ball_in_motion:
        ball_y += ball_vel_y
        ball_vel_y += 1  # gravity
        if ball_y <= goalkeeper_y + goalkeeper_height:
            check_goal()

    # Goalkeeper movement
    if not game_over:
        update_goalkeeper()

    # Draw ball
    pygame.draw.circle(screen, BLACK, (ball_x, int(ball_y)), ball_radius)

    # Draw goalkeeper
    pygame.draw.rect(screen, RED, (goalkeeper_x, goalkeeper_y, goalkeeper_width, goalkeeper_height))

    # Draw power bar
    pygame.draw.rect(screen, BLACK, (50, HEIGHT - 40, 100, 20))
    pygame.draw.rect(screen, RED, (50, HEIGHT - 40, kick_power, 20))

    # Draw score and attempts
    draw_text(f"Score: {score}", font_small, BLACK, 10, 10, center=False)
    draw_text(f"Attempts Left: {attempts}", font_small, BLACK, 10, 40, center=False)

    # Game over screen
    if game_over:
        draw_text("Game Over!", font_large, BLACK, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Press R to Restart", font_small, BLACK, WIDTH // 2, HEIGHT // 2 + 20)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()