import sys
import pygame
from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from button import Button  # Import the Button class from button.py

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Deadline Dash')
        self.screen = pygame.display.set_mode((1366, 768))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        
        # Load menu assets
        self.load_menu_assets()

        self.player = PhysicsEntity(self, 'player', (50, 50), (15, 17))
        self.tilemap = Tilemap(self, tile_size=16)


        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png')
        }

        
    def load_menu_assets(self):
        # Load button images
        start_img = pygame.image.load('data/images/menubuttons/START.png').convert_alpha()
        exit_img = pygame.image.load('data/images/menubuttons/EXIT.png').convert_alpha()

        # Background Image
        self.background_img = pygame.image.load('data/images/MENUBG.png').convert()

        
        # Button objects
        self.start_button = Button(550, 450, start_img, 0.7)
        self.exit_button = Button(700, 650, exit_img, 0.5)

    def draw_menu(self):
        # Blit background image
        self.screen.blit(self.background_img, (0, 0))


        # Draw buttons and handle actions
        if self.start_button.draw(self.screen):
            self.start_game()
        if self.exit_button.draw(self.screen):
            pygame.quit()  # Quit the game

        pygame.display.update()

    def start_game(self):
        self.menu_running = False

    def run_menu(self):
        self.menu_running = True
        while self.menu_running:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

    def run(self):
        self.run_menu()  # Run the menu
        while True:
            self.display.fill((14, 219, 248))
            
            self.tilemap.render(self.display)
            
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()
