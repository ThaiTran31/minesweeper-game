from tkinter import Label
from tkmacosx import Button
import random
import os
import sys

import settings


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label = None

    def __init__(self, x, y, is_mine=False):
        self.x = x
        self.y = y
        self.is_mine_candidate = False
        self.is_opened = False
        self.is_mine = False
        self.cell_btn = None

        Cell.all.append(self)

    def create_btn_object(self, location):
        # button of tkinter is not compatibe with Macos
        # btn = Button(
        #     location,
        #     width=12,
        #     height=4,
        #     bg="blue",
        # )
        btn = Button(
            location,
            width=144,
            height=76,
            bg='gray',
            fg="white",
        )
        btn.bind("<Button-1>", self.left_click_action)
        btn.bind("<Button-2>", self.right_click_action)  # using Button-2 instead of -3 on MacOS with trackpad
        self.cell_btn = btn

    @staticmethod
    def create_cell_count_label_object(location):
        label = Label(
            location,
            bg="black",
            fg="white",
            text=f"Cells Left:{Cell.cell_count}",
            font=("", 30)
        )
        Cell.cell_count_label = label

    def left_click_action(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounding_cells_count == 0:
                for cell in self.surrounding_cells:
                    cell.show_cell()
            self.show_cell()

        if Cell.cell_count == settings.MINES_COUNT:
            message_body = "Congratulation! You won the game!"
            message_title = "Game Over"
            os.system("osascript -e 'Tell application \"System Events\" to display dialog \"" + message_body + "\" with title \"" + message_title + "\"\'")
            sys.exit()

        self.cell_btn.unbind("<Button-1>")
        self.cell_btn.unbind("<Button-2>")

    @property
    def surrounding_cells_count(self):
        return sum([1 for cell in self.surrounding_cells if cell.is_mine])

    @property
    def surrounding_cells(self):
        surrounding_cells = []
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                cell = Cell.get_cell_by_axis(i, j)
                if cell and cell != self:
                    surrounding_cells.append(cell)
        return surrounding_cells

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            Cell.cell_count_label.configure(text=f"Cells Left:{Cell.cell_count}")
            self.cell_btn.configure(text=self.surrounding_cells_count)
            self.is_opened = True

            if self.is_mine_candidate:
                self.is_mine_candidate = False
                self.cell_btn.configure(bg="gray")

    def show_mine(self):
        self.cell_btn.configure(bg="red")
        message_body = "You just clicked on a mine!"
        message_title = "Game Over"
        os.system("osascript -e 'Tell application \"System Events\" to display dialog \"" + message_body + "\" with title \"" + message_title + "\"\'")
        sys.exit()

    def right_click_action(self, event):
        if not self.is_mine_candidate:
            self.cell_btn.configure(bg="orange")
            self.is_mine_candidate = True
        else:
            self.cell_btn.configure(bg="gray")
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True
        print(picked_cells)

    @staticmethod
    def get_cell_by_axis(x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
