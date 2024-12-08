import pygame
from sudoku_generator import generate_sudoku

class Board:
    def __init__(self, width, height, screen, difficulty):
        # basic board properties
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

        # determine how many tiles to remove based on the difficulty of the game
        if difficulty == "easy":
            removed = 30
        elif difficulty == "medium":
            removed = 40
        else:
            removed = 50

        # make the board
        self.cells = generate_sudoku(9, removed)
        self.selected_row = None
        self.selected_col = None

        # save the starting board and create space for the sketched numbers
        self.original_board = []
        self.sketched_numbers = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            self.original_board.append(self.cells[i].copy())

    # draws the entire board; grid, numbers, and highlights
    def draw(self):
        cell_width = self.width // 9
        cell_height = self.height // 9

        # highlight the selected cell in yellow
        if self.selected_row is not None and self.selected_col is not None:
            pygame.draw.rect(self.screen, (255, 255, 200),
                             (self.selected_col * cell_width,
                              self.selected_row * cell_height,
                              cell_width, cell_height))

        # draw the grid lines
        for i in range(10):
            # determine line thickness
            if i == 0 or i == 9:  # outer edges
                thickness = 4
            elif i % 3 == 0:  # box lines
                thickness = 3
            else:  # regular lines
                thickness = 1

            # draw the horizontal and vertical lines
            y_pos = i * cell_height if i < 9 else self.height - thickness // 2
            pygame.draw.line(self.screen, (0, 0, 0),
                             (0, y_pos),
                             (self.width, y_pos), thickness)

            # vertical lines - for the last line, explicitly use self.width
            x_pos = i * cell_width if i < 9 else self.width - thickness // 2
            pygame.draw.line(self.screen, (0, 0, 0),
                             (x_pos, 0),
                             (x_pos, self.height), thickness)

        # draw numbers
        font = pygame.font.Font(None, 40)
        sketch_font = pygame.font.Font(None, 30)

        for i in range(9):
            for j in range(9):
                x = j * cell_width + (cell_width // 3)
                y = i * cell_height + (cell_height // 3)

                # draw the permanent numbers in black
                if self.cells[i][j] != 0:
                    num = font.render(str(self.cells[i][j]), True, (0, 0, 0))
                    self.screen.blit(num, (x, y))
                # draw the sketched numbers in the top left corner and in blue
                elif self.sketched_numbers[i][j] != 0:
                    num = sketch_font.render(str(self.sketched_numbers[i][j]), True, (0, 0, 255))
                    self.screen.blit(num, (j * cell_width + 5, i * cell_height + 5))

    # selects a cell on the board
    def select(self, row, col):
        self.selected_row = row
        self.selected_col = col

    # allows to move the selected cell with arrow keys
    def move_selection(self, direction):
        if self.selected_row is None:
            self.selected_row = 0
            self.selected_col = 0
            return

        if direction == "up":
            self.selected_row = (self.selected_row - 1) % 9
        elif direction == "down":
            self.selected_row = (self.selected_row + 1) % 9
        elif direction == "left":
            self.selected_col = (self.selected_col - 1) % 9
        elif direction == "right":
            self.selected_col = (self.selected_col + 1) % 9

    # handles the mouse clicks on the board
    def click(self, x, y):
        if x < self.width and y < self.height:
            cell_width = self.width // 9
            cell_height = self.height // 9
            return (y // cell_height, x // cell_width)
        return None

    # adds a temporary number to a cell
    def sketch(self, value):
        if (self.selected_row is not None and self.selected_col is not None and
                self.original_board[self.selected_row][self.selected_col] == 0 and
                self.cells[self.selected_row][self.selected_col] == 0):
            self.sketched_numbers[self.selected_row][self.selected_col] = value

    # places the number on the board permanently
    def place_number(self):
        if (self.selected_row is not None and self.selected_col is not None and
                self.original_board[self.selected_row][self.selected_col] == 0 and
                self.sketched_numbers[self.selected_row][self.selected_col] != 0):  # only place if there's a sketched number
            self.cells[self.selected_row][self.selected_col] = self.sketched_numbers[self.selected_row][self.selected_col]
            self.sketched_numbers[self.selected_row][self.selected_col] = 0

    # remove numbers from a cell
    def clear(self):
        if (self.selected_row is not None and self.selected_col is not None and self.original_board[self.selected_row][self.selected_col] == 0):
            self.sketched_numbers[self.selected_row][self.selected_col] = 0
            self.cells[self.selected_row][self.selected_col] = 0

    # resets to the original board
    def reset_to_original(self):
        for i in range(9):
            self.cells[i] = self.original_board[i].copy()
            self.sketched_numbers[i] = [0] * 9

    # checks if all the cells are filled
    def is_full(self):
        for row in self.cells:
            if 0 in row:
                return False
        return True

    # checks if the solution is correct
    def check_board(self):
        # check rows
        for row in self.cells:
            if len(set(row)) != 9 or 0 in row:
                return False

        # check columns
        for col in range(9):
            column = [self.cells[row][col] for row in range(9)]
            if len(set(column)) != 9 or 0 in column:
                return False

        # check boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(self.cells[box_row + i][box_col + j])
                if len(set(box)) != 9 or 0 in box:
                    return False

        return True