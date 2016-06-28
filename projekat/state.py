from __future__ import print_function

import copy


class State(object):
    """
    Klasa koja opisuje stanje table.
    """

    def __init__(self, board, color, parent=None):
        """
        :param board: Board (tabla)
        :param parent: roditeljsko stanje
        :return:
        """
        self.color = color
        self.board = board  # sahovska tabla koja opisuje trenutno stanje
        self.parent = parent  # roditeljsko stanje
        self.value = 0.  # "vrednost" stanja - racuna ga evaluaciona funkcija calculate_value()
        self.col = ''
        
    def __str__(self):
        return "Simple material"

    def generate_next_states(self, max_player):
        """
        Generise moguca sledeca stanja (table) na osnovu svih mogucih poteza (u zavisnosti koji je igrac na potezu).
        :param max_player: bool. Da li je MAX igrac (crni)?
        :return: list. Lista mogucih sledecih stanja.
        """
        next_states = []
        if max_player:
            color = self.color
        else:
            if self.color == 'w':
                color = 'b'
            else:
                color = 'w'
        legal_moves = self.board.get_moves(color)
        for legal_move in legal_moves:
            new_board = copy.deepcopy(self.board)
            new_board.set_piece(color, legal_move[0], legal_move[1])
            for pos in legal_moves[legal_move]:
                new_board.set_piece(color, pos[0], pos[1])
            next_state = State(new_board,self.color, self)
            next_states.append(next_state)
        # TODO 5: Izmesati listu moguca sledeca stanja (da ne budu uvek u istom redosledu)
        return next_states

    def calculate_value(self):
        """
        Evaluaciona funkcija za stanje.
        :return:
        """
 
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                if self.board.data[row][col] != '.':
                    if self.board.data[row][col] == self.color:                    
                        self.value += 1
                    else:
                        self.value -= 1
        return self.value
        
