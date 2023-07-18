import tkinter as tk
from tkinter import Frame, Label

import settings as st
import utils
from cell import Cell


window = tk.Tk()
window.title("Minesweeper")
window.geometry(f"{st.WIDTH}x{st.HEIGHT}")
window.resizable(False, False)
window.configure(
    bg="black"
)

top_frame = Frame(
    window,
    width=utils.width_prct(100),
    height=utils.height_prct(25),
    bg="black",
)
top_frame.place(x=0, y=0)

left_frame = Frame(
    window,
    width=utils.width_prct(25),
    height=utils.height_prct(75),
    bg="black",
)
left_frame.place(x=0, y=utils.height_prct(25))


main_frame = Frame(
    window,
    width=utils.width_prct(75),
    height=utils.height_prct(75),
    bg="black",
)
main_frame.place(x=utils.width_prct(25), y=utils.height_prct(25))

top_title = Label(
    top_frame,
    bg="black",
    fg="blue",
    text="Minesweeper Game",
    font=("", st.GAME_TOP_TITLE_FONTSIZE),
)
top_title.place(x=utils.width_prct(25), y=0)

for i in range(st.GRID_SIZE):
    for j in range(st.GRID_SIZE):
        cell = Cell(x=i, y=j)
        cell.create_btn_object(main_frame)
        cell.cell_btn.grid(
            column=i,
            row=j
        )
Cell.create_cell_count_label_object(left_frame)
Cell.cell_count_label.place(x=0, y=0)

Cell.randomize_mines()


window.mainloop()
