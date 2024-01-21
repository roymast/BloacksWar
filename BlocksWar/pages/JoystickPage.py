# This page is for the user to pick whether he want to play with or without joystick

from pages.Page import *


class JoystickPickPage(Page):
    """
    child class of Page.
    this class is for the user to pick whether he wants to play with or without joystick.
    """
    def __init__(self, screen, my_socket):
        super().__init__()
        self.screen = screen
        self.my_socket = my_socket
        self.is_joystick = None
        self.pickedConfirm = False

    def goToPage(self):
        print("in joystick")
        while not self.pickedConfirm:
            self.handleUserInputs()
            self.displayPage()
        print("out of joystick")
        return self.init_joystick()

    def handleUserInputs(self):
        """
        func to handle the user inputs
        :return: None
        """
        for event in pygame.event.get():
            button_pressed = self.handleUser(event)
            if button_pressed == EXITGAMESYS:
                exitGame(self.screen, self.my_socket)
            if (button_pressed == CONFIRMSYS or button_pressed == STARTGAMESYS or button_pressed == NEXTPAGESYS) and \
                    self.is_joystick is not None:
                self.pickedConfirm = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PygameConstans.YES_BUTTON.value[RECT_INDEX].collidepoint(event.pos):
                    self.is_joystick = True
                if PygameConstans.NO_BUTTON.value[RECT_INDEX].collidepoint(event.pos):
                    self.is_joystick = False

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        self.screen.fill(GREY)
        self.screen.blit(PygameConstans.YES_BUTTON.value[IMG_INDEX], PygameConstans.YES_BUTTON.value[RECT_INDEX])
        self.screen.blit(PygameConstans.NO_BUTTON.value[IMG_INDEX], PygameConstans.NO_BUTTON.value[RECT_INDEX])
        self.displayButtons(self.screen, is_confirm=self.is_joystick is not None)
        if self.is_joystick:
            pygame.draw.rect(self.screen, (99, 245, 91), PygameConstans.YES_BUTTON.value[RECT_INDEX], 5)
        elif self.is_joystick == False:
            pygame.draw.rect(self.screen, (99, 245, 91), PygameConstans.NO_BUTTON.value[RECT_INDEX], 5)
        draw_text('Would you like to play with a controller?', self.screen, 50, 80, 50, BLUE)
        pygame.display.flip()

    @staticmethod
    def init_joystick():
        """
            init joystick
            return the joystick if found
        """
        pygame.joystick.init()
        try:
            j = pygame.joystick.Joystick(0)  # create a joystick instance
            j.init()  # init instance
            print("Enabled joystick: {0}".format(j.get_name()))
            return j
        except pygame.error:
            print("no joystick found.")
            return None
