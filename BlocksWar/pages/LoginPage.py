# This file is to display login page
# The login page let the user login to his account

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

THREAD_INDEX = 1
ERROR_INDEX = 0


class LoginPage(Page):
    """
    child class of Page.
    this class is for the user to insert his username and password.
    """
    def __init__(self, screen, my_socket, user):
        super().__init__()
        self.screen = screen
        self.my_socket = my_socket
        self.username = Textbox(100, 100, TEXTBOX_COLOR, 140, 30, "text", "UserName")
        self.username.set_picked(True)
        self.password = Textbox(100, 180, TEXTBOX_COLOR, 140, 30, "password", "Password")
        font = pygame.font.SysFont('Times New Roman', 25)
        self.show_password = PygameConstans.SHOW_PASSWORD_IMG.value
        self.show_password_rect = self.show_password.get_rect(
            topright=(self.password.get_x() + 165, self.password.get_y() + 3))
        self.got_approval = False
        self.user = user
        self.error = None

    def gotToPage(self):
        self.screen.fill(self.username.get_background())
        username_text = ""
        password_text = ""
        while self.got_approval is not None and not self.got_approval:
            self.handleUserInputs()
            self.displayPage()
        if self.got_approval:
            return True, username_text, password_text
        return False, "", ""

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        self.screen.fill(GREY)
        self.username.print_box(self.screen)
        self.password.print_box(self.screen)
        draw_text("Login page", self.screen, 30, 30, 40, BLUE)
        self.screen.blit(PygameConstans.SHOW_PASSWORD_IMG.value, self.show_password_rect)
        self.displayButtons(self.screen, True, True)
        print(self.error)
        if self.error is not None:
            if self.error[THREAD_INDEX].is_alive():
                draw_text(self.error[ERROR_INDEX], self.screen, 10, 290, size=30, color=RED)
            else:
                self.error = None
        PygameConstans.CLOCK.value.tick(20)
        pygame.display.update()

    def handleUserInputs(self):
        """
        func to handle the user inputs
        :return: None
        """
        for event in pygame.event.get():
            button_pressed = self.handleUser(event)
            # pressed on X
            if button_pressed == EXITGAMESYS:
                exitGame(self.screen, self.my_socket)
            if button_pressed == BACKPAGESYS:
                self.got_approval = None
            if button_pressed == NEXTPAGESYS:
                self.try_login()
            # mouse pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_password_rect.collidepoint(event.pos):
                    self.password.showHidePassword()
                    self.screen.fill(self.password.get_background(), self.password.get_rect())
                pickTextboxByMouse([self.username, self.password], event)
            # keyboard press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    removeCharFromTextboxes([self.username, self.password])
                elif event.key == pygame.K_TAB:
                    pick_next([self.username, self.password])
                else:
                    add_char_to_textboxes([self.username, self.password], event, 7)

    def try_login(self):
        """
        func check the input of the login, send it to the server and check whether he loged in
        :return: bool
        """
        if self.check_user_login():
            self.got_approval = self.send_login()
            if not self.got_approval:
                NOT_LOGGED_IN = "user name or password incorrect"
                self.error = [NOT_LOGGED_IN, threading.Thread(target=self.waitXSeconds, args=[2])]
                self.error[THREAD_INDEX].start()
            else:
                self.user.setUserName(self.username)
                self.user.setPassword(self.password)
                data = receive_data_pickle(self.my_socket, self.screen)
                try:
                    data = pickle.loads(data)
                    self.user.set_all(data)
                except:
                    disconnected_from_server(self.screen)
        else:
            self.got_approval = False

    def waitXSeconds(self, sec):
        """
        func to wait some time
        :param sec: time to wait
        :return: None
        """
        time.sleep(sec)

    def check_user_login(self):
        """
        func check if the password is ok
        :return: bool
        """
        error = ""
        if len(self.username.get_text_string()) < 3 or len(self.password.get_text_string()) < 3:
            error = TOO_SHORT
        for char in self.username.get_text_string():
            if (not char.isdigit()) and (not char.isalpha()):
                error = BAD_INPUT
        for char in self.password.get_text_string():
            if not char.isdigit() and not char.isalpha():
                error = BAD_INPUT
        if error != "":
            self.error = [error, threading.Thread(target=self.waitXSeconds, args=[2])]
            self.error[THREAD_INDEX].start()
            return False
        return True

    def send_login(self):
        """
        func send login information to server and return true/false if the server approved the user
        :return: bool
        """
        password = hashlib.sha512(self.password.get_text_string().encode()).hexdigest()
        data = ["login request", self.username.get_text_string(), password]
        print("before sending info")
        send_data_socket_pickle(self.my_socket, pickle.dumps(data))
        print("before reciving")
        data = receive_data_pickle(self.my_socket, self.screen)
        try:
            data = pickle.loads(data)
            print(f"after rciving {data}")
        except:
            disconnected_from_server(self.screen)
        if data == LOGIN_OK:
            return True
        else:
            return False