import pygame
from Texts import Texts


# класс отрисовки событий
class Pictures:
    WIDTH = 750
    HEIGHT = 500
    BORDER_FIELD_PLAY = (5, 5, 490, 490)
    BORDER_FIELD_LOT = (502, 5, 240, 150)
    TEXT_RULES = (30, 150, 150)
    TEXT_BUTTON_AFTER_PRESSED = (190, 190, 190)
    TEXT_BUTTON = (30, 150, 150)
    LOT_FOND = (100, 180, 200)
    TEXT_STYLE = "arial.ttf"
    TEXT_STYLE_DEFAULT = "Arial"
    BUTTON_FRAME = (130, 200, 130)
    TEXT_SIZE = 22

    # создание окна игры
    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen.fill(pygame.Color('white'))
        pygame.display.set_caption("БРИДЖ-ИТ")

    # включение фоновой музыки
    @staticmethod
    def music():
        try:
            pygame.mixer.music.load('fon_music.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.2)
        except Exception:
            pass

    # отрисовка заставки
    def splash_screen(self):
        splash = pygame.image.load('splash.png').convert_alpha()
        new_splash = pygame.transform.scale(splash, (self.BORDER_FIELD_PLAY[2], self.BORDER_FIELD_PLAY[3]))
        self.screen.blit(new_splash, (self.BORDER_FIELD_PLAY[0], self.BORDER_FIELD_PLAY[1]))
        pygame.draw.rect(self.screen, pygame.Color('black'), self.BORDER_FIELD_PLAY, 2)
        text = Pictures.choice_style_text(90)
        self.screen.blit(text.render('БРИДЖ-ИТ', True, (50, 200, 50)), (5, 205))

    # отрисовка правил игры
    def rules_game(self):
        pygame.draw.rect(self.screen, pygame.Color('white'), self.BORDER_FIELD_PLAY, 0)
        pygame.draw.rect(self.screen, pygame.Color('black'), self.BORDER_FIELD_PLAY, 2)
        text = Pictures.choice_style_text(self.TEXT_SIZE)
        x = 10
        y = 10
        for i in range(len(Texts.RULES)):
            self.screen.blit(text.render(Texts.RULES[i], True, self.TEXT_RULES), (x, y))
            y += 32

    # отрисовка игрового поля
    def playing_field(self):
        x_red_min = y_blue_min = 50
        y_red_min = x_blue_min = 25
        x_red_max = y_blue_max = 451
        x_blue_max = y_red_max = 476
        step = 50
        pygame.draw.rect(self.screen, pygame.Color('grey'), self.BORDER_FIELD_PLAY, 0)
        pygame.draw.rect(self.screen, pygame.Color('black'), self.BORDER_FIELD_PLAY, 2)
        pygame.draw.line(self.screen, pygame.Color('red'), (x_red_min, y_red_min), (x_red_max, y_red_min), 2)
        pygame.draw.line(self.screen, pygame.Color('red'), (x_red_min, y_red_max), (x_red_max, y_red_max), 2)
        pygame.draw.line(self.screen, pygame.Color('blue'), (x_blue_min, y_blue_min), (x_blue_min, y_blue_max), 2)
        pygame.draw.line(self.screen, pygame.Color('blue'), (x_blue_max, y_blue_min), (x_blue_max, y_blue_max), 2)
        for x in range(x_red_min, x_red_max, step):
            for y in range(y_red_min, y_red_max, step):
                pygame.draw.circle(self.screen, pygame.Color('red'), (x, y), 5, 0)
        for x in range(x_blue_min, x_blue_max, step):
            for y in range(y_blue_min, y_blue_max, step):
                pygame.draw.circle(self.screen, pygame.Color('blue'), (x, y), 5, 0)

    # отрисовка ходов
    def draw_move_player(self, color, x_1, y_1, x_2, y_2):
        pygame.draw.line(self.screen, color, (x_1, y_1), (x_2, y_2), 3)

    # отрисовка кнопок до начала игры
    def draw_button(self):
        for y in range(180, 475, 60):
            pygame.draw.rect(self.screen, self.BUTTON_FRAME, (502, y, 240, 50), 0)
            pygame.draw.line(self.screen, pygame.Color('white'), (502, y), (510, y + 8), 3)
            pygame.draw.line(self.screen, pygame.Color('white'), (502, y + 50), (510, y + 42), 3)
            pygame.draw.line(self.screen, pygame.Color('white'), (742, y), (734, y + 8), 3)
            pygame.draw.line(self.screen, pygame.Color('white'), (742, y + 50), (734, y + 42), 3)
            pygame.draw.rect(self.screen, pygame.Color('white'), (510, y + 8, 225, 35), 0)
        text = Pictures.choice_style_text(self.TEXT_SIZE)
        x = 515
        y = 190
        for i in range(len(Texts.BUTTON_TEXT)):
            self.screen.blit(text.render(Texts.BUTTON_TEXT[i], True, self.TEXT_BUTTON), (x, y))
            y += 60

    # отрисовка кнопок  после нажатия
    def draw_button_after_press(self, button, y):
        text = Pictures.choice_style_text(self.TEXT_SIZE)
        self.screen.blit(text.render(button, True, self.TEXT_BUTTON_AFTER_PRESSED), (515, y))

    # отрисовка поля жеребьёвки
    def draw_lot(self, result):
        pygame.draw.rect(self.screen, self.LOT_FOND, self.BORDER_FIELD_LOT, 0)
        pygame.draw.rect(self.screen, pygame.Color('black'), self.BORDER_FIELD_LOT, 2)
        text = Pictures.choice_style_text(self.TEXT_SIZE)
        x = 540
        y = 20
        for i in range(len(result)):
            self.screen.blit(text.render(result[i], True, pygame.Color('white')), (x, y))
            y += 30

    # отрисовка победы
    def draw_victory(self, winner, color):
        text = Pictures.choice_style_text(50)
        self.screen.blit(text.render(winner, True, color), (10, 220))

    # задание шрифта текста
    @staticmethod
    def choice_style_text(size):
        try:
            text = pygame.font.Font(Pictures.TEXT_STYLE, size)
        except IOError:
            text = pygame.font.SysFont(Pictures.TEXT_STYLE_DEFAULT, size)
        return text
