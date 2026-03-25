import pygame
from source import tools,setup
from source import constants as C
from .powerup import create_powerup

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, box_type, group,name='box'):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.box_type = box_type
        self.group = group
        self.name = name
        self.rect_frames = [
            (384,0,16,16),
            (400,0,16,16),
            (416,0,16,16),
            (432,0,16,16),
        ]

        self.frames = []
        for rect_frame in self.rect_frames:
            self.frames.append(tools.get_image(setup.GRAPHICS['tile_set'],*rect_frame,(0,0,0),C.BRICK_MULTI))

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.gravity = C.GRAVITY

        self.state = 'rest'
        self.timer = 0

    def handle_states(self):
        if self.state == 'rest':
            self.rest()
        elif self.state == 'bumped':
            self.bumped()
        elif self.state == 'open':
            self.open()

    def rest(self):
        frame_durations = [400,100,100,50]
        if self.current_time - self.timer > frame_durations[self.frame_index]:
            self.frame_index = (self.frame_index + 1) % 4
            self.timer = self.current_time
        self.image = self.frames[self.frame_index]

    def go_bumped(self):
        self.y_vel = -7
        self.state = 'bumped'

    def bumped(self):
        self.rect.y += self.y_vel
        self.y_vel += self.gravity
        self.frame_index = 3
        self.image = self.frames[self.frame_index]

        if self.rect.y > self.y + 10:
            self.rect.y = self.y
            self.state = 'open'

            # box_type 0,1,2,3对应空，金币，星星，蘑菇
            if self.box_type == 1:
                pass
            else:
                self.group.add(create_powerup(self.rect.centerx,self.rect.centery,self.box_type))

    def open(self):
        pass

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.handle_states()



