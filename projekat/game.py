from __future__ import print_function

import Tkinter as tk
import tkFileDialog
import os
import copy
import time
from PIL import Image, ImageTk  # pip install --upgrade Pillow==3.1.1

from board import Board
from state import *
from search import *
from eval_f import *


def load_board_from_file(filename=None):
    if filename is None:
        filename = tkFileDialog.askopenfilename(defaultextension='.brd',
                                                filetypes=(('board files', '*.brd'), ('All files', '*.*')))
    board.load_from_file(filename)
    return filename


def save_board_to_file():
    filename = tkFileDialog.asksaveasfilename(defaultextension='.brd',
                                              filetypes=(('board files', '*.brd'), ('All files', '*.*')))
    board.save_to_file(filename)


def load_board(from_file=None):      # filename passed when reopening (resetting) same file
    load_board_from_file(from_file)
    display_board()


def reset():
    display_board()

moves = {}
start, end = time.time(), None
log = file('loglong.csv', 'a')

def automate(bdepth = 4, beval = Fancy(), wdepth = 3, weval = Simple()):
    global moves, board, history, start, end
    load_board('boards/reversi.brd')
    p1times = []
    p2times = []
    notover = True
    wturns = bturns = 0
    while notover:
        start = time.time()
        searchw = AlphaBeta(board, wdepth, "w", weval)  # ovde promeniti koji se algoritam koristi i koja je dubina pretrage
        next_state = searchw.perform_adversarial_search()  # izvrsi pretragu
        end = time.time()
        duration = end - start
        p1times.append(duration)
        print('--- {0} was thinking for {1} seconds ---'.format('White', duration))
        if next_state is None:
            print('--- {0} has no moves ---'.format('White'))
            notover = False
        else:
            board = next_state.board
            display_board()
            wturns += 1
            start = time.time()
        
                
        start = time.time()
        searchb = AlphaBeta(board, bdepth, "b", beval)  # ['p', 'c', 'l', 'm', 'f', 'd'] su svi argumenti, c- corner, p - pieces, m - mobility, f- frontier, d - piece difference, l - oko coskova
        next_state = searchb.perform_adversarial_search()  # izvrsi pretragu
        end = time.time()
        duration = end - start
        p2times.append(duration)
        print('--- {0} was thinking for {1} seconds ---'.format('Black', duration))
        if next_state is None:
            print('--- {0} has no moves ---'.format('Black'))
            notover = False
        else:
            board = next_state.board
            display_board()
            bturns += 1
            start = time.time()
            notover = True
            
        
        bs = board.find_pieces('b')
        ws = board.find_pieces('w')
        
        print("turn " + str(wturns) + " whites : " + str(len(ws)) + " blacks : " + str(len(bs))+ '\n')
      
    su = sum(p1times)
    print(str(searchw))
    log.write(str(searchw) + ',' + str(su/len(p1times)*1.) + ',')
    print("Number of moves taken = " + str(len(p1times)) + " Average thinking time = " + str(su/len(p1times)*1.))   
    print(str(searchb))
    su = sum(p2times)
    log.write(str(searchb) + ',' + str(su/len(p2times)*1.) + ',')
    print("Number of moves taken = " + str(len(p2times)) + " Average thinking time = " + str(su/len(p2times)*1.))
    log.write(str(wturns) + ',' + str(bturns) + ',' + board.white_winner() + ',' + str(len(ws)) + " : " + str(len(bs)) + '\n')
    print(board.white_winner() + " in " + str(wturns) + " turns")

def dolog():
    log.write('weval,wdepth,wavgt,beval,bdepth,bavgt,wturns,bturns,winner,w:b\n')
    evals = [Zones(), Classic(), Fancy()]
    for i in range(len(evals)):
        automate(1, evals[i], 1, Simple())
        automate(1, evals[i], 2, Simple())
        automate(1, evals[i], 3, Simple())
        automate(2, evals[i], 3, Simple())
        automate(2, evals[i], 5, Simple())
        automate(3, evals[i], 5, Simple())
        if i > 0:
            j = i - 1
            automate(1, evals[i], 1, evals[j])
            automate(1, evals[i], 2, evals[j])
            automate(1, evals[i], 3, evals[j])
            automate(2, evals[i], 3, evals[j])
            automate(2, evals[i], 5, evals[j])
            automate(3, evals[i], 5, evals[j])
        if i > 1:
            j = i - 2
            automate(1, evals[i], 1, evals[j])
            automate(1, evals[i], 2, evals[j])
            automate(1, evals[i], 3, evals[j])
            automate(2, evals[i], 3, evals[j])
            automate(2, evals[i], 5, evals[j])
            automate(3, evals[i], 5, evals[j])
            
    log.close()

def append():
    automate(4, FancyTest(['d']), 5, Zones())
    automate(4, FancyTest(['d']), 5, Classic())
 
    log.close()

def move_piece(event, row=None, col=None):
    global moves, board, history, start, end, p1times, p2times
    moves = board.get_moves('b')
    for move in moves:
        update_board(move[0], move[1])
    if row is None and col is None:
        cx = event.x
        cy = event.y
        col = cx // cell_size  # column
        row = cy // cell_size  # row

        # select piece
    if (row, col) in moves:
        # determine which piece is selected
        moves_ = copy.copy(moves)
        moves = {}
        for move in moves_:
            update_board(move[0], move[1])
    
    
        history.append(copy.deepcopy(board))
    
        board.set_piece('b', row, col)
        update_board(row, col)
        for pos in moves_[(row,col)]:
            board.set_piece('b', pos[0], pos[1])
            update_board(pos[0], pos[1])
    
        end = time.time()
        duration = end - start
        p1times.append(duration)
        print('--- {0} was thinking for {1} seconds ---'.format('White', duration))
    

        
        # --------------------------------
        # AI (black player) should do a move here
        # --------------------------------

        start = time.time()
        search = Minimax(board, 4, "w")  # ovde promeniti koji se algoritam koristi i koja je dubina pretrage
        next_state = search.perform_adversarial_search()  # izvrsi pretragu
        end = time.time()
        duration = end - start
        p2times.append(duration)
        print('--- {0} was thinking for {1} seconds ---'.format('Black', duration))
        if next_state is None:
            print('--- {0} has no moves ---'.format('Black'))
        else:
            board = next_state.board
            display_board()
            start = time.time()
        print(str(search))
        su = sum(p2times)
        print("Number of moves taken = " + str(len(p2times)) + " Average thinking time = " + str(su/len(p2times)*1.))
        board.get_moves('w')
        for mov in moves:
            update_board(mov[0], mov[1])

def close():
    log.close()

def update_board(row, col):
    data = board.data
    delete_elems(row, col)
    elem = data[row][col]


    if (row, col) in moves:
        color = 'light green'
    else:
        color =  'gray'
    draw_rectangle(row, col, color)

    if elem in board_to_icons:
        icon = icons[board_to_icons[elem]]
        draw_icon(row, col, icon)


def get_cell_rectangle(row, col):
    return col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size


def draw_rectangle(row, col, color, width=1):
    rect = get_cell_rectangle(row, col)
    elem_id = canvas.create_rectangle(rect, width=width, fill=color, outline='black')
    save_elem_id(elem_id, row, col)


def draw_icon(row, col, icon):
    rect = get_cell_rectangle(row, col)
    elem_id = canvas.create_image(rect[0]+2, rect[1]+2, image=icon, anchor=tk.NW)
    canvas.icons[elem_id] = icon
    save_elem_id(elem_id, row, col)


def save_elem_id(elem_id, row, col):
    if len(grid_elem_ids[row][col]) == 0:
        grid_elem_ids[row][col] = []
    grid_elem_ids[row][col].append(elem_id)


def delete_elems(row, col):
    if 0 <= row < rows and 0 <= col < cols:
        for elem_id in grid_elem_ids[row][col]:
            canvas.delete(elem_id)
            if elem_id in canvas.icons:
                del canvas.icons[elem_id]
        grid_elem_ids[row][col] = []


def display_board():
    canvas.delete(tk.ALL)
    for row in range(len(board.data)):
        for col in range(len(board.data[0])):
            update_board(row, col)


def make_menu(win):
    top = tk.Menu(win)  # win=top-level window
    win.config(menu=top)  # set its menu option
    file_menu = tk.Menu(top)
    file_menu.add_command(label='Open...', command=load_board, underline=0)
    file_menu.add_command(label='Save...', command=lambda: save_board_to_file(), underline=0)
    file_menu.add_command(label='Quit', command=sys.exit, underline=0)
    top.add_cascade(label='File', menu=file_menu, underline=0)
    edit = tk.Menu(top, tearoff=False)
    edit.add_separator()
    top.add_cascade(label='Edit', menu=edit, underline=0)


def undo():
    global history, board
    if len(history) > 1:
        board = history[-1]
        history = history[0:-1]
        display_board()

#  main program #
rows = 8  # broj redova table
cols = 8  # broj kolona table
cell_size = 80  # velicina celije

board = Board(rows=rows, cols=cols)

history = [copy.deepcopy(board)]

grid_elem_ids = [[[]] * cols for _ in range(rows)]

# mapiranje sadrzaja table na boju celije
board_to_colors = {'.': 'white',
                   'w': 'gray',
                   'g': 'orangered'}
# mapiranje sadrzaja table na ikonicu
board_to_icons = {'b': 'sea.png',
                  'w': 'sun.png',
                  }


root = tk.Tk()
root.title('ORI - Pretrage')
make_menu(root)  # make window menu
ui = tk.Frame(root, bg='white')  # main UI
ui2 = tk.Frame(root, bg='white')

# define the user interaction widgets
canvas = tk.Canvas(root, width=cols * cell_size + 1, height=rows * cell_size + 1,
                   highlightthickness=0, bd=0, bg='white')

# load icons
canvas.icons = dict()
icons = dict()
for f in os.listdir('icons'):
    icon = Image.open(os.path.join('icons', f))
    icon = icon.resize((cell_size - 2, cell_size - 2), Image.ANTIALIAS)  # resize icon to fit cell
    icon = ImageTk.PhotoImage(icon)
    icons[f] = icon

# create buttons
do_button = tk.Button(ui, text = "TEST", width = 10, command = dolog)
close_button = tk.Button(ui, text = "TEST", width = 10, command = close)
app_button= tk.Button(ui, text = "APPEND", width = 10, command = append)
auto_button = tk.Button(ui, text = "AUTOMATE", width = 10, command = automate)
restart_button = tk.Button(ui, text='RESET', width=10, command=reset)
undo_button = tk.Button(ui, text='UNDO', width=10, command=undo)

# add buttons to UI
restart_button.grid(row=4, column=0, padx=10, pady=10)
undo_button.grid(row=5, column=0, padx=10, pady=10)
auto_button.grid(row = 6, column = 0, padx = 10, pady = 10)
do_button.grid(row = 7, column = 0, padx = 10, pady = 10)
app_button.grid(row = 8, column = 0, padx = 10, pady = 10)
close_button.grid(row = 9, column = 0, padx = 10, pady = 10)

# put everything on the screen
display_board()
canvas.bind('<Button-1>', move_piece)  # bind left mouse click event to function switch_cell
ui.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)
canvas.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
ui2.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH, anchor=tk.W)

# load default board
load_board('boards/reversi.brd')
board.get_moves('w')
for m in moves:
    update_board(m[0], m[1])

root.mainloop()
