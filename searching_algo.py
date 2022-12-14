import os

ROW = 22
COL = 20
START_ROW = 2
CURRENT_PATH = os.getcwd()
PICTURES = {}
menu = {"selected" :{
    "start": False, "end": False, "wall": False, "go": False
}}
matrix_pos = {
    "start coordinates": None,
    "exit coordinates": None
}
directions = {
    "up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0),
    "top left diagonal": (-1, -1), "bottom left diagonal": (-1, 1),
    "top right diagonal": (1, -1), "bottom right diagonal": (1, 1)}


def load_pictures():
    for file_name in os.listdir("Pictures"):
        if file_name.endswith(".png"):
            PICTURES[file_name[:-4]] = f"{os.getcwd()}\pictures\{file_name}"


def check_valid_index(row, col):
    return 0 <= row < ROW and 0 <= col < COL


def create_matrix():
    puzzel_field = [[int(0) for _ in range(COL)] for _ in range(ROW)]
    for row in range(ROW):
        for col in range(COL):
            if row in (0, 1):
                if col == 0 or col == 1:
                    puzzel_field[row][col] = Figure("MENU START", (row, col))
                    puzzel_field[row][col].picture = "square_start_point"
                elif col == 3 or col == 4:
                    puzzel_field[row][col] = Figure("MENU STOP", (row, col))
                    puzzel_field[row][col].picture = "square_end_point"
                elif col == 6 or col == 7:
                    puzzel_field[row][col] = Figure("MENU WALL", (row, col))
                    puzzel_field[row][col].picture = "square_wall"
                elif col == 9 or col == 10:
                    puzzel_field[row][col] = Figure("MENU GO", (row, col))
                    puzzel_field[row][col].picture = "square_start"
                else:
                    puzzel_field[row][col] = Figure("BLANK", (row, col))
                    puzzel_field[row][col].picture = "square_b"

            elif row < START_ROW:
                puzzel_field[row][col] = Figure("BLANK", (row, col))
                puzzel_field[row][col].picture = "square_b"
            else:
                puzzel_field[row][col] = Figure("square_empty",(row, col))
    return puzzel_field


class Figure:

    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.visited = "No"
        self.wall_square = False
        self.picture = "square_empty"

    def show_square(self):
        self.picture = self.name

    def position_add(self, symbol, position, picture):
        old_pos = matrix_pos[position]
        if old_pos:
            old_pos.picture = "square_empty"
        self.picture = picture
        matrix_pos[position] = symbol

    def wall(self, shooting):
        if self.wall_square and not shooting:
            self.wall_square = False
            self.picture = "square_empty"
        else:
            self.wall_square = True
            self.picture = "square_wall"

    def check_col(self, symbol):
        if any(symbol == x for x in matrix_pos.values()) or self.wall_square:
            return
        self.picture = "square_v"


load_pictures()

