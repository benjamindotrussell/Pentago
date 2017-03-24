import Tile
import Node

from copy import deepcopy

class Board(object):
    def __init__(self):
        self.board_state = []
        self.score = 0
        self.p1_win = None
        self.p2_win = None

    '''
        make an empty board
        return: an empty board
    '''
    def generate_board(self):
        for i in range(4):
            for j in range(9):
                self.board_state.append(Tile.Tile('*'))
        return self.board_state

    @staticmethod
    def board_value(board):
        value = 0
        for i in range(len(board)):
            if board[i].wb == '*':
                value += i * 1
            elif board[i].wb == 'b':
                value += i * 2
            else:
                value += i * 3
        return value

    @staticmethod
    def copy_board(board):
        board_clone = deepcopy(board)
        return board_clone
    '''
        min-max algorithm
    '''
    def ai_move(self, player):
        list_of_ai_moves = [] #list of possible AI moves aka. board_states.
        min_moves = []  #human player potential moves based on AI moves
        #a copy of the board state
        clone = self.copy_board(self.board_state)
        for i in range(len(clone)):
            if clone[i].wb == '*':
                clone2 = self.copy_board(clone)
                clone2[i].set_wb(player.wb)
                list_of_ai_moves.extend(self.get_rotations(clone2))
        list_of_ai_moves = self.remove_redundant_boards(list_of_ai_moves)

        for b in list_of_ai_moves:
            for j in range(len(b)):
                if b[j].wb == '*':
                    copy = self.copy_board(b)
                    copy[j].set_wb(player.not_wb())
                    min_moves.extend(self.get_rotations(copy))
        m = self.get_max(min_moves, player)
        print (len(min_moves) + len(list_of_ai_moves))
        max_state = list_of_ai_moves[m]
        return max_state


    def abp_search(self, node, depth, mini, maxi, p, count):
        list_of_moves = ['    1R', '    2R', '    3R', '    4R', '    1L', '    2L', '    3L', '    4L']
        count += 1
        if depth == 0:
            node.value = self.score_board(node.board_state, p)
            return node.value
        if node.ab == 'max':
            v = mini
            for i in range(len(node.board_state)):
                if node.board_state[i].wb == '*':
                    for j in list_of_moves:
                        node3 = Node.Node(self.copy_board(node.board_state), node.depth + 1, node)
                        node.is_leaf = False
                        node.children.append(node3)
                        if node3.ab == 'min':
                            node3.board_state[i].set_wb(p.wb)
                        else:
                            node3.board_state[i].set_wb(p.not_wb())
                        self.rotate(j, node3.board_state)
                        count += 1
                        vp = self.abp_search(node3, depth - 1, v, maxi, p, count)
                        if vp > v:
                            v = vp
                        if v > maxi:
                            node.value = maxi
                            return maxi
            node.value = v
            return v
        if node.ab == 'min':
            v = maxi
            for i in range(len(node.board_state)):
                if node.board_state[i].wb == '*':
                    for j in list_of_moves:
                        node3 = Node.Node(self.copy_board(node.board_state), node.depth + 1, node)
                        node.is_leaf = False
                        node.children.append(node3)
                        if node3.ab == 'min':
                            node3.board_state[i].set_wb(p.wb)
                        else:
                            node3.board_state[i].set_wb(p.not_wb())
                        self.rotate(j, node3.board_state)
                        count += 1
                        vp = self.abp_search(node3, depth - 1, mini, v, p, count)
                        if vp < v:
                            v = vp
                        if v < mini:
                            node.value = mini
                            return mini
            node.value = v
            return v

    def remove_redundant_boards(self, board_states):
        boards = []
        board_values = set()
        for b in board_states:
            value = self.board_value(b)
            if value not in board_values:
                boards.append(b)
                board_values.add(value)
        return boards
    '''
        place a piece on the board and rotate tht board right or left
        in: player: the player that is making the move
            move: the move made
        return: win:    w: win for white
                        b: win for black
                        1: not a win
    '''
    def rotate(self, move, board):
        #rotate a block to the right
        if move[5].lower() == 'r':
            block1 = board[0:9]
            block2 = board[9:18]
            block3 = board[18:27]
            block4 = board[27:36]
            if (int(move[4])-1) == 0:
                block1 = self.rotate_right(block1)
            elif (int(move[4])-1) == 1:
                block2 = self.rotate_right(block2)
            elif (int(move[4])-1) == 2:
                block3 = self.rotate_right(block3)
            elif (int(move[4])-1) == 3:
                block4 = self.rotate_right(block4)
            board = block1 + block2 + block3 + block4
        elif move[5].lower() == 'l':
            # rotate a block to the left
            block1 = board[0:9]
            block2 = board[9:18]
            block3 = board[18:27]
            block4 = board[27:36]
            if (int(move[4]) - 1) == 0:
                block1 = self.rotate_left(block1)
            elif (int(move[4]) - 1) == 1:
                block2 = self.rotate_left(block2)
            elif (int(move[4]) - 1) == 2:
                block3 = self.rotate_left(block3)
            elif (int(move[4]) - 1) == 3:
                block4 = self.rotate_left(block4)
            board = block1 + block2 + block3 + block4
        else: return 1
        return board

    def get_rotations(self, clone):
        list_of_moves = []#list of board_states
        copy3 = self.copy_board(clone)#copy of the clone
        list_of_moves.append(self.rotate('    1R', copy3))
        copy4 = self.copy_board(clone)
        list_of_moves.append(self.rotate('    2R', copy4))
        copy5 = self.copy_board(clone)
        list_of_moves.append(self.rotate('    3R', copy5))
        copy6 = self.copy_board(clone)
        list_of_moves.append(self.rotate('    4R', copy6))
        copy7 = self.copy_board(clone)
        list_of_moves.append(self.rotate('    1L', copy7))
        copy8 = self.copy_board(clone)
        list_of_moves.append(self.rotate('    2L', copy8))
        copy9 = self.copy_board(clone)
        list_of_moves.append(self.rotate('    3L', copy9))
        copy10 = self.copy_board(clone)
        list_of_moves.append(self.rotate('    4L', copy10))
        #if tf:
        #    return self.get_min(list_of_moves, p)
        return list_of_moves

    def get_max(self, bl, p):
        max_state = 0
        max_score = self.score_board(bl[0], p)
        for i in range(1, len(bl)):
            s = self.score_board(bl[i], p)
            if s > max_score:
                max_state = i
                max_score = s
        return max_state
    '''
        Find the minimum element in a list of board states.
    '''
    def get_min(self, l, p):
        min_state = l[0]
        min_score = self.score_board(l[0], p)
        #get a minimum score for the boards in the list
        for i in range(1, len(l)):
            s = self.score_board(l[i], p)
            if s < min_score:
                min_state = l[i]
                min_score = s
        return min_state

    '''
        set a tile to either w or b
        in:
            tile: tile to set
            wb: w for white
                b for black
    '''
    def set_position(self, player, move):
        # set piece on board
        if self.board_state[((int(move[0]) - 1) * 9) + int(move[2]) - 1].wb == '*':
            self.board_state[((int(move[0]) - 1) * 9) + int(move[2]) - 1].set_wb(player.wb)
            return 1
        else:
            return None

    '''
        look through a list of tiles to find 5 in a row
        in:
            a: a list of tiles
            wb: a white- b or black- b value to look for
        out:
            w
            b
            1
    '''
    def score_board(self, board, p):
        max_count = 0
        # check horizontal lines
        a = board[0:3] + board[9:12]
        max_count += self.find_consecutive(a, p)
        a = board[3:6] + board[12:15]
        max_count += self.find_consecutive(a, p)
        a = board[6:9] + board[15:18]
        max_count += self.find_consecutive(a, p)
        a = board[18:21] + board[27:30]
        max_count += self.find_consecutive(a, p)
        a = board[21:24] + board[30:33]
        max_count += self.find_consecutive(a, p)
        a = board[24:27] + board[33:36]
        max_count += self.find_consecutive(a, p)

        #count vertical
        a = board[0:7:3] + board[18:25:3]
        #a = board[0] + board[3] + board[6] + board[18] + board[21] + board[24]
        max_count += self.find_consecutive(a, p)
        a = board[1:8:3] + board[19:26:3]
        #a = board[1] + board[4] + board[7] + board[19] + board[22] + board[25]
        max_count += self.find_consecutive(a, p)
        a = board[2:9:3] + board[20:27:3]
        #a = board[2] + board[5] + board[8] + board[20] + board[22] + board[26]
        max_count += self.find_consecutive(a, p)
        a = board[9:16:3] + board[27:34:3]
        #a = board[9] + board[12] + board[15] + board[27] + board[30] + board[33]
        max_count += self.find_consecutive(a, p)
        a = board[10:17:3] + board[28:35:3]
        #a = board[10] + board[13] + board[16] + board[28] + board[31] + board[34]
        max_count += self.find_consecutive(a, p)
        a = board[11:18:3] + board[29:36:3]
        #a = board[11] + board[14] + board[17] + board[29] + board[32] + board[35]
        max_count += self.find_consecutive(a, p)

        # check diagonal lines

        a = board[3:4]
        a.append(board[7])
        a.append(board[20])
        a.append(board[30])
        a.append(board[34])
        max_count += self.find_consecutive(a, p)
        a = board[0:1]
        a.append(board[4])
        a.append(board[8])
        a.append(board[27])
        a.append(board[31])
        a.append(board[35])
        max_count += self.find_consecutive(a, p)
        a = board[1:2]
        a.append(board[5])
        a.append(board[15])
        a.append(board[28])
        a.append(board[32])
        max_count += self.find_consecutive(a, p)
        a = board[10:11]
        a.append(board[12])
        a.append(board[8])
        a.append(board[19])
        a.append(board[21])
        max_count += self.find_consecutive(a, p)
        a = board[14:15]
        a.append(board[16])
        a.append(board[27])
        a.append(board[23])
        a.append(board[25])
        max_count += self.find_consecutive(a, p)
        a = board[11:12]
        a.append(board[13])
        a.append(board[15])
        a.append(board[20])
        a.append(board[22])
        a.append(board[24])
        max_count += self.find_consecutive(a, p)
        return max_count

    def check_win(self, p):
        #check horizontal lines
        a = self.board_state[0:3] + self.board_state[9:12]
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[3:6] + self.board_state[12:15]
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[6:9] + self.board_state[15:18]
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[18:21] + self.board_state[27:30]
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[21:24] + self.board_state[30:33]
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[24:27] + self.board_state[33:36]
        if self.find_consecutive(a, p) == 10000:
            return True

        #check vertical lines
        a = self.board_state[0:7:3] + self.board_state[18:25:3]
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[1:8:3] + self.board_state[19:26:3]
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[2:9:3] + self.board_state[20:27:3]
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[9:16:3] + self.board_state[27:34:3]
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[10:17:3] + self.board_state[28:35:3]
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[11:18:3] + self.board_state[29:36:3]
        if self.find_consecutive(a, p) == 10000:
            return True

        # check diagonal lines
        a = self.board_state[3:4]
        a.append(self.board_state[7])
        a.append(self.board_state[20])
        a.append(self.board_state[30])
        a.append(self.board_state[34])
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[0:1]
        a.append(self.board_state[4])
        a.append(self.board_state[8])
        a.append(self.board_state[27])
        a.append(self.board_state[31])
        a.append(self.board_state[35])
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[1:2]
        a.append(self.board_state[5])
        a.append(self.board_state[15])
        a.append(self.board_state[28])
        a.append(self.board_state[32])
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[10:11]
        a.append(self.board_state[12])
        a.append(self.board_state[8])
        a.append(self.board_state[19])
        a.append(self.board_state[21])
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[14:15]
        a.append(self.board_state[16])
        a.append(self.board_state[27])
        a.append(self.board_state[23])
        a.append(self.board_state[25])
        if self.find_consecutive(a, p) == 10000:
            return True
        a = self.board_state[11:12]
        a.append(self.board_state[13])
        a.append(self.board_state[15])
        a.append(self.board_state[20])
        a.append(self.board_state[22])
        a.append(self.board_state[24])
        if self.find_consecutive(a, p) == 10000:
            return True

        return False

    '''
        look through a list of tiles to find 5 in a row
        in:
            a: a list of tiles
            wb: a white- b or black- b value to look for
        out:
            w
            b
            1
    '''
    @staticmethod
    def find_consecutive(a, p):
        pos_count = 1
        neg_count = 1
        for i in range(1, len(a)):
            if a[i-1].wb == a[i].wb:
                if a[i].wb == p.wb:
                    pos_count *= 5
                elif a[i].wb == p.not_wb():
                    neg_count *= 5
        if pos_count >= 625:
            return 10000
        elif neg_count >= 625:
            return -10000
        return pos_count - neg_count

    '''
        rotate a block of the board to the right
        variables-
            block: a 9 tile block of the board
         return: block
    '''
    @staticmethod
    def rotate_right(block):
        temp = block[0].copy()
        block[0].switch(block[6])
        block[6].switch(block[8])
        block[8].switch(block[2])
        block[2].switch(temp)
        temp = block[1].copy()
        block[1].switch(block[3])
        block[3].switch(block[7])
        block[7].switch(block[5])
        block[5].switch(temp)
        return block

    '''
        rotate a block of the board to the left
        variables-
            block: a 9 tile block of the board
        return: block
    '''
    @staticmethod
    def rotate_left( block):
        temp = block[0].copy()
        block[0].switch(block[2])
        block[2].switch(block[8])
        block[8].switch(block[6])
        block[6].switch(temp)
        temp = block[1].copy()
        block[1].switch(block[5])
        block[5].switch(block[7])
        block[7].switch(block[3])
        block[3].switch(temp)
        return block


    '''
        method to output a representation of the board.
    '''
    def to_string(self, game):
        print ' ---------------'
        print '|',
        for i in range(3): print str(self.board_state[i].wb),
        print '|',
        for i in range(9,12): print str(self.board_state[i].wb),
        print '|'
        print '|',
        for i in range(3, 6): print str(self.board_state[i].wb),
        print '|',
        for i in range(12, 15): print str(self.board_state[i].wb),
        print '|'
        print '|',
        for i in range(6, 9): print str(self.board_state[i].wb),
        print '|',
        for i in range(15, 18): print str(self.board_state[i].wb),
        print '|'
        print ' ---------------'
        print '|',
        for i in range(18, 21): print str(self.board_state[i].wb),
        print '|',
        for i in range(27, 30): print str(self.board_state[i].wb),
        print '|'
        print '|',
        for i in range(21, 24): print str(self.board_state[i].wb),
        print '|',
        for i in range(30, 33): print str(self.board_state[i].wb),
        print '|'
        print '|',
        for i in range(24, 27): print str(self.board_state[i].wb),
        print '|',
        for i in range(33, 36): print str(self.board_state[i].wb),
        print '|'
        print ' ---------------'
        print

        game.write(' ---------------\n')
        game.write('| ', )
        for i in range(3): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('| ', )
        for i in range(9, 12): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('|\n')
        game.write('| ', )
        for i in range(3, 6): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('| ', )
        for i in range(12, 15): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('|\n')
        game.write('| ', )
        for i in range(6, 9): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('| ', )
        for i in range(15, 18): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('|\n')
        game.write(' ---------------\n')
        game.write('| ', )
        for i in range(18, 21): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('| ', )
        for i in range(27, 30): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('|\n')
        game.write('| ', )
        for i in range(21, 24): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('| ', )
        for i in range(30, 33): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('|\n')
        game.write('| ', )
        for i in range(24, 27): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('| ', )
        for i in range(33, 36): game.write(str(self.board_state[i].wb) + ' ', )
        game.write('|\n')
        game.write(' ---------------\n')
        game.write('\n')