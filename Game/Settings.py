class GameSet:

    def __init__(self, root):
        self.engine_str = None
        self.mode = None
        self.pl_white = None
        self.pl_black = None
        self.white_turn = None
        self.root = root
        self.depth = 2

    def update(self):
        self.engine_str = self.root.engine_str.get()
        self.mode = self.root.mode.get()
        self.white_turn = True
        if self.mode == "PvP":
            self.pl_white = True
            self.pl_black = True
        elif self.mode == "EvE":
            self.pl_white = False
            self.pl_black = False
        elif self.mode == "PvE Pl.White":
            self.pl_white = True
            self.pl_black = False
        elif self.mode == "PvE Pl.Black":
            self.pl_white = False
            self.pl_black = True
