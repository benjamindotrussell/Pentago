
class Player(object):

    def __init__(self, player, wb, order, name):
        self.player = player
        self.wb = wb
        self.order = order
        self.name = name
    def not_wb(self):
        if self.wb == 'w':
            return 'b'
        else: return 'w'

    def turn(self):
        if self.order == 1:
            self.order = 2
        else: self.order = 1