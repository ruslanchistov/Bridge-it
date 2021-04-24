class Players:

    def creation_graph(self):

        # создаём граф ходов красных в виде списка смежности
        # соединяем все стартовые и финишные точки
        self.graph_red = {"start": {str(x) + "25" for x in range(50, 500, 50)},
                          "finish": {str(x) + "475" for x in range(50, 500, 50)}}
        # создаём граф ходов синих в виде списка смежности
        # соединяем все стартовые и финишные точки
        self.graph_blue = {"start": {"25" + str(y) for y in range(50, 500, 50)},
                           "finish": {"475" + str(y) for y in range(50, 500, 50)}}
        for x in range(50, 500, 50):
            self.graph_red[str(x) + "25"] = {"start"}
            self.graph_red[str(x) + "475"] = {"finish"}

        for y in range(50, 500, 50):
            self.graph_blue["25" + str(y)] = {"start"}
            self.graph_blue["475" + str(y)] = {"finish"}

    @staticmethod  # округляем координаты курсора при нажатии (до центра точки)
    def correction_coordinate(x, y, factor_x, factor_y):
        if x % factor_x < 6:
            x = x - x % factor_x
        else:
            x = x + factor_x - x % factor_x
        if y % factor_y < 6:
            y = y - y % factor_y
        else:
            y = y + factor_y - y % factor_y
        return (x, y)

    @staticmethod
    def check_coordinate(x_1,y_1,x_2,y_2):
        if x_1 % 50 == 0 and x_2 % 50 == 0 and y_1 % 25 == 0 and y_2 % 25 == 0 and y_1 % 50 != 0 and y_2 % 50 != 0 and \
                ((abs(x_1 - x_2) == 50 and (y_1 - y_2) == 0) or (abs(y_1 - y_2) == 50 and (x_1 - x_2) == 0)):return True

        if x_1 % 25 == 0 and x_2 % 25 == 0 and y_1 % 50 == 0 and y_2 % 50 == 0 and x_1 % 50 != 0 and x_2 % 50 != 0 and \
                ((abs(x_1 - x_2) == 50 and (y_1 - y_2) == 0) or (abs(y_1 - y_2) == 50 and (x_1 - x_2) == 0)): return True

    # ходы красных
    def move_red_player(self, x_1, y_1, x_2, y_2):
        # округляем координаты курсора при нажатии (до центра точки)
        (x_1, y_1) = Players.correction_coordinate(x_1, y_1, 50, 25)
        (x_2, y_2) = Players.correction_coordinate(x_2, y_2, 50, 25)

        # проверяем правильно ли игрок указал точки (соседние точки и не по диагонали)
        if x_1 % 50 == 0 and x_2 % 50 == 0 and y_1 % 25 == 0 and y_2 % 25 == 0 and y_1 % 50 != 0 and y_2 % 50 != 0 and \
                ((abs(x_1 - x_2) == 50 and (y_1 - y_2) == 0) or (abs(y_1 - y_2) == 50 and (x_1 - x_2) == 0)):

            # если "красный" игрок проводит вертикальную линию,
            if x_1 == x_2:
                node_blue_1 = str(x_1 - 25) + str(round((y_1 + y_2) / 2))
                node_blue_2 = str(x_1 + 25) + str(round((y_1 + y_2) / 2))
                # то проверяем нет ли в данном квадрате горизонтальной синей линии
                if node_blue_1 in self.graph_blue:
                    if not node_blue_2 in self.graph_blue[node_blue_1]:
                        # сохраняем ход в графе
                        Players.save_move_player(x_1, y_1, x_2, y_2, self.graph_red)
                        return (x_1, y_1, x_2, y_2, 1)


                    else:
                        return (0, 0, 0, 0, 0)
                else:
                    # сохраняем ход в графе
                    Players.save_move_player(x_1, y_1, x_2, y_2, self.graph_red)
                    return (x_1, y_1, x_2, y_2, 1)

            # если "красный" игрок проводит горизонтальную линию,
            if y_1 == y_2:
                node_blue_1 = str(round((x_1 + x_2) / 2)) + str(y_1 - 25)
                node_blue_2 = str(round((x_1 + x_2) / 2)) + str(y_1 + 25)

                # то проверяем нет ли в данном квадрате вертикальной синей линии
                if node_blue_1 in self.graph_blue:
                    if not node_blue_2 in self.graph_blue[node_blue_1]:
                        # сохраняем ход в графе
                        Players.save_move_player(x_1, y_1, x_2, y_2, self.graph_red)
                        return (x_1, y_1, x_2, y_2, 1)

                    else:
                        return (0, 0, 0, 0, 0)

                else:
                    # сохраняем ход в графе
                    Players.save_move_player(x_1, y_1, x_2, y_2, self.graph_red)
                    return (x_1, y_1, x_2, y_2, 1)

        else:
            return (0, 0, 0, 0, 0)

    # ходы синих
    def move_blue_player(self, x_1, y_1, x_2, y_2):

        (x_1, y_1) = Players.correction_coordinate(x_1, y_1, 25, 50)
        (x_2, y_2) = Players.correction_coordinate(x_2, y_2, 25, 50)

        # проверяем правильно ли игрок указал точки (соседние точки и не по диагонали)
        if x_1 % 25 == 0 and x_2 % 25 == 0 and y_1 % 50 == 0 and y_2 % 50 == 0 and x_1 % 50 != 0 and x_2 % 50 != 0 and \
                ((abs(x_1 - x_2) == 50 and (y_1 - y_2) == 0) or (abs(y_1 - y_2) == 50 and (x_1 - x_2) == 0)):

            # если "синий" игрок проводит вертикальную линию,
            if x_1 == x_2:
                node_red_1 = str(x_1 - 25) + str(round((y_1 + y_2) / 2))
                node_red_2 = str(x_1 + 25) + str(round((y_1 + y_2) / 2))

                # то проверяем нет ли в данном квадрате горизонтальной красной линии
                if node_red_1 in self.graph_red:
                    if not node_red_2 in self.graph_red[node_red_1]:
                        # сохраняем ход в графе
                        Players.save_move_player(x_1, y_1, x_2, y_2, self.graph_blue)
                        return (x_1, y_1, x_2, y_2, 1)

                    else:
                        return (0, 0, 0, 0, 0)
                else:
                    # сохраняем ход в графе
                    Players.save_move_player(x_1, y_1, x_2, y_2, self.graph_blue)
                    return (x_1, y_1, x_2, y_2, 1)

            # если "синий" игрок проводит горизонтальную линию,
            if y_1 == y_2:
                node_red_1 = str(round((x_1 + x_2) / 2)) + str(y_1 - 25)
                node_red_2 = str(round((x_1 + x_2) / 2)) + str(y_1 + 25)
                # то проверяем нет ли в данном квадрате вертикальной красной линии
                if node_red_1 in self.graph_red:
                    if not node_red_2 in self.graph_red[node_red_1]:
                        # сохраняем ход в графе
                        Players.save_move_player(x_1, y_1, x_2, y_2, self.graph_blue)
                        return (x_1, y_1, x_2, y_2, 1)

                    else:
                        return (0, 0, 0, 0, 0)
                else:
                    # сохраняем ход в графе
                    Players.save_move_player(x_1, y_1, x_2, y_2, self.graph_blue)
                    return (x_1, y_1, x_2, y_2, 1)

        else:
            return (0, 0, 0, 0, 0)

    # запись ходов в графы
    @staticmethod
    def save_move_player(x_1, y_1, x_2, y_2, graph):

        # добавляем сделанный ход в граф ходов
        node_1 = str(x_1) + str(y_1)
        node_2 = str(x_2) + str(y_2)

        if not node_1 in graph:
            graph[node_1] = {node_2}
        else:
            graph[node_1].add(node_2)
        if not node_2 in graph:
            graph[node_2] = {node_1}
        else:
            graph[node_2].add(node_1)

    # ходы компьютера
    def move_computer(self, x_1_p, y_1_p, x_2_p, y_2_p):
        (x_1_c, y_1_c, x_2_c, y_2_c) = (0, 0, 0, 0)
        # срабатывает когда компьютер начинает ходить вторым
        # при таком ходе синих
        if y_1_p == 450 and (x_1_p == 25 or x_2_p == 25):
            x_1_c = 50
            x_2_c = 100
            y_1_c = y_2_c = 475
        else:
            # если игрок сделал вертикальный ход выше побочной диагонали
            if x_1_p == x_2_p and (x_1_p < 475 - y_1_p or x_2_p < 475 - y_2_p):
                x_1_c = x_2_c = x_1_p - 25
                y_1_c = y_1_p - 25
                y_2_c = y_2_p - 25
            # если игрок сделал горизонтальный ход выше побочной диагонали
            if y_1_p == y_2_p and x_1_p < 475 - y_1_p and x_2_p < 475 - y_2_p:
                y_1_c = y_2_c = y_1_p + 25
                x_1_c = x_1_p + 25
                x_2_c = x_2_p + 25
            # если игрок сделал вертикальный ход ниже побочной диагонали
            if x_1_p == x_2_p and (x_1_p > 475 - y_1_p or x_2_p > 475 - y_2_p):
                x_1_c = x_2_c = x_1_p + 25
                y_1_c = y_1_p + 25
                y_2_c = y_2_p + 25
            # если игрок сделал горизонтальный ход ниже побочной диагонали
            if y_1_p == y_2_p and x_1_p > 475 - y_1_p and x_2_p > 475 - y_2_p:
                y_1_c = y_2_c = y_1_p - 25
                x_1_c = x_1_p - 25
                x_2_c = x_2_p - 25
            # если игрок сделал горизонтальный ход на побочной диагонали
            if y_1_p == y_2_p and x_1_p == 475 - y_1_p and x_2_p > 475 - y_2_p:
                x_1_c = x_2_c = x_1_p - 25
                y_1_c = y_1_p - 25
                y_2_c = y_2_p + 25
            if y_1_p == y_2_p and x_2_p == 475 - y_1_p and x_1_p > 475 - y_1_p:
                x_1_c = x_2_c = x_2_p - 25
                y_1_c = y_1_p - 25
                y_2_c = y_2_p + 25
            if y_1_p == y_2_p and x_1_p == 475 - y_1_p and x_2_p < 475 - y_2_p:
                x_1_c = x_2_c = x_1_p + 25
                y_1_c = y_1_p - 25
                y_2_c = y_2_p + 25
            if y_1_p == y_2_p and x_2_p == 475 - y_1_p and x_1_p < 475 - y_1_p:
                x_1_c = x_2_c = x_2_p + 25
                y_1_c = y_1_p - 25
                y_2_c = y_2_p + 25
        # сохраняем ход
        Players.save_move_player(x_1_c, y_1_c, x_2_c, y_2_c, self.graph_red)
        return (x_1_c, y_1_c, x_2_c, y_2_c)

    # запись первого хода компьютера
    def save_first_move_computer(self, x_1, y_1, x_2, y_2):
        Players.save_move_player(x_1, y_1, x_2, y_2, self.graph_red)
