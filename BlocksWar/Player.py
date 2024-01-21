import pygame
import math
import random
import base64
from constants import *
import pickle
import select
import traceback
import sys

FULL_HP = 1000
MAX_LIFE = 3
FULL_ENERGY = 100
PUSH_FACTOR = 0.1
ENERGY_FACTOR = 0.2
MOVE_FACTOR = 2
JUMP_FACTOR = 5
GRAVITY = -0.25
PUSH_MOVE_FACTOR = 20
FRICTION = 0.5
MAX_JUMPS = 2
PATH = r"pics/"
REGULAR_COLOR = (24, 255, 255)
REGULAR_PIC = "regular"
PUNCH_PIC = "punch"
SWORD_PIC = "sword"
GUN_PIC = "gun"
MAX_HEIGHT = 409
MAX_BULLETS = 10


GAME_ENDED = "!game over"
SPLIT_CHAR = "+"
WINDOW_WIDTH = 728
WINDOW_HEIGHT = 409
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FONT = "bowlbyonesc"


empty_gun_sound = pygame.mixer.Sound('sounds/Empty_gun.wav')


class User:
    def __init__(self):
        self.name = ""
        self.username = ""
        self.password = ""
        self.games_played = 0
        self.games_won = 0
        self.img_bytes = ""
        self.img = PygameConstans.USER.value[IMG_INDEX]

    def changeImg(self, img_path):
        self.img = pygame.transform.scale(pygame.image.load(img_path), (250, 250))
        self.img_bytes = pygame.image.tostring(self.img, "RGBX", False)
        self.img_bytes = base64.b64encode(self.img_bytes)

    def getImg(self):
        return self.img

    def getImgBytes(self):
        return self.img_bytes

    def isGuest(self):
        # only guests can have password ""
        if self.password == "":
            return True
        return False

    def set_games_won(self, games_won):
        self.games_won = games_won

    def set_games_played(self, games_played):
        self.games_played = games_played

    def getPassword(self):
        return self.password

    def getUserName(self):
        return self.username

    def getName(self):
        return self.name

    def getGamesPlayed(self):
        return self.games_played

    def getGamesWon(self):
        return self.games_won

    # set from server
    def set_all(self, data):
        """
        func to get all the data about the user from the server's database
        :param data: the data about the user from the server
        (data will look like:[name, username, game_played, games_won, img_bytes])
        :return: None
        """
        self.name = data[0]
        self.username = data[1]
        self.games_played = data[2]
        self.games_won = data[3]
        self.img_bytes = data[4]
        if not self.img_bytes == "":
            self.img_bytes = base64.b64decode(self.img_bytes)
            self.img = pygame.image.fromstring(self.img_bytes, (250, 250), 'RGBX')

    def setUserName(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def __str__(self):
        return f"name: {self.name}, username: {self.username}, games_played: {self.games_played}, games_won: {self.games_won}"


class Bullet:
    def __init__(self, x, y, direction, shot_by):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = None
        self.bulletPower = 2
        self.shot_by = shot_by

    def getPosition(self):
        return self.x, self.y

    def getDirection(self):
        return self.direction

    def setImage(self):
        if self.direction == "right":
            self.image = Images.BULLET.value
        else:
            self.image = pygame.transform.flip(Images.BULLET.value, True, False)

    def get_Image(self):
        return self.image

    def move(self):
        if self.direction == "right":
            self.x += GameConstans.BULLET_SPEED.value
        else:
            self.x -= GameConstans.BULLET_SPEED.value

    def hittedPlayer(self, players):
        for index_of_player, player in enumerate(players):
            if self.isTouch(player) and self.shot_by != index_of_player:
                player.set_hitted_x(self.x)
                player.set_hitted_power(self.bulletPower)
                player.set_hitted(True)
                player.got_hit()
                return True
        return False

    def isTouch(self, player):
        """
        func to check whether the bullet hit specific player
        :param player: the player to check if got hit by the bullet
        :return: bool
        """
        dis_x = math.fabs(player.get_x() - self.x)
        dis_y = math.fabs(player.get_y() - self.y)
        dis_t = math.sqrt(math.pow(dis_x, 2) + math.pow(dis_y, 2))
        if dis_t < Images.BULLET_SIZE.value:
            return True
        return False


class Mode:
    def __init__(self, is_single_player, is_ai):
        self.is_single_player = is_single_player
        self.is_ai = is_ai

    def getSinglePlayer(self):
        return self.is_single_player

    def getIsAI(self):
        return self.is_ai

    def setIsSinglePlayer(self, is_single_player):
        self.is_single_player = is_single_player

    def setIsAI(self, is_ai):
        self.is_ai = is_ai


class BasicSettings:
    def __init__(self, basic_setting_list):
        if basic_setting_list is not None:
            self.is_none = False
            self.index_of_background = basic_setting_list[0]
            self.index_of_color = basic_setting_list[1]
            self.index_of_hats = basic_setting_list[2]
            self.joystick = basic_setting_list[3]
        else:
            self.is_none = True


class Player:
    def __init__(self):
        self.hp = FULL_HP                   # helth point
        self.life_count = MAX_LIFE          # the amount of life
        self.dead = False                   # bolian that say if the player is dead
        self.energy = FULL_ENERGY
        self.punch_hit_power = 2            # power of punch hit
        self.gun_hit_power = 1              # power of gun hit
        self.sword_hit_power = 5            # power of sword hit
        self.x = random.randint(0, 500)      # x position
        self.y = 0                          # y position
        self.direction = "right"            # direction of player(left/right)
        self.hit_kind = "regular"           # can be
        self.kind_of_pic = "walk"
        self.current = None                 # current shown picture
        self.y_vel = 0                      # velocity of player while falling
        self.pics = []                      # list of the pictures of the players(started as empty)
        self.pics_mirror = []               # pics but mirrored(started as empty)
        self.rect = None
        self.jump_count = 0                 # counting how many jumps the player made(so the player wont be able to jump forever)
        # self.path = None
        self.color = ""                     # color of the player
        self.socket = None                  # socket to comunicate with server
        self.hitted = False
        self.hitted_power = 0
        self.hitted_x = None
        self.hit = False
        self.last_time_hitted = pygame.time.get_ticks()
        self.push_vel = 0
        self.push_acceleration = PUSH_MOVE_FACTOR
        self.final_point_push = None
        self.name = None
        self.passw = None
        self.is_logedin = False
        self.bullet_amount = MAX_BULLETS
        self.last_time_gun = pygame.time.get_ticks()
        self.index_of_hat = None
        self.in_pick_color = False
        self.hat_img = None
        self.quit_game = False

    def isQuit(self):
        return self.quit_game

    def quitPlayer(self):
        self.quit_game = True

    def set_hat(self, index_of_hat):
        if index_of_hat==0:
            self.index_of_hat = None
        else:
            self.index_of_hat = index_of_hat

    def get_hat(self):
        return self.index_of_hat

    def get_hat_img(self):
        return self.hat_img

    def getBulletsAmount(self):
        return self.bullet_amount

    def isLogedin(self):
        return self.is_logedin

    def set_login(self, is_logedin):
        self.is_logedin = is_logedin

    def __str__(self):
        return(f"""color: {self.color} {type(self.color)}\n
        x: {self.x} {type(self.x)}\n
        y: {self.y} {type(self.y)}\n
        name: {self.name}\n""")

    def set_hitted_power(self, hitted_power):
        self.hitted_power = hitted_power

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_hitted_power(self):
        return self.hitted_power

    def get_hitted_x(self):
        return self.hitted_x

    def set_hitted_x(self, hitted_x):
        self.hitted_x = hitted_x

    def is_hitted(self):
        return self.hitted

    def get_all(self):
        return [self.hp, self.energy, self.x, self.y, self.hit_kind]

    def set_all(self, hp, x, y, hit_kind):
        self.hp = hp
        self.x = x
        self.y = y

    def check(self):
        return self.color #+ "/walk.png"

    def set_pics(self):
        """
        func set the pictures of the player into list.
        :return: None
        """
        print(PATH + self.color + "/walk.png")
        self.pics.append(pygame.image.load(PATH + self.color + "/walk.png").convert())
        self.pics_mirror.append(pygame.transform.flip(self.pics[0], True, False))
        self.pics.append(pygame.image.load(PATH + self.color+"/punch.png"))
        self.pics_mirror.append(pygame.transform.flip(self.pics[-1], True, False))
        self.pics.append(pygame.image.load(PATH + self.color+"/sword.png"))
        self.pics_mirror.append(pygame.transform.flip(self.pics[-1], True, False))
        self.pics.append(pygame.image.load(PATH + self.color+"/gun.png"))
        self.pics_mirror.append(pygame.transform.flip(self.pics[-1], True, False))
        self.current = self.pics[0]
        self.kind_of_pic = "walk"
        if self.index_of_hat is not None:
            self.hat_img = PygameConstans.HATS_IMGS.value[IMG_INDEX][self.index_of_hat]
        self.rect = self.pics[0].get_rect(topleft=(self.x, self.y))

    def drawHealth(self, screen):
        """
        func to draw health bar on top of the player
        :param screen: the screen
        :return: None
        """
        if not self.is_dead():
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y-20, 50, 10))
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y-20, int(50 * (self.hp / FULL_HP)), 10))
            pygame.draw.rect(screen, (0, 0, 0,), (self.x-1, self.y-21, 52, 12), 1)

    def get_walk_pics(self):
        return self.pics[0], self.pics_mirror[0]

    def rem(self):
        self.current = self.pics_mirror[-3]
        self.current = self.pics_mirror[-2]
        self.current = self.pics_mirror[-1]

    def punch(self):
        """
        func change users image to punch
        :return: None
        """
        if self.direction == "left":
            self.kind_of_pic = "punch"
            self.current = self.pics_mirror[-3]
            self.x -= MOVE_FACTOR
        else:
            self.current = self.pics[-3]
            self.kind_of_pic = "punch"
            self.x += MOVE_FACTOR
        self.rect = self.current.get_rect(topleft=(self.x, self.y))

    def sword(self):
        """
        func change users image to sword
        :return: None
        """
        if self.direction == "left":
            self.kind_of_pic = "sword"
            self.current = self.pics_mirror[-2]
            self.x -= MOVE_FACTOR
        else:
            self.kind_of_pic = "sword"
            self.current = self.pics[-2]
            self.x += MOVE_FACTOR
        self.rect = self.current.get_rect(topleft=(self.x, self.y))

    def gun(self):
        """
        func change users image to gun
        :return: None
        """
        if self.bullet_amount > 0:
            self.bullet_amount -= 1
            if self.direction == "left":
                self.kind_of_pic = "gun"
                self.current = self.pics_mirror[-1]
                self.x += MOVE_FACTOR
            else:
                self.kind_of_pic = "gun"
                self.current = self.pics[-1]
                self.x -= MOVE_FACTOR
        else:
            pygame.mixer.Channel(pygame.mixer.get_num_channels()-2).play(empty_gun_sound)
        self.rect = self.current.get_rect(topleft=(self.x, self.y))

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def get_kind_of_pic(self):
        return self.kind_of_pic

    def set_kind_of_pic(self, kind_of_pic):
        self.kind_of_pic = kind_of_pic

    def get_socket(self):
        return self.socket

    def set_socket(self, socket):
        self.socket = socket

    def check_fell_of_screen(self):
        """
        func check if the player fell of the screen
        :return: None
        """
        if self.y > MAX_HEIGHT:
            self.life_count -= 1
            if self.life_count == 0:
                print ("dead")
                self.dead = True
            else:
                self.hp = FULL_HP
                self.y_vel = 0
                self.push_vel = 0
                self.push_acceleration = 0
                self.hitted = False
                self.x = random.randint(0, 500)  # x position
                self.y = 0  # y position

    def falling(self):
        """
        func move the player in the y dimention
        :return: None
        """
        on_ground = False
        for floor in GameConstans.FLOORS_RECTS.value:       # for every floor
            if self.rect.colliderect(floor):        # if touche
                if self.y < math.ceil(floor.top):   # if on top of it
                    on_ground = True
                    self.y_vel = 0
                    self.y = math.ceil(floor.top - 50)
                    self.jump_count = 0
                elif floor.top < self.y < floor.bottom:     # if on the between top and bottom
                    if abs(floor.bottom - self.y) < 10:
                        self.y = floor.bottom
                        self.y_vel = 0
                    else:
                        self.y_vel = 0
                        self.jump_count = 0
                        if abs(self.x - floor.left) > abs(self.x - floor.right):
                            self.x = floor.right
                        else:
                            self.x = floor.left - 50
                else:   # if touch in bottom
                    self.y = floor.bottom
                    self.y_vel = 0
        if not on_ground:
            self.y_vel += GRAVITY
            self.y -= self.y_vel

    def move_x_dimention(self, change_x):
        """
        func moves the player in the x dimention
        :param change_x: tells the directrection to move to
        :return: None
        """
        if change_x > 0:
            self.x -= MOVE_FACTOR
        if change_x < 0:
            self.x += MOVE_FACTOR

    def move_by_push(self):
        """
        func moves the user by power of hitting
        :return: None
        """
        if self.x > self.final_point_push:
            if self.x - self.push_acceleration <= self.final_point_push:    # if got to the final point from left
                self.x = self.final_point_push
                self.hitted = False
                self.push_acceleration = PUSH_MOVE_FACTOR
            else:
                self.x -= self.push_acceleration
                if self.push_acceleration - FRICTION < 1:
                    self.push_acceleration = 1
                else:
                    self.push_acceleration += 8
        elif self.x < self.final_point_push:
            if self.x + self.push_acceleration >= self.final_point_push:    # if got to the final point from right
                self.x = self.final_point_push
                self.hitted = False
                self.push_acceleration = PUSH_MOVE_FACTOR
            else:
                self.x += PUSH_MOVE_FACTOR
                if self.push_acceleration - FRICTION < 1:
                    self.push_acceleration = 1
                else:
                    self.push_acceleration += 8
        else:
            self.hitted = False
            self.push_acceleration = PUSH_MOVE_FACTOR

    def move(self, change_x, is_single_player=False):
        """
        func moves the player
        :param is_single_player: whether the user picked single player mode
        :param change_x: where the player want to move in x
        :return: None
        """
        if is_single_player:
            # I decided to let the player infinite bullets and life counts
            # so every time i enter this function, I update it to the start amount
            self.life_count = MAX_LIFE+1
            self.bullet_amount = MAX_BULLETS
        if not self.dead:
            self.check_fell_of_screen()     # check if the player fell ot of the screen
            self.falling()                  # move the player down like he is falling
            if not self.hitted:     # if the player didn't get hit
                self.move_x_dimention(change_x)
            else:
                self.move_by_push()
            self.rect = self.current.get_rect(topleft=(self.x, self.y + 1))

    def is_dead(self):
        return self.dead

    def set_dead(self, is_dead):
        self.dead = is_dead

    def get_push_acceleration(self):
        return self.push_acceleration

    def got_hit(self):
        """
        called when player gets hit, func tell how far he need to go from the hit
        :return: None
        """
        if pygame.time.get_ticks() - self.last_time_hitted > 150:
            self.last_time_hitted = pygame.time.get_ticks()     # last time that the user got hit(so he wouldn't get hit twice in a row)
            self.hitted = True  # whether the player got hit
            if not self.hp - self.hitted_power <= 0:    # making sure that hp doesn't get below 1
                self.hp -= self.hitted_power
            else:
                self.hp = 1
            if not self.energy - self.hitted_power * ENERGY_FACTOR <= 0:    # making sure that energy doesn't get below 1
                self.energy -= self.hitted_power * ENERGY_FACTOR
            else:
                self.energy = 1
            # this variable contain the amount of pixels that the player need to move.
            # this amount is mathematics calculation by the power of the hit, the energy of the player and the hp
            push = math.sqrt(self.hitted_power * (FULL_ENERGY-self.energy) * (FULL_HP-self.hp) * PUSH_FACTOR)
            if self.hitted_x > self.x:      # picking the direction he need to go to
                self.final_point_push = self.x - push
            else:
                self.final_point_push = self.x + push

    def get_hit_power(self):
        return self.punch_hit_power

    def get_sword_power(self):
        return self.sword_hit_power

    def get_gun_power(self):
        return self.gun_hit_power

    def get_hitted(self):
        return self.hitted

    def set_hitted(self, hitted):
        self.hitted = hitted

    def get_pic(self):
        return self.current

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def set_pic(self, pic):
        self.current = pic

    def set_pic_by_name(self):
        """
        func change the image by the name of it
        :return: None
        """
        if self.direction == "right":
            if self.kind_of_pic == "walk":
                self.current = self.pics[0]
            elif self.kind_of_pic == "punch":
                self.current = self.pics[-3]
            elif self.kind_of_pic == "sword":
                self.current = self.pics[-2]
            else:
                self.current = self.pics[-1]
        else:
            if self.kind_of_pic == "walk":
                self.current = self.pics_mirror[0]
            elif self.kind_of_pic== "punch":
                self.current = self.pics_mirror[-3]
            elif self.kind_of_pic == "sword":
                self.current = self.pics_mirror[-2]
            else:
                self.current = self.pics_mirror[-1]

    def move_left(self):
        self.x -= MOVE_FACTOR

    def move_right(self):
        self.x += MOVE_FACTOR

    """def fall(self):
        self.y_vel -= GRAVITY
        if self.y - self.y_vel > 50:

            self.y += self.y_vel
        else:
            self.y = 50
            self.jump_count = 0"""

    """def end_fall(self):
        self.y_vel = 0
        self.jump_count = 0"""

    def jump(self):
        """
        func move the player uppward
        :return:
        """
        if not self.jump_count == MAX_JUMPS:
            self.y_vel = JUMP_FACTOR
            self.y -= self.y_vel
            self.y_vel += GRAVITY
            self.jump_count += 1
            self.rect = self.current.get_rect(topleft=(self.x, self.y + 1))

    def get_life_count(self):
        return self.life_count

    def decrease_life(self):
        self.life_count -= 1
        if self.life_count == 0:
            self.dead = True
        else:
            self.hp = FULL_HP
            self.y_vel = 0
            self.push_vel = 0
            self.push_acceleration = 0
            self.hitted = False

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_hp(self):
        return self.hp

    def getRect(self):
        return self.rect

    def set_hp(self, hp):
        self.hp = hp

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
