import pygame
from source import setup,tools
from source import constants as C
import json
import os

class Player(pygame.sprite.Sprite):
    def __init__(self,name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.load_data()
        self.setup_player_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('source/data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)

    def setup_player_states(self):
        self.state = 'stand'
        self.face_right = True
        self.dead = False
        self.big = False
        self.can_jump = True

    def setup_velocities(self):
        speed = self.player_data['speed']
        self.x_vel = 0
        self.y_vel = 0

        self.max_walk_vel = speed['max_walk_speed']
        self.max_run_vel = speed['max_run_speed']
        self.max_y_vel = speed['max_y_velocity']
        self.jump_vel = speed['jump_velocity']
        self.walk_accel = speed['walk_accel']
        self.turn_accel = speed['turn_accel']
        self.run_accel = speed['run_accel']
        self.gravity = C.GRAVITY
        self.anti_gravity = C.ANTI_GRAVITY

        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel

    def setup_timers(self):
        self.walking_timer = 0
        self.transition_timer = 0

    def load_images(self):
        sheet = setup.GRAPHICS['mario_bros']
        frame_rects = self.player_data['image_frames']
        self.right_small_normal_frames = []
        self.right_big_normal_frames = []
        self.right_big_fire_frames = []
        self.left_small_normal_frames = []
        self.left_big_normal_frames = []
        self.left_big_fire_frames = []

        self.small_normal_frames = [self.right_small_normal_frames, self.left_small_normal_frames]
        self.big_normal_frames = [self.right_big_normal_frames, self.left_big_normal_frames]
        self.big_fire_frames = [self.right_big_fire_frames, self.left_big_fire_frames]

        self.all_frames = [
            self.right_small_normal_frames,
            self.right_big_normal_frames,
            self.right_big_fire_frames,
            self.left_small_normal_frames,
            self.left_big_normal_frames,
            self.left_big_fire_frames
        ]

        self.right_frames = self.right_small_normal_frames
        self.left_frames = self.left_small_normal_frames

        for group, group_frame_rects in frame_rects.items(): #返回字典中的所有键值对,每个键值对是一个元组
            for frame_rect in group_frame_rects:
                right_image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'],
                                              frame_rect['width'], frame_rect['height'],(0,0,0),C.PLAYER_MULTI)
                left_image = pygame.transform.flip(right_image, True, False)
                if group == 'right_small_normal':
                    self.right_small_normal_frames.append(right_image)
                    self.left_small_normal_frames.append(left_image)
                if group == 'right_big_normal':
                    self.right_big_normal_frames.append(right_image)
                    self.left_big_normal_frames.append(left_image)
                if group == 'right_big_fire':
                    self.right_big_fire_frames.append(right_image)
                    self.left_big_fire_frames.append(left_image)

            self.frame_index = 0
            self.frames = self.right_frames
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect()

    def stand(self,keys):
        self.frame_index  = 0
        self.x_vel = 0
        self.y_vel = 0
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            self.state = 'walk'
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            self.state = 'walk'

        if keys[pygame.K_SPACE] and self.can_jump:
            self.state = 'jump'
            self.y_vel = self.jump_vel

    def walk(self,keys):
        if keys[pygame.K_LSHIFT]:
            self.max_x_vel = self.max_run_vel
            self.x_accel = self.run_accel
        else:
            self.max_x_vel = self.max_walk_vel
            self.x_accel = self.walk_accel

        if keys[pygame.K_SPACE] and self.can_jump:
            self.state = 'jump'
            self.y_vel = self.jump_vel

        if keys[pygame.K_RIGHT]:
            self.face_right = True
            if self.x_vel < 0:
                self.frame_index = 5
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel,self.max_x_vel,True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 5
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel,self.max_x_vel,False)
        else: #无按键按下时
            if self.face_right:
                self.x_vel -= self.x_accel
                if self.x_vel < 0:
                    self.x_vel = 0
                    self.state = 'stand'
            else:
                self.x_vel += self.x_accel
                if self.x_vel > 0:
                    self.x_vel = 0
                    self.state = 'stand'

    def jump(self,keys):
        self.can_jump = False

        self.frame_index = 4
        self.y_vel += self.anti_gravity
        if self.y_vel > 0:
            self.state = 'fall'

        if keys[pygame.K_RIGHT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel,self.max_x_vel,True)
        elif keys[pygame.K_LEFT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel,self.max_x_vel,False)

        if not keys[pygame.K_SPACE]:
            self.state = 'fall'

    def fall(self,keys):
        self.y_vel = self.calc_vel(self.y_vel,self.gravity,self.max_y_vel,True)


    def can_jump_or_not(self,keys):
        if not keys[pygame.K_SPACE]:
            self.can_jump = True

    def handle_states(self,keys):

        self.can_jump_or_not(keys)

        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'fall':
            self.fall(keys)

        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.walking_timer > self.frame_duration():
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time

    def frame_duration(self):
        duration = -60/self.max_run_vel * abs(self.x_vel) + 80
        return duration

    def calc_vel(self,vel,accel,max_vel,is_positive=True):
        if is_positive:
            return min(vel+accel, max_vel)
        else:
            return max(vel-accel, -max_vel)

    def update(self,keys):
        self.handle_states(keys)


"""
1. 初始状态: can_jump = True
        ↓
2. 玩家按下空格键 (在 stand 或 walk 状态)
        ↓
3. 进入 jump() 方法: can_jump = False
        ↓
4. 玩家在空中，持续按或不按空格键
        ↓
5. 玩家落地后 (在 fall 或 walk 状态)
        ↓
6. can_jump_or_not() 被调用
   - 如果 keys[K_SPACE] == False → can_jump = True
   - 如果 keys[K_SPACE] == True → can_jump = False (保持)
        ↓
7. 回到步骤 2，可以再次跳跃
"""

