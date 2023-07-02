import pygame
import pygame.freetype
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set the frame rate
FPS = 60
clock = pygame.time.Clock()

# Set box parameters
BOX_COLOR = (173, 216, 230)  # Light blue
BOX_SIZE = (200, 100)
box = pygame.Surface(BOX_SIZE)
box.fill(BOX_COLOR)

# Set the message
font = pygame.freetype.SysFont(None, 50)
MESSAGE = "donut"

# Frame control
DISPLAY_FRAME = 1
HIDE_SEC = 2
HIDE_FRAMES = HIDE_SEC*60

frame_counter = 0


def draw_subliminal_message(screen):
    global frame_counter

    # Determine whether to show the message
    show_message = frame_counter % (
        DISPLAY_FRAME + HIDE_FRAMES) < DISPLAY_FRAME

    # Draw the box
    box_pos = (screen.get_width() // 2 -
               BOX_SIZE[0] // 2, screen.get_height() // 2 - BOX_SIZE[1] // 2)
    screen.blit(box, box_pos)

    # If it's time to show the message, draw it
    if show_message:
        text_surface, _ = font.render(MESSAGE, fgcolor=(0, 0, 0), size=50)
        text_pos = (box_pos[0] + BOX_SIZE[0] // 2 - text_surface.get_width() // 2,
                    box_pos[1] + BOX_SIZE[1] // 2 - text_surface.get_height() // 2)
        screen.blit(text_surface, text_pos)

    # Increase the frame counter
    frame_counter += 1

    # Limit the frame rate
    clock.tick(FPS)
