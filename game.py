# for representing the board as a matrix and doing operations on it
import numpy as np
import pygame
import requests
import sys
import argparse
import math
from threading import Timer
import random

SQUARESIZE = 120

# row and column count
ROWS, COLS = 6, 7

SERVER_TURN = 0
AI_TURN = 1

# pieces represented as numbers
SERVER_PIECE = 1
AI_PIECE = 2

# colors for GUI
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SERVER_ADRESS = "https://vilde.cs.lth.se/edap01-4inarow/"
API_KEY = 'nyckel'
STIL_ID = ["vi3851gu-s"] # TODO: fill this list with your stil-id's

def call_server(move):
   res = requests.post(SERVER_ADRESS + "move",
                       data={
                           "stil_id": STIL_ID,
                           "move": move, # -1 signals the system to start a new game. any running game is counted as a loss
                           "api_key": API_KEY,
                       })
   # For safety some respose checking is done here
   if res.status_code != 200:
      print("Server gave a bad response, error code={}".format(res.status_code))
      exit()
   if not res.json()['status']:
      print("Server returned a bad status. Return message: ")
      print(res.json()['msg'])
      exit()
   return res

def check_stats():
   res = requests.post(SERVER_ADRESS + "stats",
                       data={
                           "stil_id": STIL_ID,
                           "api_key": API_KEY,
                       })

   stats = res.json()
   return stats

def next_free_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r

def place_piece(board, row, col, piece):
    board[row][col] = piece

def valid_location(board, col):
    return board[0][col] == 0

def check_win(board, piece):
    # check horizontal 'windows' of 4 for win
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    
    # check vertical 'windows' of 4 for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    
    # check positively sloped diagonals for win
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    
    # check negatively sloped diagonals for win
    for r in range(3, ROWS):
        for c in range(3, COLS):
            if all(board[r-i][c-i] == piece for i in range(4)):
                return True
    
    return False

def render_board(screen, board, circle_radius):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE ))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            else :
                pygame.draw.circle(screen, GREEN, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)

    pygame.display.update()


def evaluate(window, piece):
    opponent_piece = SERVER_PIECE if piece == AI_PIECE else AI_PIECE

    # initial score of a window is 0
    score = 0

    if window.count(piece) == 4:
        score += 150
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 14
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 3
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 15

    return score    

def calculate_score(board, piece):
    score = 0

    # prioritise center column
    center_col = [int(i) for i in list(board[:,COLS//2])]
    center_count = center_col.count(piece)
    score += center_count * 12

    # Evaluate positively sloped diagonal windows
    for r in range(3,ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate(window, piece)

    # Evaluate negatively sloped diagonal windows
    for r in range(3,ROWS):
        for c in range(3,COLS):
            window = [board[r-i][c-i] for i in range(4)]
            score += evaluate(window, piece)

    # Evaluate horizontal windows
    for r in range(ROWS):
        row = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row[c:c + 4]
            score += evaluate(window, piece)

    # Evaluate vertical windows
    for c in range(COLS):
        col = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col[r:r+4]
            score += evaluate(window, piece)

    return score

def terminal_node(board):
    return check_win(board, SERVER_PIECE) or check_win(board, AI_PIECE) or len(valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locs = valid_locations(board)
    is_term = terminal_node(board)
    if depth == 0 or is_term:
        if is_term:
            if check_win(board, AI_PIECE):
                return (None, 10000000)
            elif check_win(board, SERVER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        else:
            return (None, calculate_score(board, AI_PIECE))
    if maximizing_player:
        value = -math.inf
        col = random.choice(valid_locs)
        for c in valid_locs:
            row = next_free_row(board, c)
            b_copy = board.copy()
            place_piece(b_copy, row, c, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                col = c
            alpha = max(value, alpha) 
            if alpha >= beta:
                break
        return col, value
    else:
        value = math.inf
        col = random.choice(valid_locs)
        for c in valid_locs:
            row = next_free_row(board, c)
            b_copy = board.copy()
            place_piece(b_copy, row, c, SERVER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                col = c
            beta = min(value, beta) 
            if alpha >= beta:
                break
        return col, value


def valid_locations(board):
    valid_locations = []
    for column in range(COLS):
        if valid_location(board, column):
            valid_locations.append(column)

    return valid_locations


def render_win_message(screen, who, font):
    print(f"PLAYER {who} WINS!")
    label = font.render(f"PLAYER {who} WINS!", 1, GREEN)
    screen.blit(label, (80, 10))

def check_results_server(result):
    over=True
    if result != 0:
        over = False
        if result == 1:
            print("You won!")
        elif result == 0.5:
            print("It's a draw!")
        elif result == -1:
            print("You lost!")
        elif result == -10:
            print("You made an illegal move and have lost!")
        else:
            print("Unexpected result result={}".format(result))
    else:
        print("Current state (1 are student discs, -1 are servers, 0 is empty): ")
    return over

def end_game():
    global game_over
    game_over = True
    print(game_over)

def start_game(vs_server):
    global game_over

    #Start new game on server
    if vs_server:
        res = call_server(-1) # -1 signals the system to start a new game. any running game is counted as a loss
        print(res.json()['msg'])
        botmove = res.json()['botmove']
        state = np.array(res.json()['state'])
        board = state
    else:
        board = np.zeros((ROWS, COLS), dtype=int)

    game_over = False
    not_over = True

    turn = random.randint(SERVER_TURN, AI_TURN)

    pygame.init()

    width = COLS * SQUARESIZE
    height = (ROWS + 1) * SQUARESIZE
    circle_radius = int(SQUARESIZE/2 - 5)
    size = (width, height)
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont("monospace", 75)

    render_board(screen, board, circle_radius)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if not_over:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

            if turn == AI_TURN:

                col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

                if valid_location(board, col):
                    place_piece(board, next_free_row(board, col), col, AI_PIECE)
                    if vs_server:
                        res = call_server(col)
                        print(res.json()['msg'])
                        result = res.json()['result']
                        botmove = res.json()['botmove']
                        not_over = check_results_server(result)
                    else:

                        botmove, minimax_score = minimax(board, 3, -math.inf, math.inf, True)
                    if check_win(board, AI_PIECE):
                        render_win_message(screen, "AI", font)
                        not_over = False
                        t = Timer(5.0, end_game)
                        t.start()
                    
                    turn += 1
                    turn = turn % 2
                
                    render_board(screen, board, circle_radius)

            pygame.display.update()

        if turn == SERVER_TURN and not game_over and not_over:
            
            if valid_location(board, botmove):
                place_piece(board, next_free_row(board, botmove), botmove, SERVER_PIECE)
                if check_win(board, SERVER_PIECE):
                    render_win_message(screen, "SERVER", font)
                    not_over = False
                    t = Timer(5.0, end_game)
                    t.start()
                turn += 1
                turn = turn % 2

                render_board(screen, board, circle_radius)    


# main function
def main():

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--local", help = "Play locally", action="store_true")
    group.add_argument("-o", "--online", help = "Play online vs server", action="store_true")
    parser.add_argument("-s", "--stats", help = "Show your current online stats", action="store_true")
    args = parser.parse_args()

    # Print usage info if no arguments are given
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.local:
        start_game(vs_server = False)
    elif args.online:
        start_game(vs_server = True)

    if args.stats:
        stats = check_stats()
        print(stats)

if __name__ == "__main__":
    main()