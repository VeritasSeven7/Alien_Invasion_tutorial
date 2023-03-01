import sys
import pygame

from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
# noinspection PyTypeChecker


class AlienInvasion:
    """"Overall class to manage game assets and behavior"""

    def __init__(self):
        # Initialize and create resources
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self._create_fleet()

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.game_active = False

        self.play_button = Button(self, "PLAY")

        self.ship = Ship(self)
        self.bg_color = (230, 230, 230)

    def run_game(self):
        # main loop for the game
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # Watching for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # check mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            # check key down and up events
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Moving the player ship
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

        # close game if esc is pressed
        if event.key == pygame.K_ESCAPE:
            self._save_hs()
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        # start the game when the player clicks play
        button_click = self.play_button.rect.collidepoint(mouse_pos)
        if button_click and not self.game_active:
            self.settings.initialize_dynamics()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            pygame.mouse.set_visible(False)

            # empty the screen and start a new fleet and player
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        # redraw each time through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # draw the scoreboard
        self.sb.show_score()

        # draw the button if the game is not active
        if not self.game_active:
            self.play_button.draw_button()

        # Display the latest drawn screen
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()

        self._bullet_collisions()

        # getting rid of off-screen bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _bullet_collisions(self):
        # check for bullet collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # score hits
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # clear bullets and send a new fleet at player
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_difficulty()

            # increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        # make an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # create and alien and keep adding until there is no room
        # spacing is one alien width and height
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3*alien_height):
            while current_x < (self.settings.screen_width - 2*alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

                # reset x and increment y when done with row
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        # create an alien and place it in a row
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # look for player collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # check for aliens reaching the bottom
        self._aliens_bottom()

    def _check_fleet_edges(self):
        # respond to the fleet reaching an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # drop the fleet and change direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # decrement ships left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # clear the screen
            self.aliens.empty()
            self.bullets.empty()

            # new ship and fleet
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self._save_hs()
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _aliens_bottom(self):
        # Check if any aliens make it to the bottom of the screen
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _save_hs(self):
        # save high score to file
        if self.stats.high_score > self.stats.loaded_score:
            self.stats.score_path.write_text(str(self.stats.high_score).rstrip())


if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
