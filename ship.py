import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    # class for managing the ship
    def __init__(self, ai_game):
        # initialize ship and set starting position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # load ship and get rect
        self.image = pygame.image.load('assets/ship.bmp')
        self.rect = self.image.get_rect()

        # start the ship at bottom center
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for horizontal position
        self.x = float(self.rect.x)

        # set movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # update ship location and check for edge of screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update rect from object
        self.rect.x = self.x

    def blitme(self):
        # draw the ship at its current location
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
