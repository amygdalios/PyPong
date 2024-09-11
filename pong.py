import pygame
import sys
import random
import time

def show_message(text, duration):
    screen.fill(BLACK)
    message_text = font.render(text, True, WHITE)
    screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2 - message_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(duration)

def main_menu():
    player1_name = ""
    player2_name = ""
    winning_score = ""
    input_active = [False, False, False]
    font_small = pygame.font.Font(None, 50)
    font_large = pygame.font.Font(None, 74)
    
    # Define colors
    default_color = WHITE
    selected_color = (255, 255, 0) 
    hover_color = (255, 255, 200)   
    
    input_boxes = [
        pygame.Rect(WIDTH // 2 - 200, HEIGHT // 3, 400, 40), 
        pygame.Rect(WIDTH // 2 - 200, HEIGHT // 3 + 50, 400, 40), 
        pygame.Rect(WIDTH // 2 - 200, HEIGHT // 3 + 100, 400, 40) 
    ]
    
    while True:
        screen.fill(BLACK)
        
        mouse_pos = pygame.mouse.get_pos()
        for i, box in enumerate(input_boxes):
            if box.collidepoint(mouse_pos):
                if input_active[i]:
                    text_color = selected_color
                else:
                    text_color = hover_color
            else:
                if input_active[i]:
                    text_color = selected_color
                else:
                    text_color = default_color

            if i == 0:
                player1_text = font_small.render("Player 1 Name: " + player1_name, True, text_color)
                screen.blit(player1_text, (WIDTH // 2 - player1_text.get_width() // 2, HEIGHT // 3))
            elif i == 1:
                player2_text = font_small.render("Player 2 Name: " + player2_name, True, text_color)
                screen.blit(player2_text, (WIDTH // 2 - player2_text.get_width() // 2, HEIGHT // 3 + 50))
            elif i == 2:
                score_text = font_small.render("Winning Score: " + winning_score, True, text_color)
                screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 100))

        title_text = font_large.render("Pong Game Setup", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6))

        start_text = font_small.render("Press ENTER to Start", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player1_name and player2_name and winning_score.isdigit():
                        return player1_name, player2_name, int(winning_score)
                elif event.key == pygame.K_BACKSPACE:
                    if input_active[0] and len(player1_name) > 0:
                        player1_name = player1_name[:-1]
                    elif input_active[1] and len(player2_name) > 0:
                        player2_name = player2_name[:-1]
                    elif input_active[2] and len(winning_score) > 0:
                        winning_score = winning_score[:-1]
                else:
                    if input_active[0]:
                        player1_name += event.unicode
                    elif input_active[1]:
                        player2_name += event.unicode
                    elif input_active[2]:
                        if event.unicode.isdigit(): 
                            winning_score += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        input_active = [False, False, False]
                        input_active[i] = True  

        pygame.display.flip()
        clock.tick(30)

def reset_ball():
    global ball_x, ball_y, ball_speed_x
    ball_x = WIDTH // 2 - ball_width // 2
    ball_y = HEIGHT // 2 - ball_height // 2
    ball_speed_x *= -1

def display_score_update(scorer_name):
    show_message(f"{scorer_name} scored!", 1000)

def spawn_power_up():
    power_up_type = random.choice(list(POWER_UPS.keys()))
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    power_up = {
        "type": power_up_type,
        "rect": pygame.Rect(x, y, 50, 50),
        "spawn_time": time.time()
    }
    return power_up


pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")


# Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
POWER_UP_COLORS = {
    "larger_paddle": (0, 255, 0),  # Green
    "faster_ball": (255, 0, 0),    # Red
    "shield": (0, 0, 255)         # Blue
}

# Game object vars
ball_speed_x = 7
ball_speed_y = 7
paddle_speed = 10
POWER_UP_DURATION = 5
POWER_UP_INTERVAL_MIN = 5
POWER_UP_INTERVAL_MAX = 10 

power_ups = []
power_up_timer = time.time()
active_power_ups = {"player1": None, "player2": None}


# Game object dimensions
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

# Score vars
p1_score = 0
p2_score = 0

#powerup types
POWER_UPS = {
    "larger_paddle": "Larger Paddle",
    "faster_ball": "Faster Ball",
    "shield": "Shield"
}

# Font for displaying score
font = pygame.font.Font(None, 74)

clock = pygame.time.Clock()

player1_name, player2_name, winning_score = main_menu()

# Initial power-up spawn
power_up = spawn_power_up()
power_up_timer = time.time()


# Game loop
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

    #Disable player shields
    player1_shield_active, player2_shield_active = False, False

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with top/bottom walls
    if ball_y <= 0 or ball_y >= HEIGHT - ball_height:
        ball_speed_y *= -1

    # Ball collision with paddles
    if (ball_x <= player1_x + paddle_width and player1_y < ball_y < player1_y + paddle_height) or \
       (ball_x >= player2_x - ball_width and player2_y < ball_y < player2_y + paddle_height):
        ball_speed_x *= -1
        last_hit_player = "player1" if ball_x < WIDTH // 2 else "player2"

    # Check for Point Scoring
    if ball_x < 0:  # Ball went past the left edge
        p2_score += 1
        display_score_update(player2_name)
        reset_ball()
        last_hit_player = None
        active_power_ups["player1"] = None
        active_power_ups["player2"] = None

    elif ball_x > WIDTH:  # Ball went past the right edge
        p1_score += 1
        display_score_update(player1_name)
        reset_ball()
        last_hit_player = None
        active_power_ups["player1"] = None
        active_power_ups["player2"] = None

    # Check for winning condition
    if p1_score >= winning_score:
        show_message(f"{player1_name} Wins!", 2000)
        player1_name, player2_name, winning_score = main_menu()
        p1_score, p2_score = 0, 0  # Reset scores
    elif p2_score >= winning_score:
        show_message(f"{player2_name} Wins!", 2000)
        player1_name, player2_name, winning_score = main_menu()
        p1_score, p2_score = 0, 0  # Reset scores

    # Power-up collision detection
    ball_rect = pygame.Rect(ball_x, ball_y, ball_width, ball_height)
    if power_up["rect"].colliderect(ball_rect):
        if last_hit_player:
            active_power_ups[last_hit_player] = power_up["type"]
            power_up = spawn_power_up()
            power_up_timer = time.time()

    # Handle power-up expiration
    for player in ["player1", "player2"]:
        if active_power_ups[player] and time.time() - power_up["spawn_time"] > POWER_UP_DURATION:
            active_power_ups[player] = None
            paddle_height = 100
            ball_speed_x = 7 if ball_speed_x > 0 else -7

    # Apply power-up effects
    if active_power_ups["player1"]:
        if active_power_ups["player1"] == "larger_paddle":
            paddle_height = 150
        elif active_power_ups["player1"] == "faster_ball":
            ball_speed_x = 10
        elif active_power_ups["player1"] == "shield":
            player1_shield_active = True  # Activate shield for player 1

    if active_power_ups["player2"]:
        if active_power_ups["player2"] == "larger_paddle":
            paddle_height = 150
        elif active_power_ups["player2"] == "faster_ball":
            ball_speed_x = 10
        elif active_power_ups["player2"] == "shield":
            player2_shield_active = True  # Activate shield for player 2

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (player1_x, player1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (player2_x, player2_y, paddle_width, paddle_height))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_width, ball_height))
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw shields
    if player1_shield_active:
        pygame.draw.line(screen, WHITE, (10, 0), (10, HEIGHT), 5)  # Draw shield behind player 1 paddle
    if player2_shield_active:
        pygame.draw.line(screen, WHITE, (WIDTH - 10, 0), (WIDTH - 10, HEIGHT), 5)  # Draw shield behind player 2 paddle

    # Draw power-up
    pygame.draw.rect(screen, POWER_UP_COLORS[power_up["type"]], power_up["rect"])

    player1_text = font.render(f"{p1_score}", True, WHITE)
    player2_text = font.render(f"{p2_score}", True, WHITE)
    screen.blit(player1_text, (WIDTH // 4, 20))
    screen.blit(player2_text, (WIDTH * 3 // 4, 20))

    pygame.display.flip()
    clock.tick(60)

    # Collision detection with shields
    if player1_shield_active and ball_x <= 10:  # Shield for Player 1
        ball_speed_x *= -1

    if player2_shield_active and ball_x >= WIDTH - 10 - ball_width:  # Shield for Player 2
        ball_speed_x *= -1
