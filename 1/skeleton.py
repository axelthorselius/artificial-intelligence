import gym
import random
import requests
import numpy as np
import argparse
import sys
from gym_connect_four import ConnectFourEnv
import copy

env: ConnectFourEnv = gym.make("ConnectFour-v0")

ROW_LEN = 7
COL_LEN = 6
CONNECT_LEN = 4

SEARCH_DEPTH = 5

#SERVER_ADRESS = "http://localhost:8000/"
SERVER_ADRESS = "https://vilde.cs.lth.se/edap01-4inarow/"
API_KEY = 'nyckel'
STIL_ID = ["ax744th-s"] # TODO: fill this list with your stil-id's

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

"""
You can make your code work against this simple random agent
before playing against the server.
It returns a move 0-6 or -1 if it could not make a move.
To check your code for better performance, change this code to
use your own algorithm for selecting actions too
"""
def opponents_move(env):
   env.change_player() # change to oppoent
   avmoves = env.available_moves()
   if not avmoves:
      env.change_player() # change back to student before returning
      return -1

   # TODO: Optional? change this to select actions with your policy too
   # that way you get way more interesting games, and you can see if starting
   # is enough to guarrantee a win
   action = random.choice(list(avmoves))
   # action = get_move(True)
   state, reward, done, _ = env.step(action)
   if done:
      if reward == 1: # reward is always in current players view
         reward = -1
   env.change_player() # change back to student before returning
   return state, reward, done

def score_line(line: list):
   player_pieces = line.count(1)
   opponent_pieces = line.count(-1)
   free_slots = line.count(0)

   if player_pieces == 4:
      return sys.maxsize
   if player_pieces == 3 and free_slots == 1:
      return 100
   if player_pieces == 2 and free_slots == 2:
      return 20
   if player_pieces == 1 and free_slots == 3:
      return 5
   if free_slots == 0:
      return 1
   if opponent_pieces == 1 and free_slots == 3:
      return -4
   if opponent_pieces == 2 and free_slots == 2:
      return -19
   if opponent_pieces == 3 and free_slots == 1:
      return -99
   if opponent_pieces == 4:
      return -(sys.maxsize - 1)
   # if a 4-segment has a combination of 1 and -1
   return 0

def score(env):
   score = 0

   # Horizontal lines
   for row in range(COL_LEN):
      row_list = env[row]
      for col in range(ROW_LEN - 3):
         score += score_line(list(row_list[col:col + CONNECT_LEN]))
   
   # Vertical lines
   for col in range(ROW_LEN):
      col_list = env[:, col]
      for row in range(COL_LEN - 3):
         score += score_line(list(col_list[row: row + CONNECT_LEN]))
   
   # Diagonal left-right down-up
   for row in range(COL_LEN - 3):
      for col in range(ROW_LEN - 3):
         score += score_line(list(env[row + i][col + i] for i in range(CONNECT_LEN)))

   # Diagonal left-right up-down
   for row in range(COL_LEN - 3):
      for col in range(ROW_LEN - 3):
         score += score_line(list(env[row - i + 3][col + i] for i in range(CONNECT_LEN)))

   return score

def minimax(env: ConnectFourEnv,
    depth: int, alpha: int, beta: int, maximizing_player: bool) -> int:
   
   available_moves = list(env.available_moves())
   if depth == 0 or env.is_win_state() or len(available_moves) == 0:
      return score(env.board)
   if maximizing_player:
      value = -sys.maxsize
      for move in available_moves:
         child = copy.deepcopy(env)
         child.change_player()
         child.step(move)
         value = max(value, minimax(
            child, depth - 1, alpha, beta, False))
         if value >= beta:
            break
         alpha = max(alpha, value)
      return value
   else:
      value = sys.maxsize
      for move in available_moves:
         child = copy.deepcopy(env)
         child.change_player()
         child.step(move)
         value = min(value, minimax(
            child, depth - 1, alpha, beta, True))
         if value <= alpha:
            break
         beta = min(beta, value)
      return value

def student_move():
   available_moves = env.available_moves()
   best_score = -sys.maxsize
   for move in available_moves:
      env_copy = copy.deepcopy(env)
      env_copy.step(move)
      # Search depth -1 due to one layer search in this function
      score = minimax(env_copy, SEARCH_DEPTH - 1,
                         -sys.maxsize, sys.maxsize, False)
      if score > best_score:
         best_score = score
         best_move = move
   return best_move

def play_game(vs_server = False):
   """
   The reward for a game is as follows. You get a
   botaction = random.choice(list(avmoves)) reward from the
   server after each move, but it is 0 while the game is running
   loss = -1
   win = +1
   draw = +0.5
   error = -10 (you get this if you try to play in a full column)
   Currently the player always makes the first move
   """

   # default state
   state = np.zeros((6, 7), dtype=int)

   # setup new game
   if vs_server:
      # Start a new game
      res = call_server(-1) # -1 signals the system to start a new game. any running game is counted as a loss

      # This should tell you if you or the bot starts
      print(res.json()['msg'])
      botmove = res.json()['botmove']
      state = np.array(res.json()['state'])
      env.reset(board=state)
   else:
      # reset game to starting state
      env.reset(board=None)
      # determine first player
      student_gets_move = random.choice([True, False])
      if student_gets_move:
         print('You start!')
         print()
      else:
         print('Bot starts!')
         print()

   # Print current gamestate
   print("Current state (1 are student discs, -1 are servers, 0 is empty): ")
   print(state)
   print()

   done = False
   while not done:
      # Select your move
      stmove = student_move() # TODO: change input here

      # make both student and bot/server moves
      if vs_server:
         # Send your move to server and get response
         res = call_server(stmove)
         print(res.json()['msg'])

         # Extract response values
         result = res.json()['result']
         botmove = res.json()['botmove']
         state = np.array(res.json()['state'])
         env.reset(board=state)
      else:
         if student_gets_move:
            # Execute your move
            avmoves = env.available_moves()
            if stmove not in avmoves:
               print("You tied to make an illegal move! You have lost the game.")
               break
            state, result, done, _ = env.step(stmove)

         student_gets_move = True # student only skips move first turn if bot starts

         # print or render state here if you like
         # env.render()

         # select and make a move for the opponent, returned reward from students view
         if not done:
            state, result, done = opponents_move(env)

      # Check if the game is over
      if result != 0:
         done = True
         if not vs_server:
            print("Game over. ", end="")
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
         if not vs_server:
            print("Final state (1 are student discs, -1 are servers, 0 is empty): ")
      else:
         print("Current state (1 are student discs, -1 are servers, 0 is empty): ")

      # Print current gamestate
      print(state)
      print()

def main():
   # Parse command line arguments
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
      play_game(vs_server = False)
   elif args.online:
      play_game(vs_server = True)

   if args.stats:
      stats = check_stats()
      print(stats)

if __name__ == "__main__":
    main()
