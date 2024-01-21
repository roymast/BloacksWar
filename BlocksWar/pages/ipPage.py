# This page is for the user to insert the ip of the server

from pages.Page import *
from constants import *


class IPPage(Page):
    """
    child class of Page.
    this class is for the user to pick the ip of the server
    """
    def __init__(self, screen):
        super().__init__()
        box_x, box_y, box_color, box_width, box_height = 130, 80, GREY, 40, 27
        ip_textbox1 = Textbox(box_x, box_y, box_color, box_width, box_height, "text")       # first part of the ip
        ip_textbox2 = Textbox(box_x + 50, box_y, box_color, box_width, box_height, "text")  # second part of the ip
        ip_textbox3 = Textbox(box_x + 100, box_y, box_color, box_width, box_height, "text") # third part of the ip
        ip_textbox4 = Textbox(box_x + 150, box_y, box_color, box_width, box_height, "text") # forth part of the ip
        self.ip_textboxes = [ip_textbox1, ip_textbox2, ip_textbox3, ip_textbox4]            # list of the ip textboxes
        self.ip_textboxes[0].set_picked(True)
        self.ip = ""        # the full ip address
        self.screen = screen    # the screen

    def goToPage(self):
        while self.ip == "":  # while the user didn't picked valid ip
            for event in pygame.event.get():
                self.ip = self.handleUserInputs(event)
            self.displayPage()
        return self.ip

    def handleUserInputs(self, event):
        """
        func to handle the users inputs
        if the user pressed "enter", and managed to connect the server, the func will return the socket
        :return: socket object/None
        """
        ip = ""
        if event.type == pygame.QUIT:
            exitGame(self.screen, None)
        # if keyboard press
        if event.type == pygame.KEYDOWN:
            # enter pressed
            if event.key == pygame.K_RETURN:
                # if all of the textboxes are not empty
                if not is_textboxes_empty(self.ip_textboxes):
                    if self.check_ip():
                        for textbox in self.ip_textboxes:
                            ip += textbox.get_text_string() + "."
                        ip = ip[:-1]
                else:
                    pick_next(self.ip_textboxes)
            # pressed 'tab' or '.'
            elif event.key == pygame.K_TAB or event.key == pygame.K_PERIOD:
                pick_next(self.ip_textboxes)
            # pressed backspace
            elif event.key == pygame.K_BACKSPACE:
                removeCharFromTextboxes(self.ip_textboxes, True)
            # for any other key
            else:
                add_char_to_textboxes(self.ip_textboxes, event, 3, True)
        # if mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if pressed 'confirm' and the ip is not empty
            if PygameConstans.CONFIRM_BUTTON.value[RECT_INDEX].collidepoint(event.pos) and not is_textboxes_empty(
                    self.ip_textboxes):
                if self.check_ip():
                    for textbox in self.ip_textboxes:
                        ip += textbox.get_text_string() + "."
                    ip = ip[:-1]
            else:
                pickTextboxByMouse(self.ip_textboxes, event)
        return ip

    def displayPage(self):
        """
        func to display the page
        :return: None
        """
        self.screen.fill(GREY)
        printTextboxes(self.ip_textboxes, self.screen)
        draw_text(".     .     .", self.screen, self.ip_textboxes[0].get_x() + 43, self.ip_textboxes[0].get_y())
        draw_text("insert server's ip", self.screen, 100, 20, color=BLUE)
        self.displayButtons(self.screen, is_confirm=(not is_textboxes_empty(self.ip_textboxes)))
        pygame.display.flip()

    def check_ip(self):
        """
        func to check whether the ip is ok
        :return: bool
        """
        IP_NOT_COMPLETE = "oops your ip seems to be uncompleted"
        IP_NOT_NUMBER = "please enter only numbers"
        IP_OUT_OF_RANGE = "ip address is between 0 to 255"
        for textbox in self.ip_textboxes:
            if len(textbox.get_text_string()) == 0:
                draw_text_time(IP_NOT_COMPLETE, self.screen, 150, 150, GREY, RED, 2)
                return False
            if not textbox.get_text_string().isdigit():
                draw_text_time(IP_NOT_NUMBER, self.screen, 150, 150, GREY, RED, 2)
                return False
            if not 0 <= int(textbox.get_text_string()) <= 255:
                draw_text_time(IP_OUT_OF_RANGE, self.screen, 150, 150, GREY, RED, 2)
                return False
        return True


