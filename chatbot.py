# gridlock.py
import numpy as np

# Constants
EMPTY = "."
BLOCK = "X"
PLAYER = "P"
AI = "A"

GRID_SIZE = 5

# Initialize board
board = np.full((GRID_SIZE, GRID_SIZE), EMPTY)
player_pos = [0, 0]
ai_pos = [GRID_SIZE - 1, GRID_SIZE - 1]
board[player_pos[0]][player_pos[1]] = PLAYER
board[ai_pos[0]][ai_pos[1]] = AI

# Directions: up, down, left, right
directions = [(-1,0),(1,0),(0,-1),(0,1)]

# Print the board
def print_board():
    for row in board:
        print(" ".join(row))
    print()

# Get all valid moves for a position
def get_moves(pos):
    moves = []
    for dr, dc in directions:
        r, c = pos[0]+dr, pos[1]+dc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            if board[r][c] == EMPTY:
                moves.append([r,c])
    return moves

# Evaluate board for AI (mobility difference)
def evaluate():
    player_moves = len(get_moves(player_pos))
    ai_moves = len(get_moves(ai_pos))
    return ai_moves - player_moves

# Minimax with depth 2 (simplified)
def minimax(pos_ai, pos_player, depth, maximizing):
    if depth == 0:
        return evaluate(), None
    
    moves = get_moves(pos_ai if maximizing else pos_player)
    if not moves:
        return (-9999 if maximizing else 9999), None
    
    best_move = None
    if maximizing:
        max_eval = -9999
        for move in moves:
            orig = board[move[0]][move[1]]
            board[pos_ai[0]][pos_ai[1]] = EMPTY
            board[move[0]][move[1]] = AI
            new_pos = move
            val, _ = minimax(new_pos, pos_player, depth-1, False)
            board[move[0]][move[1]] = orig
            board[pos_ai[0]][pos_ai[1]] = AI
            if val > max_eval:
                max_eval = val
                best_move = move
        return max_eval, best_move
    else:
        min_eval = 9999
        for move in moves:
            orig = board[move[0]][move[1]]
            board[pos_player[0]][pos_player[1]] = EMPTY
            board[move[0]][move[1]] = PLAYER
            new_pos = move
            val, _ = minimax(pos_ai, new_pos, depth-1, True)
            board[move[0]][move[1]] = orig
            board[pos_player[0]][pos_player[1]] = PLAYER
            if val < min_eval:
                min_eval = val
                best_move = move
        return min_eval, best_move

# Check if someone is trapped
def is_trapped(pos):
    return len(get_moves(pos)) == 0

# Main game loop
print("=== Grid Lock Game ===")
print("You = P | AI = A | Block = X")
print_board()

while True:
    # Player Turn
    moves = get_moves(player_pos)
    if not moves:
        print("No moves left! AI Wins!")
        break
    
    print("Your possible moves:", moves)
    while True:
        try:
            move_input = input("Enter your move as row,col (e.g., 0,1): ")
            r, c = map(int, move_input.strip().split(","))
            if [r,c] in moves:
                board[player_pos[0]][player_pos[1]] = EMPTY
                player_pos = [r,c]
                board[r][c] = PLAYER
                break
            else:
                print("Invalid move! Try again.")
        except:
            print("Invalid input! Try again.")

    print_board()

    # Place block
    while True:
        try:
            block_input = input("Place a block as row,col (any empty cell): ")
            r, c = map(int, block_input.strip().split(","))
            if board[r][c] == EMPTY:
                board[r][c] = BLOCK
                break
            else:
                print("Cell not empty! Try again.")
        except:
            print("Invalid input! Try again.")

    print_board()

    # Check if AI trapped
    if is_trapped(ai_pos):
        print("AI is trapped! You Win!")
        break

    # AI Turn
    print("AI is thinking...")
    _, move = minimax(ai_pos, player_pos, depth=2, maximizing=True)
    if move:
        board[ai_pos[0]][ai_pos[1]] = EMPTY
        ai_pos = move
        board[ai_pos[0]][ai_pos[1]] = AI

    # AI places block (random best nearby)
    # Strategy: block a neighboring empty cell around player
    placed = False
    for dr, dc in directions:
        r, c = player_pos[0]+dr, player_pos[1]+dc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c] == EMPTY:
            board[r][c] = BLOCK
            placed = True
            break
    if not placed:
        # else place first empty found
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i][j] == EMPTY:
                    board[i][j] = BLOCK
                    placed = True
                    break
            if placed:
                break

    print_board()

    # Check if player trapped
    if is_trapped(player_pos):
        print("You are trapped! AI Wins!")
        break