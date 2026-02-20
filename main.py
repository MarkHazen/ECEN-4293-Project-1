import json
import numpy as np
from scipy.signal import convolve2d
import time
import tkinter as tk
from tkinter import messagebox

import json

with open("rules.json") as f:
    rules = json.load(f)

BIRTH = rules["birth"]
SURVIVE = rules["survival"]
WRAP = rules["wrap"]


CELL = rules["cell_size"]
ROWS = COLS = rules["game_size"]

ALIVE_COLOR = rules["alive_color"]
DEAD_COLOR = rules["dead_color"]
GRID_COLOR = rules["grid_color"]

running = False

def next_generation(game_board):
    kernal = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    
    # Wrap
    boundary_type = 'wrap' if WRAP else 'fill'
    neighbors = convolve2d(game_board, kernal, mode='same',boundary=boundary_type)

    new_board = ((np.isin(neighbors, BIRTH)) | ((game_board == 1) & np.isin(neighbors, SURVIVE))).astype(int)

    return new_board


randomized = messagebox.askyesno("", "Would you like to start with a randomized board?")

if randomized:
    board = np.random.choice([0,1], size=(ROWS, COLS), p=[0.7,0.3])
else:
    board = np.zeros((ROWS, COLS), dtype=int)

root = tk.Tk()
canvas = tk.Canvas(root, width=COLS*CELL, height=ROWS*CELL, bg=DEAD_COLOR)
canvas.pack()

def draw_grid():
    for x in range(0, COLS * CELL, CELL):
        canvas.create_line(x, 0, x, ROWS * CELL, fill=GRID_COLOR)
    for y in range(0, ROWS * CELL, CELL):
        canvas.create_line(0, y, COLS * CELL, y, fill=GRID_COLOR)

def toggle_running(event=None):
    global running
    running = not running

root.bind("<space>", toggle_running)

def paint_cell(event):
    global board

    #no redit if run
    if running:
        return

    row = event.y // CELL
    col = event.x // CELL

    if 0 <= row < ROWS and 0 <= col < COLS:
        board[row, col] = 1  # Paint

def erase_cell(event):
    global board

    #no redit if run
    if running:
        return

    row = event.y // CELL
    col = event.x // CELL

    if 0 <= row < ROWS and 0 <= col < COLS:
        board[row, col] = 0  # Erase

canvas.bind("<Button-1>", paint_cell)# Left click
canvas.bind("<B1-Motion>", paint_cell)# Drag left

canvas.bind("<Button-3>", erase_cell)# Right click
canvas.bind("<B3-Motion>", erase_cell)# Drag right

def save_board(event=None):
    np.savetxt("saved_state.txt", board, fmt="%d")

def load_board(event=None):
    global board
    board = np.loadtxt("saved_state.txt", dtype=int)

root.bind("s", save_board)
root.bind("l", load_board)

def draw():
    global board
    canvas.delete("all")

    draw_grid()

    if running:
        board = next_generation(board)

    for r in range(ROWS):
        for c in range(COLS):
            if board[r,c] == 1:
                canvas.create_rectangle(c*CELL, r*CELL, (c+1)*CELL, (r+1)*CELL, fill=ALIVE_COLOR, outline="")

    root.after(100, draw)

draw()
root.mainloop()