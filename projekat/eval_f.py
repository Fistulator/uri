from __future__ import print_function


class Eval(object):
    
    def get_value(self, board, color):
        pass
    
    def __str__(self):
        pass
    
class Simple(Eval):
    def get_value(self, board, color):
        value = 0
        for row in range(board.rows):
            for col in range(board.cols):
                if board.data[row][col] != '.':
                    if board.data[row][col] == color:                    
                        value += 1
                    else:
                        value -= 1
        return value
        
    def __str__(self):
        return "Simple"

class Classic(Eval):
    def classic_values(self,row, col):
        if row == 0 or row == 7:
            if col == 0 or col == 7:
                return 99
            elif col == 1 or col == 6:
                return -8
            elif col == 2 or col == 5:
                return 8
            elif col == 3 or col == 4:
                return 6                
        elif row == 1 or row == 6:
            if col == 0 or col == 7:
                return -8
            elif col == 1 or col == 6:
                return -24
            elif col == 2 or col == 5:
                return -4
            elif col == 3 or col == 4:
                return -3
        elif row == 2 or row == 5:
            if col == 0 or col == 7:
                return 8
            elif col == 1 or col == 6:
                return -4
            elif col == 2 or col == 5:
                return 7
            elif col == 3 or col == 4:
                return 4
        elif row == 3 or row == 4:
            if col == 0 or col == 7:
                return 6
            elif col == 1 or col == 6:
                return -3
            elif col == 2 or col == 5:
                return 4
            elif col == 3 or col == 4:
                return 0    
    
    def get_value(self, board, color):
        value = 0
        for row in range(board.rows):
            for col in range(board.cols):
                if board.data[row][col] != '.':
                    if board.data[row][col] == color:                    
                        value += self.classic_values(row,col)
                    else:
                        value -= self.classic_values(row,col)
        return value
        
    def __str__(self):
        return "Classic"
        
class Zones(Eval):
    def zone_values(self, row, col):
        if row == 0 or row == 7:
            if col == 0 or col == 7:
                #zona 5 (coskovi) - najbolji
                return 100
            elif col == 1 or col == 6:
                #zona 4 - losa pozicija jer otvara coskove
                return -100
            else:
                #zona 3  - odlicna jer ima manje smerova za flipovanje
                return 50
        elif col == 0 or col == 7:
            if row == 1 or row == 6:
                #zona 4 - grozno
                return -50
            else:
                #zona 3 - odlicna
                return 50
        elif row == 1 or row == 6:
            if col == 1 or col == 6:
                #jos uvek zona 4
                return -50
            else:
                #zona 2 je rizicna
                return -25
        elif col == 1 or col== 1:
            #loose cannon dvojka
            return -25
        else:
            #plain joe cetvorka
            return 25
    
    def get_value(self, board, color):
        value = 0
        for row in range(board.rows):
            for col in range(board.cols):
                if board.data[row][col] != '.':
                    if board.data[row][col] == color:                    
                        value += self.zone_values(row,col)
                    else:
                        value -= self.zone_values(row,col)
        return value
        
    def __str__(self):
        return "Zones"
        
class Fancy(Eval):
    def __str__(self):
        return "Fancy"
        
    def get_pos_value(self, row, col):
        if row == 0 or row == 7:
            if col == 0 or col == 7:
                return 20
            elif col == 1 or col == 6:
                return -3
            elif col == 2 or col == 5:
                return 11
            elif col == 3 or col == 4:
                return 6                
        elif row == 1 or row == 6:
            if col == 0 or col == 7:
                return -3
            elif col == 1 or col == 6:
                return -7
            elif col == 2 or col == 5:
                return -4
            elif col == 3 or col == 4:
                return 1
        elif row == 3 or row == 4:
            if col == 0 or col == 7:
                return 8
            elif col == 1 or col == 6:
                return 1
            elif col == 2 or col == 5:
                return 2
            elif col == 3 or col == 4:
                return -3
        elif row == 2 or row == 5:
            if col == 0 or col == 7:
                return 11
            elif col == 1 or col == 6:
                return -4
            else:
                return 2
                
    def get_value(self, board, color):
        my_tiles = 0
        opp_tiles = 0
        d = 0
        my_ftiles = 0
        opp_ftiles = 0
        
        for row in range(board.rows):
            for col in range(board.cols):
                if board.data[row][col] != '.':
                    if board.data[row][col] == color: 
                        d += self.get_pos_value(row,col)
                        my_tiles += 1
                        my_ftiles += board.is_frontier(row,col)
                    else:
                        d -= self.get_pos_value(row,col)
                        opp_tiles += 1
                        opp_ftiles += board.is_frontier(row,col)
                        
        if my_tiles > opp_tiles:
            p = (100.0 * my_tiles)/(my_tiles + opp_tiles)
        elif opp_tiles > my_tiles:
            p = -(100.0 * opp_tiles)/(my_tiles + opp_tiles)
        else:
            p = 0
            
        if my_ftiles > opp_ftiles:
            f = -(100.0 * my_ftiles)/(my_ftiles + opp_ftiles)
        elif opp_ftiles > my_ftiles:
            f = (100.0 * opp_ftiles)/(my_ftiles + opp_ftiles)
        else:
            f = 0
        
        my_tiles = 0
        opp_tiles = 0
        my_corner = 0
        opp_corner = 0
        
        xs = [0, 0, 7, 7]
        ys = [0, 7, 0, 7]        
        
        for (row, col) in zip(xs,ys):
            if board.data[row][col] != '.':
                if board.data[row][col] == color:
                    my_corner += 1
                else:
                    opp_corner += 1
            else:
                newx = abs(row - 1)
                newy = abs(col - 1)
                
                newxs = [row, newx, newx]
                newys = [newy, newy, col]
                
                for (nrow, ncol) in zip (newxs, newys):
                    if board.data[row][col] != '.':
                        if board.data[row][col] == color:
                            my_tiles += 1
                        else:
                            opp_tiles += 1
        c = 25 * (my_corner - opp_corner)
        l = -12.5 * (my_tiles - opp_tiles)
        
        my_tiles = board.get_no_of_moves(color)
        if color == 'w':
            opp_tiles = board.get_no_of_moves('b')
        else:
            opp_tiles = board.get_no_of_moves('w')
        
        if my_tiles > opp_tiles:
            m = (100.0 * my_tiles)/ (my_tiles + opp_tiles)
        elif (my_tiles < opp_tiles):
            m = -(100.0 * opp_tiles)/ (my_tiles + opp_tiles)
        else:
            m = 0
        
        value = 10 * p + 801.724 * c + 382.026 * l + 78.922 * m + 74.396 * f + 10 * d
            
        return value
        
class FancyTest(Eval):
    def __init__(self, arg = []):
        self.no = arg
    
    def __str__(self):
        retval = ''
        for no in self.no:
            retval += no + '| '
        return "Fancy test sa " + retval
        
    def get_pos_value(self, row, col):
        if row == 0 or row == 7:
            if col == 0 or col == 7:
                return 20
            elif col == 1 or col == 6:
                return -3
            elif col == 2 or col == 5:
                return 11
            elif col == 3 or col == 4:
                return 6                
        elif row == 1 or row == 6:
            if col == 0 or col == 7:
                return -3
            elif col == 1 or col == 6:
                return -7
            elif col == 2 or col == 5:
                return -4
            elif col == 3 or col == 4:
                return 1
        elif row == 3 or row == 4:
            if col == 0 or col == 7:
                return 8
            elif col == 1 or col == 6:
                return 1
            elif col == 2 or col == 5:
                return 2
            elif col == 3 or col == 4:
                return -3
        elif row == 2 or row == 5:
            if col == 0 or col == 7:
                return 11
            elif col == 1 or col == 6:
                return -4
            else:
                return 2        
        
    def get_value(self, board, color):        
        my_tiles = 0
        opp_tiles = 0
        d = 0
        my_ftiles = 0
        opp_ftiles = 0
        
        for row in range(board.rows):
            for col in range(board.cols):
                if board.data[row][col] != '.':
                    if board.data[row][col] == color: 
                        d += self.get_pos_value(row,col)
                        my_tiles += 1
                        my_ftiles += board.is_frontier(row,col)
                    else:
                        d -= self.get_pos_value(row,col)
                        opp_tiles += 1
                        opp_ftiles += board.is_frontier(row,col)
                        
        if my_tiles > opp_tiles:
            p = (100.0 * my_tiles)/(my_tiles + opp_tiles)
        elif opp_tiles > my_tiles:
            p = -(100.0 * opp_tiles)/(my_tiles + opp_tiles)
        else:
            p = 0
            
        if my_ftiles > opp_ftiles:
            f = -(100.0 * my_ftiles)/(my_ftiles + opp_ftiles)
        elif opp_ftiles > my_ftiles:
            f = (100.0 * opp_ftiles)/(my_ftiles + opp_ftiles)
        else:
            f = 0
        
        my_tiles = 0
        opp_tiles = 0
        my_corner = 0
        opp_corner = 0
        
        xs = [0, 0, 7, 7]
        ys = [0, 7, 0, 7]        
        
        for (row, col) in zip(xs,ys):
            if board.data[row][col] != '.':
                if board.data[row][col] == color:
                    my_corner += 1
                else:
                    opp_corner += 1
            else:
                newx = abs(row - 1)
                newy = abs(col - 1)
                
                newxs = [row, newx, newx]
                newys = [newy, newy, col]
                
                for (nrow, ncol) in zip (newxs, newys):
                    if board.data[row][col] != '.':
                        if board.data[row][col] == color:
                            my_tiles += 1
                        else:
                            opp_tiles += 1
        c = 25 * (my_corner - opp_corner)
        l = -12.5 * (my_tiles - opp_tiles)
        
        my_tiles = board.get_no_of_moves(color)
        if color == 'w':
            opp_tiles = board.get_no_of_moves('b')
        else:
            opp_tiles = board.get_no_of_moves('w')
        
        if my_tiles > opp_tiles:
            m = (100.0 * my_tiles)/ (my_tiles + opp_tiles)
        elif (my_tiles < opp_tiles):
            m = -(100.0 * opp_tiles)/ (my_tiles + opp_tiles)
        else:
            m = 0
      
        value = 0          
        
        if 'p' not in self.no:  # p je odnos figura
            value += 10 * p
        if 'c' not in self.no: # c je komanda coskova
            value += 801.724 * c
        if 'l' not in self.no:  #l je ono oko coskova
            value += 382.026 * l
        if 'm' not in self.no:  # m je broj poteza (mobility)
            value += 78.922 * m
        if 'f' not in self.no:  # f su figure koji se granice sa praznim (frontier)
            value += 74.396 * f
        if 'd' not in self.no:  #d je razlika u broju figura
            value += 10 * d
            
        return value
    