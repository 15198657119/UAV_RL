import pygame
from pygame.locals import *

'''
    4. 使用面向对象的方式显示飞机，以及控制其左右移动

    接下来要做的任务：
    1. 实现飞机在你想要的位置显示
    2. 实现按键控制飞机移动
'''


class HeroPlane(object):
    def __init__(self, screen):
        # 设置飞机默认的位置
        self.x = 150
        self.y = 480
        # 设置要显示内容的窗口
        self.screen = screen
        # 用来保存英雄飞机需要的图片名字
        self.imageName = "Fonts/final.png"
        # 根据名字生成飞机图片
        self.image = pygame.image.load(self.imageName).convert()

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def moveLeft(self):
        self.x -= 10

    def moveRight(self):
        self.x += 10

    def moveUp(self):
        self.y -= 10

    def moveDown(self):
        self.y += 10


def key_control(heroPlane):
    # 判断是否是点击了退出按钮
    for event in pygame.event.get():
        # print(event.type)
        if event.type == QUIT:
            print("exit")
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                print('left')
                heroPlane.moveLeft()
                # 控制飞机让其向左移动
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                heroPlane.moveRight()
            elif event.key == K_w or event.key == K_UP:
                print('up')
                # 控制飞机让其向上移动
                heroPlane.moveUp()
            elif event.key == K_s or event.key == K_DOWN:
                print('down')
                # 控制飞机让其向下移动
                heroPlane.moveDown()
            elif event.key == K_SPACE:
                print('space')


def main():
    # 1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((1000, 1000), 0, 32)

    # 2. 创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("Fonts/start.png").convert()

    # 3. 创建一个飞机对象
    heroPlane = HeroPlane(screen)

    # 3. 把背景图片放到窗口中显示
    while True:
        screen.blit(background, (0, 0))

        heroPlane.display()

        key_control(heroPlane)

        pygame.display.update()


if __name__ == "__main__":
    main()