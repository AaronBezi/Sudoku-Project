import pygame
import sys
from board import Board

pygame.init()

# CONSTANTS

# colors for buttons and other stuff
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (200, 230, 255)  # light blue background
ORANGE = (255, 165, 0) # button color

# game window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku")

# game states
START = "start"
PLAYING = "playing"
GAME_OVER = "game_over"
GAME_WON = "game_won"

# class that draws and controls all the main functions of the game
class Game:
    # starts screen with no board
    def __init__(self):
        self.state = START
        self.board = None

    # draws the start screen
    def draw_start_screen(self):
        screen.fill(LIGHT_BLUE)
        # title
        font = pygame.font.Font(None, 60)
        title = font.render("Welcome to Sudoku", True, BLACK)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 100))

        # adds difficulty buttons
        font = pygame.font.Font(None, 40)
        difficulties = ["EASY", "MEDIUM", "HARD"]
        button_y = 300

        for diff in difficulties:
            button = pygame.Rect(WINDOW_WIDTH // 2 - 100, button_y, 200, 50)
            pygame.draw.rect(screen, ORANGE, button)
            text = font.render(diff, True, BLACK)
            screen.blit(text, (button.centerx - text.get_width() // 2, button.centery - text.get_height() // 2))
            button_y += 70

    # draws the main game screen with the board and buttons
    def draw_game_screen(self):
        screen.fill(LIGHT_BLUE)

        # Center the board at the top of the screen
        board_x = (WINDOW_WIDTH - 500) // 2
        board_y = 50  # space from the top

        # white board background
        pygame.draw.rect(screen, WHITE, (board_x, board_y, 500, 500))

        # draws the board
        if self.board:
            old_screen = self.board.screen.copy()
            self.board.screen = screen.subsurface(pygame.Rect(board_x, board_y, 500, 500))
            self.board.draw()
            self.board.screen = old_screen

        # adds the control buttons
        font = pygame.font.Font(None, 40)
        buttons = ["RESET", "RESTART", "EXIT"]
        button_y = board_y + 520
        button_width = 150
        button_height = 50
        spacing = (WINDOW_WIDTH - (button_width * 3)) // 4

        for i, text in enumerate(buttons):
            button_x = spacing + i * (button_width + spacing)
            button = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, ORANGE, button)
            text_surface = font.render(text, True, BLACK)
            screen.blit(text_surface, (button.centerx - text_surface.get_width() // 2,
                                       button.centery - text_surface.get_height() // 2))

    # draws the win and loss screens
    def draw_end_screen(self, won=True):
        screen.fill(LIGHT_BLUE)
        font = pygame.font.Font(None, 80)

        # different messages depending on if user won or lost
        if won:
            text = "Game Won!"
            button_text = "EXIT"
        else:
            text = "Game Over :("
            button_text = "RESTART"

        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, 250))

        # adds button
        button = pygame.Rect(WINDOW_WIDTH // 2 - 125, 400, 250, 60)
        pygame.draw.rect(screen, ORANGE, button)
        font = pygame.font.Font(None, 40)
        button_surface = font.render(button_text, True, BLACK)
        screen.blit(button_surface, (button.centerx - button_surface.get_width() // 2,
                                     button.centery - button_surface.get_height() // 2))

    # handles what happens when a player clicks something
    def handle_click(self, pos):
        x, y = pos

        if self.state == START:
            # check if a player clicked a difficulty button
            if WINDOW_WIDTH // 2 - 100 <= x <= WINDOW_WIDTH // 2 + 100:
                if 300 <= y <= 350:
                    self.board = Board(500, 500,
                                       screen.subsurface(pygame.Rect((WINDOW_WIDTH - 500) // 2, 50, 500, 500)), "easy")
                    self.state = PLAYING
                elif 370 <= y <= 420:
                    self.board = Board(500, 500,
                                       screen.subsurface(pygame.Rect((WINDOW_WIDTH - 500) // 2, 50, 500, 500)),
                                       "medium")
                    self.state = PLAYING
                elif 440 <= y <= 490:
                    self.board = Board(500, 500,
                                       screen.subsurface(pygame.Rect((WINDOW_WIDTH - 500) // 2, 50, 500, 500)), "hard")
                    self.state = PLAYING

        # converts the click position to the board position
        elif self.state == PLAYING:
            board_x = (WINDOW_WIDTH - 500) // 2
            board_y = 50

            # adjust click position relative to board
            board_relative_x = x - board_x
            board_relative_y = y - board_y

            # check if clicked on board
            if 0 <= board_relative_x < 500 and 0 <= board_relative_y < 500:
                cell = self.board.click(board_relative_x, board_relative_y)
                if cell:
                    self.board.select(cell[0], cell[1])

            # check button clicking
            button_y = board_y + 520
            button_width = 150
            spacing = (WINDOW_WIDTH - (button_width * 3)) // 4

            if button_y <= y <= button_y + 50:
                # reset button
                if spacing <= x <= spacing + button_width:
                    self.board.reset_to_original()
                # restart button
                elif 2 * spacing + button_width <= x <= 2 * spacing + 2 * button_width:
                    self.state = START
                # exit button
                elif 3 * spacing + 2 * button_width <= x <= 3 * spacing + 3 * button_width:
                    pygame.quit()
                    sys.exit()

        # handles end screen clicking
        elif self.state in [GAME_WON, GAME_OVER]:
            if (WINDOW_WIDTH // 2 - 125 <= x <= WINDOW_WIDTH // 2 + 125 and
                    400 <= y <= 460):
                if self.state == GAME_WON:
                    pygame.quit()
                    sys.exit()
                else:
                    self.state = START


def main():
    game = Game()
    running = True

    # game loop
    while running:
        # handles what the player can do
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)

            if event.type == pygame.KEYDOWN and game.state == PLAYING:
                if event.key == pygame.K_RETURN:
                    # submit a number and check if the player won the game
                    game.board.place_number()
                    if game.board.is_full():
                        if game.board.check_board():
                            game.state = GAME_WON
                        else:
                            game.state = GAME_OVER

                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                   pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    # add a sketched number
                    num = int(event.unicode)
                    game.board.sketch(num)

                elif event.key == pygame.K_BACKSPACE:
                    game.board.clear()

                # arrow key navigation
                elif event.key == pygame.K_UP:
                    game.board.move_selection("up")
                elif event.key == pygame.K_DOWN:
                    game.board.move_selection("down")
                elif event.key == pygame.K_LEFT:
                    game.board.move_selection("left")
                elif event.key == pygame.K_RIGHT:
                    game.board.move_selection("right")

        # draw current screen
        if game.state == START:
            game.draw_start_screen()
        elif game.state == PLAYING:
            game.draw_game_screen()
        elif game.state == GAME_WON:
            game.draw_end_screen(True)
        elif game.state == GAME_OVER:
            game.draw_end_screen(False)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()