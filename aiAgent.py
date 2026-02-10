# Constants
import copy

import numpy as np

BOARD_SIZE = 8
SQUARE_SIZE = 50
WIDTH = HEIGHT = BOARD_SIZE * SQUARE_SIZE
FPS = 60

# Colors
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HIGHLIGHT = (200, 200, 0)

# Players
EMPTY = 0
BLACK_PIECE = 1
WHITE_PIECE = 2

class AIAgent:
    def __init__(self, player):
        self.player = player

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
           Minimax search with alpha–beta pruning.
           Explores the game tree up to a fixed depth and evaluates board states
           using a heuristic based on piece difference.

           alpha: best score achievable by the maximizer so far
           beta: best score achievable by the minimizer so far
           """
        valid_moves = self.get_valid_moves(board, WHITE_PIECE if maximizing_player else BLACK_PIECE)
        # Terminal condition: depth limit reached or no legal moves available
        if depth == 0 or not valid_moves:
            # Heuristic evaluation: material advantage (white - black)
            return np.sum(board == WHITE_PIECE) - np.sum(board == BLACK_PIECE)
        if maximizing_player:
            max_eval = -float('inf')
            for (row, col) in valid_moves:
                new_board = copy.deepcopy(board)
                self.apply_move(new_board, row, col, WHITE_PIECE)
                eval = self.minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                # Alpha–beta pruning: stop exploring this branch if it cannot improve the result
                if beta <= alpha:
                    break
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for (row, col) in valid_moves:
                new_board = copy.deepcopy(board)
                self.apply_move(new_board, row, col, BLACK_PIECE)
                eval = self.minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, board):
        """
         Selects the optimal move by evaluating all legal actions
         using depth-limited minimax search.
         """
        best_move = None
        best_score = -float('inf') if self.player == WHITE_PIECE else float('inf')
        valid_moves = self.get_valid_moves(board, self.player)
        for (row, col) in valid_moves:
            new_board = copy.deepcopy(board)
            self.apply_move(new_board, row, col, self.player)
            score = self.minimax(new_board, 3, -float('inf'), float('inf'), self.player == BLACK_PIECE)
            if self.player == WHITE_PIECE:
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
            else:
                if score < best_score:
                    best_score = score
                    best_move = (row, col)
        return best_move

    def get_valid_moves(self, board, player):
        """
        Generates all legal moves for the given player by checking
        board positions according to Othello rules.
        """
        valid_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_valid_move(board, row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def is_valid_move(self, board, row, col, player):
        if board[row][col] != EMPTY:
            return False
        opponent = WHITE_PIECE if player == BLACK_PIECE else BLACK_PIECE
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for d in directions:
            r, c = row + d[0], col + d[1]
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == opponent:
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    r += d[0]
                    c += d[1]
                    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                        break
                    if board[r][c] == player:
                        return True
                    if board[r][c] == EMPTY:
                        break
        return False

    def apply_move(self, board, row, col, player):
        opponent = WHITE_PIECE if player == BLACK_PIECE else BLACK_PIECE
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        board[row][col] = player
        for d in directions:
            r, c = row + d[0], col + d[1]
            cells_to_flip = []
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == opponent:
                cells_to_flip.append((r, c))
                r += d[0]
                c += d[1]
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                for (r, c) in cells_to_flip:
                    board[r][c] = player
