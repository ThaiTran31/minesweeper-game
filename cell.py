from tkmacosx import Button
import random
from tkinter import Label
import sys
import os

import settings as st


class Cell:
    all = []
    cell_count = st.CELL_COUNT
    cell_count_label = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine_candidate = False
        self.is_opened = False
        self.is_mine = False
        self.cell_btn = None
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=st.GAME_BUTTON_WIDTH,
            height=st.GAME_BUTTON_HEIGHT,
            bg=st.GAME_BUTTON_BACKGROUND_COLOR,
            fg=st.GAME_BUTTON_TEXT_COLOR,
        )
        btn.bind("<Button-1>", self.left_click_handler)
        btn.bind("<Button-2>", self.right_click_handler)
        self.cell_btn = btn

    @staticmethod
    def game_over(is_won=False):
        message_title = "Game Over"
        message_body = "You just clicked on a mine!"
        if is_won:
            message_body = "Congratulation! You won the game!"
        os.system("osascript -e 'Tell application \"System Events\" to display dialog \"" + message_body + "\" with title \"" + message_title + "\"\'")
        sys.exit()

    @staticmethod
    def create_cell_count_label_object(location):
        label = Label(
            location,
            bg="black",
            fg="white",
            text=f"Cell Left: {Cell.cell_count}",
            font=("", st.GAME_CELL_COUNT_LABEL_FONTSIZE)
        )
        Cell.cell_count_label = label

    def left_click_handler(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            self.show_cell()
            if self.get_surrounding_mines_count() == 0:
                for cell in self.get_surrounding_cells():
                    cell.show_cell()

            if Cell.cell_count == st.MINE_COUNT:
                Cell.game_over(True)

            self.cell_btn.unbind("<Button-1>")
            self.cell_btn.unbind("<Button-2>")

    def show_cell(self):
        if not self.is_opened:
            self.cell_btn.configure(
                text=self.get_surrounding_mines_count(),
            )
            Cell.cell_count -= 1
            Cell.cell_count_label.configure(text=f"Cell Left: {Cell.cell_count}")
            if self.is_mine_candidate:
                self.cell_btn.configure(bg=st.GAME_BUTTON_BACKGROUND_COLOR)
                self.is_mine_candidate = False
            self.is_opened = True

    def get_surrounding_mines_count(self):
        return sum([1 for cell in self.get_surrounding_cells() if cell.is_mine])

    def get_surrounding_cells(self):
        surrounding_cells = []
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if i != self.x or j != self.y:
                    cell = Cell.get_cell_by_axis(i, j)
                    if cell:
                        surrounding_cells.append(cell)
        return surrounding_cells

    def show_mine(self):
        self.cell_btn.configure(bg="red")
        Cell.game_over()

    def right_click_handler(self, event):
        if self.is_mine_candidate:
            self.cell_btn.configure(bg=st.GAME_BUTTON_BACKGROUND_COLOR)
            self.is_mine_candidate = False
        else:
            self.cell_btn.configure(bg="yellow")
            self.is_mine_candidate = True

    @staticmethod
    def get_cell_by_axis(x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
        # default
        return None

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all,
            st.MINE_COUNT
        )
        for cell in picked_cells:
            cell.is_mine = True
        print(picked_cells)

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
