import pygame
from source import setup
from source.components import info,player
from source import constants as C


class Level:
    def __init__(self):
        self.finished = False
        self.next_state = None
        self.info = info.Info('level')
        self.setup_background()
        self.player = player.Player('mario')
        self.setup_player()


    def setup_background(self):
        self.background = setup.GRAPHICS['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * C.BG_MULTI),
                                                                   int(self.background_rect.height * C.BG_MULTI)))

    def setup_player(self):
        self.player.rect.x = 300
        self.player.rect.y = 300

    def update(self,surface,keys):
        self.player.update(keys)
        self.update_player_position()
        self.draw(surface)

    def update_player_position(self):
        self.player.rect.x += self.player.x_vel
        self.player.rect.y += self.player.y_vel

    def draw(self,surface):
        surface.blit(self.background, (0,0))
        surface.blit(self.player.image, self.player.rect)
        self.info.draw(surface)
        self.info.update()
