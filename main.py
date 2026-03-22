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
# 1. 创建 LoadScreen 实例（使用默认的 __init__）
load_screen = load_screen.LoadScreen()  # ✅ 成功，不需要参数

# 2. 后续在其他地方调用 start 方法传递 game_info
# 在 tools.Game 的某个地方（可能是在状态切换时）
load_screen.start(game_info)  # 这时才传递 game_info
"""