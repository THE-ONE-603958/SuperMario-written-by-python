import pygame
from source import tools,setup
from source import constants as C

def create_enemy(enemy_data):
    enemy_type = enemy_data['type']
    x,y_b,direction,color = enemy_data['x'],enemy_data['y'],enemy_data['direction'],enemy_data['color']

    if enemy_type == 0:
        enemy = Goomba(x,y_b,direction,'goomba',color)
    elif enemy_type == 1:
        enemy = Koopa(x,y_b,direction,'koopa',color)
    return enemy

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y_b,direction,name,rect_frames):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.name = name
        self.frame_index = 0
        self.left_frames = []
        self.right_frames = []

        self.load_frames(rect_frames)
        self.frames = self.left_frames if self.direction == 0 else self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y_b

    def load_frames(self,rect_frames):
        for rect_frame in rect_frames:
            left_frame = tools.get_image(setup.GRAPHICS['enemies'],*rect_frame,(0,0,0),C.ENEMY_MULTI)
            right_frame = pygame.transform.flip(left_frame,True,False)
            self.left_frames.append(left_frame)
            self.right_frames.append(right_frame)

class Goomba(Enemy):
    def __init__(self,x,y_b,direction,name,color):

        bright_rect_frames = [(0,16,16,16),(16,16,16,16),(32,16,16,16)]
        dark_rect_frames = [(0,48,16,16),(16,48,16,16),(32,48,16,16)]

        if not color:
            rect_frames = bright_rect_frames
        else:
            rect_frames = dark_rect_frames

        Enemy.__init__(self,x,y_b,direction,name,rect_frames)

class Koopa(Enemy):
    def __init__(self,x,y_b,direction,name,color):

        bright_rect_frames = [(96,9,16,22),(112,9,16,22),(160,9,16,22)]
        dark_rect_frames = [(96,72,16,22),(112,72,16,22),(160,72,16,22)]

        if not color:
            rect_frames = bright_rect_frames
        else:
            rect_frames = dark_rect_frames

        Enemy.__init__(self,x,y_b,direction,name,rect_frames)
"""
继承的优势：

代码复用 - 公共代码写在父类中

多态性 - 可以统一处理不同类型的敌人

扩展性 - 容易添加新类型的敌人

维护性 - 修改公共逻辑只需改父类

################################################################
步骤1：调用 create_enemy(enemy_data)

# 传入 enemy_data
    enemy_data = {"x":1120, "y":538, "direction":0, "type":0, "color":0}
    def create_enemy(enemy_data):
        enemy_type = enemy_data['type']  # 0

    if enemy_type == 0:  # True
        # 创建 Goomba 实例
        enemy = Goomba(x, y, direction, 'goomba', color)
        # 内部调用 Enemy.__init__(self, 1120, 538, 0, 'goomba', rect_frames)
        # rect_frames 根据 color=0 选择 bright_rect_frames
    return enemy  # 返回 Goomba 实例

步骤2：
添加到精灵组
 
    group.add(goomba_instance) 
    
    第三次次迭代后：
    group = pygame.sprite.Group()
    group.add(Goomba3)  # 添加第1个Goomba
    group.add(Goomba4)  # 添加第2个Goomba
    # group现在包含2个Goomba
    ....
    
存储敌人组到字典
    self.enemy_group_dict = {
        "0": <pygame.sprite.Group with 1 Goomba>,
        "1": <pygame.sprite.Group with 1 Goomba>,
        "2": <pygame.sprite.Group with 2 Goombas>
    }
    
    setup_enemies() 开始
    │
    ├─ self.enemy_group_dict = {}
    │
    ├─ 遍历 enemy 列表 (10个组)
    │   │
    │   ├─ 迭代1: enemy_group_data = {"0": [enemy1_data]}
    │   │   ├─ group = pygame.sprite.Group()
    │   │   ├─ items() → ("0", [enemy1_data])
    │   │   ├─ 遍历 enemy_list
    │   │   │   ├─ enemy_data = {"x":1120, "y":538, "direction":0, "type":0, "color":0}
    │   │   │   ├─ create_enemy(enemy_data)
    │   │   │   │   ├─ type=0 → Goomba(1120,538,0,'goomba',0)
    │   │   │   │   └─ 返回 Goomba实例
    │   │   │   └─ group.add(goomba)
    │   │   └─ enemy_group_dict["0"] = group
    │   │
    │   ├─ 迭代2: enemy_group_data = {"1": [enemy2_data]}
    │   │   └─ ... 类似流程，创建 group "1"
    │   │
    │   ├─ 迭代3: enemy_group_data = {"2": [enemy3_data, enemy4_data]}
    │   │   ├─ group = pygame.sprite.Group()
    │   │   ├─ items() → ("2", [enemy3_data, enemy4_data])
    │   │   ├─ 遍历 enemy_list (2次)
    │   │   │   ├─ 第1次: 创建 Goomba(2320,538,0,'goomba',0)
    │   │   │   ├─ group.add(goomba1)
    │   │   │   ├─ 第2次: 创建 Goomba(2380,538,0,'goomba',0)
    │   │   │   └─ group.add(goomba2)
    │   │   └─ enemy_group_dict["2"] = group
    │   │
    │   ├─ 迭代4-10: 类似流程处理组 "3" 到 "9"
    │   │
    │   └─ 迭代5: enemy_group_data = {"5": [koopa_data]}
    │       ├─ group = pygame.sprite.Group()
    │       ├─ items() → ("5", [koopa_data])
    │       ├─ enemy_data = {"x":4700, "y":538, "direction":0, "type":1, "color":1}
    │       ├─ create_enemy(enemy_data)
    │       │   ├─ type=1 → Koopa(4700,538,0,'koopa',1)
    │       │   └─ 返回 Koopa实例
    │       ├─ group.add(koopa)
    │       └─ enemy_group_dict["5"] = group
    │
    └─ setup_enemies() 结束

"""