import pygame
from Players import Players
from Pictures import Pictures


def main():
    # объявляем переменные
    type_game = None  # тип игры
    queue = None  # очерёдность хода
    start = None  # начало игры
    permission_draw = 0  # разрешение на отрисовку хода
    counter_move = 0  # счётчик ходов
    first_move_computer = 0  # первый ход компьютера когда он ходит первым
    (x_1, y_1, x_2, y_2) = (0, 0, 0, 0)
    (x_1_p, y_1_p, x_2_p, y_2_p) = (0, 0, 0, 0)

    pygame.init()
    clock = pygame.time.Clock()
    window = Pictures()
    play = Players()

    pygame.display.set_caption("БРИДЖ-ИТ")
    # включаем фоновую музыку
    try:
        pygame.mixer.music.load('fon_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
    except Exception:
        pass
    # рисуем заставку
    try:
        window.splash_screen()
    except Exception:
        window.playing_field()

    window.draw_button()  # отрисовка кнопок
    window.field_for_lot()  # отрисовка поля жребия
    play.creation_graph()  # создаём графы ходов
    # обработка нажатия сервисных кнопок
    def service_keys(x_1, y_1, type_game, queue, start, counter_move, first_move_computer):
        if 5 <= y_1 <= 155 and type_game == "computer":
            if (x_1 + y_1) % 2 == 0:
                window.queue_human()
                queue = "blue"
                first_move_computer = 1
            else:
                window.queue_computer()
                queue = "red"

        if 5 <= y_1 <= 155 and type_game == "human":
            if (x_1 + y_1) % 2 == 0:
                window.queue_blue()
                queue = "blue"
            else:
                window.queue_red()
                queue = "red"
        if 180 <= y_1 <= 230:
            window.rules_game()
        if 240 <= y_1 <= 290:
            window.play_with_computer()
            type_game = "computer"
        if 300 <= y_1 <= 350:
            window.play_with_friend()
            type_game = "human"
        if 360 <= y_1 <= 410 and type_game != None and queue != None:
            window.start_play()
            window.playing_field()
            start = "start"
        if 420 <= y_1 <= 470:
            queue = None
            start = None
            type_game = None
            counter_move = 0
            first_move_computer = 0
            window.splash_screen()
            window.draw_button()
            window.field_for_lot()
            play.creation_graph()
        return (type_game, queue, start, counter_move, first_move_computer)

    # проверка достижения победы
    def check_winner(graph, root, color, used=None):
        if root == "finish":
            if color == "red":
                window.draw_victory_red()

            if color == "blue":
                window.draw_victory_blue()

        used = used or set()
        used.add(root)
        for node in graph[root]:
            if node not in used:
                check_winner(graph, node, color, used)

    # главный цикл игры
    process = True
    while process:
        # держим цикл на заданной скорости
        clock.tick(30)

        # цикл обработки событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                process = False

            # если игра ещё не началась
            if start == None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x_1, y_1 = pygame.mouse.get_pos()
                        if 502 <= x_1 <= 692:
                            (type_game, queue, start, counter_move, first_move_computer) = \
                                service_keys(x_1, y_1, type_game, queue, start, counter_move, first_move_computer)

            else:
                # если идёт игра с компьютером и его очередь делать ход
                if queue == "red" and type_game == "computer":
                    # если это не первый ход
                    if first_move_computer != 0:
                        (x_1, y_1, x_2, y_2) = play.move_computer(x_1_p, y_1_p, x_2_p, y_2_p)
                        window.draw_move_player((255, 0, 0), x_1, y_1, x_2, y_2)
                        counter_move += 1
                        check_winner(play.graph_red, "start", "red")
                    # если первый ход
                    else:
                        play.save_first_move_computer(50, 425, 50, 475)
                        window.draw_move_player((255, 0, 0), 50, 425, 50, 475)
                        first_move_computer = 1
                        counter_move += 1
                    # передаём очередь хода синим
                    queue = "blue"

                # считываем действие мыши
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x_1, y_1 = pygame.mouse.get_pos()
                        # если нажали кнопку новая игра
                        if 420 <= y_1 <= 470 and 502 <= x_1 <= 692:
                            type_game = None
                            queue = None
                            start = None
                            counter_move = 0
                            first_move_computer = 0
                            play.creation_graph()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        x_2, y_2 = pygame.mouse.get_pos()

                        # если игрок кликнул на игровом поле
                        if 22 <= x_1 <= 478 and 22 <= x_2 <= 478 and 22 <= y_1 <= 478 and 22 <= y_2 <= 478:
                            # если красными играет человек и его очередь делать ход
                            if queue == "red" and type_game == "human":
                                (x_1, y_1, x_2, y_2, permission_draw) = play.move_red_player(x_1, y_1, x_2, y_2)
                                # если такой ход сделать можно ,отображаем его на поле
                                if permission_draw == 1:
                                    window.draw_move_player((255, 0, 0), x_1, y_1, x_2, y_2)
                                    counter_move += 1
                                    check_winner(play.graph_red, "start", "red")
                                    # передаём очередь хода синим
                                    queue = "blue"

                            # если очередь хода пользователя (синих)
                            if queue == "blue":
                                # сохраняем последний сделанный ход синих для компьютера
                                (x_1_p, y_1_p, x_2_p, y_2_p, permission_draw) = play.move_blue_player(x_1, y_1, x_2,y_2)
                                # если такой ход возможен ,отображаем его на поле
                                if permission_draw == 1:
                                    window.draw_move_player((0, 0, 255), x_1_p, y_1_p, x_2_p, y_2_p)
                                    counter_move += 1
                                    check_winner(play.graph_blue, "start", "blue")
                                    # передаём очередь хода красным
                                    queue = "red"

        # после отрисовки меняем экран
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
