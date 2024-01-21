# this file display the single or multi player page
# this page let the user pick if he want to play single player or multi player mode
# in addition this page have button to go to the other pages:
# instruction page
# account settings page
# top 10 page

from pages.Page import *
from pages.InstructionPage import InstructionsPage
from pages.AccountSettingsPage import AccountSettingsPage
from pages.TopTenPage import TopTenPage
from button import TextButton


class SingleOrMultiPlayerPage(Page):
    """
    child class of Page.
    this class is for the user to pick whether he want to play in "single player" mode or "multi player" mode.
    (it also link the user to "account settings" page and "instructions" page)
    """
    def __init__(self, screen, my_socket, user):
        super().__init__()
        self.screen = screen
        self.my_socket = my_socket
        self.user = user
        self.confirm_pick = False
        self.is_single_player = None
        self.singleplayer_button = TextButton("Single Player", screen, PygameConstans.SINGLE_PLAYER_RECT.value, 2, 40, (255, 255, 255), (146, 168, 209))
        self.multiplayer_button = TextButton("Multi Player", screen, PygameConstans.MULTI_PLAYER_RECT.value, 2, 40, (255, 255, 255), (146, 168, 209))
        self.instructions_button = TextButton("instructions", screen, PygameConstans.INSTRUCTION_RECT.value, 2, 40, (255, 255, 255), (3, 79, 132))
        self.account_settings_button = TextButton("account settings", screen, PygameConstans.ACCOUNT_SETTING_RECT.value, 2, 40, (255, 255, 255), (3, 79, 132))
        self.topten_button = TextButton("Top10", screen, PygameConstans.TOP10_RECT.value, 2, 40, (255, 255, 255), (3, 79, 132))

    def goToPage(self):
        """
        func to ask the player whether he want to play single player or multy player
        func will send at the end what the user chose
        :return: bool(True for single player, False for multi player
        """
        while not self.confirm_pick:
            self.handleUserInputs()
            self.displayPage()
        return self.is_single_player

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        self.screen.fill(GREY)
        draw_text("What mode would you like to play?", self.screen, 20, 50, 60, BLUE)
        self.singleplayer_button.blitToScreen()
        self.multiplayer_button.blitToScreen()
        self.instructions_button.blitToScreen()
        self.account_settings_button.blitToScreen()
        self.topten_button.blitToScreen()
        if self.is_single_player is True:
            pygame.draw.rect(self.screen, LIME, self.singleplayer_button.getRect(), 5)
            self.screen.blit(PygameConstans.CONFIRM_BUTTON.value[IMG_INDEX], PygameConstans.CONFIRM_BUTTON.value[RECT_INDEX])
        elif self.is_single_player is False:
            pygame.draw.rect(self.screen, LIME, self.multiplayer_button.getRect(), 5)
            self.screen.blit(PygameConstans.CONFIRM_BUTTON.value[IMG_INDEX], PygameConstans.CONFIRM_BUTTON.value[RECT_INDEX])
        pygame.display.flip()

    def handleUserInputs(self):
        """
        func to handle the user inputs
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame(self.screen, self.my_socket)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.singleplayer_button.getRect().collidepoint(event.pos):
                    self.is_single_player = True
                if self.multiplayer_button.getRect().collidepoint(event.pos):
                    self.is_single_player = False
                if self.instructions_button.getRect().collidepoint(event.pos):
                    InstructionsPage(self.screen, self.my_socket).goToPage()
                if self.account_settings_button.getRect().collidepoint(event.pos) and self.user is not None:
                    AccountSettingsPage(self.screen, self.my_socket, self.user).goToPage()
                if self.topten_button.getRect().collidepoint(event.pos):
                    TopTenPage(self.screen, self.my_socket).goToPage()
                if PygameConstans.CONFIRM_BUTTON.value[RECT_INDEX].collidepoint(event.pos) and self.is_single_player is not None:
                    self.confirm_pick = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.is_single_player = False
                    self.confirm_pick = True
