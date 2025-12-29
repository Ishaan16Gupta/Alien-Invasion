import pygame as pg
import pygame.font

class Button:

    def __init__(self,ai_game,msg,width,height,button_color,text_color,center_x,center_y):

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.width, self.height = width,height

        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None,48)

        self.rect = pg.Rect(0,0,self.width,self.height)
        self.rect.center = (center_x, center_y)

        self._prep_msg(msg)

    def _prep_msg(self,msg):

        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        #antialiasing makes the text edges smoother
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

    def draw_border(self, border_color=(255, 255, 255), border_thickness=3):
        pg.draw.rect(self.screen, border_color, self.rect, border_thickness)
