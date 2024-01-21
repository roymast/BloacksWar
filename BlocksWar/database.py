# This file is for the database object
# The database save data about all of the users

import sqlite3
import base64
import threading
import os
import sys
import datetime
from Player import Player
from Player import User
import pygame
NAME_INDEX = 0
USERNAME_INDEX = 1
PASSWORD_INDEX = 2
GAMESPLAYED_INDEX = 3
GAMESWON_INDEX = 4
IMG_BYTES_INDEX = 5
IMG_WIDTH = 6
IMG_HEIGHT = 7


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect("databases/database.db")
        self.c = self.conn.cursor()
        self.create_players_db()
        self.create_matches_db()
        self.create_guests_names_db()
        self.create_users_connected()
        self.deleteGuestsNames()
        self.deleteConnectedUsers()

    def deleteGuestsNames(self):
        self.c.execute("DELETE FROM guests_names")
        self.conn.commit()

    def deleteConnectedUsers(self):
        self.c.execute("DELETE FROM users_connected")
        self.conn.commit()

    def addGameForPlayer(self, player):
        """
        func to increase counter of games the user played in the game
        :param player: the player
        :return:
        """
        if player.isLogedin():
            self.c.execute(f"SELECT * FROM players WHERE username=:player_name", {'player_name': player.get_name()})
            player_info = self.c.fetchone()
            self.c.execute(f"UPDATE players SET games_played=:games WHERE username=:player_name",
                           {"games": str(player_info[GAMESPLAYED_INDEX] + 1), "player_name": player.get_name()})
            self.conn.commit()

    def addWin(self, player):
        """
        func to increase the counter of the games the winner of the game have in the database
        :param player: the player
        :return: None
        """
        if player.isLogedin():
            self.c.execute(f"SELECT * FROM players WHERE username=:player_name", {'player_name': player.get_name()})
            player_info = self.c.fetchone()
            self.c.execute(f"UPDATE players SET games_won=:games WHERE username=:player_name",
                           {"games": str(player_info[GAMESWON_INDEX] + 1), "player_name": player.get_name()})
            self.conn.commit()

    def addMatch(self, players, winner="Tie"):
        """
        func to add match to the database
        :param players: the players that played
        :param winner: the winner
        :return: None
        """
        if len(players) == 4:
            player1, player2, player3, player4 = [player.get_name() for player in players]
        elif len(players) == 3:
            player1, player2, player3 = [player.get_name() for player in players]
            player4 = ""
        elif len(players) == 2:
            player1, player2 = [player.get_name() for player in players]
            player3, player4 = ["", ""]
        else:
            return
        self.c.execute(f"INSERT INTO matches VALUES (?, ?, ?, ?, ?, ?)", (str(datetime.datetime.now()), winner, player1,
                                                                          player2, player3, player4))
        self.conn.commit()

    def get_matches(self):
        """
        func to get all of the matches
        :return: list
        """
        self.c.execute(f"SELECT * FROM matches")
        return self.c.fetchall()

    def getPlayerMatches(self, player):
        """
        func to get all of the user matches
        :param player: the player for whom we looking for the matches
        :return: list
        """
        self.c.execute(f"SELECT * FROM matches WHERE player1name=:name OR player2name=:name OR player3name=:name OR "
                       f"player4name=:name", {'name': player.get_name()})
        matches = self.c.fetchall()
        return matches

    def new_player(self, name, username, password):
        """
        func to add new user to database
        func also return whether it is possible to add this user to database
        :param name: name of user
        :param username: username of user
        :param password: password of user
        :return: bool
        """
        if self.get_player(username) is None and self.c.execute(f"SELECT * FROM guests_names WHERE name=?", (username,)).fetchone() is None:
            self.c.execute(f"INSERT INTO players VALUES (?, ?, ?, 0, 0, ?, 0, 0)", (name, username, password, ""))
            self.c.execute("INSERT INTO users_connected VALUES (?)", (username,))
            self.conn.commit()
            return True
        return False

    def get_player(self, username):
        """
        func to get specific player
        :param username: the username of the player we want to find
        :return: list
        """
        self.c.execute(f"SELECT * FROM players WHERE username=?", (username,))
        return self.c.fetchone()

    def get_player_to_send(self, username):
        """
        func to get info about specefic user that we want to send at the end of the game
        :param username: the username of the user we want to get info about
        :return: list
        """
        self.c.execute(f"SELECT * FROM players WHERE username=?", (username,))
        user_info = self.c.fetchone()
        return [user_info[NAME_INDEX], user_info[USERNAME_INDEX], user_info[GAMESPLAYED_INDEX],
                user_info[GAMESWON_INDEX], user_info[IMG_BYTES_INDEX], user_info[IMG_WIDTH], user_info[IMG_HEIGHT]]

    def change_Img(self, img_bytes, img_width, img_height, username):
        """
        func to change the img of the user
        :param img_bytes: bytes of the img
        :param img_width: width of the img
        :param img_height: height of the img
        :param username: the username of the player that sent the request
        :return: None
        """
        img_width = 250
        img_height = 250
        self.c.execute(f"UPDATE players SET image=?, image_height=?, image_width=? WHERE username=?", (img_bytes, img_height, img_width, username))
        self.conn.commit()

    def login(self, username, password):
        """
        func to login user
        :param username: username got
        :param password: password got
        :return:
        """
        user = self.get_player(username)
        if user is not None:
            if user[PASSWORD_INDEX] == password:
                print(self.c.execute(f"SELECT * FROM users_connected WHERE name=?", (user[USERNAME_INDEX],)).fetchone())
                if self.c.execute(f"SELECT * FROM users_connected WHERE name=?", (user[USERNAME_INDEX],)).fetchone() is None:
                    self.c.execute("INSERT INTO users_connected VALUES (?)", (user[USERNAME_INDEX],))
                    self.conn.commit()
                    return user
        return None

    def create_players_db(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS players (
                                name text,
                                username text,
                                password text,                                
                                games_played integer,
                                games_won integer,
                                image string,
                                image_height integer,
                                image_width integer
                                )""")

    def create_matches_db(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS matches (
                            date string,                            
                            winner string,
                            player1name string,
                            player2name string,
                            player3name string,
                            player4name string
                            )""")

    def create_guests_names_db(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS guests_names (name string)""")

    def create_users_connected(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS users_connected (name string)""")

    def getNameForGuest(self):
        import random
        name = "guest" + str(random.randint(1000, 10000))
        while self.c.execute(f"SELECT * FROM guests_names WHERE name=?", (name,)).fetchone() is not None or \
                self.c.execute(f"SELECT * FROM players WHERE username=?", (name,)).fetchone() is not None:
            name = "guest" + str(random.randint(1000, 10000))
        self.c.execute(f"INSERT INTO guests_names VALUES (?)", (name, ))
        self.conn.commit()
        print(self.c.execute("SELECT * FROM guests_names").fetchall())
        return name

    def removeGuest(self, username):
        if self.c.execute(f"SELECT * FROM guests_names WHERE name=?", (username,)).fetchone() is not None:
            self.c.execute(f"DELETE FROM guests_names WHERE name={username}")
            self.conn.commit()

    def removeConnected(self, username):
        if self.c.execute(f"SELECT * FROM users_connected WHERE name=?", (username,)).fetchone() is not None:
            self.c.execute(f"DELETE FROM users_connected WHERE name=?", (username,))
            self.conn.commit()
            print("remove user from USERS_CONNECTED")

    def getTopTen(self):
        self.c.execute(f"SELECT * FROM players ORDER BY games_won DESC, games_played ASC")
        return [[user_info[USERNAME_INDEX], user_info[GAMESPLAYED_INDEX], user_info[GAMESWON_INDEX]] for user_info in self.c.fetchall()]

    # for tests only
    def getAllMatches(self):
        self.c.execute(f"SELECT * FROM matches")
        return self.c.fetchall()

    def getAllUsers(self):
        self.c.execute(f"SELECT * FROM players")
        return self.c.fetchall()

    def getAllUsers2(self):
        self.c.execute(f"SELECT * FROM players")
        return [[user_info[NAME_INDEX], user_info[USERNAME_INDEX], user_info[GAMESPLAYED_INDEX], user_info[GAMESWON_INDEX]] for user_info in self.c.fetchall()]


def main():
    pass


if __name__ == "__main__":
    main()
