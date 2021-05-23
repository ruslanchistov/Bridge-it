import random


class Players:
    __X_MAX = __Y_MAX = 475
    __X_MIN = __Y_MIN = 25
    __STEP = 50
    __HALF_STEP = 25
    __victory = False

    def __init__(self):
        self.__move_list = []
        self.__graph_red = {}
        self.__graph_blue = {}

    # создаём граф ходов красных в виде списка смежности
    def creation_graph(self):
        # соединяем все стартовые точки между собой и все финишные точки между собой
        self.__graph_red = {"start": {(x, Players.__Y_MIN) for x in range(Players.__STEP, Players.__X_MAX,
                                                                          Players.__STEP)},
                            "finish": {(x, Players.__Y_MAX) for x in range(Players.__STEP,
                                                                           Players.__X_MAX, Players.__STEP)}}
        # создаём граф ходов синих в виде списка смежности
        # соединяем все стартовые точки между собой и все финишные точки между собой
        self.__graph_blue = {"start": {(Players.__X_MIN, y) for y in range(Players.__STEP, Players.__Y_MAX,
                                                                           Players.__STEP)},
                             "finish": {(Players.__X_MAX, y) for y in range(Players.__STEP, Players.__Y_MAX,
                                                                            Players.__STEP)}}
        for x in range(Players.__STEP, Players.__X_MAX, Players.__STEP):
            self.__graph_red[(x, Players.__Y_MIN)] = {"start"}
            self.__graph_red[(x, Players.__Y_MAX)] = {"finish"}

        for y in range(Players.__STEP, Players.__Y_MAX, Players.__STEP):
            self.__graph_blue[(Players.__X_MIN, y)] = {"start"}
            self.__graph_blue[(Players.__X_MAX, y)] = {"finish"}

    # создаём список возможных ходов компьютера
    def move_comp_list(self):
        for x in range(50, Players.__X_MAX, Players.__STEP):
            for y in range(Players.__Y_MIN, Players.__Y_MAX, Players.__STEP):
                self.__move_list.append((x, y, x, y + Players.__STEP))
        for y in range(75, Players.__Y_MAX, Players.__STEP):
            for x in range(50, 450, Players.__STEP):
                self.__move_list.append((x, y, x + Players.__STEP, y))

    # округляем координаты курсора при нажатии (до центра точки)
    @staticmethod
    def __correction_coordinate(x, y, factor_x, factor_y):
        if x % factor_x < factor_x / 2:
            x = x - x % factor_x
        else:
            x = x + factor_x - x % factor_x
        if y % factor_y < factor_y / 2:
            y = y - y % factor_y
        else:
            y = y + factor_y - y % factor_y
        return x, y

    # проверяем правильно ли  красный игрок указал точки (соседние точки и не по диагонали)
    @staticmethod
    def __check_coordinate_red(x_1, y_1, x_2, y_2, step, half_step):
        if x_1 % step == 0 and x_2 % step == 0 and y_1 % half_step == 0 and y_2 % half_step == 0 and \
                y_1 % step != 0 and y_2 % step != 0 and \
                ((abs(x_1 - x_2) == step and (y_1 - y_2) == 0) or (abs(y_1 - y_2) == step and (x_1 - x_2) == 0)):
            return True

    # проверяем правильно ли  синий игрок указал точки (соседние точки и не по диагонали)
    @staticmethod
    def __check_coordinate_blue(x_1, y_1, x_2, y_2, step, half_step):
        if x_1 % half_step == 0 and x_2 % half_step == 0 and y_1 % step == 0 and y_2 % step == 0 and \
                x_1 % step != 0 and x_2 % step != 0 and \
                ((abs(x_1 - x_2) == step and (y_1 - y_2) == 0) or (abs(y_1 - y_2) == step and (x_1 - x_2) == 0)):
            return True

    # проверка нет ли хода противника в данном месте
    @staticmethod
    def __check_square(x_1, y_1, x_2, y_2, graph_1, graph_2, node_1, node_2):
        if node_1 in graph_2:
            if node_2 not in graph_2[node_1]:
                # сохраняем ход в графе
                Players.__save_move_player(x_1, y_1, x_2, y_2, graph_1)
                return x_1, y_1, x_2, y_2, 1
            else:
                return 0, 0, 0, 0, 0
        else:
            # сохраняем ход в графе ходов
            Players.__save_move_player(x_1, y_1, x_2, y_2, graph_1)
            return x_1, y_1, x_2, y_2, 1

    # горизонтальный ход
    @staticmethod
    def __horizontal_move(x_1, y_1, x_2, y_2, graph_1, graph_2, half_step):
        node_1 = ((round((x_1 + x_2) / 2)), (y_1 - half_step))
        node_2 = ((round((x_1 + x_2) / 2)), (y_1 + half_step))
        return Players.__check_square(x_1, y_1, x_2, y_2, graph_1, graph_2, node_1, node_2)

    # вертикальный ход
    @staticmethod
    def __vertical_move(x_1, y_1, x_2, y_2, graph_1, graph_2, half_step):
        node_1 = ((x_1 - half_step), (round((y_1 + y_2) / 2)))
        node_2 = ((x_1 + half_step), (round((y_1 + y_2) / 2)))
        return Players.__check_square(x_1, y_1, x_2, y_2, graph_1, graph_2, node_1, node_2)

    # ходы красного игрока
    def move_red_player(self, x_1, y_1, x_2, y_2):
        # округляем координаты курсора при нажатии (до центра точки)
        (x_1, y_1) = Players.__correction_coordinate(x_1, y_1, Players.__STEP, Players.__HALF_STEP)
        (x_2, y_2) = Players.__correction_coordinate(x_2, y_2, Players.__STEP, Players.__HALF_STEP)

        # проверяем правильно ли  красный игрок указал точки
        if Players.__check_coordinate_red(x_1, y_1, x_2, y_2, Players.__STEP, Players.__HALF_STEP):

            # если "красный" игрок проводит вертикальную линию,
            if x_1 == x_2:
                return Players.__vertical_move(x_1, y_1, x_2, y_2, self.__graph_red,
                                               self.__graph_blue, Players.__HALF_STEP)

            # если "красный" игрок проводит горизонтальную линию,
            if y_1 == y_2:
                return Players.__horizontal_move(x_1, y_1, x_2, y_2, self.__graph_red,
                                                 self.__graph_blue, Players.__HALF_STEP)
        else:
            return 0, 0, 0, 0, 0

    # ходы синего игрока
    def move_blue_player(self, x_1, y_1, x_2, y_2):

        (x_1, y_1) = Players.__correction_coordinate(x_1, y_1, Players.__HALF_STEP, Players.__STEP)
        (x_2, y_2) = Players.__correction_coordinate(x_2, y_2, Players.__HALF_STEP, Players.__STEP)

        # проверяем правильно ли игрок указал точки
        if Players.__check_coordinate_blue(x_1, y_1, x_2, y_2, Players.__STEP, Players.__HALF_STEP):

            # если "синий" игрок проводит вертикальную линию,
            if x_1 == x_2:
                return Players.__vertical_move(x_1, y_1, x_2, y_2, self.__graph_blue,
                                               self.__graph_red, Players.__HALF_STEP)

            # если "синий" игрок проводит горизонтальную линию,
            if y_1 == y_2:
                return Players.__horizontal_move(x_1, y_1, x_2, y_2, self.__graph_blue,
                                                 self.__graph_red, Players.__HALF_STEP)
        else:
            return 0, 0, 0, 0, 0

    # запись хода в граф ходов
    @staticmethod
    def __save_move_player(x_1, y_1, x_2, y_2, graph):

        # добавляем сделанный ход в граф ходов
        node_1 = (x_1, y_1)
        node_2 = (x_2, y_2)

        if node_1 not in graph:
            graph[node_1] = {node_2}
        else:
            graph[node_1].add(node_2)
        if node_2 not in graph:
            graph[node_2] = {node_1}
        else:
            graph[node_2].add(node_1)

    """вспомогательные функции для вычисления хода компьютера"""
    @staticmethod
    def __move_comp_1(x_p, y_1_p, y_2_p, coefficient):
        x_1_c = x_2_c = x_p + coefficient
        y_1_c = y_1_p - 25
        y_2_c = y_2_p + 25
        return x_1_c, y_1_c, x_2_c, y_2_c

    @staticmethod
    def __move_comp_2(x_p, y_1_p, y_2_p, coefficient):
        x_1_c = x_2_c = x_p + coefficient
        y_1_c = y_1_p + coefficient
        y_2_c = y_2_p + coefficient
        return x_1_c, y_1_c, x_2_c, y_2_c

    @staticmethod
    def __move_comp_3(y_p, x_1_p, x_2_p, coefficient):
        y_1_c = y_2_c = y_p + coefficient
        x_1_c = x_1_p + coefficient
        x_2_c = x_2_p + coefficient
        return x_1_c, y_1_c, x_2_c, y_2_c

    # первый ход компьютера
    def first_move_computer(self):
        x1, y1, x2, y2 = 50, 425, 50, 475
        if (x1, y1, x2, y2) in self.__move_list:
            Players.__save_move_player(x1, y1, x2, y2, self.__graph_red)
            self.__move_list.remove((x1, y1, x2, y2))
        else:
            (x1, y1, x2, y2) = Players.__move_comp_random(self.__move_list, self.__graph_red)
        Players.__save_move_player(x1, y1, x2, y2, self.__graph_red)
        return x1, y1, x2, y2

    # ход компьютера в любое место
    @staticmethod
    def __move_comp_random(list_move, graph):
        index = random.randint(0, len(list_move) - 1)
        (x_1, y_1, x_2, y_2) = list_move[index]
        Players.__save_move_player(x_1, y_1, x_2, y_2, graph)
        list_move.pop(index)
        return x_1, y_1, x_2, y_2

    # ход компьютера по стратегии
    def move_computer(self, x_1_p, y_1_p, x_2_p, y_2_p):
        x_1_c, y_1_c, x_2_c, y_2_c = 0, 0, 0, 0

        # если синий игрок сходил в левый нижний угол
        if y_1_p == y_2_p == 450 and x_1_p + x_2_p == 100:

            # если в списке возможных ходов есть такой ответный ход
            if (100, 425, 100, 475) in self.__move_list:
                x_1_c, y_1_c, x_2_c, y_2_c = 100, 425, 100, 475
        else:
            # если синий игрок сделал вертикальный ход
            if x_1_p == x_2_p:
                # и он расположен выше побочной диагонали
                if x_1_p < Players.__X_MAX - y_1_p or x_2_p < Players.__X_MAX - y_2_p:
                    (x_1_c, y_1_c, x_2_c, y_2_c) = Players.__move_comp_2(x_1_p, y_1_p, y_2_p, -Players.__X_MIN)
                else:
                    (x_1_c, y_1_c, x_2_c, y_2_c) = Players.__move_comp_2(x_1_p, y_1_p, y_2_p, Players.__X_MIN)
            else:
                # если синий игрок сделал горизонтальный ход
                # если сделан ход выше побочной диагонали
                if x_1_p < Players.__X_MAX - y_1_p and x_2_p < Players.__X_MAX - y_2_p:
                    (x_1_c, y_1_c, x_2_c, y_2_c) = Players.__move_comp_3(y_1_p, x_1_p, x_2_p, Players.__X_MIN)
                # если сделан ход ниже побочной диагонали
                if x_1_p > Players.__X_MAX - y_1_p and x_2_p > Players.__X_MAX - y_2_p:
                    (x_1_c, y_1_c, x_2_c, y_2_c) = Players.__move_comp_3(y_1_p, x_1_p, x_2_p, -Players.__X_MIN)
                # усли сделан ход на побочной диагонали
                if x_1_p == Players.__X_MAX - y_1_p:
                    if x_2_p > Players.__X_MAX - y_2_p:
                        (x_1_c, y_1_c, x_2_c, y_2_c) = Players.__move_comp_1(x_1_p, y_1_p, y_2_p, -Players.__X_MIN)
                    else:
                        (x_1_c, y_1_c, x_2_c, y_2_c) = Players.__move_comp_1(x_1_p, y_1_p, y_2_p, Players.__X_MIN)
                if x_2_p == Players.__X_MAX - y_1_p:
                    if x_1_p > Players.__X_MAX - y_1_p:
                        (x_1_c, y_1_c, x_2_c, y_2_c) = Players.__move_comp_1(x_2_p, y_1_p, y_2_p, -Players.__X_MIN)
                    else:
                        (x_1_c, y_1_c, x_2_c, y_2_c) = Players.__move_comp_1(x_2_p, y_1_p, y_2_p, Players.__X_MIN)

        # переставляем координаты так, как они хранятся в списке возможных ходов компьютера
        x_1 = min(x_1_c, x_2_c)
        x_2 = max(x_1_c, x_2_c)
        y_1 = min(y_1_c, y_2_c)
        y_2 = max(y_1_c, y_2_c)
        if (x_1, y_1, x_2, y_2) in self.__move_list:

            # сохраняем ход в граф ходов
            Players.__save_move_player(x_1, y_1, x_2, y_2, self.__graph_red)

            # удаляем ход из списка возможных ходов
            self.__move_list.remove((x_1, y_1, x_2, y_2))
            return x_1, y_1, x_2, y_2
        else:
            (x_1, y_1, x_2, y_2) = Players.__move_comp_random(self.__move_list, self.__graph_red)
            return x_1, y_1, x_2, y_2

    # удаление хода из списка возможных ходов компьютера после хода пользователя
    def delete_move_comp(self, x_1, y_1, x_2, y_2):
        if y_1 == y_2:
            y_1 -= Players.__HALF_STEP
            y_2 += Players.__HALF_STEP
            x_1 = x_2 = round((x_1 + x_2) / 2)
        else:
            x_1 -= Players.__HALF_STEP
            x_2 += Players.__HALF_STEP
            y_1 = y_2 = round((y_1 + y_2) / 2)
        self.__move_list.remove((x_1, y_1, x_2, y_2))

    # проверка графа на соединение старта и финиша
    @staticmethod
    def __check_graph(graph, root, used=None):

        # если достигли финиша
        if root == "finish":
            Players.__victory = True
        used = used or set()
        used.add(root)
        for node in graph[root]:
            if node not in used:
                Players.__check_graph(graph, node, used)

    # проверка достижения победы
    def check_winner(self, color):
        Players.__victory = False
        if color == "red":
            Players.__check_graph(self.__graph_red, "start", False)
        else:
            Players.__check_graph(self.__graph_blue, "start", False)
        return Players.__victory
