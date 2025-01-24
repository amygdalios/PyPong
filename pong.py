import pygame
import sys

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

# Font for displaying score
font = pygame.font.Font(None, 74)

clock = pygame.time.Clock()

# Run main menu to get player names and winning score
player1_name, player2_name, winning_score = main_menu()

def reset_ball():
    global ball_x, ball_y, ball_speed_x
    ball_x = WIDTH // 2 - ball_width // 2
    ball_y = HEIGHT // 2 - ball_height // 2
    ball_speed_x *= -1

def display_score_update(scorer_name):
    show_message(f"{scorer_name} scored!", 1000)

while True:
    # Initial countdown
    show_message("Game Start", 1000)

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

        # Update score and reset ball
        if ball_x < 0:
            p2_score += 1
            display_score_update(player2_name)
            if p2_score >= winning_score:
                show_message(f"{player2_name} wins!", 2000)
                player1_name, player2_name, winning_score = main_menu()
                p1_score, p2_score = 0, 0  # Reset scores
            reset_ball()

        elif ball_x > WIDTH:
            p1_score += 1
            display_score_update(player1_name)
            if p1_score >= winning_score:
                show_message(f"{player1_name} wins!", 2000)
                player1_name, player2_name, winning_score = main_menu()
                p1_score, p2_score = 0, 0  # Reset scores
            reset_ball()

        # Draw game
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (player1_x, player1_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, WHITE, (player2_x, player2_y, paddle_width, paddle_height))
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_width, ball_height))
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Display scores
        player1_text = font.render(str(p1_score), True, WHITE)
        player2_text = font.render(str(p2_score), True, WHITE)
        screen.blit(player1_text, (WIDTH // 4, 20))  # Position for Player 1 score
        screen.blit(player2_text, (WIDTH * 3 // 4, 20))  # Position for Player 2 score

        pygame.display.flip()
        clock.tick(60)
