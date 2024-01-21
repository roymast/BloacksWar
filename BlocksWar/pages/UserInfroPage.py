# this file show the userinfo page
# this page is for the user to see other users information that save in the servers database

from pages.Page import *
NAME_OF_USER = 0
USERNAME = 1
GAMES_PLAYED = 2
GAMES_WON = 3
USER_IMAGE_INDEX = 4
SIZE_USER_IMAGE = (250, 250)


class UserInfoPage(Page):
    """
    child class of Page.
    this class is for the user to see the stats of specific user.
    """
    def __init__(self, screen, my_socket, user_info):
        import base64
        super().__init__()
        self.my_socket = my_socket
        self.screen = screen
        self.user_info = user_info
        if self.user_info[USER_IMAGE_INDEX] == "":
            self.user_img = PygameConstans.USER.value[IMG_INDEX]
        else:
            print(len(user_info[USER_IMAGE_INDEX]))
            imgstring = base64.b64decode(user_info[USER_IMAGE_INDEX])
            self.user_img = pygame.image.fromstring(imgstring, SIZE_USER_IMAGE, 'RGBX')
        self.finish = False

    def goToPage(self):
        while not self.finish:
            self.handleUserInputs()
            self.displayPage()
        self.screen.fill(GREY)

    def handleUserInputs(self):
        """
        func to handle the user inputs
        :return: None
        """
        for event in pygame.event.get():
            button_pressed = self.handleUser(event)
            if button_pressed == EXITGAMESYS:
                exitGame(self.screen, self.my_socket)
            elif button_pressed == BACKPAGESYS:
                self.finish = True

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        x = 360
        self.screen.fill(GREY)
        draw_text("user info", self.screen, WINDOW_WIDTH / 2 - 100, 30, 50, BLUE)
        pygame.draw.line(self.screen, BLUE, (WINDOW_WIDTH / 2 - 100, 70), (WINDOW_WIDTH / 2 + 50, 70), 3)
        draw_text("name:", self.screen, x, 200 - 50)
        draw_text(self.user_info[NAME_OF_USER], self.screen, x + 100, 200 - 50, color=BLUE)
        draw_text("username:", self.screen, x, 250 - 50)
        draw_text(self.user_info[USERNAME], self.screen, x + 160, 250 - 50, color=BLUE)
        draw_text("games played:", self.screen, x, 300 - 50)
        draw_text(str(self.user_info[GAMES_PLAYED]), self.screen, x + 210, 300 - 50, color=BLUE)
        draw_text("games won:", self.screen, x, 350 - 50)
        draw_text(str(self.user_info[GAMES_WON]), self.screen, x + 170, 350 - 50, color=BLUE)
        self.screen.blit(self.user_img, PygameConstans.USER.value[RECT_INDEX])
        self.displayButtons(self.screen, is_back=True)
        pygame.draw.rect(self.screen, BLACK, PygameConstans.USER.value[RECT_INDEX], 3)
        pygame.display.flip()
