'''
    Author: Cristian Mosqueda
    Purpose: Practice Python and Pygame by building Connect4.

'''

import numpy as np
import pygame
import sys
import math

BABY_BLUE = (10, 100, 230)
BLACK = (0, 0, 0)
RED = (240, 10, 10)
YELLOW = (250, 250, 11)

# number of columns and rows
NUM_OF_ROW = 6
NUM_OF_COL = 7

# building a board made up of 6 rows and 7 columns
def build_board():
    board = np.zeros((NUM_OF_ROW, NUM_OF_COL))
    return board
# placing the piece in the chosen row/column
def drop_piece(board, row, choice, piece):
        board[row][choice] = piece
# check if choice is valid
def is_valid_loc(board, choice):
    return board[NUM_OF_ROW-1][choice] == 0
def get_next_open_row(board, choice):
    for i in range(NUM_OF_ROW):
        # checking to see which row in the column is available for insertion
        if board[i][choice] == 0:
            # returning the available index
            return i
def display_board(board):
    # flipping the board to display it correctly from 5-0 rows and 0-6 columns
    print(np.flip(board, 0))
def detect_win(board, piece):
    # check all horizontal locations incase there is a win
    for c in range(NUM_OF_COL - 3):
        for r in range(NUM_OF_ROW):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                # found the connecting 4 pieces
                return True;

    # check for vertical locations
    for c in range(NUM_OF_COL):
        for r in range(NUM_OF_ROW - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                # found the connecting 4 pieces
                return True;

    # check for diagonals
    for c in range(NUM_OF_COL - 3):
        for r in range(NUM_OF_ROW - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                # found the connecting 4 pieces
                return True;

    for c in range(NUM_OF_COL - 3):
        for r in range(3, NUM_OF_ROW):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                # found the connecting 4 pieces
                return True;

def draw_board(board):
    for c in range(NUM_OF_COL):
        for r in range(NUM_OF_ROW):
            pygame.draw.rect(screen, BABY_BLUE, (c*width_height, r*width_height+width_height, width_height, width_height))
            # empty spot has to be black
            pygame.draw.circle(screen, BLACK, (int(c*width_height+width_height/2), int(r*width_height+width_height+width_height/2)), radius)

    for c in range(NUM_OF_COL):
        for r in range(NUM_OF_ROW):
            # player 1 inserts piece
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*width_height+width_height/2), height-int(r*width_height+width_height/2)), radius)
            # if player 2 inserts a piece
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*width_height+width_height/2), height-int(r*width_height+width_height/2)), radius)
    pygame.display.update()


board = build_board()
display_board(board)
there_is_winner = False;
turn = 0

# intializing pygame
pygame.init()
# pixel size of a given portion of the game screen
width_height = 100
width = NUM_OF_COL * width_height
height = (NUM_OF_ROW + 1) * width_height

radius = int(width_height/2 - 7)

# tuple
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
draw_board(board)
pygame.display.update()

game_font = pygame.font.Font('ARCADE_I.ttf', 48)


while not there_is_winner:
    # pygame reading events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, width_height))
            pos_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (pos_x, int(width_height/2)), radius)
            else:
                pygame.draw.circle(screen, YELLOW, (pos_x, int(width_height/2)), radius)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, width_height))
            # prompt player 1 for input
            if turn == 0:
                pos_x = event.pos[0]
                # column choice
                choice = int(math.floor(pos_x/width_height))
                if is_valid_loc(board, choice):
                    # getting the row/col position that is free and inserting the piece
                    row = get_next_open_row(board, choice)
                    drop_piece(board, row, choice, 1)
                    if detect_win(board, 1):
                        game_winner_label = game_font.render("PLAYER 1 WINS!", 1, RED)
                        screen.blit(game_winner_label, (45,15))
                        there_is_winner = True;


            else:
            # prompt player 2 for their choice
                pos_x = event.pos[0]
                # column choice
                choice = int(math.floor(pos_x/width_height))
                if is_valid_loc(board, choice):
                    # getting the row/col position that is free and inserting the piece
                    row = get_next_open_row(board, choice)
                    drop_piece(board, row, choice, 2)
                    if detect_win(board, 2):
                        game_winner_label = game_font.render("PLAYER 2 WINS!", 1, YELLOW)
                        screen.blit(game_winner_label, (45,15))
                        there_is_winner = True;

            display_board(board)
            draw_board(board)
            # incrementing turn
            turn += 1
            # turn will now only be able to be either a 0 or 1
            turn = turn % 2

            # will stall for 5 seconds after a player has won and the close down
            if there_is_winner:
                pygame.time.wait(5000)
