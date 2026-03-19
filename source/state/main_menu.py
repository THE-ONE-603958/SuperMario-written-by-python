import pygame
from source import setup,tools
from source import constants as C
from source.components import info

class MainMenu:
    def __init__(self):
        self.setup_background()
        self.setup_player()
        self.setup_cursor()
        self.info = info.Info('main_menu')

        self.finished = False
        self.next_state = 'load_screen'

    def setup_background(self):
        self.background = setup.GRAPHICS['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background,(int(self.background_rect.width*C.BG_MULTI),
                                                                  int(self.background_rect.height*C.BG_MULTI)))
        self.viewport = setup.SCREEN.get_rect()#记录画布位置信息
        self.caption = tools.get_image(setup.GRAPHICS['title_screen'],1,60,176,88,(255,0,220),C.BG_MULTI)

    def setup_player(self):
        self.player_image = tools.get_image(setup.GRAPHICS['mario_bros'],178,32,12,16,(0,0,0),C.PLAYER_MULTI)

    def setup_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = tools.get_image(setup.GRAPHICS['item_objects'],24,160,8,8,(0,0,0),C.PLAYER_MULTI)
        self.cursor.rect = self.cursor.image.get_rect()
        self.cursor.rect.x, self.cursor.rect.y = (220,360)

        self.cursor.state = '1P'

    def update_cursor_state(self,keys):
        if keys[pygame.K_UP]:
            self.cursor.state = '1P'
            self.cursor.rect.y = 360
        elif keys[pygame.K_DOWN]:
            self.cursor.state = '2P'
            self.cursor.rect.y = 405
        elif keys[pygame.K_RETURN]:
            if self.cursor.state == '1P':
                self.finished = True
            elif self.cursor.state == '2P':
                self.finished = True

    def update(self,surface,keys):
        self.update_cursor_state(keys)
        surface.blit(self.background,self.viewport)
        surface.blit(self.caption,(170,100))
        surface.blit(self.player_image,(110,490))
        surface.blit(self.cursor.image,self.cursor.rect)

        self.info.update()
        self.info.draw(surface)




