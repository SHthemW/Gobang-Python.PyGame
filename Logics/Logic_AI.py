import random


class AIProgram:

    _computer_side = None
    _offset = [(1, 0), (0, 1), (1, 1), (1, -1)]

    def __init__(self, line_points, player_choice_side):
        self._line_points = line_points
        self._player_side = player_choice_side
        self._computer_side = 1 if player_choice_side == -1 else -1
        self._checkerboard = [[0] * line_points for _ in range(line_points)]

    def set_last_player_drop(self, pos_x, pos_y):
        self._checkerboard[pos_y][pos_x] = self._computer_side

    def get_ai_drop(self):
        score = 0
        target_pos_x = 0
        target_pos_y = 0

        for i in range(self._line_points):
            for j in range(self._line_points):
                if self._checkerboard[j][i] == 0:
                    _score = self._get_point_score(i, j)
                    if _score > score:
                        score = _score
                        target_pos_x = i
                        target_pos_y = j
                    elif _score == score and _score > 0:
                        r = random.randint(0, 100)
                        if r % 2 == 0:
                            target_pos_x = i
                            target_pos_y = j

        self._checkerboard[target_pos_y][target_pos_x] = self._player_side
        return [target_pos_x, target_pos_y]

    def _get_point_score(self, pos_x, pos_y):
        score = 0
        for os in self._offset:
            score += self._get_direction_score(pos_x, pos_y, os[0], os[1])
        return score

    def _get_direction_score(self, pos_x, pos_y, x_offset, y_offset):
        count = 0  # 落子处我方连续子数
        _count = 0  # 落子处对方连续子数
        space = None  # 我方连续子中有无空格
        _space = None  # 对方连续子中有无空格
        both = 0  # 我方连续子两端有无阻挡
        _both = 0  # 对方连续子两端有无阻挡

        # 如果是 1 表示是边上是我方子，2 表示敌方子
        flag = self._get_stone_color(pos_x, pos_y, x_offset, y_offset, True)
        if flag != 0:
            for step in range(1, 6):
                x = pos_x + step * x_offset
                y = pos_y + step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if flag == 1:
                        if self._checkerboard[y][x] == self._player_side:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._computer_side:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break  # 遇到第二个空格退出
                    elif flag == 2:
                        if self._checkerboard[y][x] == self._player_side:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._computer_side:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # 遇到边也就是阻挡
                    if flag == 1:
                        both += 1
                    elif flag == 2:
                        _both += 1

        if space is False:
            space = None
        if _space is False:
            _space = None

        _flag = self._get_stone_color(pos_x, pos_y, -x_offset, -y_offset, True)
        if _flag != 0:
            for step in range(1, 6):
                x = pos_x - step * x_offset
                y = pos_y - step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points:
                    if _flag == 1:
                        if self._checkerboard[y][x] == self._player_side:
                            count += 1
                            if space is False:
                                space = True
                        elif self._checkerboard[y][x] == self._computer_side:
                            _both += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break  # 遇到第二个空格退出
                    elif _flag == 2:
                        if self._checkerboard[y][x] == self._player_side:
                            _both += 1
                            break
                        elif self._checkerboard[y][x] == self._computer_side:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    # 遇到边也就是阻挡
                    if _flag == 1:
                        both += 1
                    elif _flag == 2:
                        _both += 1

        # get score

        score = 0
        if count == 4:
            score = 10000
        elif _count == 4:
            score = 9000
        elif count == 3:
            if both == 0:
                score = 1000
            elif both == 1:
                score = 100
            else:
                score = 0
        elif _count == 3:
            if _both == 0:
                score = 900
            elif _both == 1:
                score = 90
            else:
                score = 0
        elif count == 2:
            if both == 0:
                score = 100
            elif both == 1:
                score = 10
            else:
                score = 0
        elif _count == 2:
            if _both == 0:
                score = 90
            elif _both == 1:
                score = 9
            else:
                score = 0
        elif count == 1:
            score = 10
        elif _count == 1:
            score = 9
        else:
            score = 0

        if space or _space:
            score /= 2

        return score

    # 判断指定位置处在指定方向上是我方子、对方子、空
    def _get_stone_color(self, pos_x, pos_y, x_offset, y_offset, next_):
        x = pos_x + x_offset
        y = pos_y + y_offset
        if 0 <= x < self._line_points and 0 <= y < self._line_points:
            if self._checkerboard[y][x] == self._player_side:
                return 1
            elif self._checkerboard[y][x] == self._computer_side:
                return 2
            else:
                if next_:
                    return self._get_stone_color(pos_x, pos_y, x_offset, y_offset, False)
                else:
                    return 0
        else:
            return 0
