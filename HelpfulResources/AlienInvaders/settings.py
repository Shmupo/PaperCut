class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        
        self.lasers_every = 50
        #smaller is faster
        self.alien_fire_rate = 90

        self.alien_points = 50
        self.big_alien_points = 500

        self.ship_limit = 3         # total ships allowed in game before game over
        self.barrier_hp = 5

        self.fleet_drop_speed = 3
        self.fleet_direction = 1     # change to a Vector(1, 0) move to the right, and ...
        self.initialize_speed_settings()

    def initialize_speed_settings(self):
        self.alien_speed_factor = .5
        self.ship_speed_factor = 1
        self.laser_speed_factor = 1

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.laser_speed_factor *= scale
