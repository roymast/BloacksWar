# This file is for creating textbox

import pygame
from constants import *
BLACK = (0, 0, 0)
GREEN = (124, 252, 0)
size = 30


class Textbox:

    def __init__(self, x, y, background_color, width, height, kind_of_text, text_when_empty=""):
        self.x = x      # set x coordinate of textbox
        self.y = y      # set y coordinate of textbox
        # self.font = pygame.font.Font(None, 32)  # set font of text
        self.font = pygame.font.Font(pygame.font.match_font(FONT), size)
        self.input_box = pygame.Rect(x, y, width, height)     # create rect
        self.color_picked = pygame.Color(GREEN)        # set color of box
        self.color_not_picked = pygame.Color(BLACK)        # set color of box
        self.color = self.color_not_picked
        self.background_color = background_color        # set background color
        self.text = ""                                  # text that the user insert(set to "")
        self.text_surface = self.font.render(self.text, True, self.color)   # serface of textbox
        self.change = False         # var that say if user press on keyboard
        self.first = True
        self.input_box.w = width
        self.picked = False
        self.kind_of_text = kind_of_text
        self.text_when_empty = text_when_empty

    def get_x(self):
        """
        return the x coordinates of box
        """
        return self.x

    def get_y(self):
        """
        return the y coordinates of box
        """
        return self.y

    def get_background(self):
        """
        return the background color
        """
        return self.background_color

    def update(self, text):
        """
        update the text
        """
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)

    def get_rect(self):
        """
        return the rect
        """
        return self.input_box

    """def get(self):
        return self.text_surface"""

    def get_text(self):
        """
        return the text
        """
        if self.kind_of_text == 'text':
            return self.text
        else:
            returned_text = ""
            for _ in self.text:
                returned_text += '*'
            return returned_text

    def get_text_string(self):
        """
        return password
        """
        return self.text

    def add_char(self, char):
        """
        func get char and add it to text
        """
        self.text += char
        self.text_surface = self.font.render(self.text, True, self.color)

    def remove_char(self):
        """
        func remove char from the text
        """
        self.text = self.text[:-1]
        self.text_surface = self.font.render(self.text, True, self.color)

    def clear(self):
        """
        func put "" in text
        """
        self.text = ""
        self.text_surface = self.font.render(self.text, True, self.color)

    def is_empty(self):
        """
        func return true if the text is empty
        else return false
        """
        if self.text == "":
            return True
        return False

    def print_box(self, screen):
        """
        func get screen
        func print to screen the textbox
        """
        if self.kind_of_text == "text":
            # font = pygame.font.Font(r"fonts\secret_word_2.ttf", 30)
            # Blit the text.
            screen.blit(self.text_surface, (self.input_box.x+5, self.input_box.y+5))
        else:
            shown_text = ""
            for _ in self.text:
                shown_text += '*'
            shown_text_surface = self.font.render(shown_text, True, self.color)
            screen.blit(shown_text_surface, (self.input_box.x + 5, self.input_box.y + 7))
        if self.is_empty():
            empty_font = pygame.font.Font(pygame.font.match_font(FONT), size)
            # empty_font = pygame.font.SysFont('Times New Roman', 25)
            empty_text = empty_font.render(self.text_when_empty, True, (51, 77, 77))
            # empty_text.set_alpha(2)
            screen.blit(empty_text, (self.input_box.x+5, self.input_box.y+5))
        # Blit the input_box rect.
        # pygame.display.flip()
        if self.is_picked():
            pygame.draw.rect(screen, self.color_picked, self.input_box, 2)
        else:
            pygame.draw.rect(screen, self.color_not_picked, self.input_box, 2)
        # pygame.display.flip()

    def is_picked(self):
        return self.picked

    def set_picked(self, picked):
        self.picked = picked

    def get_kind(self):
        return self.kind_of_text

    def set_kind(self, kind_of_text):
        if kind_of_text == "text" or kind_of_text == "password":
            self.kind_of_text = kind_of_text

    def showHidePassword(self):
        if self.kind_of_text == "password":
            self.kind_of_text = "text"
        else:
            self.kind_of_text = "password"


def is_textboxes_empty(textboxes):
    """
    func to check whether all of the textboxes are not empty
    :param textboxes: list of the textboxses
    :return: bool
    """
    for textbox in textboxes:
        if textbox.get_text_string() == "":
            return True
    return False


def pickTextboxByMouse(textboxes, event):
    """
    func to pick textbox by the position of the mouse
    :param textboxes: list of the textboxes
    :param event: pygame event
    :return: None
    """
    for textbox in textboxes:
        if textbox.get_rect().collidepoint(event.pos):
            for other_textboxes in textboxes:
                other_textboxes.set_picked(False)
            textbox.set_picked(True)


def removeCharFromTextboxes(textboxes, auto_remove=False):
    """
    func to remove char from the textbox
    :param auto_remove: bolean variable- if true: when current textbox is empty, start remove from previous textbox
    :param textboxes: list of the textboxes
    :return: None
    """
    for index, textbox in enumerate(textboxes):
        # if the specific textbox is picked
        if textbox.is_picked():
            if not textbox.is_empty():
                textbox.remove_char()
            elif auto_remove:
                if index != 0:
                    textbox.set_picked(False)
                    textboxes[index - 1].set_picked(True)


def add_char_to_textboxes(textboxes, event, max_length, auto_continue=False):
    """
    func to add char to the specific textbox
    :param auto_continue: bolean variable- if true: when current textbox get fill, start fill the next one
    :param max_length: the length that can be inserted
    :param event: what key the user pressed
    :param textboxes: list of textboxes
    :return: None
    """
    for index, textbox in enumerate(textboxes):
        # if the specific textbox is picked
        if textbox.is_picked():
            # if the specific textbox is full
            if len(textbox.get_text_string()) == max_length:
                if auto_continue:
                    # if it is not the last textbox
                    if index != len(textboxes) - 1:
                        textbox.set_picked(False)
                        textboxes[index + 1].set_picked(True)
                        continue
                    else:
                        break
            else:
                textbox.add_char(event.unicode)


def pick_next(textboxes):
    """
    func to switch between the current textbox to the next one
    :param textboxes: list of the textboxes
    :return: None
    """
    for index, textbox in enumerate(textboxes):
        if textbox.is_picked():
            textbox.set_picked(False)
            if index == len(textboxes) - 1:
                textboxes[0].set_picked(True)
                break
            else:
                textboxes[index + 1].set_picked(True)
                break


def printTextboxes(textboxes, screen):
    for textbox in textboxes:
        screen.fill(textbox.get_background(), textbox.get_rect())
        textbox.print_box(screen)
