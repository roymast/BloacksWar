# this file is for displaying the sign up page
# in this page the user insert username and password in order to sign up

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


class SignUpPage(Page):
    """
    child class of Page.
    this class is for the user to insert his sign up data(real name, username, password and confirm password).
    """
    def __init__(self, screen, my_socket, user):
        super().__init__()
        self.screen = screen
        self.my_socket = my_socket
        self.user = user
        self.name = Textbox(100, 100, TEXTBOX_COLOR, 140, 30, "text", "RealName")
        self.name.set_picked(True)
        self.username = Textbox(100, 160, TEXTBOX_COLOR, 140, 30, "text", "UserName")
        self.password = Textbox(100, 220, TEXTBOX_COLOR, 140, 30, "password", "Password")
        self.confirm_password = Textbox(100, 280, TEXTBOX_COLOR, 140, 30, "password", "Confirm")
        self.show_password = PygameConstans.SHOW_PASSWORD_IMG.value
        self.show_password_rect = self.show_password.get_rect(topright=(self.password.get_x() + 165, self.password.get_y() + 3))
        self.got_approval = False
        self.error = None

    def goToPage(self):
        while self.got_approval is not None and not self.got_approval:
            self.handleUserInputs()
            self.displayPage()
        return self.got_approval is not None, self.username.get_text(), self.password.get_text_string()

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        self.screen.fill(GREY)
        printTextboxes([self.name, self.username, self.password, self.confirm_password], self.screen)
        self.displayButtons(self.screen, True, True)
        self.screen.blit(PygameConstans.SHOW_PASSWORD_IMG.value, self.show_password_rect)
        self.screen.fill(GREY, (30, 30, 190, 35))
        draw_text("Sign up page", self.screen, 30, 30, color=BLUE)
        if self.error is not None:
            if self.error[THREAD_INDEX].is_alive():
                draw_text(self.error[ERROR_INDEX], self.screen, 10, self.confirm_password.get_y() + 50, size=32, color=RED)
        pygame.display.update()

    def handleUserInputs(self):
        """
        func to handle the user inputs
        :return: None
        """
        for event in pygame.event.get():
            button_pressed = self.handleUser(event)
            if button_pressed == EXITGAMESYS:
                exitGame(self.screen, self.my_socket)
            if button_pressed == NEXTPAGESYS:
                self.try_sign_up()
            if button_pressed == BACKPAGESYS:
                self.got_approval = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_password_rect.collidepoint(event.pos):
                    self.password.showHidePassword()
                    self.confirm_password.showHidePassword()
                pickTextboxByMouse([self.name, self.username, self.password, self.confirm_password], event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    removeCharFromTextboxes([self.username, self.password, self.name, self.confirm_password])
                elif event.key == pygame.K_TAB:
                    pick_next([self.name, self.username, self.password, self.confirm_password])
                else:
                    add_char_to_textboxes([self.username, self.password, self.name, self.confirm_password], event, MAX_LENGTH)

    def try_sign_up(self):
        """
        func to check sign up inputs, send it to the server and check whether the server approve the request to sign up
        :return: bool
        """
        if self.check_user_sign_up():
            self.got_approval = self.send_sign_up()
            print(f"self.got_approval {self.got_approval}")
            if self.got_approval == True:
                self.user.setUserName(self.username.get_text_string())
                self.user.setPassword(self.password.get_text_string())
                self.user.set_all([self.name.get_text_string(), self.username.get_text_string(), 0, 0, ""])
            else:
                self.error = [self.got_approval[1:], threading.Thread(target=self.wait2seconds)]
                self.error[THREAD_INDEX].start()
                self.got_approval = False
        else:
            self.got_approval = False

    def check_user_sign_up(self):
        """
        func check if the password is ok
        :return: bool
        """
        MIN_LENGTH = 3
        GUEST_NAME = "guest"
        GUEST_NAME_FOUND = "please do not use \"guest\" in your name"
        ENGLISH_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        print("name: " + self.username.get_text() + " pass: " + self.password.get_text_string())
        error = ""
        if len(self.username.get_text()) < MIN_LENGTH or len(self.password.get_text()) < MIN_LENGTH:
            error = TOO_SHORT
        for char in self.username.get_text():
            if (not char.isdigit()) and (char not in ENGLISH_ALPHABET):
                error = BAD_INPUT
        for char in self.name.get_text():
            if (not char.isdigit()) and (char not in ENGLISH_ALPHABET):
                error = BAD_INPUT
        for char in self.password.get_text_string():
            if (not char.isdigit()) and (char not in ENGLISH_ALPHABET):
                error = BAD_INPUT
        if self.password.get_text_string() != self.confirm_password.get_text_string():
            error = BAD_CONFIRMED
        if GUEST_NAME in self.username.get_text_string().lower():
            error = GUEST_NAME_FOUND
        if error != "":
            self.error = [error, threading.Thread(target=self.wait2seconds)]
            self.error[THREAD_INDEX].start()
            return False
        return True

    def wait2seconds(self):
        time.sleep(2)

    def send_sign_up(self):
        """
        func send the signup properties and return whether the server accept the user or not
        :return: bool
        """
        password = hashlib.sha512(self.password.get_text_string().encode()).hexdigest()
        data = ["sign up request", self.name.get_text(), self.username.get_text(), password]
        data = pickle.dumps(data)
        try:
            send_data_socket_pickle(self.my_socket, data)
            print("sent sign up request")
        except:
            print(ConnectionError)
        data = pickle.loads(receive_data_pickle(self.my_socket, self.screen))
        print("logged in?: " + str(data))
        if data == SIGNED_UP:
            return True
        else:
            return data