#游戏主入口
import pygame
from source import tools, setup
from source.state import main_menu


def main():
    game = tools.Game()
    state = main_menu.MainMenu()
    game.run(state)

if __name__ == '__main__':
    main()