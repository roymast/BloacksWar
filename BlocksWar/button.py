# this file is for text button object

import pygame
from constants import *
BLACK = (0, 0, 0)
GREY = (127, 127, 127)


class TextButton:
    def __init__(self, text, surface, position, border=0, size=40, color=BLACK, background=GREY, box_color=BLACK):
        """
        this class is button
        :param text:
        :param surface:
        :param position:
        :param border:
        :param size:
        :param color:
        :param background:
        :param box_color:
        """
        self.text = text
        self.surface = surface
        self.position = position
        self.border = border
        self.size = size
        self.color = color
        self.background = background

        self.font = pygame.font.Font(pygame.font.match_font(FONT), self.size)
        self.textobj = self.font.render(self.text, True, self.color)
        if type(self.position) == tuple:
            self.rect = self.textobj.get_rect(center=(self.position[0], self.position[1]))
        else:
            self.rect = self.position

        y_factor = 0.2
        x_factor = 0.1
        self.box = pygame.rect.Rect(self.rect.x - (self.rect.width * (2*x_factor)), self.rect.y - (self.rect.height * (2*y_factor)), self.rect.width + self.rect.width*2*x_factor, self.rect.height+self.rect.height*2*y_factor)
        # print(self.box)
        self.box_color = box_color

    def blitToScreen(self):
        self.surface.fill(self.background, self.box)
        self.surface.blit(self.textobj, self.rect)
        pygame.draw.rect(self.surface, self.box_color, self.box, self.border)
        # pygame.draw.rect(self.surface, self.box_color, self.rect, self.border)

    def getRect(self):
        return self.box