# this file is for displaying the waiting room
# in this page, it shows all of the users in the room and let the users to continue to the next page

from pages.Page import *


class WaitingRoom(Page):
    """
    child class of Page.
    this class is for the user to show the user who is in the room, and to continue to the next screen with everyone.
    """
    def __init__(self, my_socket, screen, players_names, room_number, server_ip):
        super().__init__()
        self.my_socket = my_socket
        self.screen = screen
        self.players_names = players_names
        self.room_number = room_number
        self.start_game_order = False
        self.server_ip = server_ip

    def goToRoom(self):
        while self.start_game_order is not None and not self.start_game_order:
            self.displayPage()
            self.handleUserInputs()
            self.updateData()
        return self.start_game_order

    def handleUserInputs(self):
        """
        func to handle the user inputs
        :return: None
        """
        GO_TO_BASIC_SETTINGS = "go to basic settings page"
        for event in pygame.event.get():
            button_pressed = self.handleUser(event)
            if button_pressed == EXITGAMESYS:
                exitGame(self.screen, self.my_socket)
            # if user want to start the game
            if (button_pressed == STARTGAMESYS or button_pressed == NEXTPAGESYS or button_pressed == CONFIRMSYS) and len(self.players_names) > 1:
                send_data_socket_pickle(self.my_socket, pickle.dumps(GO_TO_BASIC_SETTINGS))
            # if user want to exit
            if button_pressed == BACKPAGESYS:
                send_data_socket_pickle(self.my_socket, pickle.dumps(EXIT_ROOM_REQ))
                self.start_game_order = None

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        self.screen.fill(GREY)
        # print(self.players_names)
        self.displayButtons(self.screen, True, is_start=len(self.players_names) > 1)
        draw_text(f"room number: {self.room_number}", self.screen, 0, 0, color=DARK_BLUE)
        draw_text(f"server ip: {self.server_ip}", self.screen, 0, 40, color=LIGHT_BLUE)
        draw_text("players in room: ", self.screen, 100, 100, color=BLUE)
        self.drawNamesInRoom()
        pygame.display.flip()

    def drawNamesInRoom(self):
        """
        func to display the names of the users that in the specific room
        :return: None
        """
        x, y = 150, 150
        for index, name in enumerate(self.players_names):
            draw_text(name, self.screen, x, y, color=GREEN)
            y += 30

    def updateData(self):
        """
        func to check whether there is new data about the room,
        and change the room stats according the information got from the server
        :return: None
        """
        UPDATE_ROOM_MSG = "room update"
        GO_TO_BASIC_SETTINGS = "go to basic settings page"
        update_data = new_data(self.my_socket, self.screen)
        print(update_data)
        if update_data:
            if type(update_data) == list and update_data[0] == UPDATE_ROOM_MSG:
                self.room_number = update_data[1]
                self.players_names = update_data[2]
            elif update_data == GO_TO_BASIC_SETTINGS:
                self.start_game_order = True
