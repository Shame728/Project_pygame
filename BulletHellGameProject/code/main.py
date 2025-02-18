import pygame.mixer
import ctypes
from level import Level
from menu import *
from settings import *

ctypes.windll.user32.SetProcessDPIAware()


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)

        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('BulletHell')
        self.clock = pygame.time.Clock()
        self.effect = pygame.mixer.Sound('../audio/sound_effect.wav')
        self.transition = pygame.mixer.Sound('../audio/transition.wav')

        self.menu_loop = pygame.mixer.Sound('../audio/main_menu_fon.mp3')
        self.menu_loop.play(-1)
        self.win_sound = pygame.mixer.Sound('../audio/win.mp3')
        self.lost_sound = pygame.mixer.Sound('../audio/lose.wav')
        self.FPS = 60

        self.current_level = LEVEL_1
        self.starting = True
        self.playing = False
        self.pause = False
        self.win = False

        self.database = []
        self.load_data()

        self.health = self.database[0]
        self.exp = self.database[1]
        self.bullet_resets = self.database[2]
        self.level_index = self.database[3]

        self.get_level_index()
        self.level = Level(self.current_level, self.health, self.exp, self.bullet_resets)

        self.last_time = time.time()
        self.main_clock = pygame.time.Clock()
        self.myfont = pygame.font.Font(os.path.join("..", "graphics", "font.ttf"),
                                       int((WIDTH * 60 + HEIGHT * 60) / (1920 + 1080)))
        self.menu = Menu(self.screen, FPS, self.main_clock, self.myfont, WIDTH, HEIGHT)
        self.pause_win = Pause(self.screen, FPS, self.main_clock, self.myfont, WIDTH, HEIGHT)
        self.Game_Lost_Text = self.myfont.render("ВЫ ПРОИГРАЛИ", False, 'black')
        self.Game_Win_Text = self.myfont.render("ВЫ ВЫИГРАЛИ", False, 'black')
        self.Pause_Window_Text = self.myfont.render('ПАУЗА', False, 'black')
        self.Pause_Window_Text_continue = self.myfont.render('ПРОДОЛЖИТЬ', False, 'black')
        self.Pause_Window_Text_back_main = self.myfont.render('ВЫЙТИ В ГЛАВНОЕ МЕНЮ', False, 'black')
        self.Score = self.myfont.render('КОЛИЧЕСТВО ОЧКОВ:', False, 'black')
        self.Game_Lost_text_retry = self.myfont.render('ENTER - НАЧАТЬ ИГРУ С НАЧАЛА', False, 'black')
        self.Game_Lost_text_back = self.myfont.render('BACKSPACE - ГЛАВНОЕ МЕНЮ', False,
                                                      'black')
        self.cursor = self.myfont.render(">", False, 'black')

    def get_level_index(self):
        if self.level_index == 0:
            self.current_level = LEVEL_1
        elif self.level_index == 1:
            self.current_level = LEVEL_2
        elif self.level_index == 2:
            self.current_level = LEVEL_3
        else:
            self.playing = False
            self.win = True
            self.win_sound.play()
            self.level_index = 0
            self.current_level = LEVEL_1
            return None

    def fade(self, width, height):
        fade = pygame.surface.Surface((width, height))
        fade.fill((255, 255, 255))
        for alpha in range(0, 255):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)

    def load_data(self):
        f = open("../saves/save.txt", 'r')
        for i in f.readlines():
            self.database.append(int(i[:-1]))
        f.close()

    def save_and_exit(self):
        f = open("../saves/save.txt", 'w')
        for i in self.database:
            f.write(f"{str(i)}\n")
        f.close()

        self.effect.play(0)
        time.sleep(0.4)
        self.menu.running = False

    def run(self):
        while self.menu.running:
            dt = self.last_time - time.time()
            dt *= 240
            self.last_time = time.time()

            if self.starting:
                if self.menu.change:
                    if self.pause:
                        self.pause_win.run(dt)
                    else:
                        if self.menu.new_game:
                            self.health = 100
                            self.exp = 0
                            self.bullet_resets = 3
                            self.level = Level(LEVEL_1, self.health, self.exp, self.bullet_resets)
                        self.starting = False
                        self.playing = True
                        self.level.game_over = False
                self.menu.run(dt)
            else:
                self.menu_loop.stop()

            if self.playing:
                self.screen.fill('black')
                self.level.run()
                
            if self.level.game_over:
                self.playing = False
                self.screen.fill('white')
                self.screen.blit(self.Game_Lost_Text, (WIDTH * 600 / 1920, HEIGHT * 0.3))
                self.screen.blit(self.Game_Lost_text_retry, (WIDTH * 300 / 1920, HEIGHT * 0.6))
                self.screen.blit(self.Game_Lost_text_back, (WIDTH * 350 / 1920, HEIGHT * 0.7))

            if self.pause:
                self.playing = False
                if self.pause_win.pressed:
                    self.pause = False
                    self.pause_win.pressed = False
                    if self.pause_win.current_button_is_continue:
                        self.playing = True
                    else:
                        self.starting = True
                        self.menu_loop.play(-1)
                        self.pause_win.current_button_is_continue = True
                else:
                    self.pause_win.run(dt)

            if self.win:
                self.menu.win = True
                self.Score = self.myfont.render(f"КОЛИЧЕСТВО ОЧКОВ: {self.exp}", False, 'black')
                self.screen.fill('white')
                self.screen.blit(self.Game_Win_Text, (WIDTH * 650 / 1920, HEIGHT * 0.3))
                self.screen.blit(self.Score, (WIDTH * 400 / 1920, HEIGHT * 0.45))
                self.screen.blit(self.Game_Lost_text_back, (WIDTH * 350 / 1920, HEIGHT * 0.7))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu.running = False

                if self.win and event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.win = False
                    self.effect.play(0)
                    self.starting = True
                    self.menu_loop.play(-1)

                if self.playing and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause = True
                    self.effect.play(0)
                    self.playing = False

                if self.level.game_over:
                    self.health = 100
                    self.exp = 0
                    self.bullet_resets = 3

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.playing = True
                        self.level = Level(LEVEL_1, self.health, self.exp, self.bullet_resets)
                        self.level.game_over = False
                        self.effect.play(0)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        self.starting = True
                        self.level = Level(LEVEL_1, self.health, self.exp, self.bullet_resets)
                        self.effect.play(0)
                        self.level.game_over = False
                        self.menu_loop.play(-1)
                
            if self.level.level_complete:
                self.level_index += 1
                self.get_level_index()
                self.database = self.level.level_complete_data + [self.level_index]
                self.health = self.database[0]
                self.exp = self.database[1]
                self.bullet_resets = self.database[2]
                self.level = Level(self.current_level, self.health, self.exp, self.bullet_resets)
                self.transition.play()
                self.fade(self.screen.get_width(), self.screen.get_height())
                self.effect.play()

            if self.menu.exit:
                self.save_and_exit()

            pygame.display.update()
            self.main_clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
