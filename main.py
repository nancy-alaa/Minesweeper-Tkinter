from tkinter import *
import settings
import utils
from cell import Cell

# A regular window, root is just a naming convention
root = Tk()

# Override the settings of the window ---------------

# To change the size of the window
# geometry method takes a string WIDTHxHEIGHT
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')

# To change the title of the game
root.title("Minesweeper")

# To change the background color
root.configure(bg='black')

# To make the window not resizable, the first parameter is for
# width, the second for height
root.resizable(False, False)


top_frame = Frame(
    root,
    bg="black",
    width=settings.WIDTH,
    height=utils.height_percentage(25)
)
# Where to place that frame,
# where it starts x-axis and y-axis
top_frame.place(x=0, y=0)

right_frame = Frame(
    root,
    bg="black",
    width=utils.width_percentage(25),
    height=utils.height_percentage(75)
)
right_frame.place(x=utils.width_percentage(75), y=utils.height_percentage(50))


center_frame = Frame(
    root,
    bg="black",
    width=utils.width_percentage(75),
    height=utils.height_percentage(75)
)
center_frame.place(
    x=utils.width_percentage(5),
    y=utils.height_percentage(25)
)


for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        # instead of using place
        c.cell_btn_object.grid(
            column=y, row=x
        )

Cell.randomize_mines()
for c in Cell.all:
    if c.is_mine:
        print(c)

# call the label from Cell class
Cell.create_cell_count_label(right_frame)
Cell.cell_count_label.place(
    x=0, y=0
)


# Run the window
root.mainloop()
