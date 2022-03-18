class GameRegister:

    def __init__(self, root):
        self.root = root
        self.game_fen = None
        self.white_turn = None
        self.white_castle_king = True
        self.white_castle_queen = True
        self.black_castle_king = True
        self.black_castle_queen = True
        self.en_passant = ""
        self.enp_temp = ""
        self.half_moves = 0
        self.full_moves = 0
        self.game = []
        self.current_moves = None
        self.move_made = True
        self.move = None
        self.last_capture = None
        self.current_promotion = None
        self.game_over = False
        self.engine_working = False
        self.last_game = None

    def reset(self):
        self.last_game = self.game
        self.game = []
        self.game_fen = self.root.starting_pos
        self._set_from_fen(self.root.starting_pos)
        self.current_moves = None
        self.move_made = True
        if int(self.half_moves) or int(self.full_moves):
            self.game.append("Starting_Pos:" + self.root.starting_pos)

    def print_reg(self):
        print("Game FEN: ", self.game_fen)
        print("White Turn: ", self.white_turn)
        print("White castle: ", self.white_castle_king, self.white_castle_queen)
        print("Black castle: ", self.black_castle_king, self.black_castle_queen)
        print("En Passant: ", self.en_passant)
        print("Half moves: ", self.half_moves)
        print("Full moves: ", self.full_moves)
        print(self.game)

    def _set_from_fen(self, fen):
        split = fen.split()

        # 2  - turn
        if split[1] == "w":
            self.white_turn = True
        else:
            self.white_turn = False

        # 3 - castles
        if split[2] == "-" or split[2] == "--":
            self.white_castle_queen = False
            self.black_castle_queen = False
            self.black_castle_king = False
            self.white_castle_king = False
        else:
            self.white_castle_queen = False
            self.black_castle_queen = False
            self.black_castle_king = False
            self.white_castle_king = False
            for char in split[2]:
                if char == "K":
                    self.white_castle_king = True
                elif char == "Q":
                    self.white_castle_queen = True
                elif char == "k":
                    self.black_castle_king = True
                elif char == "q":
                    self.black_castle_queen = True

        # 4 - en_passant
        if split[3] != "-":
            self.en_passant = split[3]
        else:
            self.en_passant = ""

        # half/full moves
        self.half_moves = int(split[4])
        self.full_moves = int(split[5])
