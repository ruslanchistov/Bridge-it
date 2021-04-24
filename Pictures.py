from random import randint
import pygame


# класс для отрисовки событий
class Pictures:
    WIDTH = 700
    HEIGHT = 500
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (122, 122, 122)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    # создание окна игры
    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen.fill(self.WHITE)

    # отрисовка заставки
    def splash_screen(self):
        splash = pygame.image.load('./splash.png').convert_alpha()
        new_splash = pygame.transform.scale(splash, (490, 490))
        self.screen.blit(new_splash, (5, 5))
        pygame.draw.rect(self.screen, self.BLACK, (5, 5, 490, 490), 2)
        text = pygame.font.SysFont(None, 120, italic=True)
        self.screen.blit(text.render('БРИДЖ-ИТ', True, (50, 200, 50)), (5, 210))

    # отрисовка правил игры
    def rules_game(self):
        pygame.draw.rect(self.screen, self.WHITE, (5, 5, 490, 490), 0)
        pygame.draw.rect(self.screen, self.BLACK, (5, 5, 490, 490), 2)
        text = pygame.font.SysFont(None, 30)
        self.screen.blit(text.render('Игроки по очереди проводят вертикальные ', True, (30, 150, 150)), (10, 20))
        self.screen.blit(text.render('или горизонтальные отрезки, соединяющие', True, (30, 150, 150)), (10, 50))
        self.screen.blit(text.render('какие-либо две соседние точки своего цвета ', True, (30, 150, 150)), (10, 80))
        self.screen.blit(text.render('(первый игрок проводит синие отрезки,', True, (30, 150, 150)), (10, 110))
        self.screen.blit(text.render(' второй — красные). При этом отрезки ', True, (30, 150, 150)), (10, 140))
        self.screen.blit(text.render('не должны пересекаться.', True, (30, 150, 150)), (10, 170))
        self.screen.blit(text.render('Побеждает тот игрок, кто первый построит', True, (30, 150, 150)), (10, 200))
        self.screen.blit(text.render('ломаную линию,соединяющую две ', True, (30, 150, 150)), (10, 230))
        self.screen.blit(text.render('противоположные стороны доски своего цвета', True, (30, 150, 150)), (10, 260))
        self.screen.blit(text.render('(первый игрок должен соединить нижнюю и  ', True, (30, 150, 150)), (10, 290))
        self.screen.blit(text.render('верхнюю стороны доски,', True, (30, 150, 150)), (10, 320))
        self.screen.blit(text.render('второй — правую и левую).', True, (30, 150, 150)), (10, 350))
        self.screen.blit(text.render('Для осуществления хода нажать левую', True, (30, 150, 150)), (10, 380))
        self.screen.blit(text.render('кнопку мышки в одной точке,довести до ', True, (30, 150, 150)), (10, 410))
        self.screen.blit(text.render('второй  и отпустить.', True, (30, 150, 150)), (10, 440))

    # отрисовка игрового поля
    def playing_field(self):
        pygame.draw.rect(self.screen, self.GREY, (5, 5, 490, 490), 0)
        pygame.draw.rect(self.screen, self.BLACK, (5, 5, 490, 490), 2)
        pygame.draw.line(self.screen, self.RED, (50, 25), (450, 25), 1)
        pygame.draw.line(self.screen, self.RED, (50, 475), (450, 475), 1)
        pygame.draw.line(self.screen, self.BLUE, (25, 50), (25, 450), 1)
        pygame.draw.line(self.screen, self.BLUE, (475, 50), (475, 450), 1)
        for x in range(50, 500, 50):
            for y in range(25, 500, 50):
                pygame.draw.circle(self.screen, self.RED, (x, y), 5, 0)
        for x in range(25, 500, 50):
            for y in range(50, 500, 50):
                pygame.draw.circle(self.screen, self.BLUE, (x, y), 5, 0)

    # отрисовка ходов
    def draw_move_player(self, color, x_1, y_1, x_2, y_2):
        pygame.draw.line(self.screen, color, (x_1, y_1), (x_2, y_2), 3)

    # отрисовка кнопок до начала игры
    def draw_button(self):
        for y in range(180, 475, 60):
            pygame.draw.rect(self.screen, (180, 180, 180), (502, y, 190, 50), 0)
            pygame.draw.line(self.screen, self.WHITE, (502, y), (510, y + 8), 3)
            pygame.draw.line(self.screen, self.WHITE, (502, y + 50), (510, y + 42), 3)
            pygame.draw.line(self.screen, self.WHITE, (692, y), (684, y + 8), 3)
            pygame.draw.line(self.screen, self.WHITE, (692, y + 50), (684, y + 42), 3)
            pygame.draw.rect(self.screen, self.WHITE, (510, y + 8, 175, 35), 0)
        text = pygame.font.SysFont(None, 30)
        self.screen.blit(text.render('правила игры ', True, (30, 150, 150)), (530, 195))
        self.screen.blit(text.render('игра', True, (30, 150, 150)), (580, 245))
        self.screen.blit(text.render('с компьютером ', True, (30, 150, 150)), (520, 265))
        self.screen.blit(text.render('игра с другом ', True, (30, 150, 150)), (528, 315))
        self.screen.blit(text.render('старт ', True, (30, 150, 150)), (570, 375))
        self.screen.blit(text.render('новая игра', True, (30, 150, 150)), (545, 435))

    # отрисовка поля жребия до начала игры
    def field_for_lot(self):
        pygame.draw.rect(self.screen, (30, 50, 110), (502, 5, 190, 150), 0)
        pygame.draw.rect(self.screen, self.BLACK, (502, 5, 190, 150), 2)
        for i in range(50):
            pygame.draw.circle(self.screen, self.WHITE, (randint(505, 680), randint(8, 150)), 1, 0)
        text = pygame.font.SysFont(None, 30)
        self.screen.blit(text.render('кликни мышкой ', True, (230, 230, 230)), (520, 25))
        self.screen.blit(text.render('в этом окне,', True, (230, 230, 230)), (538, 55))
        self.screen.blit(text.render('чтобы узнать,', True, (230, 230, 230)), (530, 85))
        self.screen.blit(text.render('чей первый ход', True, (230, 230, 230)), (520, 115))

    """отрисовка кнопок  после нажатия"""

    def play_with_computer(self):
        text = pygame.font.SysFont(None, 30)
        self.screen.blit(text.render('игра', True, (210, 210, 210)), (580, 245))
        self.screen.blit(text.render('с компьютером ', True, (210, 210, 210)), (520, 265))
        self.screen.blit(text.render('игра с другом ', True, (30, 150, 150)), (528, 315))

    def play_with_friend(self):
        text = pygame.font.SysFont(None, 30)
        self.screen.blit(text.render('игра с другом ', True, (210, 210, 210)), (528, 315))
        self.screen.blit(text.render('игра', True, (30, 150, 150)), (580, 245))
        self.screen.blit(text.render('с компьютером ', True, (30, 150, 150)), (520, 265))

    def start_play(self):
        text = pygame.font.SysFont(None, 30)
        self.screen.blit(text.render('старт ', True, (210, 210, 210)), (570, 375))

    """отрисовка поля жребия после жеребьёвки"""
    def queue_human(self):
        pygame.draw.rect(self.screen, (30, 50, 110), (502, 5, 190, 150), 0)
        pygame.draw.rect(self.screen, self.BLACK, (502, 5, 190, 150), 2)
        for i in range(50):
            pygame.draw.circle(self.screen, self.WHITE, (randint(505, 680), randint(8, 150)), 1, 0)
        text = pygame.font.SysFont(None, 30)
        self.screen.blit(text.render('поздравляю', True, (230, 230, 230)), (532, 25))
        self.screen.blit(text.render('первый ход', True, (230, 230, 230)), (537, 55))
        self.screen.blit(text.render('достался вам вы', True, (230, 230, 230)), (511, 85))
        self.screen.blit(text.render('играете синими', True, (230, 230, 230)), (517, 115))

    def queue_blue(self):
        pygame.draw.rect(self.screen, (30, 50, 110), (502, 5, 190, 150), 0)
        pygame.draw.rect(self.screen, self.BLACK, (502, 5, 190, 150), 2)
        for i in range(50):
            pygame.draw.circle(self.screen, self.WHITE, (randint(505, 680), randint(8, 150)), 1, 0)
        text = pygame.font.SysFont(None, 30)
        self.screen.blit(text.render('поздравляю', True, (230, 230, 230)), (532, 25))
        self.screen.blit(text.render('первый ход', True, (230, 230, 230)), (537, 55))
        self.screen.blit(text.render('достался синим', True, (230, 230, 230)), (512, 85))

    def queue_red(self):
        pygame.draw.rect(self.screen, (30, 50, 110), (502, 5, 190, 150), 0)
        pygame.draw.rect(self.screen, self.BLACK, (502, 5, 190, 150), 2)
        for i in range(50):
            pygame.draw.circle(self.screen, self.WHITE, (randint(505, 680), randint(8, 150)), 1, 0)
        text = pygame.font.SysFont(None, 30)
        self.screen.blit(text.render('поздравляю', True, (230, 230, 230)), (532, 25))
        self.screen.blit(text.render('первый ход', True, (230, 230, 230)), (534, 55))
        self.screen.blit(text.render('достался', True, (230, 230, 230)), (547, 85))
        self.screen.blit(text.render('красным', True, (230, 230, 230)), (554, 115))

    def queue_computer(self):
        pygame.draw.rect(self.screen, (30, 50, 110), (502, 5, 190, 150), 0)
        pygame.draw.rect(self.screen, self.BLACK, (502, 5, 190, 150), 2)
        for i in range(50):
            pygame.draw.circle(self.screen, self.WHITE, (randint(505, 680), randint(8, 150)), 1, 0)
        text = pygame.font.SysFont(None, 30)
        self.screen.blit(text.render('сожалею,первый', True, (230, 230, 230)), (509, 25))
        self.screen.blit(text.render('ход достался', True, (230, 230, 230)), (528, 55))
        self.screen.blit(text.render('компьютеру,он', True, (230, 230, 230)), (517, 85))
        self.screen.blit(text.render('играет красными', True, (230, 230, 230)), (510, 115))

    # отрисовка победа красных
    def draw_victory_red(self):
        text = pygame.font.SysFont(None, 70)
        self.screen.blit(text.render('ПОБЕДА КРАСНЫХ', True, (200, 50, 50)), (10, 210))

    # отрисовка победа синих
    def draw_victory_blue(self):
        text = pygame.font.SysFont(None, 80)
        self.screen.blit(text.render('ПОБЕДА СИНИХ', True, (50, 50, 200)), (20, 210))
