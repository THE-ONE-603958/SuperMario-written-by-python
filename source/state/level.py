import pygame
from source import setup
from source.components import info
from source import constants as C


class Level:
    def __init__(self):
        self.finished = False
        self.next_state = None
        self.setup_background()
        self.info = info.Info('level')

    def setup_background(self):
        self.background = setup.GRAPHICS['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * C.BG_MULTI),
                                                                   int(self.background_rect.height * C.BG_MULTI)))

    def update(self,surface,keys):
        self.draw(surface)

    def draw(self,surface):
        surface.blit(self.background, self.background_rect)
        self.info.draw(surface)
