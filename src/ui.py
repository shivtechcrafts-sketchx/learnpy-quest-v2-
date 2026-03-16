import pygame
from src.settings import WHITE, YELLOW, RED, GREEN, BLACK

def draw_text(screen, text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_hud(screen, font, score, lives, level_name, has_key):
    draw_text(screen, f"Score: {score}", font, YELLOW, 20, 15)
    draw_text(screen, f"Lives: {lives}", font, RED, 160, 15)
    draw_text(screen, level_name, font, GREEN, 300, 15)
    draw_text(screen, f"Key: {'Yes' if has_key else 'No'}", font, WHITE, 620, 15)

def draw_center_message(screen, text, big_font, color=WHITE):
    msg = big_font.render(text, True, color)
    rect = msg.get_rect(center=(400, 300))
    screen.blit(msg, rect)

def draw_instructions(screen, font):
    instructions = [
        "Move: WASD / Arrow Keys",
        "Collect the KEY",
        "Go to the DOOR",
        "Answer Python question to unlock next level"
    ]
    y = 520
    for line in instructions:
        txt = font.render(line, True, BLACK)
        screen.blit(txt, (20, y))
        y += 20