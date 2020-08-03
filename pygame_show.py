import pygame
from pygame.locals import *
import os
import sys

import pygame


class Draw:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.init()
        pygame.display.set_caption('hello world')
        self.screen = pygame.display.set_mode([self.x, self.y])
        self.screen.fill([255, 255, 255])

    def drawText(self, text, posx, posy, textHeight=15, fontColor=(0, 0, 0), backgroudColor=(255, 255, 255)):
        ttf_abs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Fonts', 'Deng.ttf')
        fontObj = pygame.font.Font(ttf_abs, textHeight)  # 通过字体文件获得字体对象
        textSurfaceObj = fontObj.render(text, True, fontColor, backgroudColor)  # 配置要显示的文字
        textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
        textRectObj.center = (posx, posy)  # 设置显示对象的坐标
        self.screen.blit(textSurfaceObj, textRectObj)  # 绘制字

    def draw_info(self,x_1,y_1):
        color = 0, 0, 0
        width = 2
        # 画坐标系
        pygame.draw.line(self.screen, color, (0, 0), (self.x, 0), width)
        pygame.draw.line(self.screen, color, (0, 0), (0, self.y), width)
        pygame.draw.line(self.screen, color, (self.x, 0), (self.x - 10, 10), width)
        pygame.draw.line(self.screen, color, (0, self.y), (10, self.y - 10), width)
        x_list = []
        y_list = []
        self.drawText(str(0), 10, 10, textHeight=12)
        self.drawText(str(self.x), self.x - 10, 14, textHeight=12)
        self.drawText(str(self.y), 15, self.y - 10, textHeight=12)
        n = 5  # 轴分为n段
        for i in range(1, n):
            x_list.append(int(self.x / n * i))
            y_list.append(int(self.y / n * i))
        for x_item in x_list:
            pygame.draw.line(self.screen, color, (x_item, 0), (x_item, 10), width)
            self.drawText(str(x_item), x_item, 12, textHeight=15)
        for y_item in y_list:
            pygame.draw.line(self.screen, color, (0, y_item), (10, y_item), width)
            self.drawText(str(y_item), 16, y_item, textHeight=14)
        # 加载画图
        pic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Fonts', 'zzz.jpg')
        space = pygame.image.load(pic_path).convert_alpha()
        # 获取位图的宽和高
        width, height = space.get_size()
        # 对图片进行缩放
        space = pygame.transform.smoothscale(space, (width // 5, height // 5))
        # 对图片进行设置位置
        self.screen.blit(space, (x_1, y_1))
        # 画点（其实是画圆）
        pygame.draw.circle(self.screen, color, (300, 500), 1, 1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
            pygame.image.save(self.screen, "circle" + ".png")  # 这句话保存图片
            pygame.quit()
            break

    def run(self):
        self.draw_info()


if __name__ == '__main__':
    x = 1000
    y = 1000
    x_1=10
    y_1=10
    while 1:
        Draw(x, y).draw_info(x_1,y_1)
        x_1 += x_1
        y_1 += y_1
        if x_1 == 1000:
            x_1=0
            y_1=0