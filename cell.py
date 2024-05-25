import sys
from tkinter import Button, Label
import random
import settings
import subprocess


class Cell:
    # to store the 36 instances
    all = []
    cell_count_label = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.is_open = False
        self.is_mine_candidate = False

        # append the object to the Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            # to increase the button's size
            width=12,
            height=4,
        )
        # to assign an event
        # <Button-1> for left click
        btn.bind('<Button-1>', self.left_click_actions)
        # <Button-2> for right click
        btn.bind('<Button-2>', self.right_click_actions)

        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        label = Label(
            location,
            text=f"Cells Left: {settings.CELL_COUNT}",
            width=12,
            height=4,
            bg='black',
            fg='white',
            font="Times 25 italic bold"
        )
        Cell.cell_count_label = label

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell in self.surrounded_cells:
                    cell.show_cell()
            self.show_cell()
            # if mines count is equal to the cells left count, player wins
            if settings.CELL_COUNT == settings.MINES:
                script = f'display dialog "{"Congratulations! YOU WON THE GAME!"}" with title "{"Game Over!"}" buttons {{"OK"}} default button "OK"'
                subprocess.run(["osascript", "-e", script])
                sys.exit()


        # cancel left and right events if the cell is opened
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-2>')



    def show_mine(self):
        # self.cell_btn_object.configure(text='mine')
        script = f'display dialog "{"You clicked on a mine."}" with title "{"Game Over!"}" buttons {{"OK"}} default button "OK"'
        subprocess.run(["osascript", "-e", script])
        sys.exit()



    def get_cell_by_axis(self, x, y):
        # return a cell object based on the value of x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    # read only attribute
    @property
    def surrounded_cells(self):
        sur_cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]
        sur_cells = [cell for cell in sur_cells if cell is not None]

        return sur_cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine: counter += 1
        return counter

    def show_cell(self):
        if not self.is_open:
            settings.CELL_COUNT -= 1
        self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
        # replace the text of cell count label with the new count
        if Cell.cell_count_label:
            Cell.cell_count_label.configure(text=f"Cells Left: {settings.CELL_COUNT}")
        self.is_open = True

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(text='x')
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(text='')
            self.is_mine_candidate = False


    @staticmethod
    def randomize_mines():
        mine_cells = random.sample(
            Cell.all, settings.MINES
        )
        for cell in mine_cells:
            cell.is_mine = True


    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
