import pygame
from . import  constants as C
from . import tools
from .constants import SCREEN_SIZE

pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)#创建一个新的显示表面

GRAPHICS = tools.load_graphics('resources/graphics')