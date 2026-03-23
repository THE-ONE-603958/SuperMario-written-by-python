#游戏主入口
import pygame
from source import tools, setup
from source.state import main_menu,load_screen,level


def main():
    state_dict ={
        'main_menu':main_menu.MainMenu(),
        'load_screen':load_screen.LoadScreen(),
        'level':level.Level(),
        'game_over':load_screen.GameOverScreen()
    }
    game = tools.Game(state_dict,'main_menu')
    game.run()

if __name__ == '__main__':
    main()


"""
当类没有定义 __init__ 方法时：
class LoadScreen:
    def start(self,game_info):
        self.game_info = game_info
        self.finished = False
        self.next_state = 'level'
        self.timer = 0
        self.duration = 2000
        self.info = info.Info('load_screen',self.game_info)
Python 会自动提供默认的 __init__ 方法
默认的 __init__ 方法不接受任何参数（除了 self）
因此 LoadScreen() 可以无参数创建实例
    load_screen.LoadScreen(self,game_info)
"""