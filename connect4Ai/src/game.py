import copy
from colorama import init, Fore, Style
init(autoreset=True)

def main():
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
    
def twoPlayer():
    global run
    global board 
    run = True
    board = []
    for i in range(6):
        board.append(['O'] * 7)
    while(run):
        getMove()
        if not checkIfThereIsMove():
            print("Board Full Game Over\n")
            quit()
    
def checkIfThereIsMove():
    for i in range(6):
        for j in range(7):  
            if board[i][j] == 'O':
                return True   
    return False              

def getMove():
    redMove()
    checkWin()
    yellowMove()
    checkWin()
    print("\n ")
        
def redMove():
    while(True):    
        print("It is red's turn\n")
        temp = int(input("Please enter a column number 1 , 2, 3, 4, 5, 6, 7\n"))
        column  = temp -1
        for i in range(6):
            if board[5-i][column] == 'O':
                board[5-i][column] = 'R'
                return
        print("Please enter legit column\n")

def yellowMove():
    while(True):
        print("It is yellow's turn\n")
        temp = int(input("Please enter a column number 1 , 2, 3, 4, 5, 6, 7 \n"))
        column  = temp -1
        for i in range(6):
            if board[5-i][column] == 'O':
                board[5 - i][column] = 'Y'
                return
        print("Please enter legit column\n")          
    
def boardLook():
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

def checkWin():
        verticalWinforRed()
        verticalWinforYellow()
        horizontalWinforRed()   
        horizontalWinforYellow()
        crossWinforRed()
        crossWinforYellow()

def verticalWinforRed():
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
    for i in range(3):
        for j in range(4):
            if board[i][j] == 'R' and board[i+1][j+1] == 'R' and board[i+2][j+2] == 'R' and board[i+3][j+3] == 'R':
                boardLook()
                print("Red Won")
                quit()

    for i in range(3):
        for j in range(3, 7):
            if board[i][j] == 'R' and board[i+1][j-1] == 'R' and board[i+2][j-2] == 'R' and board[i+3][j-3] == 'R':
                boardLook()
                print("Red Won")
                quit()

def crossWinforYellow():
    for i in range(3):
        for j in range(4):
            if board[i][j] == 'Y' and board[i+1][j+1] == 'Y' and board[i+2][j+2] == 'Y' and board[i+3][j+3] == 'Y':
                boardLook()
                print("Yellow Won")
                quit()

    for i in range(3):
        for j in range(3, 7):
            if board[i][j] == 'Y' and board[i+1][j-1] == 'Y' and board[i+2][j-2] == 'Y' and board[i+3][j-3] == 'Y':
                boardLook()
                print("Yellow Won")
                quit()

def onePlayer():
    global run
    global board
    run = True
    board = []
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
    column, _ = minimax(board, 4, True)
    for i in range(6):
        if board[5 - i][column] == 'O':
            board[5 - i][column] = 'Y'
            print("AI moved at column", column+1)
            return

def get_valid_columns():
    valid_cols = []
    for col in range(7):
        if board[0][col] == 'O':
            valid_cols.append(col)
    return valid_cols

def make_move(board_copy, col, player):
    for row in range(5, -1, -1):
        if board_copy[row][col] == 'O':
            board_copy[row][col] = player
            break

def check_winner(board_check, player):
    for r in range(6):
        for c in range(4):
            if all(board_check[r][c+i] == player for i in range(4)):
                return True
    for r in range(3):
        for c in range(7):
            if all(board_check[r+i][c] == player for i in range(4)):
                return True
    for r in range(3):
        for c in range(4):
            if all(board_check[r+i][c+i] == player for i in range(4)):
                return True
    for r in range(3):
        for c in range(3, 7):
            if all(board_check[r+i][c-i] == player for i in range(4)):
                return True
    return False

def score_position(board_eval, player):
    opponent = 'R' if player == 'Y' else 'Y'
    if check_winner(board_eval, player):
        return 100
    elif check_winner(board_eval, opponent):
        return -100
    else:
        return 0

def minimax(board_state, depth, is_maximizing):
    valid_columns = get_valid_columns()
    is_terminal = check_winner(board_state, 'Y') or check_winner(board_state, 'R') or len(valid_columns) == 0

    if depth == 0 or is_terminal:
        return (None, score_position(board_state, 'Y'))

    if is_maximizing:
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

main()