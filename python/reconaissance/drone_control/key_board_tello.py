import pygame

def init():
#initialize pygame library
    pygame.init()
#Set Control Display as 400x400 pixel
    windows = pygame.display.set_mode((400,400))

if __name__ == '__main__':
    init()
    while True:
        main()  