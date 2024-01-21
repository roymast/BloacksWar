# This file is the file that responsible to run the project
# This file is the file that the user need to run
# Please make sure you installed all of the needed libraries and have all of the files

from button import *
from GameClass import *
from Player import *
from pages.GamePages import *
from pages.loginSignup import *
from database import *
from socketFunctions import *

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
NOPREVIOUSMATCHES = "oops, it's looks like you don't have previous matches"
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
ROOM_NUMBER_LENGTH = 4
ROOM_NUMBER_TOO_SHORT = f"the room number should be {ROOM_NUMBER_LENGTH} characters"
JOINING_COMPLETE = "joining room completed"


def main():
    screen = init_screen()  # init screen
    FirstPage(screen).goToPage()  # display first page
    my_socket = connect(screen)  # socket object to communicate the server
    user = User()  # user object
    user = connection_way(screen, my_socket, user)  # connect
    mode_object = Mode(None, None)  # mode object
    while True:
        HandleSinglePlayerAndMultiPlayer(screen, my_socket, user, mode_object)
        basic_user_setting = BasicSettings(
            BasicSettingsPage(screen, mode_object.is_single_player, user, my_socket).goToPage())
        if not basic_user_setting.is_none:  # if didn't got out of the page
            players = Game(mode_object, screen, my_socket).run_game(basic_user_setting)  # run the game
            if players is not None:  # if the user didn't wanted to get out of the game
                GameOverPage(screen, my_socket, players).goToPage()


def HandleSinglePlayerAndMultiPlayer(screen, my_socket, user, mode_object):
    """
    this function let the player choose whether he want to play single player or multi player.
    it also let the user pick room, and pick to play with bot or not
    :param screen: the screen
    :param my_socket: the socket to comunicate with the server
    :param user: the user
    :param mode_object: object that saves the mode
    :return: None
    """
    got_approved = False
    while not got_approved:
        # picking single or multi player
        mode_object.is_single_player = SingleOrMultiPlayerPage(screen, my_socket, user).goToPage()
        if mode_object.is_single_player:
            send_data_socket_pickle(my_socket, pickle.dumps(clientReq.SINGLE_PLAYER.value))
            mode_object.is_ai = PickBotPage(screen, my_socket).goToPage()  # pick bot or not
            if mode_object.is_ai != None:
                got_approved = True
        else:
            send_data_socket_pickle(my_socket, pickle.dumps(clientReq.MULTI_PLAYER.value))
            got_approved = roomHandler(screen, my_socket)


def roomHandler(screen, my_socket):
    """
    func to hanlde the rooms.
    it let the user to pick whether he want to join room, or to create room.
    than, if there are too many room or the user change his mind, he can pick again
    :param screen:the screen
    :param my_socket: the socket to communicate the server
    :return: bool
    """
    players_names, room_number, server_ip = None, None, None
    TOO_MANY_ROOMS = "there are too many rooms right now, try again later"
    ROOM_NUMBER_INDEX = 1
    PLAYERS_NAMES_INDEX = 2
    SERVER_IP_INDEX = 3
    while type(players_names) != list:
        is_create_room = JoinOrCreateRoomPage(screen, my_socket).gotToPage()
        if is_create_room is None:
            return False
        elif is_create_room:
            send_data_socket_pickle(my_socket, pickle.dumps(clientReq.CREATE_ROOM.value))
            data = pickle.loads(receive_data_pickle(my_socket, screen))
            print(data)
            if data == TOO_MANY_ROOMS:
                draw_text_time(TOO_MANY_ROOMS, screen, 10, 300, GREY, RED, 2)
                return False
            else:
                room_number = data[ROOM_NUMBER_INDEX]
                players_names = data[PLAYERS_NAMES_INDEX]
                server_ip = data[SERVER_IP_INDEX]
        else:
            room_number, players_names, server_ip = JoinRoomPage(screen, my_socket).goToPage()
    if server_ip is None or players_names is None or room_number is None:
        return False
    else:
        return WaitingRoom(my_socket, screen, players_names, room_number, server_ip).goToRoom()


def connect(screen):
    """
    func to connect to the server
    :param screen: the screen
    :return: socket object(to communicate with the server)
    """
    my_socket = None
    while my_socket is None:
        ip = "127.0.0.1"  # IPPage(screen).goToPage()
        my_socket = try_connect(ip, screen)
    return my_socket


def try_connect(ip, screen):
    """
    func to try and connect to the server with the ip got from the user
    :param ip: ip of the server
    :param screen: the screen
    :return: socket object
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(1)
    try:  # connect to server
        # my_socket.connect(('2.tcp.ngrok.io', 19399))
        my_socket.connect((ip, PORT))
        print("connected")
        return my_socket
    except:
        print("error")
        draw_text("oops, could't connect to server, please try again later", screen, 10, WINDOW_HEIGHT / 2, color=RED)
        pygame.display.update()
        time.sleep(2)
        sys.exit()


def init_screen():
    """
    init screen
    return the screen
    """
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Blocks war")
    pygame.display.set_icon(pygame.image.load("pics/blue/walk.png"))
    pygame.mixer.init()
    return screen


if __name__ == '__main__':
    main()
