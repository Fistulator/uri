from __future__ import print_function

from abc import *
from state import State
import sys

MAX_FLOAT = sys.float_info.max
MIN_FLOAT = -MAX_FLOAT


class AdversarialSearch(object):
    """
    Apstraktna klasa za suparnicku/protivnicku pretragu.
    """

    def __init__(self, board, max_depth, color, Eval):
        """
        :param board: tabla koja predstavlja pocetno stanje.
        :param max_depth: maksimalna dubina pretrage (koliko poteza unapred).
        :return:
        """
#        if color == "w":
#            col = 'b'
#        else:
#            col = 'w'
        self.initial_state = State(board, color, Eval, parent=None)
        self.max_depth = max_depth
        self.color = color

    @abstractmethod
    def perform_adversarial_search(self):
        """
        Apstraktna metoda koja vrsi pretragu i vraca sledece stanje.
        """
        pass
    
    def __str__(self):
        return(str(self.initial_state) + "," + str(self.max_depth))


class Minimax(AdversarialSearch):
    def minimax(self, state, depth):   
        #print('\t'*depth + str(state.calculate_value()) + " depth " + str(depth) + " max " + str(depth % 2 == 0))        
        
        
        if depth == self.max_depth:
            return state.calculate_value()
            
        max_player = depth % 2 == 0
        min_player = not max_player
       
        next_states = state.generate_next_states(max_player)
        best_value = MAX_FLOAT if min_player else MIN_FLOAT
        next_state_best = None
         
        for next_state in next_states:
            #print('\t'*depth + str(next_state.calculate_value()) + " depth " + str(depth) + " max " + str(depth % 2 == 0))
            next_state_value = self.minimax(next_state, depth + 1)
           
            if max_player and next_state_value > best_value:
                #print('\t' + "mak poredim " + str(best_value) + " i " + str(next_state_value))
                best_value = next_state_value
                next_state_best = next_state
               
            if min_player and next_state_value < best_value:
                #print('\t'* depth + "min poredim " + str(best_value) + " i " + str(next_state_value))
                best_value = next_state_value
                next_state_best = next_state
       
        if depth == 0:
            return next_state_best
        
        return best_value
            
        
    def perform_adversarial_search(self):
        # TODO 1: Implementiran minimax algoritam
        return self.minimax(self.initial_state, 0)


class AlphaBeta(AdversarialSearch):
    def alphabeta(self, state, depth, alpha, beta):
        if depth == self.max_depth:
            return state.calculate_value()
         
        max_player = depth % 2 == 0
        min_player = not max_player
       
        next_states = state.generate_next_states(max_player)
        best_value = MAX_FLOAT if min_player else MIN_FLOAT
        next_state_best = None
         
        for next_state in next_states:
            next_state_value = self.alphabeta(next_state, depth + 1, alpha, beta)
           
            if max_player and next_state_value > best_value:
                best_value = next_state_value
                next_state_best = next_state
                alpha = max(alpha, next_state_value)
               
            if min_player and next_state_value < best_value:
                best_value = next_state_value
                next_state_best = next_state
                beta = min(beta, next_state_value)
               
            if beta <= alpha:
                break
       
        if depth == 0:
            return next_state_best
           
        return best_value

    def perform_adversarial_search(self):
        # TODO 4: Implementiran alpha-beta algoritam
        return self.alphabeta(self.initial_state, 0, MIN_FLOAT, MAX_FLOAT)