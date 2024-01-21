import socket
import select
import pygame
import sys
import pickle
from Player import *
import time
import random
import threading
from textboxClass import *
import hashlib
from constants import PygameConstans
import traceback
from pages.Page import *
from socketFunctions import *


class ConnectionWayPage(Page):
    """
    child class of Page.
    this class is for the user to pick which way he want to connect(login, sign up or guest)
    """
    def __init__(self, screen, my_socket, user):
        super().__init__()
        self.screen = screen        # the screen
        self.my_socket = my_socket  # the socket
        self.user = user            # user object
        self.connection_way_picked = ""     # the way of connection the user picked

    def goToPage(self):
        self.screen.fill(GREY)
        pygame.display.update()
        while self.connection_way_picked == "":
            self.handleUserInputs()
            self.displayPage()
        return self.connection_way_picked

    def handleUserInputs(self):
        """
        func to handle the user inputs
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame(self.screen, self.my_socket)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if PygameConstans.SIGNEDUP_IMG.value[RECT_INDEX].collidepoint(mouse_pos):
                    self.connection_way_picked = "sign up"
                elif PygameConstans.LOGIN_IMG.value[RECT_INDEX].collidepoint(mouse_pos):
                    self.connection_way_picked = "login"
                elif PygameConstans.GUEST_IMG.value[RECT_INDEX].collidepoint(mouse_pos):
                    self.connection_way_picked = "guest"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.connection_way_picked = "sign_up"

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        self.screen.blit(PygameConstans.LOGIN_IMG.value[IMG_INDEX], PygameConstans.LOGIN_IMG.value[RECT_INDEX])
        self.screen.blit(PygameConstans.SIGNEDUP_IMG.value[IMG_INDEX], PygameConstans.SIGNEDUP_IMG.value[RECT_INDEX])
        self.screen.blit(PygameConstans.GUEST_IMG.value[IMG_INDEX], PygameConstans.GUEST_IMG.value[RECT_INDEX])
        pygame.draw.rect(self.screen, BLACK, PygameConstans.LOGIN_IMG.value[RECT_INDEX], 3)
        pygame.draw.rect(self.screen, BLACK, PygameConstans.SIGNEDUP_IMG.value[RECT_INDEX], 3)
        pygame.draw.rect(self.screen, BLACK, PygameConstans.GUEST_IMG.value[RECT_INDEX], 3)
        pygame.display.update()