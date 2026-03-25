import pygame
from source import setup
from source.components import info,player,stuff,brick,box,enemy
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
        self.setup_bricks_and_boxes()
        self.init_enemy_system()
        self.setup_checkpoints()

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
        self.check_x_collision()
        # y direction
        if not self.player.dead:
            self.player.rect.y += self.player.y_vel
            self.check_y_collision()

    def init_enemy_system(self):
        """初始化敌人系统"""
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group_dict = {}
        self.setup_enemies()  # 实际加载敌人数据
        self.dying_group = pygame.sprite.Group()
        self.shell_group = pygame.sprite.Group()

    def setup_game_items(self):
        self.ground_items_group = pygame.sprite.Group()
        for name in ['ground', 'pipe', 'step']:
            for item in self.map_datas[name]:
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))

    def setup_bricks_and_boxes(self):
        self.brick_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()

        if 'brick' in self.map_datas:
            for brick_data in self.map_datas['brick']:
                x, y = brick_data['x'], brick_data['y']
                brick_type = brick_data['type']
                if brick_type == 0:
                    if 'brick_num' in brick_data:
                        # TODO BATCH BRICKS
                        pass
                    else:
                        self.brick_group.add(brick.Brick(x, y, brick_type,None))
                elif brick_type == 1:
                    self.brick_group.add(brick.Brick(x, y, brick_type,self.coin_group))
                else:
                    self.brick_group.add(brick.Brick(x, y, brick_type,self.powerup_group))

        if 'box' in self.map_datas:
            for box_data in self.map_datas['box']:
                x, y = box_data['x'], box_data['y']
                box_type = box_data['type']
                if box_type == 1:
                    self.box_group.add(box.Box(x, y, box_type,self.coin_group))
                else:
                    self.box_group.add(box.Box(x, y, box_type,self.powerup_group))

    def setup_enemies(self):
        for enemy_group_data in self.map_datas['enemy']:
            group = pygame.sprite.Group()
            for enemy_group_id, enemy_data_list in enemy_group_data.items(): #这里的enemy_group_id是字符串
                for enemy_data in enemy_data_list:
                    group.add(enemy.create_enemy(enemy_data))
                    self.enemy_group_dict[enemy_group_id] = group

    def activate_enemy_group(self, group_id):
        """激活指定的敌人组"""
        if group_id in self.enemy_group_dict:
            self.enemy_group.add(self.enemy_group_dict[group_id])
        # self.debug_enemy_system()

    def setup_checkpoints(self):
        self.checkpoint_group = pygame.sprite.Group()
        for item in self.map_datas['checkpoint']:
            x, y,w,h = item['x'], item['y'], item['width'], item['height']
            checkpoint_type = item['type']
            enemy_groupid = item.get('enemy_groupid')
            self.checkpoint_group.add(stuff.Checkpoint(x,y,w,h,checkpoint_type,enemy_groupid))

    def Check_checkpoints(self):
        checkpoint = pygame.sprite.spritecollideany(self.player, self.checkpoint_group)#返回第一个碰撞的精灵
        if checkpoint:
            if checkpoint.checkpoint_type == 0: # type 0 = 激活敌人
                self.activate_enemy_group(str(checkpoint.enemy_groupid)) #将敌人组ID从整数类型转换为字符串类型
            checkpoint.kill() # 移除检查点，避免重复激活

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

            if sprite.name == 'box':
                if sprite.state == 'rest':
                    sprite.go_bumped()

            if sprite.name == 'brick':
                if sprite.state == 'rest':
                    sprite.go_bumped()

    def check_x_collision(self):
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group)
        collision_occurs = pygame.sprite.spritecollideany(self.player, check_group)
        if collision_occurs:
            self.adjust_player_x(collision_occurs)
        #玩家碰撞后死亡
        # enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        # if enemy:
        #     self.player.go_die()
        #
        shell = pygame.sprite.spritecollideany(self.player, self.shell_group)
        if shell:
            if shell.state == 'slide':
                self.player.go_die()
            else:
                if self.player.rect.x < shell.rect.x:
                    shell.x_vel = 10
                    shell.rect.x += 40
                    shell.direction = 1
                else:
                    shell.x_vel = -10
                    shell.rect.x -= 40
                    shell.direction = 0
                shell.state = 'slide'

    def check_y_collision(self):
        ground_item = pygame.sprite.spritecollideany(self.player,self.ground_items_group)
        brick = pygame.sprite.spritecollideany(self.player,self.brick_group)
        box = pygame.sprite.spritecollideany(self.player,self.box_group)
        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)

        # 选择距离玩家最近的碰撞目标
        if brick and box:
            # 选择距离更近的物体
            if abs(self.player.rect.centerx - brick.rect.centerx) > abs(self.player.rect.centerx - box.rect.centerx):
                brick = None
            else:
                box = None
        if ground_item:
            self.adjust_player_y(ground_item)
        elif brick:
            self.adjust_player_y(brick)
        elif box:
            self.adjust_player_y(box)
        elif enemy:
            self.enemy_group.remove(enemy)
            if enemy.name == 'koopa':
                self.shell_group.add(enemy)
            else:
                self.dying_group.add(enemy)

            if self.player.y_vel < 0:
                how =  'bumped'
            else:
                how = 'trampled'
                self.player.state = 'jump'
                self.player.rect.bottom = enemy.rect.top
                self.player.y_vel = self.player.jump_vel * 0.8
            enemy.go_die(how)

        self.check_will_fall_or_not(self.player)

    def check_will_fall_or_not(self, sprite):
        sprite.rect.y += 1
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group,self.box_group)
        collided_sprite = pygame.sprite.spritecollideany(sprite,  check_group)
        if not collided_sprite and sprite.state != 'jump':
            sprite.state = 'fall'
        sprite.rect.y -= 1

    def check_if_go_die(self):
        if self.player.rect.y > C.SCREEN_H:
            self.player.go_die()

    def update_game_window(self):#相机系统
        third = self.game_window.x + self.game_window.width / 3
        if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < self.map_end_x:
            self.game_window.x += self.player.x_vel # 相机跟随
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
            self.Check_checkpoints()
            self.update_player_position()
            self.update_game_window()
            self.brick_group.update()
            self.box_group.update()
            self.check_if_go_die()
            self.enemy_group.update(self)# 更新敌人（传递关卡对象）
            self.dying_group.update(self)
            self.shell_group.update(self)
            self.coin_group.update()
            self.box_group.update()

        self.draw(surface)

    def draw(self,surface):
        self.game_ground.fill((0,0,0))
        self.game_ground.blit(self.background, self.game_window,self.game_window)# 绘制背景（相机裁剪）
        self.brick_group.draw(self.game_ground)
        self.box_group.draw(self.game_ground)
        self.game_ground.blit(self.player.image,self.player.rect)
        self.enemy_group.draw(self.game_ground)
        self.dying_group.draw(self.game_ground)
        self.shell_group.draw(self.game_ground)
        self.powerup_group.draw(self.game_ground)
        self.coin_group.draw(self.game_ground)
        surface.blit(self.game_ground,(0,0),self.game_window)# 将画布绘制到屏幕（相机效果）
        self.info.draw(surface)



"""
##############################################################
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
###########################################################################################################  

enemy_group.update(self) 中的 self 是当前 Level 实例，传给每个敌人，让敌人能够访问 Level 的属性和方法（例如 level.ground_items_group）

Level.update(self, surface, keys)
    │
    ├─ self 是 Level 实例 (包含 ground_items_group, brick_group, box_group 等)
    │
    └─ for enemy_group in self.enemy_group_dict.values():
            enemy_group.update(self)  # 传递 Level 实例
                │
                └─ pygame.sprite.Group.update(self, *args)
                    │
                    └─ for sprite in self.sprites():
                            sprite.update(*args)  # args = (self,)
                                │
                                └─ Enemy.update(self, level)  # level = Level 实例
                                    │
                                    ├─ self.handle_states()
                                    │
                                    └─ self.update_enemy_positon(level)
                                        │
                                        └─ self.check_x_collsion(level)
                                            │
                                            └─ 使用 level.ground_items_group
                                            
###########################################################################################################                                               
json示例：
"enemy":[
    {"0":[
        {"x":1120, "y":538, "direction":0, "type":0, "color":0}
    ]},
    {"1":[
        {"x":1920, "y":538, "direction":0, "type":0, "color":0}
    ]}
]

创建敌人字典：
self.enemy_group_dict = {
    "0": Group[Goomba(x=1120, y=538, direction=0)],
    "1": Group[Goomba(x=1920, y=538, direction=0)]
}

###########################################################################################################                                  
    
    初始化阶段:
┌─────────────────────────────────────────────┐
│  self.enemy_group_dict (休眠敌人仓库)         │
├─────────────────────────────────────────────┤
│  "0" → [Goomba1]     (未激活)                │
│  "1" → [Goomba2]     (未激活)                │
│  "2" → [Goomba3, Goomba4] (未激活)           │
└─────────────────────────────────────────────┘
                    ↓
         self.enemy_group = [] (活跃敌人组)

玩家移动:
    x=0 → x=510 (触发检查点0)
                    ↓
┌─────────────────────────────────────────────┐
│  激活敌人组"0"                                
│  self.enemy_group = [Goomba1]               │
└─────────────────────────────────────────────┘

玩家继续移动:
    x=1400 (触发检查点1)
                    ↓
┌─────────────────────────────────────────────┐
│  激活敌人组"1"                                
│  self.enemy_group = [Goomba1, Goomba2]      │
└─────────────────────────────────────────────┘

玩家继续移动:
    x=1740 (触发检查点2)
                    ↓
┌─────────────────────────────────────────────┐
│  激活敌人组"2"                               
│  self.enemy_group = [Goomba1, Goomba2,      │
│                     Goomba3, Goomba4]       │
└─────────────────────────────────────────────┘


###########################################################################################################   
按键触发调试
def update(self, surface, keys):
    # ... 游戏逻辑 ...
    
    # 按F3键输出调试信息
    if keys[pygame.K_F3]:
        self.debug_enemy_system()
    
    self.draw(surface)

在特定事件时调用
def Check_checkpoints(self):
    checkpoint = pygame.sprite.spritecollideany(self.player, self.checkpoint_group)
    if checkpoint:
        if checkpoint.checkpoint_type == 0:
            self.activate_enemy_group(str(checkpoint.enemy_groupid))
            # 激活敌人后立即输出状态
            print(f"激活敌人组{checkpoint.enemy_groupid}后的状态：")
            self.debug_enemy_system()
        checkpoint.kill()
调试代码：
   def debug_enemy_system(self):
        print("=== 敌人系统状态 ===")
        print(f"活跃敌人数量: {len(self.enemy_group)}") #获取活跃敌人组中的精灵数量
        print(f"休眠敌人组: {list(self.enemy_group_dict.keys())}") #获取字典的所有键,list()：将键转换为列表，便于显示 

        for group_id, group in self.enemy_group_dict.items():
            print(f"组{group_id}: {len(group)}个敌人") #len(group)：获取该组中的敌人数量

        for enemy in self.enemy_group:
            print(f"活跃敌人: {enemy.name} at ({enemy.rect.x}, {enemy.rect.y})")
"""
