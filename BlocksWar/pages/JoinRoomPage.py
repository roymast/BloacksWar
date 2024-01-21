# This page is for the user to insert the number of the room, so he can join it

from pages.Page import *
ROOM_NUMBER_LENGTH = 4
ROOM_NUMBER_TOO_SHORT = f"the room number should be {ROOM_NUMBER_LENGTH} characters"
JOINING_COMPLETE = "joining room completed"
THREAD_INDEX = 1
ERROR_INDEX = 0

ROOM_NUMBER_INDEX = 1
PLAYERS_NAMES_INDEX = 2
SERVER_IP_INDEX = 3


class JoinRoomPage(Page):
    """
    child class of Page.
    this class is for the user to let the user pick room number, and to join one.
    """
    def __init__(self, screen, my_socket):
        super().__init__()
        self.screen = screen
        self.my_socket = my_socket
        self.confirmed = False
        self.room_number_textbox = Textbox(300, 50, GREY, 200, 30, "text")
        self.room_number_textbox.set_picked(True)
        self.msg = ""
        self.data_on_room = None
        self.error = None

    def goToPage(self):
        while self.confirmed is not None and not self.confirmed:
            self.handleUserInputs()
            self.displayPage()
            self.msg = ""
        if self.confirmed is None:
            return None, None, None
        return self.data_on_room[ROOM_NUMBER_INDEX], self.data_on_room[PLAYERS_NAMES_INDEX], self.data_on_room[SERVER_IP_INDEX]

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
                self.confirmed, self.msg = self.sendRoomNumber()
                if type(self.msg) != str:
                    self.data_on_room = self.msg
                else:
                    error = self.msg
                    self.error = [error, threading.Thread(target=self.waitXSeconds, args=[2])]
                    self.error[THREAD_INDEX].start()
            if button_pressed == BACKPAGESYS:
                self.confirmed = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.room_number_textbox.remove_char()
                if len(self.room_number_textbox.get_text_string()) < ROOM_NUMBER_LENGTH:
                    self.room_number_textbox.add_char(event.unicode)

    def waitXSeconds(self, sec):
        time.sleep(sec)

    def displayPage(self):
        """
        func to display the page on the screen
        :return: None
        """
        self.screen.fill(GREY)
        draw_text("enter room number:", self.screen, 10, 50)
        self.room_number_textbox.print_box(self.screen)
        self.displayButtons(self.screen, True, True)
        if self.error is not None and self.error[THREAD_INDEX].is_alive():
            draw_text(self.error[ERROR_INDEX], self.screen, 100, 300, color=RED)
        else:
            self.error = None
        pygame.display.flip()
        PygameConstans.CLOCK.value.tick(15)

    def sendRoomNumber(self):
        """
        func to send that the user want to join room, and recive whether he got into the room successfully.
        if the user got into the room successfully,
            the func will return the names of the players that are already in the room
        :return: bool, string
        """
        ROOM_NUMBER_NOT_NUMBER = "room number should be only numbers"
        if len(self.room_number_textbox.get_text_string()) != ROOM_NUMBER_LENGTH:
            return False, ROOM_NUMBER_TOO_SHORT
        if not self.room_number_textbox.get_text_string().isdigit():
            return False, ROOM_NUMBER_NOT_NUMBER
        send_data_socket_pickle(self.my_socket, pickle.dumps(["join room", self.room_number_textbox.get_text_string()]))
        msg = receive_data_pickle(self.my_socket, self.screen)
        if msg is not None:
            msg = pickle.loads(msg)
            print(f"msg in send room number{msg}")
            if type(msg) == list and msg[0] == JOINING_COMPLETE:
                return True, msg
            return False, msg
