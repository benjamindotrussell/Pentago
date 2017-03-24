"""
	AI Assignment 2
	Author: Ben Russell
	Date:2/6/2017
"""
"""
	Class that represents a node.
	The node will be used to represent a location on the board.
	the node knows about the nodes that are adjacent to it
	and what color peg has been placed on it
"""


class Tile(object):

    def __init__(self, wb):
        self.wb = wb

    def switch(self, node):
        self.set_wb(node.wb)

    def set_wb(self, wb):
        self.wb = wb

    def get_wb(self):
        return self.wb

    def copy(self):
        node = Tile(self.wb)
        return node
