import pygame

pygame.init()

white = (255, 255, 255)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('Fonts/zzz.jpg')


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


x = display_width * 0.45
y = display_height * 0.8

crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        print(event)
    gameDisplay.fill(white)
    car(x, y)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
