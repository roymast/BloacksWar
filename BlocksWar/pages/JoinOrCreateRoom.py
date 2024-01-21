# this page is for the user to pick whether he want to create room or join room

from pages.Page import *


class JoinOrCreateRoomPage(Page):
    """
    child class of Page.
    this class is for the user to pick whether he want to create room or to join one.
    """
    def __init__(self, screen, my_socket):
        from button import TextButton
        super().__init__()
        self.screen = screen
        self.my_socket = my_socket
        self.is_create_room = None
        self.create_room_button = TextButton("create room", screen, pygame.rect.Rect(100, 100, 170, 40), 2, 40, BLACK, LIGHT_BLUE2)
        self.join_room_button = TextButton("join room", screen, pygame.rect.Rect(100, 200, 140, 40), 2, 40, BLACK, LIGHT_BLUE)
        self.back_last_screen = False

    def gotToPage(self):
        while self.is_create_room is None and not self.back_last_screen:
            self.handleUserInputs()
            self.displayPage()
        if self.back_last_screen:
            return None
        return self.is_create_room

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
                self.back_last_screen = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.create_room_button.getRect().collidepoint(event.pos):
                    self.is_create_room = True
                elif self.join_room_button.getRect().collidepoint(event.pos):
                    self.is_create_room = False

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        self.screen.fill(GREY)
        self.create_room_button.blitToScreen()
        self.join_room_button.blitToScreen()
        self.displayButtons(self.screen, is_back=True)
        pygame.display.flip()
