# This file is responsible to run the game and comunicate with the server

import pygame
from socketFunctions import *
from Player import Bullet
import math
from BotFunctions import *
empty_gun_sound = pygame.mixer.Sound('sounds/Empty_gun.wav')
gun_sound = pygame.mixer.Sound('sounds/Gun.wav')
punch_hit_sound = pygame.mixer.Sound('sounds/Punch_hit.wav')
punch_miss_sound = pygame.mixer.Sound('sounds/Punch_miss.wav')
sword_miss_sound = pygame.mixer.Sound('sounds/Sword_miss.wav')
sword_hit_sound = pygame.mixer.Sound('sounds/sword_hit.wav')
pygame.mixer.set_num_channels(10)

PUNCH_TIME_DELAY = 100
SWORD_TIME_DELAY = 200
GUN_TIME_DELAY = 300
AI_INDEX = 1

IS_DEAD_INDEX = 0
X_POSITION_INDEX = 1
Y_POSITION_INDEX = 2
DIRECTION_POSITION = 3
IMG_KIND_INDEX = 4
HP_INDEX = 5
IS_GOT_HIT_INDEX = 6
POWER_HIT_INDEX = 7
HIT_X_INDEX = 8

STAY = 0


class Game:
    def __init__(self, mode_obj, screen, my_socket):
        self.mode_obj = mode_obj
        self.change_x = 0       # direction the user want to go to
        self.over = False       # is the game over
        self.last_time_hit = pygame.time.get_ticks()        # the time of the last time the user hit
        self.last_time_hit_ai = pygame.time.get_ticks()     # the tune of the last time the ai hit
        self.is_dead_sent = False  # bool var that say if the client sent that the player died
        self.changed_back = True  # bool var that say if after the hit, the screen return the pic to the regular pic
        self.ai_changed_back = True # bool var that say if after the hit, the pic returned to the regular pic of ai
        self.sounds = [pygame.mixer.Channel(i) for i in range(0, 8)]    # make sounds channels
        self.hits_sounds = []       # list of the sounds
        self.players = []           # list of the players
        self.bullets = []           # list of the bullets
        self.self_index = None      # index of the user in the list of the players
        self.last_coordinates = (10, 0) # last coordinates the user were when he sent the last packet
        self.last_pic = None            # last image of the character to return to
        self.last_pic_sent = None       # last image that sent to the server
        self.screen = screen            # the screen
        self.my_socket = my_socket      # the socket to comunicate with the server
        self.break_out_of_func = False  # boolean that say that the user want to exit the game
        self.ai_path = []

    def isOver(self):
        return self.over

    def play_sound(self, kind_of_pic, index_of_user):
        """
        func to play sound of hit
        :param kind_of_pic: name of the img(punch, sword or gun)
        :param index_of_user: index of the user that hit
        :return: None
        """
        if not self.sounds[index_of_user].get_busy():
            if kind_of_pic == "punch":
                self.sounds[index_of_user].play(punch_miss_sound)
            elif kind_of_pic == "sword":
                self.sounds[index_of_user].play(sword_miss_sound)
            elif kind_of_pic == "gun":
                self.sounds[index_of_user].play(gun_sound)

    def play_sounds(self, hits_sounds):
        """
        func to play sounds got fro the server
        :param hits_sounds: list if the sounds
        :return: None
        """
        for sound in hits_sounds:
            if sound[0] == "punch":
                self.sounds[sound[1]+4].play(punch_hit_sound)
            elif sound[0] == "sword":
                self.sounds[sound[1] + 4].play(sword_hit_sound)
            elif sound[0] == "bullet":
                self.sounds[sound[1] + 4].play(gun_sound)

    def create_players_objects(self, stats):
        """
        func create players objects from the data from the server
        :param stats: the data from the server
        :return: list of Player object
        """
        print("stats is next")
        print(stats)
        for i_player in range(len(stats)):
            player_color = stats[i_player][0]
            player_x = stats[i_player][1]
            player_y = stats[i_player][2]
            self.players.append(Player())
            self.players[i_player].set_pos(player_x, player_y)
            self.players[i_player].set_color(player_color)
            self.players[i_player].set_hat(stats[i_player][3])

    def prepare_game(self):
        """
        func make the preparetions before the game
        """
        stats = pickle.loads(receive_data_pickle(self.my_socket, self.screen))
        data = pickle.loads(receive_data_pickle(self.my_socket, self.screen))
        print(data, stats)
        while data[0] != "index":
            stats = pickle.loads(receive_data_pickle(self.my_socket, self.screen))
            data = pickle.loads(receive_data_pickle(self.my_socket, self.screen))
            print(data, stats)
        self.self_index = data[1]
        self.create_players_objects(stats)

    def init_players(self, basic_user_settings):
        """
        func to create objects of the plaeyrs in the game
        :param basic_user_settings: object of basicSettings
        :return: None
        """
        COLOR_LIST = ["red", 'blue', "green", "pink", "brown", "black", "yellow"]
        # create 2 players, one for the user and one for the bot/puppet
        if self.mode_obj.is_single_player:
            self.self_index = 0
            self.players = [Player(), Player()]
            self.players[self.self_index].set_color(COLOR_LIST[basic_user_settings.index_of_color])
            self.players[self.self_index].set_hat(basic_user_settings.index_of_hats)
            self.players[AI_INDEX].set_color("red")
            self.players[self.self_index].set_pics()
            self.players[AI_INDEX].set_pics()
            self.players[AI_INDEX].set_x(450)
            self.players[self.self_index].set_x(450)
            self.players[self.self_index].set_y(250)
        # get players from the server
        else:
            self.prepare_game()
            # load images of the players
            for player in self.players:
                player.set_pics()

    def setInitialStats(self, basic_user_settings):
        """
        func to init the basic of the game
        :param basic_user_settings: object that hold the color of the user, hat of the user and background
        :return: None
        """
        self.init_players(basic_user_settings)
        self.last_coordinates = (self.players[self.self_index].get_x(), self.players[self.self_index].get_y())
        self.last_pic = self.players[self.self_index].get_pic()
        self.last_pic_sent = self.players[self.self_index].get_pic()
        self.screen.blit(PygameConstans.BACKGROUND.value, (0, 0))

    def run_game(self, basic_user_settings):
        """
        This is the main func of the game.
        It communicate with the server, shows the game, and receive data from the user
        :param basic_user_settings: object that hold the color of the user, hat of the user and background
        :return: None
        """
        self.setInitialStats(basic_user_settings)
        # main loop
        while not self.isOver() and not self.break_out_of_func:
            # draw the board
            self.drawGameScreen(basic_user_settings.index_of_background)
            # handle user inputs
            self.handleUserInputs(basic_user_settings)
            if not self.mode_obj.is_single_player:
                # send and receive data
                self.over = self.handleNewDataInGame(new_data(self.my_socket, self.screen))
                self.multiPlayerPart()
            else:
                self.handleBullets()
                # move the enemy
                if self.mode_obj.is_ai:
                    self.moving_ai()
                else:
                    self.players[AI_INDEX].move(STAY, self.mode_obj.is_single_player)
            # move the player
            self.players[self.self_index].move(self.change_x, self.mode_obj.is_single_player)
        if self.break_out_of_func:
            return None
        return self.players

    def handleBullets(self):
        """
        func to move bullets on the screen, and handle the clients that got hit from the bullets
        :return: list of the bullets
        """
        remove_bullets = []
        for index, bullet in enumerate(self.bullets):
            bullet.move()
            if (bullet.getDirection() == "right" and bullet.getPosition()[0] > WINDOW_WIDTH) or \
                    (bullet.getDirection() == "left" and bullet.getPosition()[0] < 0) or \
                    (bullet.hittedPlayer(self.players)):
                remove_bullets.append(index)
                if bullet.hittedPlayer(self.players):
                    print("need to play sound")
        for index_bullet_to_remove in reversed(remove_bullets):
            self.bullets.pop(index_bullet_to_remove)

    def moving_ai(self):
        """
        func to handle the ai.
        this function move the ai, and make him hit the player
        :return: None
        """
        if self.is_touch(self.players[self.self_index], self.players[AI_INDEX]) and pygame.time.get_ticks() - self.last_time_hit_ai > 300:
            self.hitAi()
        elif pygame.time.get_ticks() - self.last_time_hit_ai > 150:
            self.returnToWalkImgAI()
        self.moveAI()

    def returnToWalkImgAI(self):
        """
        func to change the ai image to walk img
        :return: None
        """
        self.players[AI_INDEX].set_kind_of_pic("walk")
        if self.players[AI_INDEX].get_direction() == "left":
            self.players[AI_INDEX].set_pic(self.players[AI_INDEX].get_walk_pics()[1])
        else:
            self.players[AI_INDEX].set_pic(self.players[AI_INDEX].get_walk_pics()[0])

    def hitAi(self):
        """
        func for the ai to hit the user
        :return: None
        """
        self.last_time_hit_ai = pygame.time.get_ticks()
        if random.randint(1, 2) == 1:
            self.players[AI_INDEX].sword()
        else:
            self.players[AI_INDEX].punch()
        self.players[self.self_index].set_hitted(True)
        self.players[self.self_index].set_hitted_x(self.players[AI_INDEX].get_x())
        self.players[self.self_index].set_hitted_power(self.players[AI_INDEX].get_hit_power())
        self.players[self.self_index].got_hit()

    def moveAI(self):
        """
        func to pick which way to move the ai, and move it
        :return: None
        """
        if self.ai_path != []:
            if self.ai_path[0] == "right":
                self.moveAiRight()
            elif self.ai_path[0] == "left":
                self.moveAiLeft()
            elif self.ai_path[0] == "jump":
                self.players[1].jump()
            elif self.ai_path[0] is None:
                self.players[AI_INDEX].move(0, True)
            else:
                print(self.ai_path[0])
            self.ai_path = self.ai_path[1:]
        else:
            self.ai_path = pickWay(self.players[self.self_index], self.players[AI_INDEX])
            # move right
            if self.players[self.self_index].get_x() > self.players[AI_INDEX].get_x() + 45:
                self.moveAiRight()
            # move left
            elif self.players[self.self_index].get_x() < self.players[AI_INDEX].get_x() - 45:
                self.moveAiLeft()
            # stay
            else:
                self.players[AI_INDEX].move(STAY, True)

    def moveAiRight(self):
        """
        func to move the ai player to the right
        :return: None
        """
        self.players[AI_INDEX].set_direction("right")
        self.players[AI_INDEX].set_pic(self.players[AI_INDEX].get_walk_pics()[0])
        self.players[AI_INDEX].move(-1, True)

    def moveAiLeft(self):
        """
        func to move the ai left
        :return: None
        """
        self.players[AI_INDEX].set_direction("left")
        self.players[AI_INDEX].set_pic(self.players[AI_INDEX].get_walk_pics()[1])
        self.players[AI_INDEX].move(1, True)

    def handleUserInputs(self, basic_user_settings):
        """
        func to pick which function to pick to handle user inputs
        :param basic_user_settings:
        :return:
        """
        if basic_user_settings.joystick is not None:
            self.handleUserJoystick(basic_user_settings.joystick)
        else:
            self.handleUserKeyboard()

    def handleUserJoystick(self, joystick):
        """
                func handle the user clicks
                """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.getOutOfGame()
            if self.players[self.self_index].is_dead():
                break
            if joystick.get_axis(0) <= -0.5:  # left
                self.moveLeft()
            elif joystick.get_axis(0) >= 0.5:  # right
                self.moveRight()
            else:
                self.change_x = 0
            if event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(5):
                    self.getOutOfGame()
                if joystick.get_button(2):  # jump:
                    self.players[self.self_index].jump()
                if joystick.get_button(3) and pygame.time.get_ticks() - self.last_time_hit > 100:   # punch
                    self.hitFunc("punch")
                if joystick.get_button(1) and pygame.time.get_ticks() - self.last_time_hit > 200:   # sword
                    self.hitFunc("sword")
                if joystick.get_button(0) and pygame.time.get_ticks() - self.last_time_hit > 300:   # gun
                    self.hitFunc("gun")
        if not self.changed_back and pygame.time.get_ticks() - self.last_time_hit > 100 and not self.players[self.self_index].is_dead():
            self.changeBack()

    def handleUserKeyboard(self):
        """
        func handle the user clicks
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.getOutOfGame()
            if self.players[self.self_index].is_dead():
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.getOutOfGame()
                if event.key == pygame.K_UP:
                    self.players[self.self_index].jump()
                if event.key == pygame.K_LEFT:
                    self.moveLeft()
                if event.key == pygame.K_RIGHT:
                    self.moveRight()
                if event.key == pygame.K_1 and pygame.time.get_ticks() - self.last_time_hit > PUNCH_TIME_DELAY:
                    self.hitFunc("punch")
                if event.key == pygame.K_2 and pygame.time.get_ticks() - self.last_time_hit > SWORD_TIME_DELAY:
                    self.hitFunc("sword")
                if event.key == pygame.K_3 and pygame.time.get_ticks() - self.last_time_hit > GUN_TIME_DELAY:
                    self.hitFunc("gun")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.change_x = 0
        # print(f"{not game_object.changed_back} {pygame.time.get_ticks() - game_object.last_time_hit > 100}")
        if not self.changed_back and pygame.time.get_ticks() - self.last_time_hit > GUN_TIME_DELAY and not self.players[
            self.self_index].is_dead():
            self.changeBack()

    def changeBack(self):
        """
        func to change user img back from hitting img to walk img
        :return: None
        """
        self.players[self.self_index].set_pic(self.last_pic)
        self.players[self.self_index].set_kind_of_pic("walk")
        self.changed_back = True
        if not self.mode_obj.is_single_player:
            self.send_data_on_player()

    def moveLeft(self):
        """
        func to move the user to the left
        :return: None
        """
        self.change_x = 1
        if self.changed_back:
            self.players[self.self_index].current = self.players[self.self_index].pics_mirror[0]
            self.players[self.self_index].direction = "left"
            self.players[self.self_index].kind_of_pic = "walk"
            self.last_pic = self.players[self.self_index].get_walk_pics()[1]

    def moveRight(self):
        """
        func to move the user to the right
        :return: None
        """
        MOVE_LEFT = -1

        self.change_x = -1
        if self.changed_back:
            self.players[self.self_index].current = self.players[self.self_index].pics[0]
            self.players[self.self_index].direction = "right"
            self.players[self.self_index].kind_of_pic = "walk"
            self.last_pic = self.players[self.self_index].get_walk_pics()[0]

    def getOutOfGame(self):
        """
        func to get out of the game
        :return: None
        """
        if not self.mode_obj.is_single_player:
            send_data_socket_pickle(self.my_socket, pickle.dumps(clientReq.RETURN_TO_LOBY_REQ.value))
        self.break_out_of_func = True

    def send_data_on_player(self):
        """
        func send properties of the player to the server
        :return: None
        """
        player = self.players[self.self_index]
        data = [player.is_dead(), player.get_x(), player.get_y(), player.get_direction(), player.get_kind_of_pic(),
                player.get_hitted()]
        data = pickle.dumps(data)
        self.send_data_socket_pickle(self.my_socket, data)

    def send_data_socket_pickle(self, socket, data):
        try:
            socket.send((str(len(data)) + SPLIT_CHAR).encode('utf-8') + data)
        except:
            pass

    def hitFunc(self, kind_of_hit):
        """
        func to hit the other player by the kind_of_hit that got
        :param kind_of_hit: kind of hit as a string
        :return: last_time_hit, last_pic, changed_back
        """
        self.last_time_hit = pygame.time.get_ticks()
        if self.players[self.self_index].get_direction == "right":
            self.last_pic = self.players[self.self_index].get_walk_pics()[1]
        else:
            self.last_pic = self.players[self.self_index].get_walk_pics()[0]
        if kind_of_hit == "punch":
            self.players[self.self_index].punch()
        elif kind_of_hit == "sword":
            self.players[self.self_index].sword()
        elif kind_of_hit == "gun":
            self.players[self.self_index].gun()
            if self.mode_obj.is_single_player:
                self.bullets.append(Bullet(self.players[self.self_index].get_x(), self.players[self.self_index].get_y()+10, self.players[self.self_index].get_direction(), self.self_index))
        if self.mode_obj.is_single_player and self.is_touch(self.players[0], self.players[1]):
            self.hitSinglePlayer(kind_of_hit)
        self.changed_back = False

    @staticmethod
    def is_touch(player1, player2):
        """
        func check if 2 players are touching each other
        :param player1: first player
        :param player2: second player
        :return: Bool
        """
        SIZE_OF_CHARACTER = 50
        dis_x = math.fabs(player1.get_x() - player2.get_x())
        dis_y = math.fabs(player1.get_y() - player2.get_y())
        dis_t = math.sqrt(math.pow(dis_x, 2)+math.pow(dis_y, 2))
        if dis_t < SIZE_OF_CHARACTER:
            return True
        return False

    def hitSinglePlayer(self, kind_of_hit):
        """
        func to hit the other player in single mode
        :param kind_of_hit: the jind of the hit(punch/sword)
        :return: None
        """
        self.players[1].set_hitted(True)
        self.players[1].set_hitted_x(self.players[0].get_x())
        if kind_of_hit == "punch":
            self.players[1].set_hitted_power(self.players[0].get_hit_power())
        elif kind_of_hit == "sword":
            self.players[1].set_hitted_power(self.players[0].get_sword_power())
        self.players[1].got_hit()

    def multiPlayerPart(self):
        if self.is_changed() and not self.players[self.self_index].is_dead() and not self.players[
            self.self_index].is_hitted():
            self.send_data_on_player()
            self.last_coordinates = (self.players[self.self_index].get_x(), self.players[self.self_index].get_y())
            # game_object.last_pic_sent = players[self_index].get_pic()
            self.last_pic_sent = self.last_pic
        elif not self.is_dead_sent and self.players[self.self_index].is_dead():
            print("dead msg sent")
            self.send_data_on_player()
            self.is_dead_sent = True

    def is_changed(self):
        """
        func check if the user did anything, and return if he did
        :return: bool
        """
        if self.players[self.self_index].get_x() == self.last_coordinates[0] and self.players[self.self_index].get_y() == self.last_coordinates[
            1] and self.last_pic_sent == self.players[self.self_index].get_pic():
            return False
        return True

    def handleNewDataInGame(self, data):
        """
        func to handle the data about what the server said
        :param data: what the server sent
        :return: None
        """
        if data:
            if data == GAME_ENDED:
                print("over")
                pygame.time.wait(1000)
                over = True
            else:
                self.change_players(data[0])
                self.bullets = data[1]
                self.play_sounds(data[2])
                over = False
            return over
        return False

    def change_players(self, data):
        """
        func change the players list according to the server data
        :param data: what the server sent
        :return: None
        """
        if data:    # if got data from the server
            for i_player in range(len(self.players)):
                if not i_player == self.self_index:
                    # "data" is looks like this: [int X player, int Y player, DIRECION player("left"/"right"),
                    # KIND_OF_PIC("walk"/"punch"/"gun"/sword"), int HP player, bool IS_HITTED player,
                    # int POWER_OF_HIT enemy, int Xenemy]*players amount
                    self.players[i_player].set_dead(data[i_player][IS_DEAD_INDEX])
                    self.players[i_player].set_pos(data[i_player][X_POSITION_INDEX], data[i_player][Y_POSITION_INDEX])  # pos of player
                    self.players[i_player].set_direction(data[i_player][DIRECTION_POSITION])  # direction of player
                    self.players[i_player].set_kind_of_pic(data[i_player][IMG_KIND_INDEX])
                    self.players[i_player].set_pic_by_name()
                self.players[i_player].set_hp(data[i_player][HP_INDEX])
                if data[i_player][IS_GOT_HIT_INDEX]:    # if player got hit
                    self.players[i_player].set_hitted(data[i_player][IS_GOT_HIT_INDEX])
                    self.players[i_player].set_hitted_power(data[i_player][POWER_HIT_INDEX])
                    self.players[i_player].set_hitted_x(data[i_player][HIT_X_INDEX])
                    self.players[i_player].got_hit()

    def drawBullets(self):
        """
        func to draw all of the bullets
        :return: None
        """
        for bullet in self.bullets:
            bullet.setImage()
            self.screen.blit(bullet.get_Image(), (bullet.getPosition()))

    def drawGameScreen(self, index_of_background):
        """
        func to draw players to the screen
        :return: None
        """
        self.screen.blit(PygameConstans.BACKGROUNDS_IMGS_FULLSIZE.value[IMG_INDEX][index_of_background], (0, 0))
        self.drawFloors()
        self.drawPlayers()
        self.drawHealthBar()
        self.drawLeftBullets()
        self.drawBullets()
        if not self.mode_obj.is_single_player:
            self.drawLifes()
        PygameConstans.CLOCK.value.tick(60)
        pygame.display.update()

    def drawLeftBullets(self):
        """
        func to draw how many bullets left to the player
        func will draw it on the left upper corner of the screen
        :return: None
        """
        self.screen.blit(GameConstans.LEFT_BULLETS_IMG.value, (10, 10))
        # if no more bullets left, draw "0" in red color instead of green
        if self.players[self.self_index].getBulletsAmount() > 0:
            self.draw_text(str(self.players[self.self_index].getBulletsAmount()), self.screen, 45, 10, 35, GREEN)
        else:
            self.draw_text(str(self.players[self.self_index].getBulletsAmount()), self.screen, 45, 10, 35, RED)

    @staticmethod
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

    def drawFloors(self):
        """
        func to draw the floors
        :return: None
        """
        for floor_rect in GameConstans.FLOORS_RECTS.value:
            self.screen.blit(GameConstans.FLOOR_IMG.value, floor_rect)

    def drawPlayers(self):
        """
        func to draw the players
        :return: None
        """
        # screen.blit(players[0].get_pic(), (int(players[0].get_x()), int(players[0].get_y())))
        for index, player in enumerate(self.players):
            if index != self.self_index:
                if not player.is_dead():
                    self.screen.blit(player.get_pic(), (int(player.get_x()), int(player.get_y())))
                    if player.get_hat() is not None:
                        self.screen.blit(player.get_hat_img(), (int(player.get_x() - 5), int(player.get_y() - 50)))
            self.play_sound(player.get_kind_of_pic(), index)
        self.screen.blit(self.players[self.self_index].get_pic(), (int(self.players[self.self_index].get_x()), int(self.players[self.self_index].get_y())))
        if self.players[self.self_index].get_hat() is not None:
            self.screen.blit(self.players[self.self_index].get_hat_img(), (int(self.players[self.self_index].get_x() - 5), int(self.players[self.self_index].get_y() - 50)))

    def drawHealthBar(self):
        """
        func to draw health bar for all of the players
        :return: None
        """
        for player in self.players:
            player.drawHealth(self.screen)

    def drawLifes(self):
        """
        func to draw the amount of lifes the player left
        :return: None
        """
        DISTANCE_BETWEEN_HEARTS = 40
        DISTANCE_FROM_RIGHT = 35
        for ii in range(self.players[self.self_index].get_life_count()):
            self.screen.blit(GameConstans.HEART_IMG.value, (WINDOW_WIDTH - DISTANCE_FROM_RIGHT - ii*DISTANCE_BETWEEN_HEARTS, 5))
