#工具和游戏主控
import os
import pygame
import random

class Game:
    def __init__(self,state_dict,start_state):
        self.screen = pygame.display.get_surface()#获取当前已存在的显示表面
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state =self.state_dict[start_state]

    def update(self):
        if self.state.finished:
            next_state = self.state.next_state
            self.state.finished = False
            self.state = self.state_dict[next_state]
        self.state.update(self.screen,self.keys)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()
            self.update()
            pygame.display.update()
            self.clock.tick(60)

def load_graphics(path,accept=('.jpg','.png','.bmp','.gif')):
    graphics = {}
    for pic in os.listdir(path): # 获取文件夹中的所有文件和子文件夹
        name, ext = os.path.splitext(pic) #分割文件名和扩展名
        if ext.lower() in accept: #将扩展名转换为小写
            img = pygame.image.load(os.path.join(path,pic)) #构建完整的文件路径
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img
    return graphics

def get_image(sheet,x,y,width,height,colorkey,scale):
    img = pygame.Surface((width,height))
    img.blit(sheet,(0,0),(x,y,width,height))
    img.set_colorkey(colorkey)
    img = pygame.transform.scale(img,(int(width*scale),int(height*scale)))
    return img


