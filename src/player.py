import os
import pygame
from src.settings import PLAYER_SIZE, PLAYER_SPEED, BLUE

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED
        self.image = self.load_image("assets/images/player.png", (PLAYER_SIZE, PLAYER_SIZE))

    def load_image(self, path, size):
        try:
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, size)
                return img
        except Exception as e:
            print(f"[WARN] Could not load player image {path}: {e}")
        return None

    def move(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed

        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                if dx < 0:
                    self.rect.left = wall.right

        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                if dy < 0:
                    self.rect.top = wall.bottom

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, BLUE, self.rect, border_radius=6)