import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    # class for player fired bullets

    def __init__(self, ai_game):
        # create a bullet at player position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # create the rect and position at ship nose
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # store y value as a float for speed adjustment
        self.y = float(self.rect.y)

    def update(self):
        # Update bullet position
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
