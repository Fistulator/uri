from __future__ import print_function

import copy

class Board:
    """
    Klasa koja implementira strukturu table.
    """

    def __init__(self, rows=20, cols=20):
        self.rows = rows  # broj redova
        self.cols = cols  # broj kolona
        self.elems = ['.',   # prazno polje
                      'b',  # crni pijun
                      'w',  # crni top
                      ]

        self.data = [['.'] * cols for _ in range(rows)]
        

    def load_from_file(self, file_path):
        """
        Ucitavanje table iz fajla.
        :param file_path: putanja fajla.
        """
        board_f = open(file_path, 'r')
        row = board_f.readline().strip('\n')
        self.data = []
        while row != '':
            self.data.append(list(row.split()))
            row = board_f.readline().strip('\n')
        board_f.close()

    def save_to_file(self, file_path):
        """
        Snimanje table u fajl.
        :param file_path: putanja fajla.
        """
        if file_path:
            f = open(file_path, 'w')
            for row in range(self.rows):
                f.write(''.join(self.data[row]) + '\n')
            f.close()
            
    def set_piece(self, color, x, y):
        self.data[x][y] = color

    def clear(self):
        """
        Ciscenje sadrzaja cele table.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                self.data[row][col] = '.'

    def find_position(self, element):
        """
        Pronalazenje specificnog elementa unutar table.
        :param element: kod elementa.
        :returns: tuple(int, int)
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] == element:
                    return row, col
        return None, None

    def find_pieces(self, color):
        """ 
        Ovom funkcijom nalazimo sve figure jedne boje
        """
        ret = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] == color:
                    ret.append((row,col))
        return ret
        
    def get_moves(self,color):
        """
        Svi legalni potezi se vracaju u formi recnika, gde je kljuc lokacija na koju stavljamo novu figuru, 
        a vrednost sve figure cija ce se boja menjati
        """

        moves = {}  
        
        dir_x = [-1, -1, -1, 0, 0, 1, 1, 1]
        dir_y = [-1, 0, 1, -1, 1, -1, 0, 1]
        

        pieces = self.find_pieces(color)
        #print(str(pieces))
        for p in pieces:
            #print ("Krecem iz " + str(p ) + 'prijatelji su '+ color + " figura ovde je " + self.data[p[0]][p[1]])
            for x, y in zip(dir_x, dir_y):
                #print("X : " + str(x) + " Y : " + str(y))
                toflip = []
                newx = p[0] + x
                newy = p[1] + y
                #print("Newx " + str(newx) + " newy " + str(newy) + " data " + board.data[newx][newy])
                while 0 <= newx < self.rows and 0 <= newy < self.cols and self.data[newx][newy] != color and self.data[newx][newy] != '.':
    #                print("Newx " + str(newx) + " newy " + str(newy) + " data " + board.data[newx][newy])
                    #print("na poziciji " + str ((newx, newy)) + " najden protivnik, idem dalje")
                    toflip.append((newx, newy))
                    newx += x
                    newy += y
                if 0 <= newx < self.rows and 0 <= newy < self.cols:
                    if self.data[newx][newy] == '.' and len(toflip) > 0:
                        #print("Dodajem poziciju " + str(newx) + "  " + str(newy))
                        if (newx, newy) in moves:
                            moves[(newx, newy)].extend(copy.deepcopy(toflip))
                        else:
                            moves[(newx,newy)] = copy.deepcopy(toflip)
        return moves
        
    def is_frontier(self, row, col):
        dir_x = [-1, -1, -1, 0, 0, 1, 1, 1]
        dir_y = [-1, 0, 1, -1, 1, -1, 0, 1]
        
        for x, y in zip(dir_x, dir_y):
            newx = row + x
            newy = col + y
            if 0 <= newx < self.rows and 0 <= newy < self.cols:
                    if self.data[newx][newy] == '.':
                        return 1
        return 0
        
    def get_no_of_moves(self,color):
        dir_x = [-1, -1, -1, 0, 0, 1, 1, 1]
        dir_y = [-1, 0, 1, -1, 1, -1, 0, 1]
        

        pieces = self.find_pieces(color)
        l = []
        #print(str(pieces))
        for p in pieces:
            #print ("Krecem iz " + str(p ) + 'prijatelji su '+ color + " figura ovde je " + self.data[p[0]][p[1]])
            for x, y in zip(dir_x, dir_y):
                #print("X : " + str(x) + " Y : " + str(y))
                add = False
                newx = p[0] + x
                newy = p[1] + y
                #print("Newx " + str(newx) + " newy " + str(newy) + " data " + board.data[newx][newy])
                while 0 <= newx < self.rows and 0 <= newy < self.cols and self.data[newx][newy] != color and self.data[newx][newy] != '.':
    #                print("Newx " + str(newx) + " newy " + str(newy) + " data " + board.data[newx][newy])
                    #print("na poziciji " + str ((newx, newy)) + " najden protivnik, idem dalje")
                    add = True
                    newx += x
                    newy += y
                if 0 <= newx < self.rows and 0 <= newy < self.cols:
                    if self.data[newx][newy] == '.' and add and (newx, newy) not in l:
                        l.append((newx,newy))
        return len(l)
        
    def white_winner(self):
        val = 0 
        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] == 'w':
                    val += 1
                elif self.data[row][col] == 'b':
                    val -= 1
        if val > 0:
            return "w"
        elif val < 0:
            return "b"
        else:
            return "s"
    
            
            
    