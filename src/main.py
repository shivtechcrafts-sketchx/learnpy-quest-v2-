import os
import sys
import random
import pygame

# ==========================================
# SETTINGS
# ==========================================
WIDTH, HEIGHT = 1000, 700
FPS = 60
TITLE = "LearnPy Quest V2"

WHITE = (245, 250, 255)
BLACK = (10, 15, 20)
CYAN = (0, 220, 255)
BLUE = (0, 120, 255)
GREEN = (0, 255, 140)
RED = (255, 80, 80)
YELLOW = (255, 220, 0)
GRAY = (70, 80, 95)
DARK_BG = (8, 16, 28)
PANEL = (18, 28, 45)
PANEL_2 = (28, 38, 58)

PLAYER_SIZE = 32
PLAYER_SPEED = 4
KEY_SIZE = 24
DOOR_SIZE = (48, 72)
WALL_TILE = 32

# ==========================================
# DATA: QUESTIONS
# ==========================================
QUESTIONS = [
    {
        "concept": "Variables",
        "question": "What is the output of print(2 + 3)?",
        "options": ["23", "5", "Error", "None"],
        "answer": "5"
    },
    {
        "concept": "Data Types",
        "question": "Which data type is 'Hello'?",
        "options": ["int", "float", "str", "bool"],
        "answer": "str"
    },
    {
        "concept": "Variables",
        "question": "What does this print?\n\nx = 10\nprint(x)",
        "options": ["x", "10", "Error", "None"],
        "answer": "10"
    },
    {
        "concept": "Conditionals",
        "question": "Which keyword is used for condition checking?",
        "options": ["for", "if", "def", "while"],
        "answer": "if"
    },
    {
        "concept": "Operators",
        "question": "What is the output of print(10 % 3)?",
        "options": ["3", "1", "0", "10"],
        "answer": "1"
    },
    {
        "concept": "Loops",
        "question": "Which loop is used to iterate over a sequence?",
        "options": ["if", "for", "def", "class"],
        "answer": "for"
    },
    {
        "concept": "Lists",
        "question": "What is the index of the first item in a list?",
        "options": ["0", "1", "-1", "None"],
        "answer": "0"
    },
    {
        "concept": "Functions",
        "question": "Which keyword is used to create a function?",
        "options": ["func", "define", "def", "lambda"],
        "answer": "def"
    },
    {
        "concept": "Booleans",
        "question": "What is the value of: 5 > 2 ?",
        "options": ["True", "False", "None", "0"],
        "answer": "True"
    },
    {
        "concept": "Lists",
        "question": "Which method adds an item to a list?",
        "options": ["push()", "add()", "append()", "insertEnd()"],
        "answer": "append()"
    },
    {
        "concept": "Loops",
        "question": "How many times will this run?\n\nfor i in range(3):",
        "options": ["2", "3", "4", "Infinite"],
        "answer": "3"
    },
    {
        "concept": "Functions",
        "question": "What does a function use to send back a value?",
        "options": ["print", "send", "return", "yieldback"],
        "answer": "return"
    }
]

# ==========================================
# DATA: LEVELS
# Each level has a maze + question count
# ==========================================
LEVELS = [
    {
        "name": "Level 1 - Basics",
        "question_count": 2,
        "walls": [
            (100, 80, 800, 20),
            (100, 80, 20, 520),
            (100, 580, 800, 20),
            (880, 80, 20, 520),

            (220, 140, 20, 380),
            (340, 80, 20, 280),
            (460, 220, 20, 380),
            (580, 80, 20, 280),
            (700, 220, 20, 380),
        ],
        "player_start": (140, 120),
        "key_pos": (150, 530),
        "door_pos": (820, 500)
    },
    {
        "name": "Level 2 - Logic",
        "question_count": 3,
        "walls": [
            (70, 60, 860, 20),
            (70, 60, 20, 560),
            (70, 600, 860, 20),
            (910, 60, 20, 560),

            (180, 120, 20, 420),
            (300, 60, 20, 280),
            (420, 220, 20, 400),
            (540, 60, 20, 280),
            (660, 220, 20, 400),
            (780, 60, 20, 280),
        ],
        "player_start": (110, 100),
        "key_pos": (120, 560),
        "door_pos": (850, 520)
    },
    {
        "name": "Level 3 - Python Master",
        "question_count": 4,
        "walls": [
            (60, 50, 880, 20),
            (60, 50, 20, 580),
            (60, 610, 880, 20),
            (920, 50, 20, 580),

            (160, 100, 20, 450),
            (280, 50, 20, 300),
            (400, 200, 20, 430),
            (520, 50, 20, 300),
            (640, 200, 20, 430),
            (760, 50, 20, 300),
        ],
        "player_start": (100, 90),
        "key_pos": (100, 580),
        "door_pos": (860, 540)
    }
]

# ==========================================
# INIT
# ==========================================
pygame.init()

SOUND_ENABLED = True
try:
    pygame.mixer.init()
except pygame.error:
    SOUND_ENABLED = False
    print("[WARN] Audio unavailable. Continuing without sound.")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("consolas", 20)
font = pygame.font.SysFont("consolas", 24)
font_big = pygame.font.SysFont("consolas", 40, bold=True)
font_huge = pygame.font.SysFont("consolas", 58, bold=True)

# ==========================================
# ASSET LOADERS
# ==========================================
def load_image(path, size=None, alpha=True):
    try:
        if os.path.exists(path):
            img = pygame.image.load(path)
            img = img.convert_alpha() if alpha else img.convert()
            if size:
                img = pygame.transform.scale(img, size)
            return img
    except Exception as e:
        print(f"[WARN] Could not load image {path}: {e}")
    return None

def load_sound(path):
    if not SOUND_ENABLED:
        return None
    try:
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"[WARN] Could not load sound {path}: {e}")
    return None

# ==========================================
# LOAD ASSETS
# ==========================================
bg_img = load_image("assets/images/background.png", (WIDTH, HEIGHT), alpha=False)
logo_img = load_image("assets/images/logo.png", (500, 140))
player_img = load_image("assets/images/player.png", (PLAYER_SIZE, PLAYER_SIZE))
wall_img = load_image("assets/images/wall.png", (WALL_TILE, WALL_TILE))
key_img = load_image("assets/images/key.png", (KEY_SIZE, KEY_SIZE))
door_locked_img = load_image("assets/images/door_locked.png", DOOR_SIZE)
door_unlocked_img = load_image("assets/images/door_unlocked.png", DOOR_SIZE)

correct_sound = load_sound("assets/sounds/correct.wav")
wrong_sound = load_sound("assets/sounds/wrong.wav")
key_sound = load_sound("assets/sounds/key_pickup.wav")
door_sound = load_sound("assets/sounds/door_open.wav")

if SOUND_ENABLED and os.path.exists("assets/sounds/bg_music.wav"):
    try:
        pygame.mixer.music.load("assets/sounds/bg_music.wav")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"[WARN] Could not play bg music: {e}")

def play_sound(snd):
    if SOUND_ENABLED and snd:
        snd.play()

# ==========================================
# UI COMPONENTS
# ==========================================
class Button:
    def __init__(self, x, y, w, h, text, color=CYAN):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surf):
        fill = PANEL_2 if self.hovered else PANEL
        border = self.color if self.hovered else WHITE
        pygame.draw.rect(surf, fill, self.rect, border_radius=14)
        pygame.draw.rect(surf, border, self.rect, 3, border_radius=14)

        text_surf = font.render(self.text, True, self.color if self.hovered else WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surf.blit(text_surf, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered

# ==========================================
# PLAYER
# ==========================================
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED

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

        # Horizontal
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right

        # Vertical
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                elif dy < 0:
                    self.rect.top = wall.bottom

    def draw(self, surf):
        if player_img:
            surf.blit(player_img, self.rect.topleft)
        else:
            pygame.draw.rect(surf, BLUE, self.rect, border_radius=8)
            pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=8)

# ==========================================
# LEVEL MANAGER
# ==========================================
class LevelManager:
    def __init__(self):
        self.level_index = 0
        self.level_data = None
        self.walls = []
        self.key_rect = None
        self.door_rect = None
        self.load_level()

    def load_level(self):
        self.level_data = LEVELS[self.level_index]
        self.walls = [pygame.Rect(*wall) for wall in self.level_data["walls"]]
        self.key_rect = pygame.Rect(
            self.level_data["key_pos"][0],
            self.level_data["key_pos"][1],
            KEY_SIZE,
            KEY_SIZE
        )
        self.door_rect = pygame.Rect(
            self.level_data["door_pos"][0],
            self.level_data["door_pos"][1],
            DOOR_SIZE[0],
            DOOR_SIZE[1]
        )

    def next_level(self):
        self.level_index += 1
        if self.level_index >= len(LEVELS):
            return False
        self.load_level()
        return True

    def get_start_pos(self):
        return self.level_data["player_start"]

    def get_question_count(self):
        return self.level_data["question_count"]

    def draw_walls(self, surf):
        for wall in self.walls:
            if wall_img:
                for x in range(wall.left, wall.right, WALL_TILE):
                    for y in range(wall.top, wall.bottom, WALL_TILE):
                        surf.blit(wall_img, (x, y))
            else:
                pygame.draw.rect(surf, GRAY, wall)

    def draw(self, surf, has_key):
        self.draw_walls(surf)

        # Key
        if self.key_rect:
            if key_img:
                surf.blit(key_img, self.key_rect.topleft)
            else:
                pygame.draw.rect(surf, YELLOW, self.key_rect, border_radius=4)

        # Door
        if has_key:
            if door_unlocked_img:
                surf.blit(door_unlocked_img, self.door_rect.topleft)
            else:
                pygame.draw.rect(surf, GREEN, self.door_rect, border_radius=8)
        else:
            if door_locked_img:
                surf.blit(door_locked_img, self.door_rect.topleft)
            else:
                pygame.draw.rect(surf, RED, self.door_rect, border_radius=8)

# ==========================================
# QUIZ MANAGER
# ==========================================
class QuizManager:
    def __init__(self):
        self.active = False
        self.question = None
        self.selected = None
        self.option_buttons = []
        self.submit_button = Button(410, 560, 180, 50, "Submit", GREEN)

    def start(self, question):
        self.active = True
        self.question = question
        self.selected = None
        self.option_buttons = []

        start_y = 340
        for i, option in enumerate(question["options"]):
            btn = Button(180, start_y + i * 60, 640, 45, f"{i+1}. {option}", CYAN)
            self.option_buttons.append(btn)

    def handle_event(self, event):
        if not self.active:
            return None

        mouse_pos = pygame.mouse.get_pos()
        for btn in self.option_buttons:
            btn.update(mouse_pos)
        self.submit_button.update(mouse_pos)

        # Mouse select
        for i, btn in enumerate(self.option_buttons):
            if btn.clicked(event):
                self.selected = i

        # Mouse submit
        if self.submit_button.clicked(event) and self.selected is not None:
            return self.check_answer()

        # Keyboard support
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selected = 0
            elif event.key == pygame.K_2:
                self.selected = 1
            elif event.key == pygame.K_3:
                self.selected = 2
            elif event.key == pygame.K_4:
                self.selected = 3
            elif event.key == pygame.K_RETURN and self.selected is not None:
                return self.check_answer()

        return None

    def check_answer(self):
        selected_text = self.question["options"][self.selected]
        correct = selected_text == self.question["answer"]
        self.active = False
        return correct

    def draw_wrapped_text(self, surf, text, x, y, max_width, line_height=28, color=WHITE):
        words = text.split(" ")
        line = ""
        current_y = y

        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                text_surf = font.render(line.strip(), True, color)
                surf.blit(text_surf, (x, current_y))
                current_y += line_height
                line = word + " "

        if line:
            text_surf = font.render(line.strip(), True, color)
            surf.blit(text_surf, (x, current_y))

    def draw(self, surf):
        if not self.active or not self.question:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surf.blit(overlay, (0, 0))

        panel = pygame.Rect(120, 90, 760, 540)
        pygame.draw.rect(surf, PANEL, panel, border_radius=18)
        pygame.draw.rect(surf, CYAN, panel, 3, border_radius=18)

        title = font_big.render("Python Challenge", True, CYAN)
        surf.blit(title, (panel.x + 25, panel.y + 20))

        concept = font_small.render(f"Concept: {self.question['concept']}", True, YELLOW)
        surf.blit(concept, (panel.x + 25, panel.y + 75))

        # Question
        q_lines = self.question["question"].split("\n")
        qy = panel.y + 120
        for line in q_lines:
            self.draw_wrapped_text(surf, line, panel.x + 25, qy, 700, color=WHITE)
            qy += 34

        # Options
        mouse_pos = pygame.mouse.get_pos()
        for i, btn in enumerate(self.option_buttons):
            btn.update(mouse_pos)

            # Highlight selected option
            if self.selected == i:
                pygame.draw.rect(surf, (30, 70, 100), btn.rect, border_radius=12)
                pygame.draw.rect(surf, GREEN, btn.rect, 3, border_radius=12)
                text_surf = font.render(btn.text, True, GREEN)
                surf.blit(text_surf, text_surf.get_rect(center=btn.rect.center))
            else:
                btn.draw(surf)

        self.submit_button.update(mouse_pos)
        self.submit_button.draw(surf)

        hint = font_small.render("Mouse click or press 1-4, then ENTER", True, WHITE)
        surf.blit(hint, (panel.x + 25, panel.bottom - 35))

# ==========================================
# GAME CLASS
# ==========================================
class Game:
    def __init__(self):
        self.state = "menu"

        self.level_manager = LevelManager()
        start_x, start_y = self.level_manager.get_start_pos()
        self.player = Player(start_x, start_y)

        self.quiz = QuizManager()

        self.score = 0
        self.lives = 3
        self.has_key = False
        self.door_triggered = False

        self.current_level_questions = []
        self.questions_answered = 0
        self.level_complete_timer = 0

        # Buttons
        self.start_btn = Button(380, 420, 240, 60, "Start Game", CYAN)
        self.restart_btn = Button(380, 500, 240, 60, "Restart", GREEN)
        self.quit_btn = Button(380, 580, 240, 60, "Quit", RED)

        self.prepare_level_questions()

    # --------------------------------------
    # Level / Reset
    # --------------------------------------
    def prepare_level_questions(self):
        count = self.level_manager.get_question_count()
        count = min(count, len(QUESTIONS))
        self.current_level_questions = random.sample(QUESTIONS, count)
        self.questions_answered = 0

    def reset_player_to_level_start(self):
        x, y = self.level_manager.get_start_pos()
        self.player.rect.topleft = (x, y)

    def start_level(self):
        self.has_key = False
        self.door_triggered = False
        self.level_complete_timer = 0
        self.reset_player_to_level_start()
        self.prepare_level_questions()

    def full_reset(self):
        self.level_manager = LevelManager()
        sx, sy = self.level_manager.get_start_pos()
        self.player = Player(sx, sy)
        self.quiz = QuizManager()

        self.score = 0
        self.lives = 3
        self.has_key = False
        self.door_triggered = False
        self.level_complete_timer = 0
        self.prepare_level_questions()
        self.state = "menu"

    # --------------------------------------
    # Quiz Flow
    # --------------------------------------
    def get_next_question(self):
        if self.questions_answered < len(self.current_level_questions):
            return self.current_level_questions[self.questions_answered]
        return None

    def handle_correct_answer(self):
        play_sound(correct_sound)
        self.score += 10
        self.questions_answered += 1

        # If still questions left, reopen quiz on same door
        next_q = self.get_next_question()
        if next_q:
            self.quiz.start(next_q)
        else:
            # Level complete
            self.state = "level_complete"
            self.level_complete_timer = pygame.time.get_ticks()

    def handle_wrong_answer(self):
        play_sound(wrong_sound)
        self.lives -= 1
        self.door_triggered = False
        self.reset_player_to_level_start()

        if self.lives <= 0:
            self.state = "game_over"

    # --------------------------------------
    # Drawing Helpers
    # --------------------------------------
    def draw_background(self):
        if bg_img:
            screen.blit(bg_img, (0, 0))
        else:
            screen.fill(DARK_BG)

    def draw_logo_or_title(self):
        if logo_img:
            screen.blit(logo_img, (250, 120))
        else:
            title = font_huge.render("LearnPy Quest", True, CYAN)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))

    def draw_hud(self):
        hud = pygame.Rect(20, 15, WIDTH - 40, 50)
        pygame.draw.rect(screen, PANEL, hud, border_radius=12)
        pygame.draw.rect(screen, CYAN, hud, 2, border_radius=12)

        level_name = self.level_manager.level_data["name"]
        total_q = len(self.current_level_questions)
        progress = f"{self.questions_answered}/{total_q}"

        hud_items = [
            (f"Score: {self.score}", YELLOW, 40),
            (f"Lives: {self.lives}", RED, 200),
            (f"{level_name}", GREEN, 350),
            (f"Key: {'Yes' if self.has_key else 'No'}", WHITE, 680),
            (f"Q: {progress}", CYAN, 850),
        ]

        for text, color, x in hud_items:
            surf = font_small.render(text, True, color)
            screen.blit(surf, (x, 30))

    def draw_instructions(self):
        box = pygame.Rect(20, HEIGHT - 70, WIDTH - 40, 45)
        pygame.draw.rect(screen, PANEL, box, border_radius=10)
        pygame.draw.rect(screen, WHITE, box, 1, border_radius=10)

        txt = "Move: WASD / Arrows | Collect KEY | Reach DOOR | Solve all Python questions"
        surf = font_small.render(txt, True, WHITE)
        screen.blit(surf, (35, HEIGHT - 57))

    def draw_menu(self):
        self.draw_background()
        self.draw_logo_or_title()

        subtitle = font.render("Learn Python Basics Through Gameplay", True, WHITE)
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 300)))

        mouse_pos = pygame.mouse.get_pos()
        self.start_btn.update(mouse_pos)
        self.quit_btn.update(mouse_pos)

        self.start_btn.draw(screen)
        self.quit_btn.draw(screen)

    def draw_game(self):
        self.draw_background()
        self.level_manager.draw(screen, self.has_key)
        self.player.draw(screen)
        self.draw_hud()
        self.draw_instructions()

        if self.quiz.active:
            self.quiz.draw(screen)

    def draw_level_complete(self):
        self.draw_game()

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(250, 220, 500, 220)
        pygame.draw.rect(screen, PANEL, panel, border_radius=18)
        pygame.draw.rect(screen, GREEN, panel, 3, border_radius=18)

        t1 = font_big.render("Level Complete!", True, GREEN)
        t2 = font.render("Get ready for the next challenge...", True, WHITE)

        screen.blit(t1, t1.get_rect(center=(WIDTH // 2, 290)))
        screen.blit(t2, t2.get_rect(center=(WIDTH // 2, 350)))

    def draw_game_over(self):
        self.draw_background()
        title = font_huge.render("GAME OVER", True, RED)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 200)))

        score_txt = font.render(f"Final Score: {self.score}", True, WHITE)
        screen.blit(score_txt, score_txt.get_rect(center=(WIDTH // 2, 290)))

        mouse_pos = pygame.mouse.get_pos()
        self.restart_btn.update(mouse_pos)
        self.quit_btn.update(mouse_pos)

        self.restart_btn.draw(screen)
        self.quit_btn.draw(screen)

    def draw_win(self):
        self.draw_background()
        title = font_huge.render("YOU MASTERED PYTHON!", True, GREEN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))

        score_txt = font.render(f"Final Score: {self.score}", True, YELLOW)
        screen.blit(score_txt, score_txt.get_rect(center=(WIDTH // 2, 260)))

        badge_txt = font.render("🏆 Python Basics Conquered", True, WHITE)
        screen.blit(badge_txt, badge_txt.get_rect(center=(WIDTH // 2, 320)))

        mouse_pos = pygame.mouse.get_pos()
        self.restart_btn.update(mouse_pos)
        self.quit_btn.update(mouse_pos)

        self.restart_btn.draw(screen)
        self.quit_btn.draw(screen)

    # --------------------------------------
    # Event Handling
    # --------------------------------------
    def handle_menu_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.start_btn.update(mouse_pos)
        self.quit_btn.update(mouse_pos)

        if self.start_btn.clicked(event):
            self.state = "playing"
            self.start_level()

        if self.quit_btn.clicked(event):
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state = "playing"
                self.start_level()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def handle_playing_events(self, event):
        if self.quiz.active:
            result = self.quiz.handle_event(event)
            if result is not None:
                if result:
                    self.handle_correct_answer()
                else:
                    self.handle_wrong_answer()

    def handle_end_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.restart_btn.update(mouse_pos)
        self.quit_btn.update(mouse_pos)

        if self.restart_btn.clicked(event):
            self.full_reset()

        if self.quit_btn.clicked(event):
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.full_reset()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # --------------------------------------
    # Update
    # --------------------------------------
    def update_playing(self):
        if not self.quiz.active:
            self.player.move(self.level_manager.walls)

            # Key pickup
            if self.level_manager.key_rect and self.player.rect.colliderect(self.level_manager.key_rect):
                self.has_key = True
                self.level_manager.key_rect = None
                self.score += 5
                play_sound(key_sound)

            # Door trigger
            if self.has_key and not self.door_triggered and self.player.rect.colliderect(self.level_manager.door_rect):
                play_sound(door_sound)
                next_q = self.get_next_question()
                if next_q:
                    self.quiz.start(next_q)
                    self.door_triggered = True

    def update_level_complete(self):
        # Wait 1.8 sec then go next level / win
        now = pygame.time.get_ticks()
        if now - self.level_complete_timer > 1800:
            has_next = self.level_manager.next_level()
            if has_next:
                self.start_level()
                self.state = "playing"
            else:
                self.state = "win"

    def update(self):
        if self.state == "playing":
            self.update_playing()
        elif self.state == "level_complete":
            self.update_level_complete()

    # --------------------------------------
    # Draw
    # --------------------------------------
    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "level_complete":
            self.draw_level_complete()
        elif self.state == "game_over":
            self.draw_game_over()
        elif self.state == "win":
            self.draw_win()

# ==========================================
# MAIN LOOP
# ==========================================
game = Game()

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game.state == "menu":
            game.handle_menu_events(event)
        elif game.state == "playing":
            game.handle_playing_events(event)
        elif game.state in ["game_over", "win"]:
            game.handle_end_events(event)

    game.update()
    game.draw()
    pygame.display.flip()