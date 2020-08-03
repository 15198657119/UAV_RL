import pygame
import time
import sys
from pygame.locals import *
from change_random_system_env_set_affinity import *
'''
    4. 使用面向对象的方式显示飞机，以及控制其左右移动

    接下来要做的任务：
    1. 实现飞机在你想要的位置显示
    2. 实现按键控制飞机移动
'''


class HeroPlane(object):
    def __init__(self, screen):
        # 设置飞机默认的位置
        self.x = 0
        self.y = 0
        # 设置要显示内容的窗口
        self.screen = screen
        # 用来保存英雄飞机需要的图片名字
        self.imageName = "Fonts/plane2.png"
        # 根据名字生成飞机图片
        self.image = pygame.image.load(self.imageName).convert()
        self.image1 = pygame.image.load("Fonts/home.png").convert()
        self.image2 = pygame.image.load("Fonts/final.png").convert()
        self.image3 = pygame.image.load("Fonts/start.png").convert()

    def display(self):
        plane_size =80
        home_size = 80
        start_label_size =80
        pygame.display.set_caption('RL_UAV')
        self.screen.blit(pygame.transform.scale(self.image,(plane_size,plane_size)), (self.x, self.y))
        self.screen.blit(pygame.transform.scale(self.image1, (home_size, home_size)), (100, 100))
        self.screen.blit(pygame.transform.scale(self.image1, (home_size, home_size)), (136, 200))
        self.screen.blit(pygame.transform.scale(self.image1, (home_size, home_size)), (300, 300))
        self.screen.blit(pygame.transform.scale(self.image1, (home_size, home_size)), (550, 400))
        self.screen.blit(pygame.transform.scale(self.image1, (home_size,home_size)), (400, 300))
        self.screen.blit(pygame.transform.scale(self.image1, (home_size, home_size)), (600, 40))

        self.screen.blit(pygame.transform.scale(self.image2, (start_label_size, start_label_size)), (720, 700))
        self.screen.blit(pygame.transform.scale(self.image3, (start_label_size, start_label_size)), (0 ,700))
        # ( (0, 0)
    def move(self,x,y):
        self.x = x
        self.y = y
    def moveLeft(self):
        self.x -= 10

    def moveRight(self):
        self.x += 10

    def moveUp(self):
        self.y -= 10

    def moveDown(self):
        self.y += 10


def key_control(heroPlane,x,y):
    heroPlane.move(x,y)

def main():
    # 1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((800, 800), 0, 32)
    screen.fill((255, 255, 255))

    # 2. 创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("Fonts/bg1.png").convert()

    # 3. 创建一个飞机对象
    heroPlane = HeroPlane(screen)

    # 3. 把背景图片放到窗口中显示
    x = 0
    y = 700
    while True:
        screen.blit(background, (0, 800))

        heroPlane.display()

        key_control(heroPlane,x,y)

        pygame.display.update()
        time.sleep(0.1)
        x += 3
        y -= 0.8
        screen = pygame.display.set_mode((800, 800), 0, 32)
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def control(x=0,y=700):
    # 1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((800, 800), 0, 32)
    screen.fill((255, 255, 255))

    # 2. 创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("Fonts/bg1.png").convert()

    # 3. 创建一个飞机对象
    heroPlane = HeroPlane(screen)

    # 3. 把背景图片放到窗口中显示
    # x = 0
    # y = 700
    while True:
        screen.blit(background, (0, 800))

        heroPlane.display()

        key_control(heroPlane,x,y)

        pygame.display.update()
        time.sleep(0.1)
        # x += 3
        # y -= 0.8
        screen = pygame.display.set_mode((800, 800), 0, 32)
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if x > 800 or y>800:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
   main()
   # x=0
   # y=700
   # control(x,y)