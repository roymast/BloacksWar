# This page is for the user to learn how to play the game

from pages.Page import *
from constants import *


class InstructionsPage(Page):
    """
    child class of Page.
    this class is for the user to learn how to play the game.
    """
    def __init__(self, screen, my_socket):
        super().__init__()
        self.screen = screen
        self.instruction_index = 0
        self.finished = False
        self.my_socket = my_socket

    def goToPage(self):
        """
        func to display instructions
        :return: None
        """
        print(self.finished)
        while not self.finished:
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
            # last page
            if button_pressed == BACKPAGESYS:
                if self.instruction_index == 0:
                    self.finished = True
                else:
                    self.instruction_index -= 1
            # next page
            if button_pressed == NEXTPAGESYS:
                if self.instruction_index == len(PygameConstans.INSTRUCTION_IMGS.value) - 1:
                    self.finished = True
                else:
                    self.instruction_index += 1

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        self.screen.blit(PygameConstans.INSTRUCTION_IMGS.value[self.instruction_index], (0, 0))
        self.displayButtons(self.screen, True, True)
        pygame.display.flip()
