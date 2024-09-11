import pygame
import sys


pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game object vars
ball_speed_x = 7
ball_speed_y = 7
paddle_speed = 10

# Game object dimentions
ball_width = 20
ball_height = 20
paddle_width = 10
paddle_height = 100

# Ball position
ball_x = WIDTH // 2 - ball_width // 2
ball_y = HEIGHT // 2 - ball_height // 2

# Pad positions
player1_x = 10
player1_y = HEIGHT // 2 - paddle_height // 2

player2_x = WIDTH - paddle_width - 10
player2_y = HEIGHT // 2 - paddle_height // 2


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_y > 0:
        player1_y -= paddle_speed
    if keys[pygame.K_s] and player1_y < HEIGHT - paddle_height:
        player1_y += paddle_speed
    if keys[pygame.K_UP] and player2_y > 0:
        player2_y -= paddle_speed
    if keys[pygame.K_DOWN] and player2_y < HEIGHT - paddle_height:
        player2_y += paddle_speed

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_y <= 0 or ball_y >= HEIGHT - ball_height:
        ball_speed_y *= -1

    if (ball_x <= player1_x + paddle_width and player1_y < ball_y < player1_y + paddle_height) or \
       (ball_x >= player2_x - ball_width and player2_y < ball_y < player2_y + paddle_height):
        ball_speed_x *= -1

    if ball_x < 0 or ball_x > WIDTH:
        ball_x = WIDTH // 2 - ball_width // 2
        ball_y = HEIGHT // 2 - ball_height // 2
        ball_speed_x *= -1

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (player1_x, player1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (player2_x, player2_y, paddle_width, paddle_height))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_width, ball_height))
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    pygame.display.flip()
    clock.tick(60)
