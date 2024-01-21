# This file is for creating the Page object
# This object is the father class of all of the other pages

import pygame
from constants import *
from textboxClass import *
from importantFunctions import *
from socketFunctions import *
import pickle

GREY = (127, 127, 127)
EXITGAMESYS = "exit game (system)"
BACKPAGESYS = "back to last page (system)"
NEXTPAGESYS = "next page (system)"
CONFIRMSYS = "confirm button (system)"
STARTGAMESYS = "start game (system)"
RETURN_TO_LOBY_REQ = "return to loby request"
EXIT_ROOM_REQ = "exit room"     # wating room and basic settings page


class Page:
    def displayButtons(self, screen, is_back=False, is_next=False, is_start=False, is_confirm=False):
        if is_back:
            screen.blit(PygameConstans.BACK_IMG.value[IMG_INDEX], PygameConstans.BACK_IMG.value[RECT_INDEX])
        if is_next:
            screen.blit(PygameConstans.ENTER_IMG.value[IMG_INDEX], PygameConstans.ENTER_IMG.value[RECT_INDEX])
        if is_start:
            screen.blit(PygameConstans.START_GAME_IMG.value[IMG_INDEX], PygameConstans.START_GAME_IMG.value[RECT_INDEX])
        if is_confirm:
            screen.blit(PygameConstans.CONFIRM_BUTTON.value[IMG_INDEX], PygameConstans.CONFIRM_BUTTON.value[RECT_INDEX])

    def handleUser(self, event):
        if event.type == pygame.QUIT:
            return EXITGAMESYS
        if event.type == pygame.MOUSEBUTTONDOWN and PygameConstans.BACK_IMG.value[RECT_INDEX].collidepoint(event.pos) or \
                event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_LEFT):
            return BACKPAGESYS
        if event.type == pygame.MOUSEBUTTONDOWN and PygameConstans.ENTER_IMG.value[RECT_INDEX].collidepoint(event.pos) or \
                event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_RIGHT):
            return NEXTPAGESYS
        if event.type == pygame.MOUSEBUTTONDOWN and PygameConstans.START_GAME_IMG.value[RECT_INDEX].collidepoint(event.pos) or \
                event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return STARTGAMESYS
        if event.type == pygame.MOUSEBUTTONDOWN and PygameConstans.CONFIRM_BUTTON.value[RECT_INDEX].collidepoint(event.pos) or \
                event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return CONFIRMSYS
