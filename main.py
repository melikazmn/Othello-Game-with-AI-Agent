import time
import pygame
import aiAgent
import othello

# Constants
BOARD_SIZE = 8
SQUARE_SIZE = 50
WIDTH = BOARD_SIZE * SQUARE_SIZE
HEIGHT = BOARD_SIZE * SQUARE_SIZE + 150
FPS = 60

# Colors
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HIGHLIGHT = (200, 200, 0)
RED = (255, 0, 0)
BUTTON_COLOR = (50, 50, 50)
HOVER_COLOR = (100, 100, 100)
FONT_COLOR = (255, 255, 255)

# Players
EMPTY = 0
BLACK_PIECE = 1
WHITE_PIECE = 2

def show_winner(screen, game):
    font = pygame.font.SysFont(None, 48)
    winner_text = f"{'Black' if game.black_score > game.white_score else 'White'} wins!"
    winner_text_surface = font.render(winner_text, True, RED)
    screen.blit(winner_text_surface, (WIDTH // 2 - winner_text_surface.get_width() // 2,
                                      HEIGHT // 2 - winner_text_surface.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display winner for 3 seconds

def show_rules(screen, mouse_pos):
    font = pygame.font.SysFont(None, 24)
    rules = [
        "Othello Rules:",
        "1.The game is played on an 8x8 board.",
        "2.Black always goes first.",
        "3.Players take turns placing pieces on the board.",
        "4.A move is valid only if it captures at "
        ,"least one opponent's piece.",
        "5.The game ends when neither player can make"
        ," a valid move.",
        "6.The player with the most pieces on the "
        ,"board wins."
    ]
    screen.fill(GREEN)
    y_offset = 50
    for rule in rules:
        rule_surface = font.render(rule, True, WHITE)
        screen.blit(rule_surface, (WIDTH // 2 - rule_surface.get_width() // 2, y_offset))
        y_offset += 40

    # Draw back button
    back_button = draw_button(screen, "Back", WIDTH // 2 - 100, HEIGHT - 100, 200, 50, font, BUTTON_COLOR, HOVER_COLOR, mouse_pos)
    pygame.display.flip()
    return back_button

def draw_button(screen, text, x, y, width, height, font, color, hover_color, mouse_pos):
    button_rect = pygame.Rect(x, y, width, height)
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect, border_radius=15)
    else:
        pygame.draw.rect(screen, color, button_rect, border_radius=15)
    text_surface = font.render(text, True, FONT_COLOR)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
    return button_rect

def draw_menu(screen, mouse_pos):
    font = pygame.font.SysFont(None, 72)
    button_font = pygame.font.SysFont(None, 28)
    screen.fill(GREEN)

    title_text = font.render("Othello", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    start_button = draw_button(screen, "Start Game", WIDTH // 2 - 100, 200, 200, 50, button_font, BUTTON_COLOR, HOVER_COLOR, mouse_pos)
    rules_button = draw_button(screen, "Rules", WIDTH // 2 - 100, 300, 200, 50, button_font, BUTTON_COLOR, HOVER_COLOR, mouse_pos)
    exit_button = draw_button(screen, "Exit", WIDTH // 2 - 100, 400, 200, 50, button_font, BUTTON_COLOR, HOVER_COLOR, mouse_pos)

    pygame.display.flip()

    return start_button, rules_button, exit_button

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Othello")
    clock = pygame.time.Clock()
    game = othello.Othello()
    ai_agent = aiAgent.AIAgent(WHITE_PIECE)

    running = True
    in_menu = True
    in_rules = False

    while running:
        mouse_pos = pygame.mouse.get_pos()

        if in_menu:
            start_button, rules_button, exit_button = draw_menu(screen, mouse_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        in_menu = False  # Start game
                    elif rules_button.collidepoint(event.pos):
                        in_menu = False
                        in_rules = True  # Show rules
                    elif exit_button.collidepoint(event.pos):
                        running = False  # Exit

        elif in_rules:
            back_button = show_rules(screen, mouse_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        in_rules = False
                        in_menu = True  # Go back to menu

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if game.current_player == BLACK_PIECE:
                    game.update_valid_moves()

                if event.type == pygame.MOUSEBUTTONDOWN and game.current_player == BLACK_PIECE:
                    x, y = event.pos
                    col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                    if game.is_valid_move(row, col, game.current_player):
                        game.apply_move(row, col, game.current_player)
                        game.switch_turn()

                        if not game.get_valid_moves(game.current_player):
                            game.switch_turn()
                            if not game.get_valid_moves(game.current_player):
                                if game.is_game_over():
                                    show_winner(screen, game)
                                    in_menu = True  # Go back to menu
                                    game.__init__()  # Reset the game
                                    game.current_player = BLACK_PIECE  # Reset to black's turn
                                    break  # Exit the inner loop

                game.draw_board(screen)
                pygame.display.flip()
                clock.tick(FPS)

                if game.current_player == WHITE_PIECE and not game.is_game_over():
                    time.sleep(2)
                    move = ai_agent.get_best_move(game.board)
                    if move:
                        game.apply_move(move[0], move[1], WHITE_PIECE)
                        game.switch_turn()
                        if not game.get_valid_moves(game.current_player):
                            game.switch_turn()
                            if not game.get_valid_moves(game.current_player):
                                if game.is_game_over():
                                    show_winner(screen, game)
                                    in_menu = True  # Go back to menu
                                    game.__init__()  # Reset the game
                                    game.current_player = BLACK_PIECE  # Reset to black's turn
                                    break  # Exit the inner loop

    pygame.quit()

if __name__ == "__main__":
    main()
