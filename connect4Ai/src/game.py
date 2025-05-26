
# =====================================
# CONNECT 4 GAME WITH AI OPPONENT
# =====================================
# A console-based Connect 4 game implementation with two modes:
# - Two-player mode (human vs human)
# - Single-player mode (human vs AI using minimax algorithm)

import copy
from colorama import init, Fore, Style
init(autoreset=True)

# =====================================
# MAIN GAME ENTRY POINT
# =====================================

def main():
    """
    Main game loop that presents menu options to the user.
    Allows selection between two-player mode, single-player mode, or quit.
    """
    choose = 0
    while choose  < 1 or choose > 3:
        print("Press 1 For 2 Player\n")
        print("Press 2 For 1 Player\n")
        print("Press 3 For Quit\n")
        choose = int(input())            
        if choose == 1:
            twoPlayer()
        if choose == 2:
            onePlayer()
        if choose == 3:
            quit()

# =====================================
# TWO-PLAYER GAME MODE
# =====================================
    
def twoPlayer():
    """
    Initializes and runs a two-player game.
    Creates a 6x7 board and alternates turns between players until game ends.
    """
    global run
    global board 
    run = True
    board = []
    # Initialize 6x7 board with empty cells ('O')
    for i in range(6):
        board.append(['O'] * 7)
    while(run):
        getMove()
        if not checkIfThereIsMove():
            print("Board Full Game Over\n")
            quit()

# =====================================
# GAME STATE MANAGEMENT
# =====================================
    
def checkIfThereIsMove():
    """
    Checks if there are any empty cells remaining on the board.
    Returns True if moves are available, False if board is full.
    """
    for i in range(6):
        for j in range(7):  
            if board[i][j] == 'O':
                return True   
    return False              

def getMove():
    """
    Handles the turn sequence for two-player mode.
    Alternates between red and yellow players, checking for wins after each move.
    """
    redMove()
    checkWin()
    yellowMove()
    checkWin()
    print("\n ")

# =====================================
# PLAYER MOVE HANDLING
# =====================================
        
def redMove():
    """
    Handles the red player's move input and placement.
    Prompts for column selection and places piece in the lowest available row.
    """
    while(True):    
        print("It is red's turn\n")
        temp = int(input("Please enter a column number 1 , 2, 3, 4, 5, 6, 7\n"))
        column  = temp -1
        # Find the lowest available row in the selected column
        for i in range(6):
            if board[5-i][column] == 'O':
                board[5-i][column] = 'R'
                return
        print("Please enter legit column\n")

def yellowMove():
    """
    Handles the yellow player's move input and placement.
    Prompts for column selection and places piece in the lowest available row.
    """
    while(True):
        print("It is yellow's turn\n")
        temp = int(input("Please enter a column number 1 , 2, 3, 4, 5, 6, 7 \n"))
        column  = temp -1
        # Find the lowest available row in the selected column
        for i in range(6):
            if board[5-i][column] == 'O':
                board[5 - i][column] = 'Y'
                return
        print("Please enter legit column\n")

# =====================================
# BOARD DISPLAY
# =====================================          
    
def boardLook():
    """
    Displays the current board state with colored output.
    Red pieces appear in red, yellow pieces in yellow, empty cells as 'O'.
    """
    for row in board:
        row_str = ""
        for cell in row:
            if cell == 'R':
                row_str += Fore.RED + 'R ' + Style.RESET_ALL
            elif cell == 'Y':
                row_str += Fore.YELLOW + 'Y ' + Style.RESET_ALL
            else:
                row_str += 'O '
        print(row_str)
    print("\n")

# =====================================
# WIN CONDITION CHECKING
# =====================================

def checkWin():
    """
    Main win checking function that calls all win condition checkers.
    Checks vertical, horizontal, and diagonal wins for both players.
    """
    verticalWinforRed()
    verticalWinforYellow()
    horizontalWinforRed()   
    horizontalWinforYellow()
    crossWinforRed()
    crossWinforYellow()

def verticalWinforRed():
    """
    Checks for vertical win condition (4 in a column) for red player.
    Displays board and declares victory if found.
    """
    for col in range(7):
        counter = 0
        for row in range(6):
            if board[row][col] == 'R':
                counter += 1
                if counter == 4:
                    boardLook()
                    print("Red Won")
                    quit()
            else:
                counter = 0
      
def verticalWinforYellow():
    """
    Checks for vertical win condition (4 in a column) for yellow player.
    Displays board and declares victory if found.
    """
    for col in range(7):
        counter = 0
        for row in range(6):
            if board[row][col] == 'Y':
                counter += 1
                if counter == 4:
                    boardLook()
                    print("Yellow Won")
                    quit()
            else:
                counter = 0
             
def horizontalWinforRed():
    """
    Checks for horizontal win condition (4 in a row) for red player.
    Displays board and declares victory if found.
    """
    for row in range(6):
        counter = 0
        for col in range(7):
            if board[row][col] == 'R':
                counter += 1
                if counter == 4:
                    boardLook()
                    print("Red Won")
                    quit()
            else:
                counter = 0
          
def horizontalWinforYellow():
    """
    Checks for horizontal win condition (4 in a row) for yellow player.
    Displays board and declares victory if found.
    """
    for row in range(6):
        counter = 0
        for col in range(7):
            if board[row][col] == 'Y':
                counter += 1
                if counter == 4:
                    boardLook()
                    print("Yellow Won")
                    quit()
            else:
                counter = 0
                      
def crossWinforRed():
    """
    Checks for diagonal win conditions for red player.
    Checks both positive and negative diagonal directions.
    """
    # Check positive diagonal (bottom-left to top-right)
    for i in range(3):
        for j in range(4):
            if board[i][j] == 'R' and board[i+1][j+1] == 'R' and board[i+2][j+2] == 'R' and board[i+3][j+3] == 'R':
                boardLook()
                print("Red Won")
                quit()

    # Check negative diagonal (top-left to bottom-right)
    for i in range(3):
        for j in range(3, 7):
            if board[i][j] == 'R' and board[i+1][j-1] == 'R' and board[i+2][j-2] == 'R' and board[i+3][j-3] == 'R':
                boardLook()
                print("Red Won")
                quit()

def crossWinforYellow():
    """
    Checks for diagonal win conditions for yellow player.
    Checks both positive and negative diagonal directions.
    """
    # Check positive diagonal (bottom-left to top-right)
    for i in range(3):
        for j in range(4):
            if board[i][j] == 'Y' and board[i+1][j+1] == 'Y' and board[i+2][j+2] == 'Y' and board[i+3][j+3] == 'Y':
                boardLook()
                print("Yellow Won")
                quit()

    # Check negative diagonal (top-left to bottom-right)
    for i in range(3):
        for j in range(3, 7):
            if board[i][j] == 'Y' and board[i+1][j-1] == 'Y' and board[i+2][j-2] == 'Y' and board[i+3][j-3] == 'Y':
                boardLook()
                print("Yellow Won")
                quit()

# =====================================
# SINGLE-PLAYER MODE (HUMAN VS AI)
# =====================================

def onePlayer():
    """
    Initializes and runs a single-player game against AI.
    Human plays as red, AI plays as yellow using minimax algorithm.
    """
    global run
    global board
    run = True
    board = []
    # Initialize 6x7 board with empty cells ('O')
    for i in range(6):
        board.append(['O'] * 7)
    while(run):
        boardLook()
        redMove()
        checkWin()
        if not checkIfThereIsMove():
            print("Board Full Game Over\n")
            quit()
        aiMove()
        checkWin()
        if not checkIfThereIsMove():
            print("Board Full Game Over\n")
            quit()

def aiMove():
    """
    Executes AI move using minimax algorithm.
    Determines best column and places yellow piece in lowest available row.
    """
    column, _ = minimax(board, 4, True)
    for i in range(6):
        if board[5 - i][column] == 'O':
            board[5 - i][column] = 'Y'
            print("AI moved at column", column+1)
            return

# =====================================
# AI UTILITY FUNCTIONS
# =====================================

def get_valid_columns():
    """
    Returns a list of columns that have at least one empty cell.
    Used by AI to determine available moves.
    """
    valid_cols = []
    for col in range(7):
        if board[0][col] == 'O':
            valid_cols.append(col)
    return valid_cols

def make_move(board_copy, col, player):
    """
    Makes a move on a copy of the board for AI simulation.
    Places the player's piece in the lowest available row of the specified column.
    """
    for row in range(5, -1, -1):
        if board_copy[row][col] == 'O':
            board_copy[row][col] = player
            break

def check_winner(board_check, player):
    """
    Checks if the specified player has won on the given board state.
    Returns True if player has 4 in a row (horizontal, vertical, or diagonal).
    """
    # Check horizontal wins
    for r in range(6):
        for c in range(4):
            if all(board_check[r][c+i] == player for i in range(4)):
                return True
    # Check vertical wins
    for r in range(3):
        for c in range(7):
            if all(board_check[r+i][c] == player for i in range(4)):
                return True
    # Check positive diagonal wins
    for r in range(3):
        for c in range(4):
            if all(board_check[r+i][c+i] == player for i in range(4)):
                return True
    # Check negative diagonal wins
    for r in range(3):
        for c in range(3, 7):
            if all(board_check[r+i][c-i] == player for i in range(4)):
                return True
    return False

def score_position(board_eval, player):
    """
    Evaluates the board position for the given player.
    Returns positive score for wins, negative for losses, neutral for draws.
    """
    opponent = 'R' if player == 'Y' else 'Y'
    if check_winner(board_eval, player):
        return 100
    elif check_winner(board_eval, opponent):
        return -100
    else:
        return 0

# =====================================
# MINIMAX ALGORITHM
# =====================================

def minimax(board_state, depth, is_maximizing):
    """
    Minimax algorithm implementation for AI decision making.
    Recursively evaluates possible moves to find the optimal play.
    
    Args:
        board_state: Current board configuration
        depth: Search depth remaining
        is_maximizing: True if maximizing player (AI), False if minimizing player (human)
    
    Returns:
        Tuple of (best_column, best_score)
    """
    valid_columns = get_valid_columns()
    is_terminal = check_winner(board_state, 'Y') or check_winner(board_state, 'R') or len(valid_columns) == 0

    # Base case: reached max depth or terminal state
    if depth == 0 or is_terminal:
        return (None, score_position(board_state, 'Y'))

    if is_maximizing:
        # AI turn - maximize score
        value = -float('inf')
        best_col = valid_columns[0]
        for col in valid_columns:
            temp_board = copy.deepcopy(board_state)
            make_move(temp_board, col, 'Y')
            new_score = minimax(temp_board, depth-1, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
        return best_col, value
    else:
        # Human turn - minimize score
        value = float('inf')
        best_col = valid_columns[0]
        for col in valid_columns:
            temp_board = copy.deepcopy(board_state)
            make_move(temp_board, col, 'R')
            new_score = minimax(temp_board, depth-1, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
        return best_col, value

# =====================================
# GAME EXECUTION
# =====================================

# Start the game
main()