import pip
import socket
import select
import keyboard
import time
import random
BIND_IP = '0.0.0.0'
PORT = 31987
MAX_NUM_PLAYERS = 7


def install(package):
    pip.main(['install', package])


def findDup(kids):
    for i in range(0, len(kids)-1):
        if kids[i] == kids[i+1]:
            return True
    return False


def mergeSort(list, left_index, right_index):
    if left_index >= right_index:
        return

    mid_index = (right_index + left_index) // 2

    mergeSort(list, left_index, mid_index)
    mergeSort(list, mid_index + 1, right_index)

    merge(list, left_index, right_index, mid_index)


def merge(list, left_index, right_index, mid):

    left_copy = list[left_index:mid+1]
    right_copy = list[mid+1:right_index+1]

    count_left = 0
    count_right = 0
    sorted_count = left_index

    while count_left < len(left_copy) and count_right < len(right_copy):
        if left_copy[count_left] < right_copy[count_right]:
            list[sorted_count] = left_copy[count_left]
            count_left += 1
        else:
            list[sorted_count] = right_copy[count_right]
            count_right += 1
        sorted_count += 1

    while count_left < len(left_copy):
        list[sorted_count] = left_copy[count_left]
        count_left += 1
        sorted_count += 1
    while count_right < len(right_copy):
        list[sorted_count] = right_copy[count_right]
        count_right += 1
        sorted_count += 1


class databases:
    def __init__(self):
        import sqlite3
        self.conn = sqlite3.connect("d.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS kids (
                                        age integer                                        
                                        )""")

    def addKid(self, age):
        self.c.execute(f"INSERT INTO kids VALUES ({age})")

    def isExist(self, age):
        self.c.execute(f"SELECT * FROM kids WHERE age={age}")
        if self.c.fetchone() is None:
            return False
        return True

    def deleteTable(self):
        self.c.execute("DELETE FROM kids")


def drawDymond(high: int=11):
    for i in range(1, high, 2):
        print(int((high - i)) * " ", end="")
        print(i * "* ")
    for i in range(high, 0, -2):
        print(int((high - i)) * " ", end="")
        print(i * "* ")


def drawArrow(width_of_body: int = 3, len_of_body: int = 4, width_of_top: int = 9, height_of_top: int = 5):
    # מצייר עד האמצע
    for i in range((width_of_top//2)):
        if i >= (width_of_top - width_of_body)//2:
            print(len_of_body*"* ", end="")
        else:
            print(len_of_body*"  ", end="")
        print((height_of_top - ((width_of_top//2)-i+1))*"* ")
    # מצייר מהאמצע
    for i in range(width_of_top//2, 0, -1):
        if width_of_body >= width_of_top - (width_of_top - width_of_body) // 2 - i:
            print(len_of_body * "* ", end="")
        else:
            print(len_of_body * "  ", end="")
        print((height_of_top - ((width_of_top//2)-i)-1) * "* ")


def drawRectangle(height: int=5, width: int=10):
    for _ in range(height):
        print(width*"* ")


def drawRect(height: int=5, width: int=10):
    print(width*"* ")   # השורה העליונה
    for _ in range(height-2):
        for i in range(width):
            # אם זה בהתחלה או בסוף
            if i == 0 or i == width-1:
                print("* ", end="")
            else:
                print("  ", end="")
        print()
    print(width * "* ")     # השורה התחתונה


def drawX(len_of_diagnol: int = 5):
    # החלק העליון של האיקס
    for i in range(len_of_diagnol//2):
        print(i*" ", end="")
        print("*", end="")
        print((len_of_diagnol - 2 * i-2) * " ", end="")
        print("*")
    # המרכז
    print(len_of_diagnol//2*" ", end="")
    print("*")

    # החלק התחתון של האיקס
    for j in range(len_of_diagnol//2, 0, -1):
        print((j-1) * " ", end="")
        print("*", end="")
        print((len_of_diagnol - 2 * j) * " ", end="")
        print("*")


def main():
    import pyautogui
    pyautogui.mouseInfo()


def main2():
    drawDymond()
    drawArrow()
    print()
    drawRectangle()
    print()
    drawRect()
    print()
    drawX(9)
    AMOUNT_OF_KIDS = 23
    TIMES = 100
    TIMES_TO_RUN = 1000
    DAYS_IN_A_YEAR = 365
    time_found_double = 0
    avg = 0
    sum = 0
    db = databases()
    for index in range(TIMES_TO_RUN):
        for _ in range(TIMES):
            for _ in range(AMOUNT_OF_KIDS):
                age = random.randint(1, DAYS_IN_A_YEAR)
                if db.isExist(age):
                    db.deleteTable()
                    time_found_double += 1
                    break
                else:
                    db.addKid(age)
        # print(time_found_double)
        # print(time_found_double)
        if avg == 0:
            avg = time_found_double
            sum += time_found_double
        else:
            avg = (avg*index + time_found_double)/(index+1)
            sum += time_found_double
        time_found_double = 0

    print(f"avg={avg}")
    print(f"avg2={sum/TIMES_TO_RUN}")
    # kids = [1]
    # kids.sort()
    # for kid in kids:
    #     print(kid, end=" ")
    # print()
    # mergeSort(kids, 0, len(kids)-1)
    # for kid in kids:
    #     print(kid, end=" ")
    # print()
    # findDup(kids)
    # lst = [["a", "b", "c"], ["d", "e", "f", ["h", "i", "j"]]]
    # keyboard.press_and_release("ctrl + F2")
    # time.sleep(3)
    # print("pressed")
    # print(sum(lst, []))
    # a = None
    # if a:
    #     print(1)
    # elif not a:
    #     print(2)
    # elif a is None:
    #     print(3)


if __name__ == '__main__':
    main()
    # print("before installation")
    # install('pyngrok ')
    # print("after installation")
    # import pyngrok
    # print("done")