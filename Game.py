import pygame
from Players import Players
from Pictures import Pictures
from Texts import Texts


def main():
    red = (255, 0, 0)
    blue = (0, 0, 255)
    left_up = 22  # верхний левый угол игрового поля
    right_down = 478  # нижний правый угол игрового поля
    type_game = None  # тип игры
    queue = None  # очерёдность хода
    start = None  # начало игры
    rules = 1  # флаг правил игры
    first_move_computer = 0  # первый ход компьютера
    x_1, y_1, x_2, y_2 = 0, 0, 0, 0
    x_1_blue, y_1_blue, x_2_blue, y_2_blue = 0, 0, 0, 0

    # инициализация модулей pygame
    pygame.init()

    # создаём окно игры
    window = Pictures()

    # создаём объект для отслеживания времени
    clock = pygame.time.Clock()

    # создаём игроков
    play = Players()
    play.creation_graph()
    play.move_comp_list()

    # включаем фоновую музыку
    Pictures.music()

    # рисуем заставку
    try:
        window.splash_screen()
    except IOError:
        window.playing_field()

    window.draw_button()  # отрисовка клавиш игры
    window.draw_lot(Texts.LOT)  # отрисовка поля жребия

    # сброс и пуск игры снова
    def new_game():
        window.splash_screen()
        window.draw_button()
        window.draw_lot(Texts.LOT)
        play.creation_graph()
        play.move_comp_list()
        return None, None, None, 0, 1

    # обработка нажатия сервисных клавиш
    def service_keys(x1, y1, game_type, turn, starting, first_move, specific):

        # если кликаем в поле жребия и выбран тип игры
        if 5 <= y1 <= 155 and turn is None:

            # если выбран режим игры с компьютером
            if game_type == "computer":
                if x1 % 2 == 0:

                    # первый ход достался игроку
                    window.draw_lot(Texts.LOT_HUMAN)
                    turn = "blue"
                    first_move = 1
                else:

                    # первый ход достался компьютеру
                    window.draw_lot(Texts.LOT_COMPUTER)
                    turn = "red"

            if game_type == "human":
                if (x1 + y1) % 2 == 0:

                    # первый ход достался синим
                    window.draw_lot(Texts.LOT_BLUE)
                    turn = "blue"
                else:

                    # первый ход достался красным
                    window.draw_lot(Texts.LOT_RED)
                    turn = "red"

            # клавиша "правила игры"
        if 180 <= y1 <= 230:
            if specific > 0:
                window.rules_game()
                specific *= -1
            else:
                window.splash_screen()
                specific *= -1

        # клавиша "игра с компьютером"
        if 240 <= y1 <= 290 and game_type is None:
            window.draw_button_after_press(Texts.BUTTON_TEXT[1], 250)
            game_type = "computer"

        # клавиша "игра с другом"
        if 300 <= y1 <= 350 and game_type is None:
            window.draw_button_after_press(Texts.BUTTON_TEXT[2], 310)
            game_type = "human"

        # клавиша "старт"
        if 360 <= y1 <= 410 and game_type is not None and queue is not None:
            window.draw_button_after_press(Texts.BUTTON_TEXT[3], 370)
            window.playing_field()
            starting = "start"
        if 420 <= y1 <= 470:
            (game_type, turn, starting, first_move, specific) = new_game()
        return game_type, turn, starting, first_move, specific

    # игра пользователя
    def game_human(x1, y1, x2, y2, turn):
        (x_1_b, y_1_b, x_2_b, y_2_b) = (0, 0, 0, 0)

        # если красными играет человек и его очередь делать ход
        if turn == "red" and type_game == "human":
            (x1, y1, x2, y2, permission_draw) = play.move_red_player(x1, y1, x2, y2)

            # если такой ход сделать можно ,отображаем его на поле
            if permission_draw == 1:
                window.draw_move_player(red, x1, y1, x2, y2)
                if play.check_winner("red"):
                    window.draw_victory(Texts.VICTORY[0], (250, 100, 100))

                # передаём очередь хода синим
                turn = "blue"

        # если очередь хода пользователя (синих)
        if turn == "blue":

            # сохраняем последний сделанный ход синих для вычисления хода компьютера
            (x_1_b, y_1_b, x_2_b, y_2_b, permission_draw) = play.move_blue_player(x_1, y_1, x_2, y_2)

            # если такой ход возможен ,отображаем его на поле
            if permission_draw == 1:
                window.draw_move_player(blue, x_1_b, y_1_b, x_2_b, y_2_b)
                if play.check_winner("blue"):
                    window.draw_victory(Texts.VICTORY[1], (70, 70, 250))

                # удаляем ход компьютера в данном квадрате из списка возможных ходов
                play.delete_move_comp(x_1_b, y_1_b, x_2_b, y_2_b)

                # передаём очередь хода красным
                turn = "red"
        return turn, x_1_b, y_1_b, x_2_b, y_2_b

    # игра компьютера
    def game_computer(x_1_b, y_1_b, x_2_b, y_2_b, first_move):

        # если это не первый ход
        if first_move != 0:
            (x1, y1, x2, y2) = play.move_computer(x_1_b, y_1_b, x_2_b, y_2_b)
            window.draw_move_player(red, x1, y1, x2, y2)
            if play.check_winner("red"):
                window.draw_victory(Texts.VICTORY[0], (250, 70, 70))

        # если это первый ход
        else:
            (x1, y1, x2, y2) = play.first_move_computer()
            window.draw_move_player(red, x1, y1, x2, y2)
            first_move = 1

        # передаём очередь хода синим
        return "blue", first_move

    # главный цикл игры
    process = True
    while process:

        # задаём частоту обновления экрана
        clock.tick(10)

        # цикл обработки событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                process = False

            # если игра ещё не началась
            if start is None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x_1, y_1 = pygame.mouse.get_pos()

                        # если игрок кликнул на клавиши интерфейса
                        if 502 <= x_1 <= 742:
                            (type_game, queue, start, first_move_computer, rules) = \
                                service_keys(x_1, y_1, type_game, queue, start, first_move_computer, rules)
            else:
                # считываем действие мыши
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x_1, y_1 = pygame.mouse.get_pos()

                        # если нажата клавиша "новая игра"
                        if 420 <= y_1 <= 470 and 502 <= x_1 <= 742:
                            (type_game, queue, start, first_move_computer, rules) = new_game()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        x_2, y_2 = pygame.mouse.get_pos()

                        # если игрок кликнул на игровом поле
                        if left_up <= x_1 <= right_down and left_up <= x_2 <= right_down and \
                                left_up <= y_1 <= right_down and left_up <= y_2 <= right_down:
                            (queue, x_1_blue, y_1_blue, x_2_blue, y_2_blue) = game_human(x_1, y_1, x_2, y_2, queue)

                # если идёт игра с компьютером и его очередь делать ход
                if queue == "red" and type_game == "computer":
                    (queue, first_move_computer) = \
                        game_computer(x_1_blue, y_1_blue, x_2_blue, y_2_blue, first_move_computer)

        # обновляем содержимое окна игры
        pygame.display.flip()

    # выходим из игры
    pygame.quit()


if __name__ == '__main__':
    main()
