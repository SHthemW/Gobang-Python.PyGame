import pygame

from tkinter import *
from PIL import ImageTk, Image

from Datas.Config import *


class UIProgram:

    # components
    main_menu_root = None

    # 显示主菜单
    def show_main_menu(self, fn_pve, fn_pvp,  fn_quit):
        print('show')

        self.main_menu_root = Tk()
        self.main_menu_root.geometry("480x660")
        self.main_menu_root.title("Hello")

        img = Image.open(main_menu_img_path)
        img = img.resize((480, 480), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        lbl_btn_pve = Button(self.main_menu_root, text="挑战人工智能", command=fn_pve)
        lbl_btn_pvp = Button(self.main_menu_root, text="和三次元人玩", command=fn_pvp)
        lbl_btn_qut = Button(self.main_menu_root, text="退出游戏", command=fn_quit)
        text_lbl = Label(self.main_menu_root, text="要来一场愉快的五子棋游戏吗?", font=("Helvetica", 16))
        img_lbl = Label(self.main_menu_root, image=photo)

        img_lbl.grid(row=0, column=0)
        text_lbl.grid(row=1, column=0, pady=10)
        lbl_btn_pve.grid(row=2, column=0, pady=5)
        lbl_btn_pvp.grid(row=3, column=0, pady=5)
        lbl_btn_qut.grid(row=4, column=0, pady=5)

        self.main_menu_root.mainloop()
        pass

    def quit_main_menu(self):
        self.main_menu_root.destroy()
        pass

    @staticmethod
    def show_message_box(title, message):
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption(title)

        font = pygame.font.SysFont(None, 48)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (320, 240)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (255, 0, 0), (100, 100, 440, 280), 0)
            screen.blit(text, text_rect)
            pygame.display.update()
        pass
