from tkinter import *
from tkinter.ttk import Style
from time import sleep


def pop_up_message(text):
    win = Tk()
    center_window(win, height=100)
    Style(win)
    Label(win, text=text).pack()
    win.update()
    sleep(1.5)
    win.destroy()


def center_window(root, width=600, height=400):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == '__main__':
    pop_up_message('hi')
