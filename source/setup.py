import pygame
from . import  constants as C
from . import tools

pygame.init()
SCREEN = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))#确定画布大小

GRAPHICS = tools.load_graphics('resources/graphics')