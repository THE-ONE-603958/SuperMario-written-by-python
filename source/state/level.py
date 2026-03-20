import pygame
from source import setup
from source.components import info,player
from source import constants as C
import json
import os


class Level:
    def __init__(self):
        self.finished = False
        self.next_state = None
        self.info = info.Info('level')
        self.load_map_data()
        self.setup_background()
        self.player = player.Player('mario')
        self.setup_map_data()
        self.setup_player_start_position()

    def load_map_data(self):
        file_name = 'level_1.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.map_datas = json.load(f)

    def setup_background(self):
        self.image_name = self.map_datas['image_name']
        self.background = setup.GRAPHICS[self.image_name] #原视背景图像
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * C.BG_MULTI),
                                                                   int(self.background_rect.height * C.BG_MULTI)))
        self.game_ground = pygame.Surface(self.background.get_rect().size) #游戏画布（离屏缓冲区）
        self.game_window = setup.SCREEN.get_rect() #（相机）

    def setup_map_data(self):
        self.positions = []
        for map_data in self.map_datas['maps']:
            self.positions.append((map_data['start_x'], map_data['end_x'],map_data['player_x'],map_data['player_y']))
            self.map_start_x, self.map_end_x, self.player_x, self.player_y = self.positions[0]

    def setup_player_start_position(self):
        self.player.rect.x = self.game_window.x + self.player_x
        self.player.rect.bottom = self.player_y

    def update_player_position(self):
        self.player.rect.x += self.player.x_vel
        if self.player.rect.x < self.map_start_x:
            self.player.rect.x = self.map_start_x
        elif self.player.rect.right > self.map_end_x:
            self.player.rect.right = self.map_end_x
        self.player.rect.y += self.player.y_vel

    def update_game_window(self):
        third = self.game_window.x + self.game_window.width / 3
        if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < self.map_end_x:
            self.game_window.x += self.player.x_vel
            self.map_start_x = self.game_window.x

    def update(self,surface,keys):
        self.player.update(keys)
        self.update_player_position()
        self.update_game_window()
        self.draw(surface)


    def draw(self,surface):
        self.game_ground.blit(self.background, self.game_window,self.game_window)
        self.game_ground.blit(self.player.image,self.player.rect)
        surface.blit(self.game_ground,(0,0),self.game_window)
        self.info.draw(surface)
        self.info.update()
