import pygame
from button import Button  # Import the Button class from button.py
from Game import Game  # Import the Game class from game.py

# Display window
SCREEN_HEIGHT = 768
SCREEN_WIDTH = 1366

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Deadline Dash')

# Load background image
background_img = pygame.image.load('Graphics/MAIN_MENU/main_menu_bg.png').convert()

# Load button images
start_img = pygame.image.load('Graphics/MAIN_MENU/start_btn.png').convert_alpha()
leaderboard_img = pygame.image.load('Graphics/MAIN_MENU/leaderboard.png').convert_alpha()
credit_img = pygame.image.load('Graphics/MAIN_MENU/credit.png').convert_alpha()
exit_img = pygame.image.load('Graphics/MAIN_MENU/exit_btn.png').convert_alpha()

# Load game logo and scale it
logo_img = pygame.image.load('Graphics/MAIN_MENU/DEADLINEDASHLOGO.png').convert_alpha()
logo_width = int(logo_img.get_width() * 1.0)  # Scale logo width to 50%
logo_height = int(logo_img.get_height() * 1.0)  # Scale logo height to 50%
logo_img = pygame.transform.scale(logo_img, (logo_width, logo_height))

# Button objects
start_button = Button(550, 450, start_img, 0.7)
leaderboard_button = Button(550, 550, leaderboard_img, 0.7)
credit_button = Button(470, 650, credit_img, 0.5)
exit_button = Button(700, 650, exit_img, 0.5)

# Game loop
run_menu = True
while run_menu:
    # Blit background image
    screen.blit(background_img, (0, 0))

    # Blit game logo closer to the top
    logo_x = (SCREEN_WIDTH - logo_width) // 2  # Center horizontally
    logo_y = 50  # Move 50 pixels from the top
    screen.blit(logo_img, (logo_x, logo_y))

    # Draw buttons and handle actions
    if start_button.draw(screen):
        run_menu = False  # Exit the menu loop and start the game
    if exit_button.draw(screen):
        pygame.quit()  # Quit the game
    # You can add actions for leaderboard and credit buttons here if needed

    # Event handler
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            run_menu = False  # Exit the menu loop if the user quits

    pygame.display.update()

# If the menu loop exits, start the game
if not run_menu:
    game = Game()  # Create an instance of the game
    game.run()  # Run the game loop
