import sys
import pygame
from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from button import Button
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Deadline Dash')
        self.screen = pygame.display.set_mode((1366, 768))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        
        # Load menu assets and capture returned values
        logo_img, logo_width = self.load_menu_assets()

        self.player = PhysicsEntity(self, 'player', (50, 50), (15, 17))
        self.tilemap = Tilemap(self, tile_size=16)
        # Storing logo_img and logo_width for later use
        self.logo_img = logo_img
        self.logo_width = logo_width


        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
        }
        # Camera     
        self.scroll = [0,0]

        # clouds
        self.clouds = Clouds(self.assets['clouds'], count=16)


        
    def load_menu_assets(self):
        # B.L.O.A.T (Best Logo Of All Time)
        logo_img = pygame.image.load('data/images/DEADLINEDASHLOGO.png').convert_alpha()
        logo_width = int(logo_img.get_width() * 1.0)  # Scale logo width to 50%
        logo_height = int(logo_img.get_height() * 1.0)  # Scale logo height to 50%
        logo_img = pygame.transform.scale(logo_img, (logo_width, logo_height))


        # Load button images
        start_img = pygame.image.load('data/images/menubuttons/START.png').convert_alpha()
        exit_img = pygame.image.load('data/images/menubuttons/EXIT.png').convert_alpha()
        leaderb_img = pygame.image.load('data/images/menubuttons/LEADERBOARD.png').convert_alpha()
        credits_img = pygame.image.load('data/images/menubuttons/CREDITS.png').convert_alpha()
        

        # Background Image
        self.background_img = pygame.image.load('data/images/MENUBG.png').convert()

        
        # Button objects
        self.start_button = Button(550, 450, start_img, 0.7)
        self.exit_button = Button(700, 650, exit_img, 0.5)
        self.leaderb_button = Button(550, 550, leaderb_img, 0.7)
        self.credits_button = Button(470, 650, credits_img, 0.5)

        return logo_img, logo_width

    def draw_menu(self):
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.logo_img, ((self.screen.get_width() - self.logo_width) // 2, 50))  # Adjust Y position as needed

        # Draw buttons and handle actions
        if self.start_button.draw(self.screen):
            self.start_game()
        if self.exit_button.draw(self.screen):
            pygame.quit()  # Quit the game
        if self.leaderb_button.draw(self.screen):
            pygame.quit()
        if self.credits_button.draw(self.screen):
            pygame.quit()

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
            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # Clouds Rendering
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            # Camera
            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            
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
