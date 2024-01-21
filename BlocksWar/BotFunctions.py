# This file is for the bot to know where he is in the world
# and what to do from this position

import enum
from constants import GameConstans
from Player import *
AI_INDEX = 1
UPPER_LEFT_INDEX = 1
UPPER_RIGHT_INDEX = 0
MIDDLE_INDEX = 2


def createMiddleToRight():
    """
    func to create the instruction for the bot to go from the middle floor to the upper right floor
    :return: list
    """
    commands_lst = [["jump"], [None for _ in range(10)], ["jump"], ["right" for _ in range(30)], ["jump"],
           [None for _ in range(10)], ["jump"], [None for _ in range(10)], ["jump"], ["right"],
           [None for _ in range(5)], ["jump"]]
    return fixList(commands_lst)


def createUpperLeftToUpperRight():
    """
    func to create the instruction for the bot to go from the upper left floor to the upper right floor
    :return: list
    """
    commands_lst = [["jump"], ["right" for _ in range(40)], ["jump"], ["right" for _ in range(40)], ["jump"]]
    return fixList(commands_lst)


def createUnderRight():
    """
    func to create the instruction for the bot to go from the under the upper right floor to the upper right floor
    :return: list
    """
    commands_lst = [["left" for _ in range(30)], createMiddleToRight()]
    return fixList(commands_lst)


def createDeepUnderRight():
    """
    func to create the instruction for the bot to go from the under the upper right floor to the upper right floor
    :return: list
    """
    commands_lst = [["left" for _ in range(40)], createMiddleToRight()]
    return fixList(commands_lst)


def createMiddleToLeft():
    """
    func to create the instruction for the bot to go from the middle floor to the upper left floor
    :return: list
    """
    commands_lst = [["jump"], [None for _ in range(10)], ["jump"], ["left" for _ in range(30)], ["jump"],
           [None for _ in range(10)], ["jump"], [None for _ in range(10)], ["jump"], ["left"],
           [None for _ in range(5)], ["jump"]]
    return fixList(commands_lst)


def createUpperRightToUpperLeft():
    """
    func to create the instruction for the bot to go from the upper right floor to the upper left floor
    :return: list
    """
    commands_lst = [["jump"], ["left" for _ in range(40)], ["jump"],
           ["left" for _ in range(40)], ["jump"]]
    return fixList(commands_lst)


def createUnderLeft():
    """
    func to create the instruction for the bot to go from the under the upper left floor to the upper left floor
    :return: list
    """
    commands_lst = [["right" for _ in range(20)], createMiddleToLeft()]
    return fixList(commands_lst)


def createDeepUnderLeft():
    """
    func to create the instruction for the bot to go from the under the upper left floor to the upper left floor
    :return: list
    """
    commands_lst = [["right" for _ in range(40)], createMiddleToLeft()]
    return fixList(commands_lst)


def createUpperLeftToMiddle():
    commands_lst = [["upper left to middle"], ["right" for _ in range(55)]]
    return fixList(commands_lst)


def createUpperRightToMiddle():
    commands_lst = [["upper right to middle"], ["left" for _ in range(55)]]
    return fixList(commands_lst)


def fixList(commands_lst):
    """
    func to fix the list from format of list inside list, to one list.
    from - [["a", "b"], ["c"]] to ["a", "b", "c"]
    :param commands_lst: the list to fix
    :return: list
    """
    fixed_list = []
    for item in sum(commands_lst, []):
        fixed_list.append(item)
    return fixed_list


def pickWay(player, bot):
    """
    func to pick which instruction needed for the position of the player and the bot.
    func will return the instructions to go with
    :param player: the player
    :param bot: the bot
    :return: list
    """
    way_to_go = []
    if isUpperLeftToUpperRight(player, bot):
        way_to_go = WaysToGo.UPPER_LEFT_UPPER_RIGHT.value
    elif isDeepUnderRight(player, bot):
        way_to_go = WaysToGo.DEEP_UNDER_RIGHT.value
    elif isUnderRight(player, bot):
        way_to_go = WaysToGo.UNDER_RIGHT.value
    elif isMiddleToRight(player, bot):
        way_to_go = WaysToGo.MIDDLE_TO_RIGHT.value
    elif isUpperRightToUpperLeft(player, bot):
        way_to_go = WaysToGo.UPPER_RIGHT_UPPER_LEFT.value
    elif isDeepUnderLeft(player, bot):
        way_to_go = WaysToGo.DEEP_UNDER_LEFT.value
    elif isUnderLeft(player, bot):
        way_to_go = WaysToGo.UNDER_LEFT.value
    elif isMiddleToLeft(player, bot):
        way_to_go = WaysToGo.MIDDLE_TO_LEFT.value
    elif isUpperLeftToMiddle(player, bot):
        way_to_go = WaysToGo.UPPER_LEFT_TO_MIDDLE.value
    elif isUpperRightToMiddle(player, bot):
        way_to_go = WaysToGo.UPPER_RIGHT_TO_MIDDLE.value
    return way_to_go


def isUpperLeftToUpperRight(player, bot):
    """
    func to return whether the bot is on the upper left floor, and the player is of the upper right floor
    :param player: the player
    :param bot: the bot
    :return: bool
    """
    if player.get_y() + SIZE_OF_CHARACTER <= GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and\
        bot.get_y() + SIZE_OF_CHARACTER == GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and\
        player.get_x() + SIZE_OF_CHARACTER > GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x and\
            GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x-10 < bot.get_x() < GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x:
        return True
    return False


def isMiddleToRight(player, bot):
    """
    func to return whether the bot is on the middle floor, and the player is on the upper right floor
    :param player: the player
    :param bot: the bot
    :return: bool
    """
    if player.get_y() + SIZE_OF_CHARACTER <= GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and \
            bot.get_y() + SIZE_OF_CHARACTER == GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].y and \
            GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x - 100 < bot.get_x() < GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x - 60 and \
            player.get_x() + SIZE_OF_CHARACTER > GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x:
        return True
    return False


def isUnderRight(player, bot):
    """
    func to return whether the bot is under the upper right floor, and the player is on the upper right floor
    :param player: the player
    :param bot: the bot
    :return: bool
    """
    if player.get_y() + SIZE_OF_CHARACTER <= GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and \
            bot.get_y() + SIZE_OF_CHARACTER == GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].y and \
            GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x - SIZE_OF_CHARACTER < bot.get_x() < GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x and \
            player.get_x() + SIZE_OF_CHARACTER > GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x:
        return True
    return False


def isDeepUnderRight(player, bot):
    """
        func to return whether the bot is under the upper right floor, and the player is on the upper right floor
        :param player: the player
        :param bot: the bot
        :return: bool
        """
    if player.get_y() + SIZE_OF_CHARACTER <= GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and \
            bot.get_y() + SIZE_OF_CHARACTER == GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].y and \
            GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x < bot.get_x() < GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x + SIZE_OF_CHARACTER and \
            player.get_x() + SIZE_OF_CHARACTER > GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x:
        return True
    return False


def isUpperRightToUpperLeft(player, bot):
    """
    func to return whether the bot is on the upper right floor, and the player is of the upper left floor
    :param player: the player
    :param bot: the bot
    :return: bool
    """
    if player.get_y() + SIZE_OF_CHARACTER <= GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and\
        bot.get_y() + SIZE_OF_CHARACTER == GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and\
        player.get_x() + SIZE_OF_CHARACTER < GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x and\
            GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x-10 < bot.get_x() < GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x:
        return True
    return False


def isMiddleToLeft(player, bot):
    """
    func to return whether the bot is on the middle floor, and the player is on the upper left floor
    :param player: the player
    :param bot: the bot
    :return: bool
    """
    if player.get_y() + SIZE_OF_CHARACTER <= GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and \
            bot.get_y() + SIZE_OF_CHARACTER == GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].y and \
            GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x + 60 < bot.get_x() < GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x + 100 and \
            player.get_x() - SIZE_OF_CHARACTER < GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x:
        return True
    return False


def isUnderLeft(player, bot):
    """
    func to return whether the bot is under the upper left floor, and the player is on the upper left floor
    :param player: the player
    :param bot: the bot
    :return: bool
    """
    if player.get_y() + SIZE_OF_CHARACTER <= GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and \
            bot.get_y() + SIZE_OF_CHARACTER == GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].y and \
            GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x < bot.get_x() < GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x + SIZE_OF_CHARACTER and \
            player.get_x() < GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x:
        return True
    return False


def isDeepUnderLeft(player, bot):
    """
    func to return whether the bot is under the upper left floor, and the player is on the upper left floor
    :param player: the player
    :param bot: the bot
    :return: bool
    """
    if player.get_y() + SIZE_OF_CHARACTER <= GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and \
            bot.get_y() + SIZE_OF_CHARACTER == GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].y and \
            GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x - SIZE_OF_CHARACTER < bot.get_x() < GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x and \
            player.get_x() < GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x:
        return True
    return False


def isUpperLeftToMiddle(player, bot):
    if bot.get_y() + SIZE_OF_CHARACTER <= GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and \
            player.get_y() + SIZE_OF_CHARACTER == GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].y and \
            GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x - SIZE_OF_CHARACTER < player.get_x() < GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x + SIZE_OF_CHARACTER and \
            GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x - SIZE_OF_CHARACTER < bot.get_x() < GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].x:
        return True
    return False


def isUpperRightToMiddle(player, bot):
    if bot.get_y() + SIZE_OF_CHARACTER <= GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].y and \
            player.get_y() + SIZE_OF_CHARACTER == GameConstans.FLOORS_RECTS.value[MIDDLE_INDEX].y and \
            GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x - 2*SIZE_OF_CHARACTER <= player.get_x() <= GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x + 2*SIZE_OF_CHARACTER and \
            GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x - SIZE_OF_CHARACTER < bot.get_x() < GameConstans.FLOORS_RECTS.value[UPPER_RIGHT_INDEX].x:
        return True
    return False


class WaysToGo(enum.Enum):
    """
    this class contain constants.
    each constance contain list that represent instructions for the bot do to in order to get the point it need
    the instructions are built from "right" "left" "jump" and None
    "left" is for the bot to go one "step" left
    "right" is for the bot to go one "step" right
    "jump" is for the bot to jump
    "None" is for the bot to hold
    """
    UPPER_LEFT_UPPER_RIGHT = createUpperLeftToUpperRight()  # give instruction to the bot to go from upper left to upper right
    MIDDLE_TO_RIGHT = createMiddleToRight()                 # give instruction to the bot to go from middle to upper right
    UNDER_RIGHT = createUnderRight()                        # give instruction to the bot to go from under the upper right to upper right
    UPPER_RIGHT_UPPER_LEFT = createUpperRightToUpperLeft()  # give instruction to the bot to go from upper right to upper left
    MIDDLE_TO_LEFT = createMiddleToLeft()                   # give instruction to the bot to go from the middle to upper left
    UNDER_LEFT = createUnderLeft()                          # give instruction to the bot to go from under the upper left to upper left
    DEEP_UNDER_RIGHT = createDeepUnderRight()
    DEEP_UNDER_LEFT = createDeepUnderLeft()
    UPPER_LEFT_TO_MIDDLE = createUpperLeftToMiddle()
    UPPER_RIGHT_TO_MIDDLE = createUpperRightToMiddle()
