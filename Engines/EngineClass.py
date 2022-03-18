import abc


class Engine(abc.ABC):

    def __init__(self, name, board):
        self.name = name
        self.board = board
        self.reg = None

    @abc.abstractmethod
    def white_moves(self, board):
        pass
        # returns a list of lists, the first position on the sublist is the piece field,
        # the rest are possible moves for this piece

    @abc.abstractmethod
    def black_moves(self, board):
        pass
