"""
	AI Assignment 2
	Author: Ben Russell
	Date:2/6/2017
"""
"""
	Main class
"""

import Board
import random
import Player
import Node
"""
	writes the winner to the console and file
	p1: player 1
	p2: player 2
	tie: boolean: true for tie false otherwise
	pentago: file name to write to
"""
def proclaim_winner(p1, p2, tie, pentago):
    if tie:
        print "It was a draw!"
        pentago.write('It was a draw!\n')
    if p1 is None:
        print "winner is " + p2.wb + "!"
        pentago.write("winner is " + p2.name + "!\n")
    elif p2 is None:
        print "winner is " + p1.name + "!"
        pentago.write("winner is " + p1.name + "!\n")
"""
	look for a win state
	board: the current game board
	p1: player 1
	p2: player 2
	pentago: the file name to write to
"""
def find_winner(board, p1, p2, pentago):
	#find a win state for player 1
    win1 = board.check_win(p1)
	#find a win state for player 2
    win2 = board.check_win(p2)
    if win1 and win2:
        proclaim_winner(p1, p2, True, pentago)
        return 2
    elif win1 and not win2:
        proclaim_winner(p1, None, False, pentago)
        return 2
    elif win2 and not win1:
        proclaim_winner(None, p2, False, pentago)
        return 2
    else:
        return 1
"""
	driver
"""
def main():
    filename = 'alpha-beta_pentago.txt'
    pentago = open(filename, 'w')
    pentago.truncate()
    print 'Enter 1 for min-max or 2 for min-max with alpha-beta pruning'
    algorithm = raw_input()
    print "Please enter your name in the console."
    name = raw_input()
    #choose player
    wb = ''
    while wb.lower() not in ['white', 'black']:
        print 'Choose white or black.'
        wb = raw_input()

    print "You chose " + wb + ". Great let's play!"
    #create a player 1
	p1 = Player.Player('p1', wb[0], 2, name)
    pentago.write('Player1 name is ' + p1.name + '\n')
	#player 2 is the AI and will be whatever color the human player did not choose
    if wb[0] == 'w': p2 = Player.Player('p2', 'b', 2, "AI")
    else: p2 = Player.Player('p2', 'w', 2, "AI")
    pentago.write('Player2 name is ' + p2.name + '\n')
    pentago.write('Player1 is ' + p1.wb + '\n')
    pentago.write('Player2 is ' + p2.wb + '\n')
	#create a new board
    board = Board.Board()
    board.generate_board()
    board.to_string(pentago)
	
    #choose who goes first and make the first move
    if random.random() < .5:
        print 'I will go first.'
        pentago.write('AI turn\n')
        p1.turn()
		#initial turn is not too important so it just used the alpha beta search
		#root is the current state
        root = Node.Node(board.copy_board(board.board_state), 0, None)
        #generate a tree
		v = board.abp_search(root, 1, -999, 999, p2, 0)
        #AI makes its selection
		for c in root.children:
            if c.value == v:
                board.board_state = c.board_state
                break
        board.to_string(pentago)
    else:
        print "You can go first. \n Please enter your move on the command line."
        pentago.write(p1.name + ' turn\n')
        #human make a move
		move = raw_input()
        while str(move[5].lower()) != 'r' and str(move[5].lower()) != 'l':
            print 'please enter move in the format of b/t br  where b is the block t is the tile and r is the rotation r for right and l for left'
            move = raw_input()
        #set the peg on the board
		board.set_position(p1, move)
        #rotate the board
		board.board_state = board.rotate(move, board.board_state)
        board.to_string(pentago)

    win = 1
	#until a win state is found
    while win == 1:
		#if its the human players turn
        if p1.order == 1:
            print 'Your move!'
            pentago.write(p1.name + ' turn\n')
            #changes the players turn
			p1.turn()
            move = raw_input()
            while move[5].lower() != 'r' and move[5].lower() != 'l':
                print 'please enter move in the format of b/t br  where b is the block t is the tile and r is the rotation r for right and l for left'
                move = raw_input()
			#set the peg on the board
            pos = board.set_position(p1, move)
            while pos is None:
                print 'That tile is taken! Please make a different selection.'
                move = raw_input()
                while move[5].lower() != 'r' and move[5].lower() != 'l':
                    print 'please enter move in the format of b/t br  where b is the block t is the tile and r is the rotation r for right and l for left'
                    move = raw_input()
                print move[5]
                pos = board.set_position(p1, move)
			#look for winning state
            if find_winner(board, p1, p2, pentago) == 2:
                board.to_string(pentago)
                break
			#rotate the board
            board.board_state = board.rotate(move, board.board_state)
			#look for winning state
            if find_winner(board, p1, p2, pentago) == 2:
                board.to_string(pentago)
                break
        else:
            print 'My turn!'
            pentago.write(p2.name + ' turn\n')
            #changes the players turn
			p1.turn()
			#min-max algorithm
            if algorithm == '1':
                board.board_state = board.ai_move(p2)
			#min-max with alpha-beta pruning
            else:
				#root is current board state
                root = Node.Node(board.copy_board(board.board_state), 0, None)
				#generate the tree
                v = board.abp_search(root, 2, -999, 999, p2, 0)
				#AI makes a selection
                for c in root.children:
                    if c.value == v:
                        board.board_state = c.board_state
                        break
			#look for winning state
            if find_winner(board, p1, p2, pentago) == 2:
                board.to_string(pentago)
                break
        board.to_string(pentago)
    pentago.close()


if __name__ == '__main__':
    main()
