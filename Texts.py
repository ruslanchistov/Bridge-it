"""тексты используемые в игре"""


class Texts:
    # правила игры
    RULES = ('Игроки по очереди проводят вертикальные ',
             'или горизонтальные отрезки, соединяющие',
             'какие-либо две соседние точки своего цвета ',
             '(один игрок проводит красные отрезки,',
             ' другой — синие). При этом отрезки ',
             'не должны пересекаться.',
             'Побеждает тот игрок, кто первый построит',
             'ломаную линию,соединяющую две ',
             'противоположные стороны доски своего цвета',
             '(один игрок должен соединить нижнюю и  ',
             'верхнюю стороны доски,',
             'другой — правую и левую).',
             'Для осуществления хода нажать левую',
             'кнопку мышки в одной точке, довести до ',
             'второй  и отпустить.')

    # начальное поле жеребьёвки
    LOT = (' кликни мышкой ', '    в этом окне,', '   чтобы узнать,', ' чей первый ход')

    # результаты жеребьёвки
    LOT_COMPUTER = ('сожалею,первый', '   ход достался', '  компьютеру,он', 'играет красными')
    LOT_HUMAN = ('    поздравляю', '    первый ход', 'достался вам вы', '  играете синими')
    LOT_RED = ('    поздравляю', '     первый ход', '       достался', '        красным')
    LOT_BLUE = ('   поздравляю', '    первый ход', ' достался синим')

    # победитель
    VICTORY = ('ПОБЕДА КРАСНЫХ', '   ПОБЕДА СИНИХ')

    # текст клавиш
    BUTTON_TEXT = ('      правила игры ', ' игра с компьютером ', '      игра с другом ',
                   '              старт ', '         новая игра')
