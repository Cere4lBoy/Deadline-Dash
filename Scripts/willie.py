import pygame

class MovingLine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((640, 10))  
        self.image.fill((255, 0, 0))  # Fill the surface with red color
        self.rect = self.image.get_rect()
        self.rect.x = 0  # Initial x position
        self.rect.y = 240  # Initial y position
        self.speed = 1  # Speed of the line

    def update(self):
        self.rect.x += self.speed  # Move the line to the right
        if self.rect.x > 240:
            self.rect.x = 0  # Reset the line to the left edge when it reaches the right edge

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
    
