class Node(object):

    def __init__(self, b, depth, parent):
        self.board_state = b
        if parent is not None:
            if parent.ab == 'min':
                self.ab = 'max'
            else: self.ab = 'min'
        else: self.ab = 'max'
        self.parent = parent
        self.depth = depth
        self.is_leaf = True
        self.children = []
        self.value = None