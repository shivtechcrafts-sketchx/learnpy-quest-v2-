import os
import pygame
from data.levels import LEVELS
from src.settings import KEY_SIZE, DOOR_WIDTH, DOOR_HEIGHT, YELLOW, GREEN, GRAY

class LevelManager:
    def __init__(self):
        self.level_index = 0
        self.level_data = None
        self.walls = []
        self.key_rect = None
        self.door_rect = None

        # Images
        self.wall_img = self.load_image("assets/images/wall.png", (32, 32))
        self.key_img = self.load_image("assets/images/key.png", (KEY_SIZE, KEY_SIZE))
        self.door_locked_img = self.load_image("assets/images/door_locked.png", (DOOR_WIDTH, DOOR_HEIGHT))
        self.door_unlocked_img = self.load_image("assets/images/door_unlocked.png", (DOOR_WIDTH, DOOR_HEIGHT))

        self.load_level()

    def load_image(self, path, size):
        try:
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, size)
                return img
        except Exception as e:
            print(f"[WARN] Could not load image {path}: {e}")
        return None

    def load_level(self):
        self.level_data = LEVELS[self.level_index]
        self.walls = [pygame.Rect(*wall) for wall in self.level_data["walls"]]

        kx, ky = self.level_data["key_pos"]
        dx, dy = self.level_data["door_pos"]

        self.key_rect = pygame.Rect(kx, ky, KEY_SIZE, KEY_SIZE)
        self.door_rect = pygame.Rect(dx, dy, DOOR_WIDTH, DOOR_HEIGHT)

    def next_level(self):
        self.level_index += 1
        if self.level_index >= len(LEVELS):
            return False
        self.load_level()
        return True

    def draw_wall_with_tiles(self, screen, wall_rect):
        """
        Tile the wall image across the wall rect.
        Fallback to rectangle if wall image missing.
        """
        if not self.wall_img:
            pygame.draw.rect(screen, GRAY, wall_rect)
            return

        tile_w, tile_h = self.wall_img.get_size()

        for x in range(wall_rect.left, wall_rect.right, tile_w):
            for y in range(wall_rect.top, wall_rect.bottom, tile_h):
                screen.blit(self.wall_img, (x, y))

    def draw(self, screen, has_key):
        # Draw walls
        for wall in self.walls:
            self.draw_wall_with_tiles(screen, wall)

        # Draw key
        if self.key_rect:
            if self.key_img:
                screen.blit(self.key_img, self.key_rect.topleft)
            else:
                pygame.draw.rect(screen, YELLOW, self.key_rect, border_radius=4)

        # Draw door
        if has_key:
            if self.door_locked_img and self.door_unlocked_img:
                screen.blit(self.door_unlocked_img, self.door_rect.topleft)
            else:
                pygame.draw.rect(screen, GREEN, self.door_rect, border_radius=4)
        else:
            if self.door_locked_img:
                screen.blit(self.door_locked_img, self.door_rect.topleft)
            else:
                pygame.draw.rect(screen, (120, 50, 50), self.door_rect, border_radius=4)