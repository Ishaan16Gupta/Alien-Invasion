class Settings:

    def __init__(self):
        #STATIC SETTINGS

        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (50,50,75)

        # Ship settings
        self.ship_limit = 3

        #Bullet settings
        self.bullet_width = 3
        self.bullet_height = 12
        self.bullet_color = (255,0,0)
        self.bullets_allowed = 3

        #Alien settings
        self.fleet_drop_speed = 10

        #Sound settings
        #float bw 0 and 1
        self.total_volume = 0.3
        self.alien_death_volume = 0.3 * self.total_volume
        self.fire_bullet_volume = 1 * self.total_volume
        self.music_volume = 3.0 * self.total_volume

        self.speedup_scale = 1.25
        self.score_scale = 1.5

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        self.ship_speed = 5.0
        self.bullet_speed = 5.0
        self.alien_speed = 1.5
        #fleet_direction of 1 is right -1 is left
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

