import sys
from time import  sleep

import pygame as pg
import pygame.font

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import logging

# Configure logging
logging.basicConfig(
    filename="game_debug.log",
    filemode="w",  # "a" to append, "w" to overwrite each run
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print(pg.__version__)

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        pg.init()
        pg.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        # self.screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        pg.display.set_caption("Alien Invasion")
        self.clock = pg.time.Clock()
        self.stats = GameStats(self)
        self.sb =Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()

        self._create_fleet()

        self.game_active = False
        self.paused = True
        self.play_button = Button(self,"Play",200,50,(0,0,135)
                                  ,(255,255,255),self.screen_rect.centerx,self.screen_rect.centery)
        self.pause_button = Button(self,"Resume",200,50,(0,0,135)
                                  ,(255,255,255),self.screen_rect.centerx,self.screen_rect.centery)
        self.pause_music = False

    def run_game(self):
        logging.info("Starting game loop")

        while 1:
            try:
                logging.debug("Tick")
                self._check_events()

                if self.game_active and not self.paused:
                    logging.debug("Updating ship...")
                    self.ship.update()
                    self._update_bullets()
                    self._update_aliens()

                self._update_screen()
                logging.debug("Updating music")
                self._check_music()
                self.clock.tick(60)

            except Exception as e:
                logging.exception(f"Unhandled exception error occured as {e}")
                raise

    def _check_events(self):

        for event in pg.event.get():

            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_pause_button(mouse_pos)

    def _check_keydown_events(self,event):
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pg.K_q:
            sys.exit()
        elif event.key == pg.K_SPACE:
            self._fire_bullet()
        elif event.key == pg.K_p and not self.game_active:
            self.sb.prep_score()
            self._reset_game()
            self._play_background_music()
        elif event.key == pg.K_ESCAPE:
            self.paused = not self.paused
            self.pause_music = not self.pause_music
            self._change_mouse_visibility()

        elif event.key == pg.K_r:
            self._reset_game()
            self.game_active = False
            self._change_mouse_visibility()

    def _check_keyup_events(self,event):
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # print(self.paused)
        if(len(self.bullets)<self.settings.bullets_allowed):
            if not self.paused:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet) # type: ignore
                new_bullet.bullet_sound.play()


    def _create_alien(self,x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien) # type: ignore

    def _create_fleet(self):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size

        current_x,current_y = 2*alien_width,1.25*alien_height
        while current_y < (self.settings.screen_height - 3*alien_height):
            while current_x < (self.settings.screen_width - alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2*alien_width
            current_x = 2*alien_width
            current_y += 1.5*alien_height

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pg.sprite.spritecollideany(self.ship,self.aliens): # type: ignore
            self._ship_hit()

        self._check_aliens_at_bottom()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_alien_bullet_collisions()

    def _check_alien_bullet_collisions(self):
        # Check for any bullets that have hit aliens,we get a dict w/key as bullet,and val as alien
        # If so, get rid of bullet and alien
        collisions = pg.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            a1 = Alien(self)
            a1.alien_death_sound.play()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        self.ship_hit_msg = pygame.font.SysFont(None,90).render("SHIP HIT!!",
                                                                True,(255,255,0))
        self.ship_hit_msg_rect = self.ship_hit_msg.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.ship_hit_msg_rect.center = self.screen_rect.center
        self.screen.blit(self.ship_hit_msg,self.ship_hit_msg_rect)
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()
            pygame.display.flip()
            sleep(0.5)

        else:
            self.game_active = False
            pg.mixer.music.stop()
            self._change_mouse_visibility()

    def _check_aliens_at_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.y >= self.settings.screen_height:
                self._ship_hit()
                #put custom alien reached the bottom msg
                break

    def _check_play_button(self,mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._reset_game()
            self._play_background_music()

    def _check_pause_button(self,mouse_pos):
        button_clicked = self.pause_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game_active and self.paused:
            self.paused = not self.paused
            self._change_mouse_visibility()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()
            self.play_button.draw_border()

        if self.paused and self.game_active:
            self.pause_button.draw_button()
            self.pause_button.draw_border()

        pg.display.flip()

    def _reset_game(self):
        self.stats.reset_stats()
        self.game_active = True
        self.paused = False
        self.settings.initialise_dynamic_settings()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        self.bullets.empty()
        self.aliens.empty()

        self._create_fleet()
        self.ship.center_ship()

        pg.mouse.set_visible(False)

    def _change_mouse_visibility(self):
        if not pg.mouse.get_visible():
            pg.mouse.set_visible(True)
        else:
            pg.mouse.set_visible(False)

    def _play_background_music(self):
        try:
            pg.mixer.music.load("Sounds/Background/stranger-things-new.wav")
            pg.mixer.music.set_volume(self.settings.music_volume)
            pg.mixer.music.play(-1)
        except Exception as e:
            print(f"Music load/play error: {e}")

    def _check_music(self):
        logging.debug("Entered _check_music")

        try:
            logging.debug(f"Paused: {self.paused}, Music Playing: {pygame.mixer.music.get_busy()}")

            if self.paused and pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                logging.debug("Music paused.")
            elif not self.paused and not pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
                logging.debug("Music unpaused.")

        except Exception as e:
            logging.exception("Error in _check_music")
            raise

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()


