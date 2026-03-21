import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h,name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h)).convert() #将 Surface 转换为与显示格式相同的像素格式
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
