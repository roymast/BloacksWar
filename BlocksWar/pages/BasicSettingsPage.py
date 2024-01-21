# This file is for displaying basic settings page
# This page let the user pick his character for the game, its hat and the background

from pages.Page import *
from pages.JoystickPage import JoystickPickPage

COUNTER_INDEX = 2
TOP_LIMITATION = 100


class BasicSettingsPage(Page):
    """
    child class of Page.
    this class is for the user to pick his character for the game, the hat, and the background.
    in the page the user will also see the other player characters, hats and background.
    after everyone picked there colors, the users can start the game
    """
    def __init__(self, screen, is_single_player, user, my_socket):
        super().__init__()
        # images and rects of the characters the user can pick from, and the podium which the the users character are on
        self.players_images, self.players_rects, self.podium_img = setPlayersImages(50 + 64, 110 - 100)
        self.screen = screen
        self.is_single_player = is_single_player
        self.user = user
        self.my_socket = my_socket
        # players_got is list which represent the users characters and hats
        if self.is_single_player:
            self.players_got = [["", None, ""], ["red", None, ""]]
        else:
            self.players_got = [["", None, ""], ["", None, ""]]
        self.index_of_background = 0  # index of wanted background
        self.index_of_hats = 0  # index of wanted hat
        self.index_of_color = None  # index of wanted color
        self.joystick = None  # the joystick
        self.in_waiting = False  # whether the user is in waiting room(turn into true after the user pick his color
        self.start_flag = False  # whether the game started
        self.requierments_msgs = []  # list to print to screen msg of what the requierment to get the specific item
        self.locked_hats, self.locked_backgrounds = self.setLockedItems()   # lists of locked hats and of backgrounds

    def goToPage(self):
        while self.start_flag is not None and not self.start_flag:
            self.screen.fill((128, 128, 128))
            self.handleUserInputs()
            # get the characters of the other players to draw to the screen
            if not self.is_single_player:
                self.getOtherColorsWatingRoom()
            # draw everything on the screen
            self.displayPage()
        if self.start_flag is None:
            return None
        return self.index_of_background, self.index_of_color, self.index_of_hats, self.joystick

    def handleUserInputs(self):
        """
        func to handle the user inputs
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame(self.screen, self.my_socket)
            if not self.in_waiting:
                # if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.index_of_background = self.pickItem(event, PygameConstans.BACKGROUNDS_IMGS.value[RECT_INDEX], self.locked_backgrounds, self.requierments_msgs, self.index_of_background)
                    self.index_of_hats = self.pickItem(event, PygameConstans.HATS_IMGS.value[RECT_INDEX], self.locked_hats, self.requierments_msgs, self.index_of_hats)
                    self.index_of_color = self.pickItem(event, self.players_rects, [], self.requierments_msgs, self.index_of_color)
                    if self.in_waiting and PygameConstans.START_GAME_IMG.value[RECT_INDEX].collidepoint(event.pos):
                        send_data_socket_pickle(self.my_socket, pickle.dumps(START_GAME_ORDER))
                    if PygameConstans.CONFIRM_BUTTON.value[RECT_INDEX].collidepoint(event.pos) and self.index_of_color is not None and not self.in_waiting:
                        if self.is_single_player:
                            self.start_flag = True
                        else:
                            send_data_socket_pickle(self.my_socket, pickle.dumps(["color", PygameConstans.COLOR_LIST.value[self.index_of_color], self.index_of_hats]))
                            self.in_waiting = True
                    # if pressed on the icon of the joystick
                    if PygameConstans.JOYSTICK_IMG.value[RECT_INDEX].collidepoint(event.pos):
                        self.joystick = JoystickPickPage(self.screen, self.my_socket).goToPage()
                    if PygameConstans.BACK_IMG.value[RECT_INDEX].collidepoint(event.pos):
                        send_data_socket_pickle(self.my_socket, pickle.dumps(EXIT_ROOM_REQ))
                        self.start_flag = None
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and PygameConstans.START_GAME_IMG.value[RECT_INDEX].collidepoint(event.pos):
                    send_data_socket_pickle(self.my_socket, pickle.dumps(START_GAME_ORDER))
                    self.in_waiting = True

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        is_start = self.in_waiting and len(self.players_got) > 1 and self.everyonePickedColor()
        is_confirm = not self.in_waiting and self.index_of_color is not None
        self.displayButtons(self.screen, True, is_start=is_start, is_confirm=is_confirm)
        self.displayItems(PygameConstans.BACKGROUNDS_IMGS.value[IMG_INDEX], PygameConstans.BACKGROUNDS_IMGS.value[RECT_INDEX], self.index_of_background)
        self.displayItems(PygameConstans.HATS_IMGS.value[IMG_INDEX], PygameConstans.HATS_IMGS.value[RECT_INDEX], self.index_of_hats)
        self.displayItems(self.players_images, self.players_rects, self.index_of_color)
        self.displayItems([self.podium_img[IMG_INDEX] for _ in range(0, 4)], [self.podium_img[RECT_INDEX][index] for index in range(0, 4)])
        self.displayPlayersGot()
        self.screen.blit(PygameConstans.JOYSTICK_IMG.value[IMG_INDEX], PygameConstans.JOYSTICK_IMG.value[RECT_INDEX])
        self.displayLockedItems()
        self.drawBasicSettingsText()

        for msg in self.requierments_msgs:
            msg[COUNTER_INDEX] += 1
            if msg[COUNTER_INDEX] > TOP_LIMITATION:
                self.requierments_msgs.remove(msg)
            else:
                self.drawRequierment(msg[0], msg[1], self.screen)
        pygame.display.flip()

    def everyonePickedColor(self):
        """
        func to check whether everyone in the room picked color, hat and background
        :return: bool
        """
        COLOR_INDEX = 0
        for player in self.players_got:
            if player[COLOR_INDEX] == "":
                return False
        return True

    @staticmethod
    def drawRequierment(index_of_wanted, rect_of_item, screen):
        """
        if the user press on locked item, this function called.
        this function will print to the screen what requierment require to unlck this item
        :param index_of_wanted: index of the pressed item
        :param rect_of_item: rect of the specific item
        :param screen: the screen
        :return: None
        """
        LOCKED_COLOR_BACKGROUND = (255, 255, 204)
        pygame.draw.rect(screen, LOCKED_COLOR_BACKGROUND,
                         pygame.rect.Rect(rect_of_item.x + 5, rect_of_item.y + 50, 150, 60))
        if rect_of_item in PygameConstans.BACKGROUNDS_IMGS.value[RECT_INDEX]:
            draw_text(f"you need to play", screen, rect_of_item.x + 5, rect_of_item.y + 50, 25)
        elif rect_of_item in PygameConstans.HATS_IMGS.value[RECT_INDEX]:
            draw_text(f"you need to win", screen, rect_of_item.x + 5, rect_of_item.y + 50, 25)
        draw_text(f"at least      games ", screen, rect_of_item.x + 5, rect_of_item.y + 70, 25)
        draw_text(f"{index_of_wanted * 10}", screen, rect_of_item.x + 70, rect_of_item.y + 70, 25, BLUE)
        draw_text(f"to unlock the item", screen, rect_of_item.x + 5, rect_of_item.y + 90, 25)

    def drawBasicSettingsText(self):
        """
        func to print to the screen "pick background", "pick color" and "pick character"
        :return: None
        """
        draw_text("choose", self.screen, 10, 10, 30, BLUE)
        draw_text("character:", self.screen, 10, 30, 30, BLUE)
        draw_text("choose", self.screen, 10, 70, 30, BLUE)
        draw_text("hat:", self.screen, 10, 90, 30, BLUE)
        draw_text("choose", self.screen, 10, 145, 30, BLUE)
        draw_text("background:", self.screen, 10, 165, 30, BLUE)

    def displayLockedItems(self):
        """
        func to draw "locked" sign on the items that are locked
        :return: None
        """
        for index_of_locked_hat in self.locked_hats:
            self.screen.blit(PygameConstans.LOCK.value, PygameConstans.HATS_IMGS.value[RECT_INDEX][index_of_locked_hat])

        for index_of_locked_background in self.locked_backgrounds:
            self.screen.blit(PygameConstans.LOCK.value, PygameConstans.BACKGROUNDS_IMGS.value[RECT_INDEX][index_of_locked_background])

    def displayItems(self, images, rects, index_of_wanted=None):
        """
        func to display generic items to the screen
        :param images: list for the images wanted to display
        :param rects: list of the rects of the images(where to place them)
        :param index_of_wanted: index of wanted item
        :return: None
        """
        for index in range(len(images)):
            self.screen.blit(images[index], rects[index])
        if index_of_wanted is not None:
            pygame.draw.rect(self.screen, GREEN, rects[index_of_wanted], 3)

    def displayPlayersGot(self):
        """
        func to display on the screen the characters of the other users got from the server. will be displayed on the podium
        :return: None
        """
        for index, player in enumerate(self.players_got):
            # print(f"player got: {player}")
            if type(player) == list:
                if player[0] in PygameConstans.COLOR_LIST.value:
                    for index_in_list, color_in_list in enumerate(PygameConstans.COLOR_LIST.value):
                        if color_in_list == player[0]:
                            # print(f"{PATH} + {COLOR_LIST[color]} + '/walk.png'")
                            self.screen.blit(pygame.image.load(
                                PATH + PygameConstans.COLOR_LIST.value[index_in_list] + "/walk.png").convert(), ((WINDOW_WIDTH / 6) * (index + 1) + 30, WINDOW_HEIGHT - 120))
                if player[1] is not None:
                    self.screen.blit(PygameConstans.HATS_IMGS.value[IMG_INDEX][player[RECT_INDEX]], ((WINDOW_WIDTH / 6) * (index + 1) + 20, WINDOW_HEIGHT - 170))
                draw_text(player[2], self.screen, (WINDOW_WIDTH / 6) * (index + 1), WINDOW_HEIGHT - 40, 30)

    def getOtherColorsWatingRoom(self):
        """
        func to get whether the games starts and the pictures of the players that picked their picture
        :return: None
        """
        EVERYONE_EXITED_BASSIC_SETTINGS_PAGE = "everyone exited from the basic settings page"
        data = new_data(self.my_socket, self.screen)
        if data is not None:
            print(f"players got: {self.players_got}")
            if data == EVERYONE_EXITED_BASSIC_SETTINGS_PAGE:
                self.start_flag = None
                self.screen.fill(GREY)
                draw_text("everyone exited the room, return to loby", self.screen, 20, 20, color=BLUE)
                pygame.display.flip()
                pygame.time.delay(1500)
            else:
                self.players_got = data[1]
                self.start_flag = data[0]
            print("got new data")
            print(data)

    @staticmethod
    def pickItem(event, rects, locked_items, requierments_msgs, index_of_wanted=0):
        """
        func to pick item
        :param event: pygame event(what input got from the user)
        :param rects: lists of the rects of the images of the items
        :param locked_items: list of the indexes of the lockd items
        :param requierments_msgs: list of the requierments
        :param index_of_wanted: index of wanted item
        :return: the index wanted
        """
        for index, rect in enumerate(rects):
            if rect.collidepoint(event.pos):
                if index not in locked_items:
                    return index
                else:
                    requierments_msgs.append([index, rect, 0])
        return index_of_wanted

    def setLockedItems(self):
        """
        func to set which items are locked
        :return: list of the indexes of locked hats and list of locked backgrounds
        """
        locked_backgrounds, locked_hats = [], []
        for index, rect_of_item in enumerate(PygameConstans.BACKGROUNDS_IMGS.value[RECT_INDEX]):
            # if the user played less than (item position in list * 10) games
            if self.user.getGamesPlayed() < index * 10:
                locked_backgrounds.append(index)
        for index, rect_of_item in enumerate(PygameConstans.HATS_IMGS.value[RECT_INDEX]):
            # if the user won less than (item position in list * 10) games
            if self.user.getGamesWon() < index * 10:
                locked_hats.append(index)
        return locked_hats, locked_backgrounds
