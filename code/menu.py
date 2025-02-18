import math
import os
import time

import pygame


class Menu:
    def __init__(self, master, FPS, main_clock, font_, width, height):
        self.window = master
        self.running = True
        self.FPS = FPS
        self.last_time = time.time()
        self.main_clock = main_clock
        self.font = font_
        self.main_width = width
        self.main_height = height
        self.how = 0

        self.new_game = True
        self.exit = False

        self.change = False
        self.effect = pygame.mixer.Sound('../audio/sound_effect.wav')

        self.menu_index = 0
        self.max_menu_index = 2

        self.game_name = self.font.render("EXIT THE DUNGEON", False, 'black')
        self.cursor = self.font.render(">", False, 'black')
        self.start_text = self.font.render("НОВАЯ ИГРА", False, 'black')
        self.about_text = self.font.render("ПРОДОЛЖИТЬ ИГРУ", False, 'black')
        self.exit_text = self.font.render("ВЫЙТИ", False, 'black')

    def get_pulsing_text(self):
        scale = 1 + 0.05 * math.sin(self.how * 0.05)
        scaled_font = pygame.font.Font(None, int((self.main_width * 60 + self.main_height * 60) / (1920 + 1080) * scale))
        text = scaled_font.render("You did it :D", True, 'blue')
        text = pygame.transform.rotate(text, 20)
        return text

    def run(self):
        dt = time.time() - self.last_time
        dt *= 240
        self.last_time = time.time()

        self.window.fill('white')
        self.window.blit(self.game_name, (self.main_width * 600 / 1920, self.main_height * 0.3))
        self.window.blit(self.start_text, (self.main_width * 650 / 1920, self.main_height * 0.5))
        self.window.blit(self.about_text, (self.main_width * 650 / 1920, self.main_height * 0.6))
        self.window.blit(self.exit_text, (self.main_width * 650 / 1920, self.main_height * 0.7))

        if self.menu_index == 0:
            self.window.blit(self.cursor, (self.main_width * 600 / 1920, self.main_height * 0.5))
        elif self.menu_index == 1:
            self.window.blit(self.cursor, (self.main_width * 600 / 1920, self.main_height * 0.6))
        else:
            self.window.blit(self.cursor, (self.main_width * 600 / 1920, self.main_height * 0.7))
        self.change = False

        self.how += 1

        splash_text = self.get_pulsing_text()
        splash_rect = splash_text.get_rect(center=(self.main_width * 1350 / 1920, self.main_height * 380 / 1080))

        self.window.blit(splash_text, splash_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.menu_index += 1
                if self.menu_index > self.max_menu_index:
                    self.menu_index = 0

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.menu_index -= 1
                if self.menu_index < 0:
                    self.menu_index = self.max_menu_index

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.menu_index == 0:
                    self.new_game = True
                    self.change = True
                    self.effect.play(0)
                elif self.menu_index == 1:
                    self.new_game = False
                    self.change = True
                    self.effect.play(0)
                else:
                    self.exit = True

        pygame.display.update()
        self.main_clock.tick(self.FPS)


class Pause:
    def __init__(self, master, FPS, main_clock, font_, width, height):
        self.window = master
        self.running = True
        self.FPS = FPS
        self.last_time = time.time()
        self.main_clock = main_clock
        self.font = font_
        self.main_width = width
        self.main_height = height
        self.pressed = False

        self.current_button_is_continue = True

        self.effect = pygame.mixer.Sound('../audio/sound_effect.wav')

        self.myfont = pygame.font.Font(os.path.join("..", "graphics", "font.ttf"), 50)

        self.Pause_Window_Text = self.myfont.render('ПАУЗА', False, 'black')
        self.Pause_Window_Text_continue = self.myfont.render('ПРОДОЛЖИТЬ', False, 'black')
        self.Pause_Window_Text_back_main = self.myfont.render('ВЫЙТИ В ГЛАВНОЕ МЕНЮ', False, 'black')
        self.cursor = self.myfont.render(">", False, 'black')

    def pause_window(self, dt):
        if self.current_button_is_continue:
            self.window.fill('white')
            self.window.blit(self.cursor, (self.main_width * 650 / 1920, self.main_height * 0.5))
            self.window.blit(self.Pause_Window_Text_continue, (self.main_width * 700 / 1920, self.main_height * 0.5))
            self.window.blit(self.Pause_Window_Text_back_main, (self.main_width * 700 / 1920, self.main_height * 0.6))
            self.window.blit(self.Pause_Window_Text, (self.main_width * 800 / 1920, self.main_height * 0.3))
        else:
            self.window.fill('white')
            self.window.blit(self.cursor, (self.main_width * 650 / 1920, self.main_height * 0.6))
            self.window.blit(self.Pause_Window_Text_continue, (self.main_width * 700 / 1920, self.main_height * 0.5))
            self.window.blit(self.Pause_Window_Text_back_main, (self.main_width * 700 / 1920, self.main_height * 0.6))
            self.window.blit(self.Pause_Window_Text, (self.main_width * 800 / 1920, self.main_height * 0.3))
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and ((event.key == pygame.K_DOWN) or (event.key == pygame.K_UP)):
                self.current_button_is_continue = False if self.current_button_is_continue else True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.pressed = True
                self.effect.play(0)
