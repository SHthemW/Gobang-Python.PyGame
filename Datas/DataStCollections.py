from enum import Enum


# enum
class MenuOperation(Enum):
    quit = 0
    start_game = 1


# Player
class PlayerData:
    name = 'Default'
    is_new = True
    win_times = 0
    all_times = 0

    # properties
    def win_ratio(self):
        return 0 if self.all_times == 0 else round(float(int(self.win_times) / int(self.all_times)), 2)

    def __init__(self, name, all_times, win_times, is_new):
        self.name = name
        self.is_new = is_new
        self.all_times = all_times
        self.win_times = win_times
        print(f'new player is inited. '
              f'name:{self.name}, is new:{self.is_new}, all times: {self.all_times}, win times:{self.win_times}, '
              f'current ratio: {self.win_ratio()}')
        pass

    def add_win_game(self):
        t1 = int(self.all_times)
        t1 += 1
        self.all_times = t1

        t2 = int(self.win_times)
        t2 += 1
        self.win_times = t2
        pass
    def add_los_game(self):
        t = int(self.all_times)
        t += 1
        self.all_times = t
        pass
