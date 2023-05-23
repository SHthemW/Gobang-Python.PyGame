from Logics.Logic_Data import DataProgram
from Logics.Logic_Game import GameProgram
from Logics.Logic_UI import UIProgram


class Game:

    # main logic
    game = None
    data = None
    ui = None

    # properties
    game_running = True
    player_name  = None
    turn_res = 0

    def __init__(self):
        # init logic
        self.game = GameProgram()
        self.data = DataProgram()
        self.ui = UIProgram()

    def startup(self):
        # init player data
        self.data.set_player_name('SHW')
        #  show main menu
        self.ui.show_main_menu(
            fn_pve=self._start_pve_game,
            fn_pvp=self._start_pvp_game,
            fn_quit=self._quit_menu
        )
        pass

    def _start_pvp_game(self):
        # init game program
        self.game.init_prop(True)
        self._start_game_loop()
    def _start_pve_game(self):
        # init game program
        self.game.init_prop(False)
        self._start_game_loop()
    def _start_game_loop(self):
        # hide menu
        self.ui.quit_main_menu()
        # hold the game
        while self.game_running:
            self.turn_res = self.game.loop()
            self.game_running = self.turn_res == 0

        print('game over')
        self._on_game_end(self.turn_res)
        pass

    def _on_game_end(self, winner):
        print('胜负已分. 赢家是:' + str(winner))
        self.data.set_current_player_mark(winner)
        self.data.save_current_data()
        pass

    def _quit_menu(self):
        self.ui.quit_main_menu()
