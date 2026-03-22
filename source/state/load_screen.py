import pygame
from source.components import info

class LoadScreen:
    def __init__(self):
        self.finished = False
        self.next_state = 'level'
        self.timer = 0
        self.duration = 2000
        self.info = info.Info('load_screen')

    def update(self,surface,keys):
        self.draw(surface)
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.duration:
            self.finished = True
            self.timer = 0

    def draw(self,surface):
        surface.fill((0,0,0))
        self.info.draw(surface)
        self.info.update()

class GameOverScreen(LoadScreen):
    def __init__(self):
        LoadScreen.__init__(self)
        self.next = 'main_menu'
        self.duration = 4000
        self.info = info.Info('game_over')

