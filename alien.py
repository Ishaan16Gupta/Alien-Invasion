import pygame as pg
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self,ai_game):
        super().__init__()
        pg.mixer.init()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pg.image.load("images/alien_resized.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

        self.alien_death_sound = pg.mixer.Sound("Sounds/explosion.wav")
        self.alien_death_sound.set_volume(self.settings.alien_death_volume)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return(self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        self.x += self.settings.alien_speed*self.settings.fleet_direction
        self.rect.x = self.x

