# This file is to handle the users connection(login/sign up/ guest)

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
from pages.ConnectionWay import *
from pages.LoginPage import *
from pages.SignUpPage import *


GUEST_OK = "!guest ok"
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
THREAD_INDEX = 1
ERROR_INDEX = 0


def guest(screen, my_socket, user):
    """
    func send to server that the user want to connect as guest, and wait for response
    :param user: user object
    :param screen: the screen
    :param my_socket: the socket to communicate with server
    :return: bool
    """
    send_data_socket_pickle(my_socket, pickle.dumps("guest request"))
    data = pickle.loads(receive_data_pickle(my_socket, screen))
    if data == GUEST_OK:
        user.setUserName(pickle.loads(receive_data_pickle(my_socket, screen)))
        return True
    return False


def connection_way(screen, my_socket, user):
    """
    func to connect to the server in the way the user wants(login, signup or guest)
    :param user: user object
    :param screen: the screen
    :param my_socket: the socket
    :return: None
    """
    is_logedin = False
    is_signedup = False
    is_guest = False
    while (not is_logedin) and (not is_signedup) and (not is_guest):
        connection_way_picked = ConnectionWayPage(screen, my_socket, user).goToPage()
        if connection_way_picked == "login":
            print("before login")
            is_logedin, username, password = LoginPage(screen, my_socket, user).gotToPage()
            print("after login")
        elif connection_way_picked == "sign up":
            is_signedup, username, password = SignUpPage(screen, my_socket, user).goToPage()
        else:
            is_guest = guest(screen, my_socket, user)
        print("done")
    return user
