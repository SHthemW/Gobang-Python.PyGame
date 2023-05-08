import pygame

from Datas.Config import *
from Logics.Logic_AI import AIProgram
from Logics.Logic_UI import UIProgram


class GameProgram:

    # components
    pygame = None
    screen = None
    board = None
    ai_opponent = None

    # properties
    board_x = None
    board_y = None
    is_pvp_mode = False
    current_player = None
    cell_count = board_size // cell_size

    def init_prop(self, is_pvp_mode):
        self.pygame = pygame.init()
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((board_size, board_size))
        # 设置窗口标题
        pygame.display.set_caption("五子棋")
        # 定义棋盘的大小和位置
        self.board_x = (self.screen.get_width() - board_size) // 2
        self.board_y = (self.screen.get_height() - board_size) // 2
        # 定义棋盘的二维数组，用于存储棋子的位置和颜色
        self.board = [[0 for _ in range(self.cell_count)] for _ in range(self.cell_count)]
        # 定义当前下棋的玩家，1表示黑方，-1表示白方
        self.current_player = 1
        # init AI
        self.is_pvp_mode = is_pvp_mode
        self.ai_opponent = AIProgram(self.cell_count, self.current_player)

    # 判断输赢. 若当前玩家获胜返回True, 否则返回False
    def check_win(self):

        board = self.board
        cell_count = self.cell_count
        current_player = self.current_player

        # 横向判断
        for i in range(cell_count):
            for j in range(cell_count):
                if board[i][j] == current_player and board[i][j + 1] == current_player and board[i][
                    j + 2] == current_player and \
                        board[i][j + 3] == current_player and board[i][j + 4] == current_player:
                    return True
        # 纵向判断
        for i in range(cell_count):
            for j in range(cell_count):
                if board[i][j] == current_player and board[i + 1][j] == current_player and board[i + 2][
                    j] == current_player and \
                        board[i + 3][j] == current_player and board[i + 4][j] == current_player:
                    return True
        # 左斜向判断
        for i in range(cell_count):
            for j in range(cell_count):
                if board[i][j] == current_player and board[i + 1][j + 1] == current_player and board[i + 2][
                    j + 2] == current_player and \
                        board[i + 3][j + 3] == current_player and board[i + 4][j + 4] == current_player:
                    return True
        # 右斜向判断
        for i in range(cell_count):
            for j in range(cell_count):
                if board[i][j] == current_player and board[i + 1][j - 1] == current_player and board[i + 2][
                    j - 2] == current_player and \
                        board[i + 3][j - 3] == current_player and board[i + 4][j - 4] == current_player:
                    return True

        return False

    # 游戏循环. 若有玩家获胜, 返回其代号. 否则返回0.
    def loop(self):

        winner_player = 0
        player_drop_pos = None

        # 处理用户输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                winner_player = 0
                self.quit_game()
                return winner_player

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 下棋
                if self.current_player == 1 or self.is_pvp_mode:
                    player_drop_pos = self.convert_mouse_point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    if not self.drop_chess(player_drop_pos[0], player_drop_pos[1]):
                        continue

                    # 判断输赢, 赢了的话结束游戏, 否则切换玩家.
                    if self.check_win():
                        UIProgram.show_message_box('msg', f'player {self.current_player} is win.')
                        winner_player = self.current_player
                        self.quit_game()
                        return winner_player
                    else:
                        self.current_player *= -1
                        winner_player = 0

        if self.current_player == -1 and not self.is_pvp_mode:
            # AI下棋
            self.ai_opponent.set_last_player_drop(player_drop_pos[0], player_drop_pos[1])
            ai_drop_pos = self.ai_opponent.get_ai_drop()
            self.drop_chess(ai_drop_pos[0], ai_drop_pos[1])

            # 判断输赢, 赢了的话结束游戏, 否则切换玩家.
            if self.check_win():
                UIProgram.show_message_box('msg', f'player {self.current_player} is win.')
                winner_player = self.current_player
                self.quit_game()
                return winner_player
            else:
                self.current_player *= -1
                winner_player = 0

        # 绘制游戏元素
        self.screen.fill((255, 255, 255))

        # 绘制棋盘网格线
        for i in range(self.cell_count + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (self.board_x, self.board_y + i * cell_size),
                             (self.board_x + board_size, self.board_y + i * cell_size))
            pygame.draw.line(self.screen, (0, 0, 0), (self.board_x + i * cell_size, self.board_y),
                             (self.board_x + i * cell_size, self.board_y + board_size))

        # 绘制棋子
        for y in range(self.cell_count):
            for x in range(self.cell_count):
                if self.board[y][x] == 1:
                    font = pygame.font.Font(None, cell_size)
                    text = font.render("X", True, (0, 0, 0))
                    self.screen.blit(text, (self.board_x + x * cell_size - text.get_width() // 2,
                                            self.board_y + y * cell_size - text.get_height() // 2))
                elif self.board[y][x] == -1:
                    font = pygame.font.Font(None, cell_size)
                    text = font.render("O", True, (0, 0, 0))
                    self.screen.blit(text, (self.board_x + x * cell_size - text.get_width() // 2,
                                            self.board_y + y * cell_size - text.get_height() // 2))

        pygame.display.flip()
        return winner_player
        pass

    def drop_chess(self, pos_x, pos_y):
        # 判断格子是否为空，如果为空则下棋
        if self.board[pos_y][pos_x] == 0:
            self.board[pos_y][pos_x] = self.current_player
            print(f'{self.current_player} - {pos_x},{pos_y}')
            return True
        else:
            print('invalid position')
            return False
        pass

    def convert_mouse_point(self, pos_x, pos_y):
        # 计算鼠标点击的格子位置
        cell_x = (pos_x - self.board_x + cell_size // 2) // cell_size
        cell_y = (pos_y - self.board_y + cell_size // 2) // cell_size
        return [cell_x, cell_y]
        pass

    # 退出游戏
    @staticmethod
    def quit_game():
        pygame.quit()
        pass
