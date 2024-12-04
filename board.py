import pygame

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[None for i in range(9)] for j in range(9)]

    def draw(self):
        cell_w = self.width // 9
        cell_h = self.height // 9
        for i in range(10):
            if i % 3 == 0:
                line_thickness = 3
            else:
                line_thickness = 1

            # horizontal
            pygame.draw.line(
                self.screen,
                'black',
                (0, i * cell_h),
                (self.width, i * cell_h),
                line_thickness
            )

            # vertical
            pygame.draw.line(
                self.screen,
                'black',
                (i * cell_w, 0),
                (i * cell_w, self.height),
                line_thickness
            )

            for i in self.cells:
                for cell in i:
                    cell.draw(self.screen)

    def select(self, row, col):
        self.selected_row = row
        self.selected_col = col

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

    def click(self, x, y):
        if x < self.width and y < self.height:
            cell_width = self.width // 9
            cell_height = self.height // 9
            return (y // cell_height, x // cell_width)
        return None

    def sketch(self, value):
        if (self.selected_row is not None and self.selected_col is not None and
                self.original_board[self.selected_row][self.selected_col] == 0 and
                self.cells[self.selected_row][self.selected_col] == 0):
            self.sketched_numbers[self.selected_row][self.selected_col] = value

    def place_number(self, number):
        pass

    def reset_to_original(self):
        pass

    def is_full(self):
        pass

    def update_board(self):
        pass

    def find_empty(self):
        pass

    def check_board(self):
        pass
