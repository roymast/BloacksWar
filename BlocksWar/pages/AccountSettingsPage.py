# This file is for displaying the account settings page
# This page let the user see his profile that save in the server's database
# This page also let the user see his previous matches and change the profile image

from pages.Page import *
from pages.LastMatchesPage import ShowLastMathcesPage
from constants import *
import easygui
LOADING_IMG_ERROR = "oops, couldn't load this img"


class AccountSettingsPage(Page):
    """
    child class of Page.
    this class is for the user to see what the others can see about him
    (name, username, amount of games won, amount of games player and user image).
    in addition, the user can see the last 10 matches, and can change image.
    """
    def __init__(self, screen, my_socket, user):
        super().__init__()
        self.screen = screen
        self.user = user
        self.my_socket = my_socket
        self.stop_showing = False

    def goToPage(self):
        while not self.stop_showing:
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
            if event.type == pygame.MOUSEBUTTONDOWN and PygameConstans.PREVIOUS_MATCHES.value[RECT_INDEX].collidepoint(event.pos):
                ShowLastMathcesPage(self.screen, self.my_socket).goToPage()
            if button_pressed == BACKPAGESYS:
                self.stop_showing = True
            if event.type == pygame.MOUSEBUTTONDOWN and PygameConstans.ADD_IMG.value[RECT_INDEX].collidepoint(
                    event.pos) and not self.user.isGuest():
                self.changeImg()

    def changeImg(self):
        """
        func open a filedialog to let the user pick image from his computer
        :return: None
        """
        # Function for opening the
        # file explorer window
        img_path = easygui.fileopenbox()
        try:        # if the img is too large, the pygame throw exception
            if img_path is not None:
                if img_path.split(".")[1] in ["png", "jpg", "jpeg"]:
                    self.user.changeImg(img_path)
                    send_data_socket_pickle(self.my_socket, pickle.dumps(
                        [clientReq.CHANGE_IMG.value, self.user.getImgBytes(), self.user.getImg().get_size()[0], self.user.getImg().get_size()[1]]))
                else:
                    draw_text_time(LOADING_IMG_ERROR, self.screen, WINDOW_WIDTH/2-50, WINDOW_HEIGHT/4, GREY, RED, 2)
        except:
            draw_text_time(LOADING_IMG_ERROR, self.screen, WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 4, GREY, RED, 2)

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        if self.user is not None:
            if self.user.getImg() is None:
                self.screen.blit(PygameConstans.USER.value[IMG_INDEX], PygameConstans.USER.value[RECT_INDEX])
            x = 360
            self.screen.fill(GREY)
            draw_text("user info", self.screen, WINDOW_WIDTH / 2 - 100, 30, 50, BLUE)
            pygame.draw.line(self.screen, BLUE, (WINDOW_WIDTH / 2 - 100, 70), (WINDOW_WIDTH / 2 + 50, 70), 3)
            draw_text("name:", self.screen, x, 200 - 50)
            draw_text(self.user.getName(), self.screen, x + 100, 200 - 50, color=BLUE)
            draw_text("username:", self.screen, x, 250 - 50)
            draw_text(self.user.getUserName(), self.screen, x + 160, 250 - 50, color=BLUE)
            draw_text("games played:", self.screen, x, 300 - 50)
            draw_text(str(self.user.getGamesPlayed()), self.screen, x + 210, 300 - 50, color=BLUE)
            draw_text("games won:", self.screen, x, 350 - 50)
            draw_text(str(self.user.getGamesWon()), self.screen, x + 170, 350 - 50, color=BLUE)

            self.screen.blit(self.user.getImg(), PygameConstans.USER.value[RECT_INDEX])
            self.displayButtons(self.screen, is_back=True)
            pygame.draw.rect(self.screen, BLACK, PygameConstans.USER.value[RECT_INDEX], 3)
            self.screen.blit(PygameConstans.PREVIOUS_MATCHES.value[IMG_INDEX], PygameConstans.PREVIOUS_MATCHES.value[RECT_INDEX])
            draw_text("previous matches", self.screen, 380, 360, color=BLUE)
            if not self.user.isGuest():
                draw_text("add image", self.screen, 50, 50, color=BLUE)
                pygame.draw.rect(self.screen, GREEN, PygameConstans.ADD_IMG.value[RECT_INDEX], 3)
        pygame.display.flip()
