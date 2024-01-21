# This file is for sending data to the server is specific format

import socket
import select
import pygame
import sys
import pickle
from Player import Player
import time
import random
import threading
from textboxClass import Textbox
import hashlib
import traceback
from constants import *

PATH = r"pics/"
PORT = 31987
SPLIT_CHAR = "+"
NEW_CONNECTION_MSG = "hi"
GAME_STARTED_MSG = "game starting"
START_GAME_ORDER = "!start the game"
GAME_OVER_MSG = "game over"
WINDOW_WIDTH = 728
WINDOW_HEIGHT = 409
BACKGROUND_PATH = r"pics/background.png"
GAME_ENDED = "!game over"
LOGIN_OK = "!logged in"
SIGNED_UP = "!sign up ok"
GUEST_OK = "!guest ok"
COLORS_REQUEST = "colors request"
TOO_SHORT = "the name or password is too short, please use at least 3 characters"
BAD_CONFIRMED = "your password and confirmed password are different"
BAD_INPUT = "please use only english characters and numbers"
PICK_COLOR = """pick color:\nblue(recommended)\nred\ngreen\npink\nbrown\nblack\nyellow"""
COLOR_LIST = ["red", 'blue', "green", "pink", "brown", "black", "yellow"]
FONT = "bowlbyonesc"
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
RED = (255, 0, 0)
LIME = (99, 245, 91)
BLUE = (0, 0, 128)
GREEN = (0, 255, 0)
TEXTBOX_COLOR = GREY
LIGHT_BLUE = (204, 255, 255)
messages_count = 0
MAX_LENGTH = 7


def new_data(my_socket, screen):
    """
    func check if there is new data from the server
    :param screen: the screen
    :param my_socket: the socket to connect to the server
    :return: the new data from the server(if there is)
    """
    rlist, wlist, xlist = select.select([my_socket], [], [], 0)
    if rlist:
        data = receive_data_pickle(my_socket, screen)
        try:
            data = pickle.loads(data)
        except Exception as e:
            traceback.print_exc()
            disconnected_from_server(screen)
        if data:
            if data == GAME_ENDED:
                return GAME_ENDED
            elif not len(data) == 0:
                return data
            elif data is None:
                print("got Nonetype")
    return None


def send_data_on_player(my_socket, player):
    """
    func send properties of the player to the server
    :param my_socket: the socket to communicate the the server
    :param player: the player
    :return: None
    """
    data = [player.is_dead(), player.get_x(), player.get_y(), player.get_direction(), player.get_kind_of_pic(),
            player.get_hitted()]
    data = pickle.dumps(data)
    try:
        my_socket.send(("{}+".format(str(len(data)))).encode('utf-8') + data)
    except Exception as e:
        print(e)


def receive_data_pickle(c_socket, screen):
    """
    receiving data in "pickle format" from client with my protocol(sending the length of the message+SPLIT_CHAR+the message)
    c_socket: the socket of the player
    """
    leng = " "
    while not str(leng[-1]) == SPLIT_CHAR:
        try:
            leng += c_socket.recv(1).decode('utf-8')
        except Exception as e:
            traceback.print_exc()
            disconnected_from_server(screen)
            break
    if leng[1:-1].isdigit():
        data = c_socket.recv(int(leng[:-1]))
        return data


def receive_data2(s_socket):
    """
    func recieve messages that in pickle format
    :param s_socket: the socket that talk to the socket
    :return: string
    """
    leng = ""
    while SPLIT_CHAR not in leng:
        try:
            leng += s_socket.recv(1).decode('utf-8')
        except Exception as e:
            traceback.print_exc()
            break
    try:
        return s_socket.recv(int(leng[:-1]))
    except Exception as e:
        traceback.print_exc()


def send_data_socket_pickle(sockett, data):
    try:
        sockett.send((str(len(data))+SPLIT_CHAR).encode('utf-8') + data)
    except Exception as e:
        traceback.print_exc()
