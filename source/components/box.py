import pygame
from source import tools,setup
from source import constants as C

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, box_type, color= None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.box_type = box_type
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
