import pygame
from source import tools,setup
from source import constants as C

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, brick_type, color= 1,name='brick'):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.brick_type = brick_type
        self.name = name
        bright_rect_frames = [(16,0,16,16),(48,0,16,16)]
        dark_rect_frames = [(16,32,16,16),(48,32,16,16)]

        if not color:
            self.rect_frames = bright_rect_frames
        else:
            self.rect_frames = dark_rect_frames

        self.frames = []
        for rect_frame in self.rect_frames:
            self.frames.append(tools.get_image(setup.GRAPHICS['tile_set'],*rect_frame,(0,0,0),C.BRICK_MULTI))

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.state = 'rest'
        self.gravity = C.GRAVITY

    def handle_states(self):
        if self.state == 'rest':
            self.rest()
        elif self.state == 'bumped':
            self.bumped()
        elif self.state == 'open':
            self.open()

    def rest(self):
        pass

    def go_bumped(self):
        self.y_vel = -7
        self.state = 'bumped'

    def bumped(self):
        self.rect.y += self.y_vel
        self.y_vel += self.gravity

        if self.rect.y > self.y + 5:
            self.rect.y = self.y
            self.state = 'rest'

    def open(self):
        pass

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.handle_states()
