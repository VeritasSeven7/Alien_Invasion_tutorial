class Settings:
    # class for all settings for Alien Invasion
    def __init__(self):
        """ static settings """
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)

        # alien settings
        self.fleet_drop_speed = 10

        # difficulty scaling values
        self.speedup_scale = 1.2
        self.score_scale = 1.5
        """ dynamic settings """
        self.initialize_dynamics()

    def initialize_dynamics(self):
        # settings that change throughout a play-through
        self.ship_speed = 3.5
        self.alien_speed = 1.0
        self.bullet_speed = 10.0

        # fleet direction, 1 is right -1 is left
        self.fleet_direction = 1

        # scoring
        self.alien_points = 50

    def increase_difficulty(self):
        # difficulty increase
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

        # score value increase with difficulty
        self.alien_points = int(self.alien_points * self.score_scale)
