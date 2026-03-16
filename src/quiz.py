import pygame
from src.settings import WHITE, BLACK, BLUE, GREEN, RED, LIGHT_GRAY

class QuizManager:
    def __init__(self, font, big_font):
        self.font = font
        self.big_font = big_font
        self.active = False
        self.current_question = None
        self.selected_index = -1
        self.result = None

    def start_question(self, question_data):
        self.active = True
        self.current_question = question_data
        self.selected_index = -1
        self.result = None

    def handle_event(self, event):
        if not self.active or not self.current_question:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selected_index = 0
            elif event.key == pygame.K_2:
                self.selected_index = 1
            elif event.key == pygame.K_3:
                self.selected_index = 2
            elif event.key == pygame.K_4:
                self.selected_index = 3
            elif event.key == pygame.K_RETURN and self.selected_index != -1:
                selected_option = self.current_question["options"][self.selected_index]
                self.result = selected_option == self.current_question["answer"]
                self.active = False
                return self.result

        return None

    def draw(self, screen):
        if not self.active or not self.current_question:
            return

        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        box = pygame.Rect(80, 100, 640, 400)
        pygame.draw.rect(screen, WHITE, box, border_radius=12)
        pygame.draw.rect(screen, BLUE, box, 3, border_radius=12)

        title = self.big_font.render("Python Challenge", True, BLACK)
        screen.blit(title, (box.x + 20, box.y + 20))

        lines = self.wrap_text(self.current_question["question"], self.font, 580)
        y = box.y + 80
        for line in lines:
            text = self.font.render(line, True, BLACK)
            screen.blit(text, (box.x + 20, y))
            y += 28

        y += 20
        for i, option in enumerate(self.current_question["options"]):
            color = LIGHT_GRAY if i != self.selected_index else GREEN
            option_box = pygame.Rect(box.x + 20, y, 580, 40)
            pygame.draw.rect(screen, color, option_box, border_radius=8)
            opt_text = self.font.render(f"{i+1}. {option}", True, BLACK)
            screen.blit(opt_text, (option_box.x + 10, option_box.y + 8))
            y += 55

        hint = self.font.render("Press 1-4 to choose, ENTER to submit", True, RED)
        screen.blit(hint, (box.x + 20, box.bottom - 40))

    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines