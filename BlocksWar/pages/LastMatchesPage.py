# This page shows the last 10 matches of the user

from pages.Page import *

DATE_INDEX = 0
WINNER_INDEX = 1
PLAYER1 = 2
PLAYER2 = 3
PLAYER3 = 4
PLAYER4 = 5
NOPREVIOUSMATCHES = "oops, it's looks like you don't have previous matches"
NOTCONNECTED = "Connect if you want to see your previous matches"
EMPTY_NAME = ""


class ShowLastMathcesPage(Page):
    """
    child class of Page.
    this class is for the user to see his last 10 mathces
    """
    def __init__(self, screen, my_socket):
        super().__init__()
        self.screen = screen
        self.my_socket = my_socket
        self.finished = False
        self.matches = None

    def goToPage(self):
        print("in")
        self.screen.fill(GREY)
        pygame.display.flip()
        send_data_socket_pickle(self.my_socket, pickle.dumps("previous matches"))
        self.matches = pickle.loads(receive_data_pickle(self.my_socket, self.screen))
        print(f"matches=" + str(self.matches))
        while not self.finished:
            self.handleUserInputs()
            self.displayPage()
        self.screen.fill(GREY)
        pygame.display.flip()

    def handleUserInputs(self):
        """
        func to handle the user inputs
        :return: None
        """
        for event in pygame.event.get():
            button_pressed = self.handleUser(event)
            if button_pressed == EXITGAMESYS:
                exitGame(self.screen, self.my_socket)
            if button_pressed == BACKPAGESYS:
                self.finished = True

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        print(self.matches)
        self.screen.fill(GREY)
        if self.matches == NOPREVIOUSMATCHES or self.matches == NOTCONNECTED:
            draw_text(self.matches, self.screen, 30, 100, color=RED)
        else:
            self.displayMathces()
        self.displayButtons(self.screen, True)
        pygame.display.flip()

    def displayMathces(self):
        """
        func display the table of the matches
        :return: None
        """

        draw_text("matches", self.screen, WINDOW_WIDTH / 2 - 50, 15, 45)
        draw_text("players played", self.screen, 50, 45, 35, BLUE)
        draw_text("winner", self.screen, 430, 45, 35, BLUE)
        draw_text("date", self.screen, 600, 45, 35, BLUE)
        for index, matche in enumerate(self.matches):
            print(type(matche))
            date = str(matche[DATE_INDEX].split(":")[0]) + ":" + str(matche[DATE_INDEX].split(":")[1])
            players_names = self.playersNames(matche)
            if players_names == "error":
                draw_text("error while searching for previous games", self.screen, 100, 100, color=RED)
                break
            draw_text(players_names, self.screen, 20, (index + 2) * WINDOW_HEIGHT / 14 + 20, 25)
            draw_text(matche[WINNER_INDEX], self.screen, 430, (index + 2) * WINDOW_HEIGHT / 14 + 20, 25, GREEN)
            draw_text(date, self.screen, 550, (index + 2) * WINDOW_HEIGHT / 14 + 20, 25)

    def playersNames(self, match):
        """
        func to create string of the names
        :param match: the data of the specific match
        :return: string
        """
        if match[PLAYER1] == EMPTY_NAME or match[PLAYER2] == EMPTY_NAME:
            players_names = "error"
        else:
            players_names = match[PLAYER1] + ', ' + match[PLAYER2]
            if match[PLAYER3] != EMPTY_NAME:
                players_names += ', ' + match[PLAYER3]
                if match[PLAYER4] != EMPTY_NAME:
                    players_names += ', ' + match[PLAYER4]
        return players_names

    def displayMathcesTableTitles(self):
        """
        func to display "players", "winner" and "data" to the screen
        :return: None
        """
        draw_text("players", self.screen, 70, 45, 35, BLUE)
        draw_text("winner", self.screen, 440, 45, 35, BLUE)
        draw_text("date", self.screen, 590, 45, 35, BLUE)
