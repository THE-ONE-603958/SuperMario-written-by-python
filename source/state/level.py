import pygame
from source import setup
from source.components import info,player,stuff,brick,box
from source import constants as C
import json
import os

class Level:
    def start(self,game_info):
        self.game_info = game_info
        self.finished = False
        self.next_state = 'game_over'
        self.info = info.Info('level',self.game_info)
        self.load_map_data()
        self.setup_background()
        self.setup_map_data()
        self.setup_game_items()
        self.player = player.Player('mario')
        self.setup_player_start_position()
        self.setup_bricks()
        self.setup_boxs()

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

    def setup_game_items(self):
        self.game_items_group = pygame.sprite.Group()
        for name in ['ground', 'pipe', 'step']:
            for item in self.map_datas[name]:
                self.game_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))

    def setup_player_start_position(self):
        self.player.rect.x = self.game_window.x + self.player_x
        self.player.rect.bottom = self.player_y

    def update_player_position(self):
        self.player.rect.x += self.player.x_vel
        if self.player.rect.x < self.map_start_x:
            self.player.rect.x = self.map_start_x
        elif self.player.rect.right > self.map_end_x:
            self.player.rect.right = self.map_end_x
        self.check_x_collision()

        self.player.rect.y += self.player.y_vel
        self.check_y_collision()

    def setup_bricks(self):
        self.brick_group = pygame.sprite.Group()

        if 'brick' in self.map_datas:
            for brick_data in self.map_datas['brick']:
                x, y = brick_data['x'], brick_data['y']
                brick_type = brick_data['type']
                if 'brick_num' in brick_data:
                    # TODO BATCH BRICKS
                    pass
                else:
                    self.brick_group.add(brick.Brick(x, y, brick_type))

    def setup_boxs(self):
        self.box_group = pygame.sprite.Group()
        for box_data in self.map_datas['box']:
            x, y = box_data['x'], box_data['y']
            box_type = box_data['type']
            self.box_group.add(box.Box(x, y, box_type))

    def adjust_player_x(self, sprite):
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel = 0

    def adjust_player_y(self, sprite):
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.rect.bottom = sprite.rect.top
            self.player.y_vel = 0
            self.player.state ='walk'
        else:
            self.player.rect.top = sprite.rect.bottom
            self.player.y_vel = 7
            self.player.state ='fall'

    def check_x_collision(self):
        check_group = pygame.sprite.Group(self.game_items_group, self.brick_group)
        collision_occurs = pygame.sprite.spritecollideany(self.player, check_group)
        if collision_occurs:
            self.adjust_player_x(collision_occurs)

    def check_y_collision(self):
        check_group = pygame.sprite.Group(self.game_items_group, self.brick_group,self.box_group)
        collision_occurs = pygame.sprite.spritecollideany(self.player, check_group)
        if collision_occurs:
            self.adjust_player_y(collision_occurs)
        self.check_will_fall_or_not(self.player)

    def check_will_fall_or_not(self, sprite):
        sprite.rect.y += 1
        check_group = pygame.sprite.Group(self.game_items_group, self.brick_group,self.box_group)
        collided_sprite = pygame.sprite.spritecollideany(sprite,  check_group)
        if not collided_sprite and sprite.state != 'jump':
            sprite.state = 'fall'
        sprite.rect.y -= 1

    def check_if_go_die(self):
        if self.player.rect.y > C.SCREEN_H:
            self.player.go_die()

    def update_game_window(self):
        third = self.game_window.x + self.game_window.width / 3
        if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < self.map_end_x:
            self.game_window.x += self.player.x_vel
            self.map_start_x = self.game_window.x

    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives'] -= 1
        if self.game_info['lives'] == 0:
            self.next_state = 'game_over'
        else:
            self.next_state = 'load_screen'

    def update(self,surface,keys):
        self.current_time = pygame.time.get_ticks()
        self.player.update(keys)

        if self.player.dead:
            if self.current_time - self.player.death_timer > 3000:
                self.finished = True
                self.update_game_info()
        else:
            self.info.update()
            self.update_player_position()
            self.update_game_window()
            self.brick_group.update()
            self.box_group.update()
            self.check_if_go_die()
        self.draw(surface)

    def draw(self,surface):
        self.game_ground.fill((0,0,0))
        self.game_ground.blit(self.background, self.game_window,self.game_window)
        self.brick_group.draw(self.game_ground)
        self.box_group.draw(self.game_ground)
        self.game_ground.blit(self.player.image,self.player.rect)
        surface.blit(self.game_ground,(0,0),self.game_window)
        self.info.draw(surface)



"""
def adjust_player_x(self, sprite):
pass

def adjust_player_y(self, sprite):
pass

情况1：玩家在上方（从上往下掉落）
    玩家
   ┌────┐
   │    │
   └────┘ ← player.rect.bottom
   
   ┌────┐
   │    │ 平台
   └────┘ ← sprite.rect.bottom
   此时 player.rect.bottom < sprite.rect.bottom 为 True
→ 玩家应该落在平台上

情况2：玩家在下方（从下往上顶）
   
   ┌────┐
   │    │ 平台
   └────┘ ← sprite.rect.bottom
   
    玩家     
   ┌────┐
   │    │
   └────┘ ← player.rect.bottom
   
   此时 player.rect.bottom < sprite.rect.bottom 为 False
→ 玩家应该被顶下来

"""
