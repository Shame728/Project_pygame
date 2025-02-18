import pygame
from settings import *


class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(10, 10, WIDTH * HEALTH_BAR_WIDTH / 1080, HEIGHT * BAR_HEIGHT / 720)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, int(WIDTH * 3 / 1080))

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = WIDTH - 20
        y = HEIGHT - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(int(WIDTH * 20 / 1080), int(WIDTH * 20 / 1080)))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(int(WIDTH * 20 / 1080), int(WIDTH * 20 / 1080)), int(WIDTH * 3 / 1080))

    def show_blankets(self, col):
        text_surf = self.font.render(str(int(col)), False, TEXT_COLOR)
        x = WIDTH - 20
        y = 40
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(int(WIDTH * 20 / 1080), int(WIDTH * 20 / 1080)))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         text_rect.inflate(int(WIDTH * 20 / 1080), int(WIDTH * 20 / 1080)), int(WIDTH * 3 / 1080))

    def display(self, player):
        if player.godmod:
            self.show_bar(player.health, 100, self.health_bar_rect, GODMOD_COLOR)
        else:
            self.show_bar(player.health, 100, self.health_bar_rect, HEALTH_COLOR)

        self.show_exp(player.exp)
        self.show_blankets(player.bullet_resets)
