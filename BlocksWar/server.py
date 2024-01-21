# This file is for running the server
# The server get requests from the users, and handle them.
# The server also handle the game massages

# -*- coding: utf-8 -*-
import socket
import select
from Player import Player
from Player import Bullet
import sys
import pickle
import time
import math
from database import *
import random
import pygame
import threading
import traceback
from constants import *

BIND_IP = '0.0.0.0'
PORT = 31987
MAX_NUM_PLAYERS = 7


PLAYER_AMOUNT_MSG = "Players connected: "
PLAYER_NAMES_MSG = "\n players names:\n"
GAME_STARTED_MSG = "game starting"
START_GAME_ORDER = "!start the game"
DISCONNECT_MSG = "[DISCONNECT]"
GAME_ENDED = "!game over"
LOGIN_OK = "!logged in"
LOGIN_FALIED = "!login fail"
SIGNEDUP_OK = "!sign up ok"
SIGNUP_FAILED = "!the user is already exist"
NOPREVIOUSMATCHES = "oops, it's looks like you don't have previous matches"
NOTCONNECTED = "Connect if you want to see your previous matches"
GUEST_OK = "!guest ok"
TOPTEN_REQ = "top ten"
PREVIOUS_MATHCES = "previous matches"
GUEST_REQ = "guest request"
CREATE_ROOM = "create room"
JOIN_ROOM = "want to join room"
SPLIT_CHAR = "+"
WALK_PIC = "walk"
PUNCH_PIC = "punch"
SWORD_PIC = "sword"
GUN_PIC = "gun"
SIZE_OF_CHARACTER = 50
SCREEN_Y = 409
SCREEN_X = 728

GO_TO_BASIC_SETTINGS = "go to basic settings page"
EXIT_ROOM_REQ = "exit room"


PLAYERS_INDEX = 0
GAME_THREAD_INDEX = 1
IS_BASSIC_SETTING_SENT_INDEX = 2
IS_GAME_STARTED_INDEX = 3
LOBY_INDEX = 4

IS_DEAD_INDEX = 0
X_POSITION_INDEX = 1
Y_POSITION_INDEX = 2
DIRECTION_INDEX = 3
PLAYER_PIC_INDEX = 4
IS_HITTED_INDEX = 5

DISCONNECT_INDEX = 0
OUTOFGAME_INDEX = 1


def main():
    server_socket = socket.socket()
    server_socket.bind((BIND_IP, PORT))
    server_socket.listen()
    print("Your Computer IP Address is:" + getServerIP())
    print("start the game")
    main_func(server_socket)


def draw_text(text, surface, x_position, y, size=40, color=BLACK):
    """
    func draw text to the screen
    :param text: the text we want to write
    :param surface: the surface
    :param x_position: x position
    :param y: y position
    :param size: size fo the text
    :param color: color of the text
    :return: None
    """
    # font = pygame.font.Font('freesansbold.ttf', size)
    font = pygame.font.Font(pygame.font.match_font(FONT), size)
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x_position, y))
    surface.blit(textobj, textrect)


def run_game(players, loby):
    """
    func that run the game
    param players: list of all the players
    """
    send_first_msg(players)
    clock = pygame.time.Clock()
    over, winner, bullets = False, None, []
    print("in run_game()")
    while not over:
        hits_sounds = []
        have_new_data, over = get_and_change_stats(players, loby)
        if have_new_data:
            handlePlayer(players, bullets, hits_sounds)
        if have_new_data or bullets != []:
            send_stats(players, bullets, hits_sounds)
            over, winner = isGameOver(players)
        for player in players:
            if not player.isQuit():
                player.set_hitted(False)
        bullets = handleBullets(players, bullets, hits_sounds)
        clock.tick(60)
    send_game_over(players, winner)


def isGameOver(players):
    """
    func to check if the game is over
    :param players: the players
    :return: bool, name of winner
    """
    winner = None
    over = False
    deads_amount = 0
    for player in players:
        if player.is_dead():
            deads_amount += 1
    if len(players) - deads_amount <= 1:
        over = True
        for player in players:
            if not player.is_dead():
                winner = player
    return over, winner


def handlePlayer(players, bullets, hits_sounds):
    """
    func to handle all of the players actions in the game
    :param hits_sounds: list of the sounds so send to the users
    :param bullets: list of the bullets
    :param players: the players
    :return: None
    """
    players_in_game = [player for player in players if not player.isQuit()]
    for index, player in enumerate(players_in_game):
        if not player.is_dead():
            if not player.get_kind_of_pic() == WALK_PIC:
                handlePlayerHits(players_in_game, index, bullets, hits_sounds)
        if int(player.get_y()) > SCREEN_Y and not player.is_dead():
            player.decrease_life()


def handlePlayerHits(players, current_player_index, bullets, hits_sounds):
    """
    func to handle hits of specific player
    :param hits_sounds: list of hit sounds
    :param players: list of the players
    :param current_player_index: the index of the player
    :param bullets: list of the bullets
    :return: None
    """
    if players[current_player_index].get_kind_of_pic() == PUNCH_PIC or players[current_player_index].get_kind_of_pic() == SWORD_PIC:
        # checking if the player hit other player
        for other_player in players:
            if players[current_player_index] is not other_player:
                if is_touch(players[current_player_index], other_player):
                    other_player.set_hitted(True)
                    other_player.set_hitted_x(players[current_player_index].get_x())
                    if players[current_player_index].get_kind_of_pic() == PUNCH_PIC:
                        other_player.set_hitted_power(players[current_player_index].get_hit_power())
                        other_player.got_hit()
                        hits_sounds.append(["punch", current_player_index])
                    else:
                        other_player.set_hitted_power(players[current_player_index].get_sword_power())
                        other_player.got_hit()
                        hits_sounds.append(["sword", current_player_index])
    elif players[current_player_index].get_kind_of_pic() == GUN_PIC and \
            pygame.time.get_ticks() - players[current_player_index].last_time_gun > 300:
        bullets.append(Bullet(players[current_player_index].get_x(), players[current_player_index].get_y()+10, players[current_player_index].get_direction(), current_player_index))
        players[current_player_index].last_time_gun = pygame.time.get_ticks()


def handleBullets(players, bullets, hits_sounds):
    """
    func to move bullets on the screen, and handle the clients that got hit from the bullets
    :param hits_sounds: list of sounds to send to the players
    :param players: list of the players
    :param bullets: list of the bullets
    :return: list of the bullets
    """
    remove_bullets = []
    for index, bullet in enumerate(bullets):
        bullet.move()
        if (bullet.getDirection() == "right" and bullet.getPosition()[0] > SCREEN_X) or \
                (bullet.getDirection() == "left" and bullet.getPosition()[0] < 0) or \
                (bullet.hittedPlayer(players)):
            remove_bullets.append(index)
            if bullet.hittedPlayer(players):
                hits_sounds.append(["bullet", bullet.shot_by])
    for index_bullet_to_remove in reversed(remove_bullets):
        bullets.pop(index_bullet_to_remove)
    return bullets


def send_game_over(players, winner):
    """
    func send to all of the players the game ended
    :param winner: the player who won the game
    :param players: list of the players
    :return: None
    """
    database = DataBase()
    everyones_info = everyonesInfo(players, database)
    # send everyone that the game ended, the winners name and the info about every player.
    # it also increase the amount of games the user played
    for player in players:
        if not player.isQuit():
            print("before game over sent")
            send_data_player_pickle(player, pickle.dumps(GAME_ENDED))
            send_data_player_pickle(player, pickle.dumps(str(winner.get_name())))
            send_data_player_pickle(player, pickle.dumps(everyones_info))
            print("game over sent")
            database.addGameForPlayer(player)
    if winner is not None:
        database.addWin(winner)
        database.addMatch(players, winner.get_name())
    else:
        database.addMatch(players, "tie")
    print("added match to database")


def everyonesInfo(players, database):
    """
    func to get info about all of the players in the game from the database.
    the data looks like [name, usrname, games played, games won, img]
    :param players: list of the players
    :param database: the database
    :return: list of lists
    """
    info = []
    for player in players:
        if player.isLogedin():
            info.append(database.get_player_to_send(player.get_name()))
        else:
            info.append(["", player.get_name(), 0, 0, ""])
    return info


def is_touch(player1, player2):
    """
    func check if 2 players are touching each other
    :param player1: first player
    :param player2: second player
    :return: Bool
    """
    if (player1.get_direction() == "right" and player1.get_x() < player2.get_x()) or \
            (player1.get_direction() == "left" and player1.get_x() > player2.get_x()):
        dis_x = math.fabs(player1.get_x() - player2.get_x())
        dis_y = math.fabs(player1.get_y() - player2.get_y())
        dis_t = math.sqrt(math.pow(dis_x, 2)+math.pow(dis_y, 2))
        if dis_t < SIZE_OF_CHARACTER:
            return True
        return False


def get_and_change_stats(players, loby_list):
    """
    func receive data from all of the clients, and change the stats of the players
    :param loby_list: list of the players in the loby
    :param players: list of the players
    :return: bool
    """
    sockets = []
    for player in players:
        if not player.isQuit():
            sockets.append(player.get_socket())
    have_new_data = False
    if len(sockets) > 0:
        rlist, wlist, xlist = select.select(sockets, [], [], 0)
        # for every socket that have data in the buffer
        for current_socket in rlist:
            data = receive_data2(current_socket)
            try:
                data = pickle.loads(data)
                if data and type(data) == list:     # if there is data and he is data about the player
                    i = find_index_by_socket(players, current_socket)
                    player_update(players[i], data)
                    have_new_data = True
                else:
                    handleOutOfGameReq(data, current_socket, players, loby_list)
            except Exception as e:
                print(e)
                continue
        return have_new_data, False
    return False, True


def handleOutOfGameReq(data, current_socket, players, loby_list):
    """
    func to handle players that want to exit the game or disconnected
    :param data: the data got from the user
    :param current_socket: the socket that sent the req
    :param players: list of the players
    :param loby_list: list that contain 2 lists: first one is list of the players in the loby
                                                second is list the the sockets of the players in the loby
    :return: None
    """
    RETURN_TO_LOBY_REQ = "return to loby request"
    db = DataBase()
    if data == DISCONNECT_MSG:
        print("got Nonetype")
        if not players[find_index_by_socket(players, current_socket)].isQuit():
            players[find_index_by_socket(players, current_socket)].set_dead(True)
            players[find_index_by_socket(players, current_socket)].quitPlayer()
            current_socket.close()
            db.removeGuest(players[find_index_by_socket(players, current_socket)].get_name())
            db.removeConnected(players[find_index_by_socket(players, current_socket)].get_name())

    elif data == RETURN_TO_LOBY_REQ:
        if not players[find_index_by_socket(players, current_socket)].isQuit():
            players[find_index_by_socket(players, current_socket)].set_dead(True)
            players[find_index_by_socket(players, current_socket)].quitPlayer()
            loby_list[0].append(copyPlayer(players[find_index_by_socket(players, current_socket)]))
            loby_list[1].append(players[find_index_by_socket(players, current_socket)].get_socket())


def player_update(player, data):
    """
    func change the player properties
    :param player: the player
    :param data: the data
    :return: None
    """
    player.set_dead(data[IS_DEAD_INDEX])
    player.set_pos(data[X_POSITION_INDEX], data[Y_POSITION_INDEX])
    player.set_direction(data[DIRECTION_INDEX])
    player.set_kind_of_pic(data[PLAYER_PIC_INDEX])
    player.set_hitted(data[IS_HITTED_INDEX])


def find_index_by_socket(players, current_socket):
    """
    func return the index of the player by his socket
    :param players: list of players
    :param current_socket: the socket
    :return: integer
    """
    for i_player in range(len(players)):
        if players[i_player].get_socket() == current_socket:
            return i_player


def send_stats(players, bullets, hits_sounds):
    """
     func send to the players the stats
     param stats: list of every player stats([hp, x, y])
     param players: list of players
    """
    stats = []
    for player in players:
        data = [player.is_dead(), player.get_x(), player.get_y(), player.get_direction(), player.get_kind_of_pic(), player.get_hp(),
                player.get_hitted(), player.get_hitted_power(), player.get_hitted_x()]
        stats.append(data)

    sockets = []    # creating list of all of the sockets
    for player in players:
        if not player.isQuit():
            sockets.append(player.get_socket())
    rlist, wlist, xlist = select.select([], sockets, sockets, 0)
    for current_socket in wlist:
        send_by_socket(current_socket, [stats, bullets, hits_sounds])


def send_by_socket(ssocket, stats):
    """
    func send data by socket
    :param ssocket: the socket
    :param stats: the data to send
    :return: None
    """
    try:
        stats = pickle.dumps(stats)
        ssocket.send((str(len(stats))+SPLIT_CHAR).encode('utf-8') + stats)
    except Exception as e:
        print("fail")
        print(e)


def send_first_msg(players):
    """
    sending the begginng message of the game with the data of all of the players(color, x, y)
    param players: list of the players
    """
    msg = []
    for player in players:
        msg.append([player.get_color(), player.get_x(), player.get_y(), player.get_hat()])
    print(msg)
    for i_player in range(len(players)):
        send_data_socket_pickle(players[i_player].get_socket(), pickle.dumps(msg))
        send_data_socket_pickle(players[i_player].get_socket(), pickle.dumps(["index", i_player]))
    print("sent stats to everyone")


def main_func(server_socket):
    """
    func create connection with all of the clients, and handle the request of them
    func return server socket and clients list
    """
    # creating list of all of the sockets
    players_in_loby, sockets_loby = [], []
    database = DataBase()
    rooms = {}      # dictionary of the rooms. key = room number,
                    # value = [[players], thread of the game, is_started_the_game, is_in_basic_settings]
    screen = init_server_screen()
    while True:
        sockets_loby = createSockets(players_in_loby)
        handleLoby(server_socket, sockets_loby, players_in_loby, database, rooms)
        handleRooms(rooms, players_in_loby, sockets_loby)
        displayServerBackEnd(screen, len(rooms))


def init_server_screen():
    """
    func to create pygame screen object to display data to the screen
    this function is for the server to display some info about the server
    :return: pygame surface
    """
    pygame.init()
    pygame.display.set_caption("server window")
    screen = pygame.display.set_mode((728, 409))
    return screen

# def removeDoubles(players):
#     """
#     func to remove doubled players
#     :param players: list of the players
#     :return: list
#     """
#     for ii in range(len(players)):
#         for jj in range(ii+1, len(players)):
#             if players[ii].get_socket() == players[jj].get_socket():


def createSockets(players):
    """
    func to create list of all of the sockets in the loby
    :param players: list of the players
    :return: list of sockets
    """
    players_to_remove = []
    sockets_loby = []
    for player in players:
        if player.get_socket().fileno() != -1:       # if socket if closed, socket.fileno return -1
            sockets_loby.append(player.get_socket())
        else:
            players_to_remove.append(player)
    for player2 in players_to_remove:
        players.remove(player2)
    return sockets_loby


def displayServerBackEnd(screen, rooms_amount):
    """
    func to display the amount of the users connected
    :param screen: the screen
    :param rooms_amount: the amount of the rooms
    :return: None
    """
    handlePage()
    displayPage(screen, rooms_amount)


def displayPage(screen, rooms_amount):
    """
    func to display the amount of the rooms that active now
    :param screen: the screen
    :param rooms_amount: amount of the rooms
    :return: None
    """
    screen.fill(GREY)
    ip = getServerIP()
    draw_text(f"ip address: {ip}", screen, 50, 50, color=DARK_BLUE)
    draw_text(f"active rooms: {str(rooms_amount)}", screen, 50, 100)
    pygame.display.flip()


def getServerIP():
    """
    func to get the IP address of the server
    :return: string
    """
    hostname = socket.gethostname()  # get computer name
    IPAddr = socket.gethostbyname(hostname)  # get computer ip
    return IPAddr


def handlePage():
    """
    func to handle users inputs
    :return: None
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def handleRooms(rooms, players_in_loby, sockets_loby):
    """
    func to handle requests from the rooms
    :param rooms: dictionary of the rooms
    :param players_in_loby: list of the players in the loby
    :param sockets_loby: list of the sockets in the loby
    :return: None
    """
    temp_rooms = rooms.copy()
    for room_number, room in temp_rooms.items():
        handleRoomClosing(rooms, room_number, players_in_loby, sockets_loby)
        sockets_game = createSockets(room[PLAYERS_INDEX])
        # so that this func won't get the data from the game
        if room[GAME_THREAD_INDEX].is_alive():
            continue
        try:
            rlist, wlist, xlist = select.select(sockets_game, [], [], 0)
        except:
            print(sockets_game)
            print(len(sockets_game))
            print(type(sockets_game))
            continue
        for current_socket in rlist:
            data = receive_data2(current_socket)
            data = pickle.loads(data)
            print(f"data from rooms loop: {data}")
            manageClientRequestRoom(data, current_socket, players_in_loby, sockets_loby, rooms, room_number,
                                    sockets_game)


def handleLoby(server_socket, sockets_loby, players_in_loby, database, rooms):
    """
    func to handle request from the loby.
    :param server_socket: the socket of the server
    :param sockets_loby: list of the sockets in the loby
    :param players_in_loby: list of the players in the loby
    :param database: the database
    :param rooms: dictionary of the rooms
    :return: None
    """
    rlist, wlist, xlist = select.select([server_socket] + sockets_loby, [], [server_socket] + sockets_loby, 0)
    # going over all of the sockets we can read from
    for current_socket in xlist:
        remove_players(players_in_loby, current_socket, sockets_loby)
    for current_socket in rlist:
        if current_socket is server_socket:  # do we have request for connection from new client?     connect
            sockets_loby.append(new_connection(players_in_loby, server_socket))
        else:  # new data?
            data = receive_data2(current_socket)
            data = pickle.loads(data)
            print(f"data from loby loop: {data}")
            if data == DISCONNECT_MSG:
                remove_players(players_in_loby, current_socket, sockets_loby)
            else:
                manageClientRequestLoby(data, current_socket, players_in_loby, sockets_loby, database, rooms)


def handleRoomClosing(rooms, room_number, players_in_loby, sockets_loby):
    """
    func to close room if the game ended or if there is no one there
    :param rooms: dictionary of the rooms
    :param room_number: key of the room
    :param players_in_loby: list of the players in the loby
    :param sockets_loby: list of the sockets in the loby
    :return: None
    """
    if room_number in rooms.keys() and rooms[room_number][IS_GAME_STARTED_INDEX]:
        if not rooms[room_number][GAME_THREAD_INDEX].is_alive():    # game is over
            for player in rooms[room_number][PLAYERS_INDEX]:
                if not player.isQuit():
                    players_in_loby.append(copyPlayer(player))
                    sockets_loby.append(player.get_socket())
            rooms.pop(room_number)
            print("game over, returned to loby")
    if room_number in rooms.keys() and len(rooms[room_number][PLAYERS_INDEX]) == 0:
        rooms.pop(room_number)
        print(f"poped room: {room_number}")


def manageClientRequestRoom(request, current_socket, players_in_loby, sockets_loby, rooms, room_number, sockets_game):
    """
    func to handle clients requests inside the room
    :param request: the data got
    :param current_socket: the socket that sent the request
    :param players_in_loby: list of the player in the loby
    :param sockets_loby: list of the sockets of the players in the loby
    :param rooms: dictionary of the rooms
    :param room_number: key of the specific room
    :param sockets_game: list of the socket of the players in the room
    :return: None
    """
    try:
        if request == DISCONNECT_MSG:
            disconnectPlayerFromRoom(rooms, room_number, current_socket, sockets_game, players_in_loby, sockets_loby)
        elif request == EXIT_ROOM_REQ:
            removePlayerFromRoom(players_in_loby, sockets_loby, rooms, room_number, current_socket)
        elif request == GO_TO_BASIC_SETTINGS and len(rooms[room_number][PLAYERS_INDEX]) > 1:
            goToBassicSettings(rooms[room_number])
        elif request == START_GAME_ORDER and isEveryonePickedColor(rooms[room_number]):
            startGameInRoom(rooms[room_number])
        elif request[0] == "color":
            setColorInRoom(rooms[room_number], request, current_socket)
        else:
            print(f"unknown room request {request}")
    except:
        print(f"error room request {request}")


def isEveryonePickedColor(room):
    """
    this function is to make sure that everyone in the room have picked their color
    :param room: the room
    :return: bool
    """
    if room is not None:
        for player in room[PLAYERS_INDEX]:
            if player.get_color() == "":
                return False
        return True
    return False


def disconnectPlayerFromRoom(rooms, room_number, current_socket, sockets_game, players_in_loby, sockets_loby):
    """
    func to remove player from the room, if the room empty, remove the room from the dictionary of the rooms
    :param sockets_loby: list of the sockets in the loby
    :param players_in_loby: list of the players in the loby
    :param rooms: dictionary of the rooms
    :param room_number: key of the room
    :param current_socket: the socket that disconnected
    :param sockets_game: list of the sockets of the room
    :return: None
    """
    EVERYONE_EXITED_BASSIC_SETTINGS_PAGE = "everyone exited from the basic settings page"
    remove_players(rooms[room_number][PLAYERS_INDEX], current_socket, sockets_game)
    # if the room is empty now, close it
    if len(rooms[room_number][PLAYERS_INDEX]) == 0:
        rooms.pop(room_number)
        print(f"poped room: {room_number}")
    # if the users got into basic settings room
    elif rooms[room_number][IS_BASSIC_SETTING_SENT_INDEX]:
        # if there is only one member on the room
        if len(rooms[room_number][PLAYERS_INDEX]) == 1:
            send_data_socket_pickle(rooms[room_number][PLAYERS_INDEX][0].get_socket(), pickle.dumps(EVERYONE_EXITED_BASSIC_SETTINGS_PAGE))
            players_in_loby.append(copyPlayer(rooms[room_number][PLAYERS_INDEX][0]))
            rooms.pop(room_number)
        else:
            sendColorsOfRoom(rooms[room_number])
    else:
        roomUpdate(rooms, room_number)


def roomUpdate(rooms, room_number):
    """
    func to update all of the users in the room
    :param rooms: dictionary of the rooms
    :param room_number: the key of the room
    :return: None
    """
    print("in roomUpdate")
    for player in rooms[room_number][PLAYERS_INDEX]:
        players_names = [player.get_name() for player in rooms[room_number][0]]
        send_data_socket_pickle(player.get_socket(),
                                pickle.dumps(["room update", room_number, players_names]))


def removePlayerFromRoom(players_in_loby, sockets_loby, rooms, room_number, current_socket):
    """
    func remove player from the room, and insert him to the loby
    :param players_in_loby: list of the players in the loby
    :param sockets_loby: list of the socket in the loby
    :param rooms: dictionary of the rooms
    :param room_number: the key of the specific room
    :param current_socket: the socket that sent the request
    :return: None
    """
    players_in_loby.append(copyPlayer(rooms[room_number][PLAYERS_INDEX][find_index_by_socket(rooms[room_number][PLAYERS_INDEX], current_socket)]))
    rooms[room_number][PLAYERS_INDEX].pop(find_index_by_socket(rooms[room_number][PLAYERS_INDEX], current_socket))
    EVERYONE_EXITED_BASSIC_SETTINGS_PAGE = "everyone exited from the basic settings page"
    if rooms[room_number] is not None:
        # if there is not one in the room
        if len(rooms[room_number][PLAYERS_INDEX]) == 0:
            rooms.pop(room_number)
        # if the players got to basic settings page
        elif rooms[room_number][IS_BASSIC_SETTING_SENT_INDEX]:
            # if there are 1 players in the room
            if len(rooms[room_number][PLAYERS_INDEX]) == 1:
                send_data_socket_pickle(rooms[room_number][PLAYERS_INDEX][0].get_socket(), pickle.dumps(EVERYONE_EXITED_BASSIC_SETTINGS_PAGE))
                players_in_loby.append(copyPlayer(rooms[room_number][PLAYERS_INDEX][0]))
                rooms.pop(room_number)
            else:
                sendColorsOfRoom(rooms[room_number])
        else:
            roomUpdate(rooms, room_number)
        print(f"player exited from room: {room_number}")
    else:
        print("nothing happend")


def goToBassicSettings(room):
    """
    func to send everyone in the room to go the "basic settings" page.
    :param room: the room
    :return: None
    """
    colors = []     # list of lists. every list contain [color name(string), index of picked hat(int), username(string)
    for player in room[PLAYERS_INDEX]:
        send_data_socket_pickle(player.get_socket(), pickle.dumps(GO_TO_BASIC_SETTINGS))
        colors.append(["", None, player.get_name()])
    for player in room[PLAYERS_INDEX]:
        send_data_socket_pickle(player.get_socket(), pickle.dumps([False, colors]))
    "basic settings room"
    room[2] = True


def startGameInRoom(room):
    """
    func to send everyone that the game starts, and start the thread of the game
    :param room: the room to start the game to
    :return: None
    """
    for player in room[PLAYERS_INDEX]:
        send_data_socket_pickle(player.get_socket(), pickle.dumps(START_GAME_ORDER))
    room[IS_GAME_STARTED_INDEX] = True
    room[GAME_THREAD_INDEX] = threading.Thread(target=run_game, args=[room[PLAYERS_INDEX], room[LOBY_INDEX]])
    room[GAME_THREAD_INDEX].start()


def setColorInRoom(room, data, current_socket):
    """
    func set the color of the character and the hat of the character of the user that sent,
    than, send it to everyone in the room
    :param room: the room
    :param data: the color and the hat indexes
    :param current_socket: the socket of the user that sent the inforamtion
    :return: None
    """
    room[PLAYERS_INDEX][find_index_by_socket(room[PLAYERS_INDEX], current_socket)].set_color(data[1])
    room[PLAYERS_INDEX][find_index_by_socket(room[PLAYERS_INDEX], current_socket)].set_hat(data[2])
    print(f"got color:  {data[1]}, {data[2]}")
    sendColorsOfRoom(room)


def sendColorsOfRoom(room):
    """
    func to send every users color, hat and name to everyone in the room
    :param room:
    :return: None
    """
    colors = []
    print(room[PLAYERS_INDEX])
    for player in room[PLAYERS_INDEX]:
        colors.append([player.get_color(), player.get_hat(), player.get_name()])
    print(colors)
    for player in room[PLAYERS_INDEX]:
        send_data_socket_pickle(player.get_socket(), pickle.dumps([False, colors]))
        print("sent color request")


def copyPlayer(player):
    """
    func to copy the important parts of the player
    :param player: the player to copy
    :return: Player object
    """
    player_copy = Player()
    player_copy.set_socket(player.get_socket())
    player_copy.set_name(player.get_name())
    player_copy.set_login(player.isLogedin())
    return player_copy


def manageClientRequestLoby(data, current_socket, players_in_loby, sockets_loby, database, rooms):
    """
    func to manage all the request from the users in the loby
    :param data: the request
    :param current_socket: the socket who sent the request
    :param players_in_loby: list of the players in the loby
    :param sockets_loby: list of the sockets in the loby
    :param database: the database
    :param rooms: dictionary of the rooms
    :return: None
    """
    if type(data) == list:
        listRequestLoby(data, current_socket, players_in_loby, sockets_loby, rooms, database)
    elif type(data) == str:
        stringRequestLoby(data, current_socket, players_in_loby, sockets_loby, rooms, database)


def stringRequestLoby(data, current_socket, players_in_loby, sockets_loby, rooms, database):
    """
    func to handle string request from the loby
    :param data: the request
    :param current_socket: the socket that sent the request
    :param players_in_loby: list of the players in the loby
    :param sockets_loby: list of the sockets in the loby
    :param rooms: dictionary of the rooms
    :param database: the databse
    :return:
    """
    if data == GUEST_REQ:
        print(f"guest {GUEST_OK}")
        guest_name = database.getNameForGuest()
        send_data_socket_pickle(current_socket, pickle.dumps(GUEST_OK))
        send_data_socket_pickle(current_socket, pickle.dumps(guest_name))
        # print(f"sent guest name {guest_name}")
        players_in_loby[find_index_by_socket(players_in_loby, current_socket)].set_name(guest_name)
    elif data == CREATE_ROOM:
        createRoom(rooms, players_in_loby, sockets_loby, current_socket)
        print(f"room created {rooms}")
    elif data == JOIN_ROOM:
        send_data_socket_pickle(current_socket, pickle.dumps(rooms))
    elif data == PREVIOUS_MATHCES:
        sendMatches(current_socket, players_in_loby, database)
    elif data == TOPTEN_REQ:
        sendTopTen(current_socket, database)
    else:
        print(f"unknown string request loby: {data}")


def listRequestLoby(data, current_socket, players_in_loby, sockets_loby, rooms, database):
    """
    func to handle list type requests from the loby
    :param data: the request
    :param current_socket: the socket that sent the request
    :param players_in_loby: list of the players in the loby
    :param sockets_loby: list of the sockets in the loby
    :param rooms: dictionary of the rooms
    :param database: the databse
    :return: None
    """
    LOGIN_REQ = "login request"
    SIGNUP_REQ = "sign up request"
    JOIN_ROOM_REQ = "join room"
    CHANGE_IMG_REQ = "change img"
    if data[0] == LOGIN_REQ:
        loginReq(data, current_socket, players_in_loby, database)
    elif data[0] == SIGNUP_REQ:
        signupReq(data, current_socket, players_in_loby, database)
    elif data[0] == JOIN_ROOM_REQ:
        joinRoom(data[1], current_socket, players_in_loby, sockets_loby, rooms)
    elif data[0] == CHANGE_IMG_REQ:
        if players_in_loby[find_index_by_socket(players_in_loby, current_socket)].isLogedin():
            database.change_Img(data[1], data[2], data[3],
                                players_in_loby[find_index_by_socket(players_in_loby, current_socket)].get_name())
    else:
        print(f"unknown list request: {data}")


def loginReq(data, current_socket, players_in_loby, database):
    """
    func to check whether the login inputs are correct
    :param data: the login inputs
    :param current_socket: the socket sent the request to login
    :param players_in_loby: lost of the players in the loby
    :param database: the database
    :return: None
    """
    # is the login inputs correct
    if database.login(data[USERNAME_INDEX], data[PASSWORD_INDEX]) is not None:
        send_data_socket_pickle(current_socket, pickle.dumps(LOGIN_OK))
        send_data_socket_pickle(current_socket, pickle.dumps(database.get_player_to_send(data[1])))
        players_in_loby[find_index_by_socket(players_in_loby, current_socket)].set_name(data[1])
        players_in_loby[find_index_by_socket(players_in_loby, current_socket)].set_login(True)
    else:
        send_data_socket_pickle(current_socket, pickle.dumps(LOGIN_FALIED))


def signupReq(data, current_socket, players_in_loby, database):
    """
    func to check whether the user can sign up with those inputs(check whether there is already user with that name)
    :param data: the data got(name, username, password)
    :param current_socket: the socket that sent the request
    :param players_in_loby: list of the players in the loby
    :param database: the database
    :return: None
    """
    NAME = 1
    USERNAME = 2
    PASSWORD = 3
    if database.new_player(data[NAME], data[USERNAME], data[PASSWORD]):
        print(SIGNEDUP_OK)
        send_data_socket_pickle(current_socket, pickle.dumps(SIGNEDUP_OK))
        players_in_loby[find_index_by_socket(players_in_loby, current_socket)].set_name(data[USERNAME])
        players_in_loby[find_index_by_socket(players_in_loby, current_socket)].set_login(True)
    else:
        print(SIGNUP_FAILED)
        send_data_socket_pickle(current_socket, pickle.dumps(SIGNUP_FAILED))


def sendTopTen(current_socket, database):
    """
    func to send the list of the top ten to the user that requested
    :param current_socket: the socket who sent the request
    :param database: the database
    :return: None
    """
    TOPTEN_IS_EMPTY = "the database is empty"
    top_ten = database.getTopTen()
    if top_ten is None:
        send_data_socket_pickle(current_socket, pickle.dumps(TOPTEN_IS_EMPTY))
    else:
        if len(top_ten) > 10:
            top_ten = top_ten[:10]
        send_data_socket_pickle(current_socket, pickle.dumps(top_ten))


def joinRoom(room_number, current_socket, players_in_loby, sockets_loby, rooms):
    """
    func to join player into a room
    :param sockets_loby: list of the players in the loby
    :param room_number: the id of the room
    :param current_socket: the socket of the client that sent the request
    :param players_in_loby: list of the players in the loby
    :param rooms: dictionary of the rooms
    :return: None
    """
    print("in join room")
    error = ""
    ROOM_NUM_NOT_FOUND = "oops, couldn't found the room you looked for"
    MAX_AMMOUNT_IN_ROOM = 4
    GAME_ALREADY_STARTED = "oops, the match already started"
    ROOM_FULL_MSG = "oops, the room is full"
    ROOM_NUM_IS_NOT_INTEGER = "oops, the room number should be integer"
    print(f"room number: {room_number} rooms.keys(): {rooms.keys()}")
    if not room_number.isdigit():
        error = ROOM_NUM_IS_NOT_INTEGER
    else:
        room_number = int(room_number)
        if room_number not in rooms.keys():
            error = ROOM_NUM_NOT_FOUND
        elif len(rooms[room_number][PLAYERS_INDEX]) == MAX_AMMOUNT_IN_ROOM:
            error = ROOM_FULL_MSG
            # is game started
        elif rooms[room_number][IS_BASSIC_SETTING_SENT_INDEX]:
            error = GAME_ALREADY_STARTED
        else:
            print("added")
            rooms[room_number][PLAYERS_INDEX].append(players_in_loby[find_index_by_socket(players_in_loby, current_socket)])    # add the user to the room
            players_in_loby.pop(find_index_by_socket(players_in_loby, current_socket))                                          # remove the user from the loby
            sockets_loby.remove(current_socket)                                                                                 # remove the user from the loby
            players_names = [player.get_name() for player in rooms[room_number][PLAYERS_INDEX]]
            send_data_socket_pickle(current_socket, pickle.dumps(["joining room completed", room_number, players_names, getServerIP()]))
            for player in rooms[room_number][PLAYERS_INDEX]:
                send_data_socket_pickle(player.get_socket(),
                                        pickle.dumps(["room update", room_number, players_names]))
            print("fully added")
    if error != "":
        print("error")
        send_data_socket_pickle(current_socket, pickle.dumps(error))


def createRoom(rooms, players_in_loby, sockets_loby, current_socket):
    """
    func to create room. the function will also insert the player that asked to create the room into the room
    :param sockets_loby: list of the players in the loby
    :param rooms: dictionary of the rooms
    :param players_in_loby: list of the players in the loby
    :param current_socket: the current socket
    :return: None
    """
    TOO_MANY_ROOMS = "there are too many rooms right now, try again later"
    MAX_ROOMS = 10
    ROOM_CREATED_SUCCESSFULLY = "room created successfully"
    if len(rooms) >= MAX_ROOMS:
        send_data_socket_pickle(current_socket, pickle.dumps([TOO_MANY_ROOMS, 0, None]))
    room_number = generateRoomNumber(rooms)
    rooms[room_number] = [[players_in_loby[find_index_by_socket(players_in_loby, current_socket)]], threading.Thread(target=run_game, args=[]), False, False, [players_in_loby, sockets_loby]]
    print(rooms.keys())
    players_in_loby.pop(find_index_by_socket(players_in_loby, current_socket))
    sockets_loby.remove(current_socket)
    players_names = [player.get_name() for player in rooms[room_number][PLAYERS_INDEX]]
    send_data_socket_pickle(current_socket, pickle.dumps([ROOM_CREATED_SUCCESSFULLY, room_number, players_names, getServerIP()]))


def generateRoomNumber(rooms):
    """
    func to generate room number
    :param rooms: dictionary of the rooms
    :return: int
    """
    ROOMS_RANGE = 1000, 9999
    room_number = random.randint(ROOMS_RANGE[0], ROOMS_RANGE[1])
    while room_number in rooms.keys():
        room_number = random.randint(ROOMS_RANGE[0], ROOMS_RANGE[1])
    return room_number


def sendStartGame(players):
    """
    func to sent to all of the players that the game starts
    :param players:
    :return:
    """
    for player in players:  # sending to all players that the game started
        try:
            send_data_player_pickle(player, pickle.dumps([True, [["", None, ""], ["", None, ""], ["", None, ""], ["", None, ""]]]))
            print(GAME_STARTED_MSG)
            print("sent")
        except:
            continue


def sendMatches(current_socket, players, database):
    """
    func to send the user his previous matches
    :param current_socket: the socket
    :param players: players
    :param database: the database
    :return: None
    """
    if players[find_index_by_socket(players, current_socket)].isLogedin():
        matches = database.getPlayerMatches(players[find_index_by_socket(players, current_socket)])
        if len(matches) > 10:
            send_data_socket_pickle(current_socket, pickle.dumps(matches[-10:]))
            print(matches[-10:])
        elif len(matches) == 0:
            send_data_socket_pickle(current_socket, pickle.dumps(NOPREVIOUSMATCHES))
            print(NOPREVIOUSMATCHES)
        else:
            send_data_socket_pickle(current_socket, pickle.dumps(matches))
            print(matches)
    else:
        send_data_socket_pickle(current_socket, pickle.dumps(NOTCONNECTED))
        print(NOTCONNECTED)


def pickNameGuest(players):
    """
    func to give to guest a name
    :param players: the players
    :return: string
    """
    name = "guest" + str(random.randint(1000, 10000))
    counter = 0
    while counter < len(players):
        for player in players:
            if player.get_name() == name:
                name = "guest" + str(random.randint(1000, 10000))
            else:
                counter += 1
    return name


def new_connection(players, server_socket):
    """
    func accept user
    :param players: players list
    :param server_socket: the socket
    :return: the socket of the user
    """
    (new_socket, address) = server_socket.accept()
    players.append(Player())
    players[-1].set_socket(new_socket)
    game_players_msg = PLAYER_AMOUNT_MSG + str(len(players)) + "/" + str(
        MAX_NUM_PLAYERS) + PLAYER_NAMES_MSG  # make message with the players amount and their names
    print(game_players_msg)
    return new_socket


def remove_players(players, current_socket, sockets_list):
    """
    removing players from the array
    param players: list of the players
    param current_socket: the socket that disconnected
    """
    db = DataBase()
    for player in players:
        if player.get_socket() is current_socket:
            if not player.isLogedin():
                db.removeGuest(player.get_name())
            db.removeConnected(player.get_name())
            players.remove(player)
    current_socket.close()
    sockets_list.remove(current_socket)
    print("player removed")


def send_data_player_pickle(player, data):
    """
    sending "data" to "player" with my protocol(sending the length of the message+SPLIT_CHAR+the message)
    param player: the player we want to send for
    param data: the data we want to send
    """
    try:
        player.get_socket().send((str(len(data)) + SPLIT_CHAR).encode('utf-8') + data)
    except:
        pass


def send_data_socket_pickle(c_socket, data):
    try:
        print(f"~~SENDING: [{pickle.loads(data)}]")
        c_socket.send((str(len(data))+SPLIT_CHAR).encode('utf-8') + data)
    except Exception as e:
        print(f"didn't send+ {e}")


def receive_data2(c_socket):
    """
    receiving data in "pickle format" from client with my protocol(sending the length of the message+SPLIT_CHAR+the message)
    c_socket: the socket of the player
    """
    leng = " "
    while not str(leng[-1]) == SPLIT_CHAR:
        try:
            leng += c_socket.recv(1).decode('utf-8')
            if leng == " ":
                return pickle.dumps(DISCONNECT_MSG)
        except:
            # remove_players(players, c_socket)
            return pickle.dumps(DISCONNECT_MSG)
    if leng[1:-1].isdigit():
        return c_socket.recv(int(leng[:-1]))


if __name__ == '__main__':
    main()
