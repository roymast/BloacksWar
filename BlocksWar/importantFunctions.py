import pygame
import traceback
import sys
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = "bowlbyonesc"
GREY = (127, 127, 127)
WINDOW_WIDTH = 728
WINDOW_HEIGHT = 409
BLUE = (0, 0, 128)


def draw_text(text, surface, x, y, size=40, color=BLACK):
    """
    func draw text to the screen
    :param text: the text we want to write
    :param surface: the surface
    :param x: x position
    :param y: y position
    :param size: size fo the text
    :param color: color of the text
    :return: None
    """

    # font = pygame.font.Font('freesansbold.ttf', size)
    font = pygame.font.Font(pygame.font.match_font(FONT), size)
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)


def draw_text_time(text, surface, x, y, background_color, color=BLACK, sec=None, size=40):
    """
    func draw text to the screen to specific amount of second
    :param sec: amount of seconds to show the text
    :param background_color: the background
    :param text: the text we want to write
    :param surface: the surface
    :param x: x position
    :param y: y position
    :param size: size fo the text
    :param color: color of the text
    :return: None
    """
    start = pygame.time.get_ticks()
    if type(sec) == int:
        while pygame.time.get_ticks()-start < sec*1000:
            #font = pygame.font.Font('freesansbold.ttf', size)
            font = pygame.font.Font(pygame.font.match_font(FONT), size)
            textobj = font.render(text, True, color)
            textrect = textobj.get_rect(topleft=(x, y))
            surface.blit(textobj, textrect)
            pygame.display.update()
        # try:
        print("before")
        surface.fill(background_color, textrect)
        print("after")
            # print("blited")
        # except:
        #     print("error")
        #     pass


def exitGame(screen, my_socket):
    """
    func to exit the game and print to screen "thnks for playing
    :param screen: the screen
    :param my_socket: the socket we comunicated with the server
    :return:
    """
    screen.fill(GREY)
    draw_text("Thanks for playing!", screen, WINDOW_WIDTH / 3, WINDOW_HEIGHT / 2, 60, BLUE)
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    try:
        my_socket.close()
    except Exception as e:
        traceback.print_exc()
    sys.exit()
