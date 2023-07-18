import tkinter
from tkinter import Label
from tkmacosx import Button


import settings
import utils
from cell import Cell


root = tkinter.Tk()  # using root is a convention
'''
    Override the configuration of window
'''
root.configure(bg="white")
root.geometry(f"{settings.WIDTH}x{settings.HEIGHT}")
root.title("Minesweeper Game")
root.resizable(False, False)  # avoid resizing window both width & height

top_frame = tkinter.Frame(
    root,
    bg="black",
    width=settings.WIDTH,
    height=utils.height_prct(25)
)
top_frame.place(x=0, y=0)

left_frame = tkinter.Frame(
    root,
    bg="black",
    width=utils.width_prct(25),
    height=utils.height_prct(75)
)
left_frame.place(x=0, y=utils.height_prct(25))

center_frame = tkinter.Frame(
    root,
    bg="black",
    width=utils.width_prct(75),
    height=utils.height_prct(75)
)
center_frame.place(x=utils.width_prct(25), y=utils.height_prct(25))

'''
    Creating Top Game Title
'''
top_game_title = Label(
    top_frame,
    bg="black",
    fg="blue",
    text="Minesweeper Game",
    font=("", 60),
)
top_game_title.place(
    x=utils.width_prct(30),
    y=0
)

'''
    Creating Left Sidebar Label
'''
Cell.create_cell_count_label_object(left_frame)
Cell.cell_count_label.place(x=0, y=0)

'''
    Creating Cell Grid
'''
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x=x, y=y)
        c.create_btn_object(center_frame)
        c.cell_btn.grid(row=y, column=x)

Cell.randomize_mines()

'''
    Run the window
'''
root = tkinter.mainloop()
