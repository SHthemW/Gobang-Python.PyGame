import re
from Datas.Config import data_file_path
from Datas.DataStCollections import PlayerData


class DataProgram:
    _current_player = None

    _before_game_dt_str = None
    _after_game_dt_str = None

    def set_player_name(self, name):
        current_player_data_in_file = self._datafile_try_get_player_data(name)

        if current_player_data_in_file is None:
            # 新玩家
            self._current_player = PlayerData(name, 0, 0, True)
            print("欢迎新玩家:" + self._current_player.name)
            return True
        else:
            self._current_player = PlayerData(name,
                                              self._get_data_from_str(current_player_data_in_file)[1],
                                              self._get_data_from_str(current_player_data_in_file)[2],
                                              False)
            self._before_game_dt_str = current_player_data_in_file
            return False
        pass

    def set_current_player_mark(self, mark):
        if mark == 1:
            print('您赢得了游戏.')
            self._current_player.add_win_game()
        else:
            print('您输掉了游戏.')
            self._current_player.add_los_game()
        pass

    def save_current_data(self):
        self._after_game_dt_str = f'玩家{self._current_player.name},游戏次数{self._current_player.all_times},' \
                                  f'获胜次数{self._current_player.win_times},胜率{self._current_player.win_ratio()}\n'
        print('after game str:' + self._after_game_dt_str)
        self._datafile_save_current()
        pass

    # file entity operations

    def _datafile_save_current(self):
        # init
        with open(data_file_path, 'a+', encoding='utf-8') as f:

            # file operation
            if self._current_player.is_new:
                f.write(self._after_game_dt_str)
            else:
                self._update_file(data_file_path, self._before_game_dt_str, self._after_game_dt_str)

        pass

    def _datafile_try_get_player_data(self, name):
        with open(data_file_path, encoding='utf-8') as f:
            res = None
            data = f.readlines()
            for i in range(len(data)):
                name_data = self._get_data_from_str(data[i])[0]
                if name_data == name:
                    res = data[i]
        return res

    # utils

    @staticmethod
    def _update_file(file_path, old_str, new_str):

        file_data = ""
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if old_str in line:
                    line = line.replace(old_str, new_str)
                file_data += line
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_data)

    @staticmethod
    def _get_data_from_str(s):
        res = re.search('玩家(.*),游戏次数(.*),获胜次数(.*),胜率(.*)', s)
        print([res.group(1), res.group(2), res.group(3)])
        return [res.group(1), res.group(2), res.group(3)]



