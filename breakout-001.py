# breakout.py
import pygame
import sys
from subliminal import draw_subliminal_message
# add this line
from colors import BLACK, PADDLE_COLOR, BALL_COLOR, BRICK_COLORS, BUTTON_COLOR

# Initialize Pygame
pygame.init()

# Set screen parameters
infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

# Set the frame rate
FPS = 60
clock = pygame.time.Clock()

# Set brick parameters
# Decrease the brick size for 1px space around each brick
BRICK_WIDTH, BRICK_HEIGHT = 58, 18
bricks = [(pygame.Rect(j*(BRICK_WIDTH+2), i*(BRICK_HEIGHT+2) + SCREEN_HEIGHT*0.1, BRICK_WIDTH, BRICK_HEIGHT), BRICK_COLORS[i % len(BRICK_COLORS)])  # Shift bricks down
          for i in range(5) for j in range(SCREEN_WIDTH // (BRICK_WIDTH+2))]

# Set ball parameters
BALL_RADIUS = 10
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT //
                   2, BALL_RADIUS, BALL_RADIUS)
ball_dx, ball_dy = 3, 3

# Set paddle parameters
PADDLE_WIDTH, PADDLE_HEIGHT = 80, 20  # Set paddle height to 20px
paddle = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PADDLE_HEIGHT *
                     2 - SCREEN_HEIGHT*0.1, PADDLE_WIDTH, PADDLE_HEIGHT)  # Shift paddle up
paddle_dx = 8  # Quadruple the paddle speed

# Set button parameters
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 60
button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
                     SCREEN_HEIGHT - SCREEN_HEIGHT*3//4, BUTTON_WIDTH, BUTTON_HEIGHT)

# Game state
game_over = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if button.collidepoint(pos):
                game_over = False
                ball = pygame.Rect(
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
                bricks = [(pygame.Rect(j*(BRICK_WIDTH+2), i*(BRICK_HEIGHT+2) + SCREEN_HEIGHT*0.1, BRICK_WIDTH, BRICK_HEIGHT), BRICK_COLORS[i % len(BRICK_COLORS)])
                          for i in range(5) for j in range(SCREEN_WIDTH // (BRICK_WIDTH+2))]

    if not game_over:
        # Move the paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-paddle_dx, 0)
        if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.move_ip(paddle_dx, 0)

        # Move the ball and check for collision
        ball.move_ip(ball_dx, ball_dy)
        if ball.left < 0 or ball.right > SCREEN_WIDTH:
            ball_dx *= -1
        if ball.top < 0 or ball.colliderect(paddle):
            ball_dy *= -1
        if ball.bottom > SCREEN_HEIGHT:
            game_over = True

        # Check for collision with bricks
        brick_collision_index = ball.collidelist(
            [brick for brick, color in bricks])
        if brick_collision_index != -1:
            hb = bricks.pop(brick_collision_index)
            mx = ball.x + BALL_RADIUS
            if mx < hb[0].x or mx > hb[0].right:
                ball_dx *= -1
            else:
                ball_dy *= -1

    # Draw everything
    screen.fill(BLACK)
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick)
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)
    pygame.draw.circle(screen, BALL_COLOR, ball.center, BALL_RADIUS)
    if game_over:
        pygame.draw.rect(screen, BUTTON_COLOR, button)
        font = pygame.font.Font(None, 36)
        text = font.render("Try Again", True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = button.center
        screen.blit(text, text_rect)

    draw_subliminal_message(screen)  # Add this line

    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FPS)
