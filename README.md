# Othello-Game-with-AI-Agent
This project implements the classic Othello game using Python and Pygame, with an AI agent that uses the Minimax algorithm with alpha-beta pruning. The game supports both human vs. human and human vs. AI modes, with a sleek graphical user interface.

## Features

- Graphical Interface: The game features an 8x8 Othello board with smooth graphics using Pygame. Stylish rounded buttons and an intuitive design enhance the user experience.
- AI Agent: The AI agent plays as the white pieces and is powered by the Minimax algorithm with alpha-beta pruning, allowing it to play efficiently with a look-ahead of 3 moves.
- Game Modes: Play against another human or challenge the AI agent.
- Game Rules: Classic Othello rules are implemented, including piece flipping, valid move checking, and scoring.

## How to Play
- Start the Game: Launch the game by running the main.py file. A menu screen will appear where you can start a new game, view the rules, or exit the application.
- Place Pieces: The game alternates turns between the black player (who always goes first) and the white player. Players can only place pieces where they can capture at least one of their opponent's pieces.
- Winning: The player with the most pieces on the board at the end of the game wins. If no more valid moves are available, the game ends automatically, and the winner is announced.

## AI Agent (Minimax with Alpha-Beta Pruning)

The AI agent evaluates the game board and selects the best possible move using the Minimax algorithm with alpha-beta pruning, allowing for efficient and competitive play.

**How it works**:
1. Depth-Limited Search:  The AI explores potential moves up to a predefined depth (usually 3 moves ahead).
2. Pruning:  Alpha-beta pruning reduces the number of nodes the algorithm needs to evaluate, making it faster without affecting the decision quality.
3. Board Evaluation:  At the end of each branch, the AI evaluates the board to determine how favorable it is. It prioritizes capturing corners and preventing the opponent from gaining an advantage
