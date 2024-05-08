import sys
import pygame
from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from button import Button  # Import the Button class

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Deadline Dash')
        self.screen = pygame.display.set_mode((1366, 768))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png')
        }
        self.player = PhysicsEntity(self, 'player', (50, 50), (15, 17))
        self.tilemap = Tilemap(self, tile_size=16)

        # Load button images
        start_img = pygame.image.load('data/images/menubuttons/START.png').convert_alpha()
        leaderboard_img = pygame.image.load('data/images/menubuttons/LEADERBOARD.png').convert_alpha()
        credit_img = pygame.image.load('data/images/menubuttons/CREDITS.png').convert_alpha()
        exit_img = pygame.image.load('data/images/menubuttons/EXIT.png').convert_alpha()

        # Button objects
        self.start_button = Button(0, 0, start_img, 0.3)
        self.leaderboard_button = Button(15, 0, leaderboard_img, 0.7)
        self.credit_button = Button(470, 650, credit_img, 0.5)
        self.exit_button = Button(15, 15, exit_img, 0.5)

    def run(self):
        self.run_menu()

    def run_menu(self):
        while True:
            self.display.fill((14, 219, 248))

            # Draw buttons and handle actions
            if self.start_button.draw(self.display):
                self.show_menu = False  # Exit the menu loop and start the game
                break
            if self.exit_button.draw(self.display):
                pygame.quit()  # Quit the game
                sys.exit()
            # Add actions for leaderboard and credit buttons here if needed

            # Blit the display surface onto the screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            # Update the display
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
