# this file is for displaying the top ten page
# this page display the top ten players from the database

from pages.Page import *

USERNAME_INDEX = 0
GAMES_PLAYED_INDEX = 1
GAMES_WON_INDEX = 2
TOPTEN_IS_EMPTY = "the database is empty"


class TopTenPage(Page):
    def __init__(self, screen, my_socket):
        TOPTEN_REQ = "top ten"
        super().__init__()
        self.screen = screen
        self.my_socket = my_socket
        send_data_socket_pickle(self.my_socket, pickle.dumps(TOPTEN_REQ))
        self.top_ten_players = pickle.loads(receive_data_pickle(self.my_socket, self.screen))
        self.stop = False
        self.x = 160
        self.y = 80

    def goToPage(self):
        while not self.stop:
            self.handleUserInputs()
            self.displayPage()

    def handleUserInputs(self):
        """
        func to handle the inputs from the user
        :return: None
        """
        for event in pygame.event.get():
            buttons_press = self.handleUser(event)
            if buttons_press == EXITGAMESYS:
                exitGame(self.screen, self.my_socket)
            if buttons_press == BACKPAGESYS:
                self.stop = True

    def displayPage(self):
        """
        func to display the page
        :return: None
        """
        self.screen.fill(GREY)
        self.displayButtons(self.screen, is_back=True)
        self.drawTable()
        pygame.display.flip()

    def drawTable(self):
        """
        func to draw the table of the top 10
        :return: None
        """
        print(self.top_ten_players)
        draw_text("top 10", self.screen, WINDOW_WIDTH / 2 - 20, 15, color=BLUE)
        if self.top_ten_players == TOPTEN_IS_EMPTY:
            draw_text(TOPTEN_IS_EMPTY, self.screen, self.x, self.y, color=RED)
        else:
            self.drawTableTitles()
            for index, player in enumerate(self.top_ten_players):
                draw_text(f"{str(player[USERNAME_INDEX])}", self.screen, self.x, self.y + index * 30)
                draw_text(str(player[GAMES_WON_INDEX]), self.screen, self.x + 240, self.y + index * 30)
                draw_text(str(player[GAMES_PLAYED_INDEX]), self.screen, self.x + 430, self.y + index * 30)

    def drawTableTitles(self):
        """
        func to draw the title of the table
        :return: None
        """
        draw_text("player name", self.screen, self.x - 40, self.y-30, color=DARK_BLUE)
        draw_text("games won", self.screen, self.x + 180, self.y-30, color=DARK_BLUE)
        draw_text("games played", self.screen, self.x + 380, self.y-30, color=DARK_BLUE)