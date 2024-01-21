# This page shown after the game ends
# The page show who won the game,
# and give the user the information about all of the other users

from pages.Page import *
from pages.UserInfroPage import UserInfoPage


class GameOverPage(Page):
    """
    child class of Page.
    this class is for the user to see the winner and can jump to a page to see the stats of the other users.
    """
    def __init__(self, screen, my_socket, players):
        super().__init__()
        self.screen = screen
        self.my_socket = my_socket
        self.players = players
        self.winner = ""
        self.users_info = []
        self.pics_of_players = [player.get_walk_pics()[0] for player in players]
        self.rects = []
        for index, pic in enumerate(self.pics_of_players):
            self.rects.append(pic.get_rect(bottomleft=((WINDOW_WIDTH / 5 * (index + 1)), WINDOW_HEIGHT * (4 / 5))))
        self.stopGameOver = False

    def goToPage(self):
        """
        func to show game over screen
        :return: None
        """
        draw_text("game over", self.screen, WINDOW_WIDTH / 3, WINDOW_HEIGHT / 2, color=RED)
        pygame.display.flip()
        pygame.time.delay(3000)
        self.screen.fill(GREY)
        pygame.display.flip()
        self.winner = pickle.loads(receive_data_pickle(self.my_socket, self.screen))
        self.users_info = pickle.loads(receive_data_pickle(self.my_socket, self.screen))
        while not self.stopGameOver:
            self.handleUserInputs()
            self.displayPage()

    def handleUserInputs(self):
        """
        func to handle the user inputs
        :return: None
        """
        for event in pygame.event.get():
            button_pressed = self.handleUser(event)
            if button_pressed == EXITGAMESYS:
                exitGame(self.screen, self.my_socket)
            if button_pressed == NEXTPAGESYS:
                self.stopGameOver = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pickingUserInfo(event.pos)

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        self.screen.fill(GREY)
        self.drawEveryonesInfo()
        self.displayButtons(self.screen, is_next=True)
        draw_text(f"the winner is: {self.winner}", self.screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 3, 40, GREEN)
        draw_text(f"game over", self.screen, WINDOW_WIDTH / 3, WINDOW_HEIGHT / 9, 55, BLUE)
        pygame.display.flip()

    def pickingUserInfo(self, mouse_pos):
        """
        func to check which user our user want to see his stats, and go the page to display his stats
        :param mouse_pos: where the mouse clicked
        :return: None
        """
        print("in picking user info")
        for index, rect in enumerate(self.rects):
            if rect.collidepoint(mouse_pos):
                print("found")
                UserInfoPage(self.screen, self.my_socket, self.users_info[index]).goToPage()
                print("done")

    def drawEveryonesInfo(self):
        """
        func to draw everyone names and display the image of the character they picked
        :return: None
        """
        for index, user in enumerate(self.users_info):
            self.screen.blit(self.pics_of_players[index], self.rects[index])
            draw_text(user[1], self.screen, self.rects[index].x, self.rects[index].y + 70, size=35, color=BLUE)