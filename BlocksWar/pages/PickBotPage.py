# this file is for displaying the ip page
# in this page, the user insert the ip of the server

from pages.Page import *
from constants import *


class PickBotPage(Page):
    """
    child class of Page.
    this class is for the user to pick whether he wants to play with ai or not.
    """
    def __init__(self, screen, my_socket):
        super().__init__()
        self.screen = screen
        self.my_socket = my_socket
        self.is_ai = None
        self.confirm_pick = False

    def goToPage(self):
        while not self.confirm_pick:
            self.handleUserInputs()
            self.displayPage()
        return self.is_ai

    def handleUserInputs(self):
        """
        func to handle the user inputs
        :return: None
        """
        for event in pygame.event.get():
            button_pressed = self.handleUser(event)
            if button_pressed == EXITGAMESYS:
                exitGame(self.screen, self.my_socket)
            if button_pressed == CONFIRMSYS or button_pressed == NEXTPAGESYS or button_pressed == STARTGAMESYS:
                self.confirm_pick = True
            if button_pressed == BACKPAGESYS:
                self.is_ai = None
                self.confirm_pick = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PygameConstans.YES_BUTTON.value[RECT_INDEX].collidepoint(event.pos):
                    self.is_ai = True
                if PygameConstans.NO_BUTTON.value[RECT_INDEX].collidepoint(event.pos):
                    self.is_ai = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.is_ai = True
                self.confirm_pick = True


    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        self.screen.fill(GREY)
        draw_text("Would you like to play vs bot?", self.screen, 20, 50, 60, BLUE)
        self.screen.blit(PygameConstans.YES_BUTTON.value[IMG_INDEX], PygameConstans.YES_BUTTON.value[RECT_INDEX])
        self.screen.blit(PygameConstans.NO_BUTTON.value[IMG_INDEX], PygameConstans.NO_BUTTON.value[RECT_INDEX])
        self.screen.blit(PygameConstans.BOT.value[IMG_INDEX], PygameConstans.BOT.value[RECT_INDEX])
        self.displayButtons(self.screen, True)
        self.displayButtons(self.screen, is_confirm=self.is_ai is not None)
        if self.is_ai:
            pygame.draw.rect(self.screen, LIME, PygameConstans.YES_BUTTON.value[RECT_INDEX], 5)
        elif self.is_ai == False:
            pygame.draw.rect(self.screen, LIME, PygameConstans.NO_BUTTON.value[RECT_INDEX], 5)
        pygame.display.flip()
