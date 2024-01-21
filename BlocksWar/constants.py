# This is file of all of the constants that mutual in the project

import pygame
import enum
import sys
import traceback
import time
# client----------------------------------------------------------------------------------------------------------------
PATH = r"pics/"
PORT = 31987
SPLIT_CHAR = "+"
NEW_CONNECTION_MSG = "hi"
GAME_STARTED_MSG = "game starting"
START_GAME_ORDER = "!start the game"
GAME_OVER_MSG = "game over"
WINDOW_WIDTH = 728
WINDOW_HEIGHT = 409
BACKGROUND_PATH = r"pics/backgrounds/0.png"
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
# FONT = "freesansbold.ttf"
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
RED = (255, 0, 0)
LIME = (99, 245, 91)
BLUE = (0, 0, 128)
GREEN = (0, 255, 0)
TEXTBOX_COLOR = GREY
LIGHT_BLUE = (204, 255, 255)
LIGHT_BLUE2 = (146, 168, 209)
DARK_BLUE = (3, 79, 132)
messages_count = 0
MAX_LENGTH = 7

# server----------------------------------------------------------------------------------------------------------------
BIND_IP = '0.0.0.0'
MAX_NUM_PLAYERS = 7
PLAYERS_AMOUNT_REQUEST_MSG = "enter amount of players: "
PLAYERS_AMOUNT_REQUEST_AGAIN_MSG = "enter amount of players again: "
AMOUNT_OK = "amount of players is ok"
PLAYER_AMOUNT_MSG = "Players connected: "
PLAYER_NAMES_MSG = "\n players names:\n"
DISCONNECT_MSG = "[DISCONNECT]"
LOGIN_FALIED = "!login fail"
SIGNEDUP_OK = "!sign up ok"
SIGNUP_FAILED = "!the user is already exist"
NOTCONNECTED = "Connect if you want to see your previous matches"
PSLIT_BETWEEN_PLAYERS = "&"
COLOR = "18ffff"
ID_MSG = "your ID is:"
WALK_PIC = "walk"
PUNCH_PIC = "punch"
SWORD_PIC = "sword"
GUN_PIC = "gun"
SIZE_OF_CHARACTER = 50
SCREEN_Y = 409
SCREEN_X = 728
x = 4
# pygame constants------------------------------------------------------------------------------------------------------
IN_PICK_COLOR = "picking color"
RECT_INDEX = 1
IMG_INDEX = 0


def setParams(kind_of_image, name_of_files, size, x_position, y_position):
    images = []

    for file in name_of_files:
        images.append(pygame.transform.scale(pygame.image.load("pics/"+kind_of_image+'/'+file), size))
    rects = []
    for index, image in enumerate(images):
        rects.append(image.get_rect(topleft=(x_position, y_position)))
        x_position += size[0] + 10
    return images, rects


def setPlayersImages(x_position, y_position):
    pics_of_players = []
    rects = []
    for color in range(len(COLOR_LIST)):
        pics_of_players.append(pygame.image.load("pics/" + COLOR_LIST[color] + "/walk.png").convert())
        rects.append(pics_of_players[-1].get_rect(topleft=(x_position, y_position)))
        x_position += 80
    podium_img = pygame.image.load("pics/player_podium.png").convert()
    podium_img = pygame.transform.scale(podium_img, (100, 200))
    podium_img.set_colorkey((0, 0, 0))
    podium_rects = []
    for i in range(0, 4):
        podium_rects.append(podium_img.get_rect(bottomleft=((WINDOW_WIDTH / 6) * (i + 1), WINDOW_HEIGHT+50)))
    return pics_of_players, rects, [podium_img, podium_rects]


def init():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class GameConstans(enum.Enum):
    init()
    FLOOR_IMG = pygame.image.load(r"pics/floor.png").convert()
    FLOORS_RECTS = [FLOOR_IMG.get_rect(topleft=(450, 150)), FLOOR_IMG.get_rect(topleft=(50, 150)),
                    FLOOR_IMG.get_rect(topleft=(250, 300))]
    HEART_IMG = pygame.transform.scale(pygame.image.load(PATH + "/heart.png"), (30, 30))
    LEFT_BULLETS_IMG = pygame.transform.scale(pygame.image.load("pics/bullets.png"), (30, 30))
    BULLET_SPEED = 10


class Images(enum.Enum):
    init()
    BACKGROUND = pygame.image.load(BACKGROUND_PATH).convert()
    PREVIOUS_MATCHES_IMG = pygame.transform.scale(pygame.image.load(PATH + "previousMatches.png").convert(),
                                              (250, int(100 / 2.165)))
    PREVIOUS_MATCHES_RECT = PREVIOUS_MATCHES_IMG.get_rect(center=(500, 370))
    BACK_IMG = pygame.transform.scale(pygame.image.load(PATH + "back.png"), (150, 43))
    BACK_RECT = BACK_IMG.get_rect(bottomleft=(0, WINDOW_HEIGHT))
    START_GAME_IMG = pygame.transform.scale(pygame.image.load(PATH + "start_img.png"), (150, 100))
    START_GAME_RECT = START_GAME_IMG.get_rect(bottomright=(WINDOW_WIDTH, WINDOW_HEIGHT))
    ENTER_IMG = pygame.transform.scale(pygame.image.load("pics/next.jpg"), (150, 43))
    ENTER_RECT = ENTER_IMG.get_rect(bottomright=(WINDOW_WIDTH, WINDOW_HEIGHT))
    CONFIRM_BUTTON_IMG = pygame.image.load(PATH + "confirm.jpg").convert()
    CONFIRM_BUTTON_RECT = CONFIRM_BUTTON_IMG.get_rect(bottomright=(WINDOW_WIDTH, WINDOW_HEIGHT))
    JOYSTICK_IMG = pygame.transform.scale(pygame.image.load("pics/joystick.jpg"), (80, 45))
    JOYSTICK_RECT = JOYSTICK_IMG.get_rect(topright=(WINDOW_WIDTH, 0))
    YES_BUTTON = pygame.image.load(PATH + "yes.jpg").convert()
    YES_BUTTON_RECT = YES_BUTTON.get_rect(topleft=(WINDOW_WIDTH / 2 + 70, 150))
    NO_BUTTON = pygame.image.load(PATH + "no.jpg").convert()
    NO_BUTTON_RECT = NO_BUTTON.get_rect(topleft=(WINDOW_WIDTH / 2 - 200, 150))

    LOGIN_IMG = pygame.transform.scale(pygame.image.load("pics/login.jpg"), (int(555/x), int(257/x)))
    LOGIN_IMG_RECT = LOGIN_IMG.get_rect(center=(120, 90))

    SIGNUP_IMG = pygame.transform.scale(pygame.image.load("pics/signup.jpg"), (int(555/x), int(257/x)))
    SIGNUP_RECT = SIGNUP_IMG.get_rect(center=(120, 190))

    GUEST_IMG = pygame.transform.scale(pygame.image.load("pics/guest.jpg"), (int(555/x), int(257/x)))
    GUEST_RECT = GUEST_IMG.get_rect(center=(120, 290))

    SINGLE_PLAYER_RECT = pygame.rect.Rect(100, 100, 100, 50)
    MULTI_PLAYER_RECT = pygame.rect.Rect(300, 100, 100, 50)
    INSTRUCTION_RECT = pygame.rect.Rect(200, 400, 40, 20)

    BULLET_SIZE = 30
    BULLET = pygame.transform.scale(pygame.image.load("pics/bullet.png"), (30, 30))

    BOT_IMAGE = pygame.transform.flip(pygame.transform.scale(pygame.image.load("pics/bot.png"), (100, 100)), True, False)
    BOT_RECT = BOT_IMAGE.get_rect(bottomleft=((WINDOW_WIDTH/6)*5-20, 300))

    USER_IMG = pygame.transform.scale(pygame.image.load("pics/Sample_User_Icon.png"), (250, 250))
    USER_RECT = USER_IMG.get_rect(bottomleft=(20, WINDOW_HEIGHT-50))


class PygameConstans(enum.Enum):
    init()
    CLOCK = pygame.time.Clock()
    BACKGROUND = Images.BACKGROUND.value

    PREVIOUS_MATCHES = [Images.PREVIOUS_MATCHES_IMG.value, Images.PREVIOUS_MATCHES_RECT.value]

    BACK_IMG = [Images.BACK_IMG.value, Images.BACK_RECT.value]
    START_GAME_IMG = [Images.START_GAME_IMG.value, Images.START_GAME_RECT.value]
    ENTER_IMG = [Images.ENTER_IMG.value, Images.ENTER_RECT.value]

    CONFIRM_BUTTON = [Images.CONFIRM_BUTTON_IMG.value, Images.CONFIRM_BUTTON_RECT.value]
    JOYSTICK_IMG = [Images.JOYSTICK_IMG.value, Images.JOYSTICK_RECT.value]

    COLOR_LIST = ["red", 'blue', "green", "pink", "brown", "black", "yellow"]

    YES_BUTTON = [Images.YES_BUTTON.value, Images.YES_BUTTON_RECT.value]
    NO_BUTTON = [Images.NO_BUTTON.value, Images.NO_BUTTON_RECT.value]
    SHOW_PASSWORD_IMG = pygame.transform.scale(pygame.image.load(PATH + "show_pass.png").convert(), (20, 20))

    LOGIN_IMG = [Images.LOGIN_IMG.value, Images.LOGIN_IMG_RECT.value]
    SIGNEDUP_IMG = [Images.SIGNUP_IMG.value, Images.SIGNUP_RECT.value]
    GUEST_IMG = [Images.GUEST_IMG.value, Images.GUEST_RECT.value]

    SINGLE_PLAYER_RECT = pygame.rect.Rect(300 - 50 + 2, 150 - 15 + 2, 250 - 4, int(250/4.33) - 4)
    MULTI_PLAYER_RECT = pygame.rect.Rect(300 - 50 + 2, 250 - 15 + 2, 250 - 4, int(250/4.33) - 4)
    INSTRUCTION_RECT = pygame.rect.Rect(300 - 250 + 2, 350 + 2, 200 - 4, int(200/4.33) - 4)
    ACCOUNT_SETTING_RECT = pygame.rect.Rect(300 + 20 + 2, 350 + 2, 235, int(200/4.33) - 4)
    TOP10_RECT = pygame.rect.Rect(300 + 300 + 2, 200 + 2, 100, int(200/4.33) - 4)
    BUTTON = pygame.image.load("pics/genericButton.png")

    INSTRUCTION_IMGS = [pygame.image.load("pics/instructions/instruction1.png"),
                        pygame.image.load("pics/instructions/instruction2.png"),
                        pygame.image.load("pics/instructions/instruction3.png"),
                        pygame.image.load("pics/instructions/instruction4.png"),
                        pygame.image.load("pics/instructions/instruction5.png"),
                        pygame.image.load("pics/instructions/instruction6.png")]

    BOT = [Images.BOT_IMAGE.value, Images.BOT_RECT.value]

    USER = [Images.USER_IMG.value, Images.USER_RECT.value]

    BACKGROUNDS_IMGS = setParams("backgrounds", ["0.png", "1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg"], (90, 60), 50+70+10, 30+120)
    BACKGROUNDS_IMGS_FULLSIZE = setParams("backgrounds", ["0.png", "1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg"], (728, 409), 0, 0)
    HATS_IMGS = setParams("hats", ["None.png", "chrismes.png", "cowboy.png", "graduation.png", "mexican.png", "old.png", "party.png", "witch.png"], (60, 60), 50+70-7, 180-108)
    LOCK = pygame.transform.scale(pygame.image.load("pics/lock.png"), (50, 50))

    ADD_IMG = ["add image", pygame.rect.Rect(45, 45, 150, 45)]


class clientReq(enum.Enum):
    RETURN_TO_LOBY_REQ = "return to loby request"
    MULTI_PLAYER = "multi player mode"
    SINGLE_PLAYER = "single player mode"
    CREATE_ROOM = "create room"
    CHANGE_IMG = "change img"


def draw_text(text, surface, x, y, size=40, color=BLACK):
    """
    func draw text to the screen
    :param text: the text we want to write
    :param surface: the surface
    :param x: x position
    :param y: y position
    :param size: size fo the text
    :param color: color of the text
    :return: None
    """

    # font = pygame.font.Font('freesansbold.ttf', size)
    font = pygame.font.Font(pygame.font.match_font(FONT), size)
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)


def draw_text_time(text, surface, x, y, background_color, color=BLACK, sec=None, size=40):
    """
    func draw text to the screen to specific amount of second
    :param sec: amount of seconds to show the text
    :param background_color: the background
    :param text: the text we want to write
    :param surface: the surface
    :param x: x position
    :param y: y position
    :param size: size fo the text
    :param color: color of the text
    :return: None
    """
    start = pygame.time.get_ticks()
    if type(sec) == int:
        while pygame.time.get_ticks()-start < sec*1000:
            #font = pygame.font.Font('freesansbold.ttf', size)
            font = pygame.font.Font(pygame.font.match_font(FONT), size)
            textobj = font.render(text, True, color)
            textrect = textobj.get_rect(topleft=(x, y))
            surface.blit(textobj, textrect)
            pygame.display.update()
        # try:
        print("before")
        surface.fill(background_color, textrect)
        print("after")
            # print("blited")
        # except:
        #     print("error")
        #     pass


def disconnected_from_server(screen):
    """
    func print to screen that he is disconnected
    :param screen: pygame surface
    :return: None
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(GREY)
    draw_text("disconnected from server", screen, WINDOW_WIDTH/3, WINDOW_HEIGHT/2, size=50, color=RED)
    pygame.display.flip()
    pygame.time.delay(2000)
    sys.exit()


def exitGame(screen, my_socket):
    """
    func to exit the game and print to screen "thnks for playing
    :param screen: the screen
    :param my_socket: the socket we comunicated with the server
    :return:
    """
    screen.fill(GREY)
    draw_text("Thanks for playing!", screen, WINDOW_WIDTH / 3, WINDOW_HEIGHT / 2, 60, BLUE)
    pygame.display.flip()
    pygame.time.delay(1000)
    pygame.quit()
    if my_socket is not None:
        my_socket.close()
    try:
        sys.exit()
    except Exception as e:
        print(e)
        print("except")
