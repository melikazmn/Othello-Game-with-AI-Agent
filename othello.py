import time

import pygame
import numpy as np
import copy


# Constants
BOARD_SIZE = 8
SQUARE_SIZE = 50
WIDTH = HEIGHT = BOARD_SIZE * SQUARE_SIZE
FPS = 60

# Colors
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HIGHLIGHT = (200, 200, 0)
RED = (255, 0, 0)

# Players
EMPTY = 0
BLACK_PIECE = 1
WHITE_PIECE = 2


class Othello:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.board[3][3] = self.board[4][4] = WHITE_PIECE
        self.board[3][4] = self.board[4][3] = BLACK_PIECE
        self.current_player = BLACK_PIECE
        self.black_score = 2
        self.white_score = 2
        self.valid_moves = []  # Track valid moves for the current player
        self.game_over = False

    def draw_board(self, screen):
        screen.fill(GREEN)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
                if (row, col) in self.valid_moves:
                    pygame.draw.rect(screen, HIGHLIGHT,
                                     (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
                if self.board[row][col] == BLACK_PIECE:
                    pygame.draw.circle(screen, BLACK,
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                       SQUARE_SIZE // 2 - 5)
                elif self.board[row][col] == WHITE_PIECE:
                    pygame.draw.circle(screen, WHITE,
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                       SQUARE_SIZE // 2 - 5)

        # Display current turn and score
        font = pygame.font.Font(None, 32)
        turn_text = "Turn: Black" if self.current_player == BLACK_PIECE else "Turn: White"
        turn_surface = font.render(turn_text, True, BLACK)
        screen.blit(turn_surface, (10, HEIGHT + 10))

        score_text = f"Black: {self.black_score}  White: {self.white_score}"
        score_surface = font.render(score_text, True, BLACK)
        screen.blit(score_surface, (10, HEIGHT + 50))

    def is_valid_move(self, row, col, player):
        if self.board[row][col] != EMPTY:
            return False
        opponent = WHITE_PIECE if player == BLACK_PIECE else BLACK_PIECE
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for d in directions:
            r, c = row + d[0], col + d[1]
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == opponent:
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    r += d[0]
                    c += d[1]
                    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                        break
                    if self.board[r][c] == player:
                        return True
                    if self.board[r][c] == EMPTY:
                        break
        return False

    def update_scores(self):
        self.black_score = np.sum(self.board == BLACK_PIECE)
        self.white_score = np.sum(self.board == WHITE_PIECE)

    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def update_valid_moves(self):
        self.valid_moves = self.get_valid_moves(self.current_player)


    def is_game_over(self):
        if np.all(self.board != EMPTY) or (
                not self.get_valid_moves(BLACK_PIECE) and not self.get_valid_moves(WHITE_PIECE)):
            self.game_over = True
        return self.game_over

    def apply_move(self, row, col, player):
        opponent = WHITE_PIECE if player == BLACK_PIECE else BLACK_PIECE
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        self.board[row][col] = player
        for d in directions:
            r, c = row + d[0], col + d[1]
            cells_to_flip = []
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == opponent:
                cells_to_flip.append((r, c))
                r += d[0]
                c += d[1]
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                for (r, c) in cells_to_flip:
                    self.board[r][c] = player
        self.update_scores()

    def switch_turn(self):
        self.current_player = WHITE_PIECE if self.current_player == BLACK_PIECE else BLACK_PIECE
