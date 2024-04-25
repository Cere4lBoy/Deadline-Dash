import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Fist')
        self.screen = pygame.display.set_mode((1366, 768))
       
        self.clock = pygame.time.Clock()

        self.img = pygame.image.load('Graphics\MAIN MENU\PREVIEW.png')

    def run(self):
        while True:
             self.screen.blit(self.img, (1366, 768))
             for event in pygame.event.get():
               if event.type ==pygame.QUIT:
                    pygame.quit
                    sys.exit()


             pygame.display.update()
             self.clock.tick(144)
Game().run()
