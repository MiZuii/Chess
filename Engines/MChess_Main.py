from .EngineClass import *
from Game.Functions import int_enp, rev
from numpy import zeros, int8
from random import choice
from bitstring import Bits


class MChessEngine(Engine):

    def __init__(self, name, board):
        super(MChessEngine, self).__init__(name, board)
        self.w_threat_map = zeros((8, 8),   dtype=int8)
        self.b_threat_map = zeros((8, 8),   dtype=int8)
        # en passant is not in threat map !!!!!

    def white_moves(self, board):
        final_moves = []
        for piece in self.possible_moves(board):
            if 1 <= board[piece[0]//10][piece[0] % 10] <= 6:
                final_moves.append(piece)
        self.possible_moves_white(board)
        return final_moves

    def black_moves(self, board):
        final_moves = []
        for piece in self.possible_moves(board):
            if 7 <= board[piece[0]//10][piece[0] % 10] <= 12:
                final_moves.append(piece)
        self.possible_moves_black(board)
        return final_moves

    def random_move(self, board, white, root):

        if white:
            possible_moves = self.white_moves(board)
            promotion_set = (2, 3, 4, 5)
        else:
            possible_moves = self.black_moves(board)
            promotion_set = (8, 9, 10, 11)

        while len(possible_moves) > 0:
            sett = choice(possible_moves)
            if len(sett) < 2:
                possible_moves.remove(sett)
            else:
                temp = sett.pop(0)
                move = choice(sett)
                if move % 10 == 9:
                    root.reg.current_promotion = choice(promotion_set)
                return [temp, move]
        return 0

    def possible_moves(self, board):

        board_temp = board.copy()
        self.w_threat_map = zeros((8, 8), dtype=int8)
        self.b_threat_map = zeros((8, 8), dtype=int8)

        white = self.possible_moves_white(board)
        black = self.possible_moves_black(board)
        kings = self.kings_moves(board)

        legal_moves = []
        temp_moves = []
        for piece in white:
            figure = piece.pop(0)
            temp_moves.append(figure)
            for move in piece:
                # change move on temp board
                piece_index = board[figure // 10][figure % 10]
                if move % 10 == 9:
                    move //= 10
                    board_temp[figure // 10][figure % 10] = 0
                    board_temp[move // 10][move % 10] = piece_index
                    move = move * 10 + 9
                elif self.reg.en_passant != "":
                    if move == int_enp(self.reg.en_passant)[0] * 10 + int_enp(self.reg.en_passant)[1]\
                            and piece_index == 1:
                        board_temp[figure // 10][figure % 10] = 0
                        board_temp[move // 10][move % 10] = piece_index
                        pawn_cords = move + 10
                        board_temp[pawn_cords // 10][pawn_cords % 10] = 0
                    else:
                        board_temp[figure // 10][figure % 10] = 0
                        board_temp[move // 10][move % 10] = piece_index
                else:
                    board_temp[figure // 10][figure % 10] = 0
                    board_temp[move // 10][move % 10] = piece_index
                # call possible moves black for update on threat map
                self.b_threat_map = zeros((8, 8), dtype=int8)
                self.possible_moves_black(board_temp)
                # call w_incheck to check if the move is legal
                if self.w_incheck(board_temp):
                    pass
                    # this move is illegal
                else:
                    temp_moves.append(move)
                    # this move is legal
                    # add to legal moves list
                # change temp_board back to board
                board_temp = board.copy()
            legal_moves.append(temp_moves)
            temp_moves = []

        for piece in black:
            figure = piece.pop(0)
            temp_moves.append(figure)
            for move in piece:
                piece_index = board[figure // 10][figure % 10]
                if move % 10 == 9:
                    move //= 10
                    board_temp[figure // 10][figure % 10] = 0
                    board_temp[move // 10][move % 10] = piece_index
                    move = move * 10 + 9
                elif self.reg.en_passant != "":
                    if move == int_enp(self.reg.en_passant)[0] * 10 + int_enp(self.reg.en_passant)[1]\
                            and piece_index == 7:
                        board_temp[figure // 10][figure % 10] = 0
                        board_temp[move // 10][move % 10] = piece_index
                        pawn_cords = move - 10
                        board_temp[pawn_cords // 10][pawn_cords % 10] = 0
                    else:
                        board_temp[figure // 10][figure % 10] = 0
                        board_temp[move // 10][move % 10] = piece_index
                else:
                    board_temp[figure // 10][figure % 10] = 0
                    board_temp[move // 10][move % 10] = piece_index
                self.w_threat_map = zeros((8, 8), dtype=int8)
                self.possible_moves_white(board_temp)
                if self.b_incheck(board_temp):
                    pass
                else:
                    temp_moves.append(move)
                board_temp = board.copy()
            legal_moves.append(temp_moves)
            temp_moves = []

        for piece in kings:
            figure = piece.pop(0)
            temp_moves.append(figure)
            for move in piece:
                if move % 10 == 8:
                    pass
                    # check if this is needed !!!! --------------------------------------------
                    # the move is a castle
                    # if move == 76:
                    #     board_temp[7][6] = 6
                    #     board_temp[7][5] = 2
                    #     board_temp[7][7] = 0
                    # elif move == 72:
                    #     board_temp[7][2] = 6
                    #     board_temp[7][3] = 2
                    #     board_temp[7][0] = 0
                    # elif move == 6:
                    #     board_temp[0][6] = 6
                    #     board_temp[0][5] = 2
                    #     board_temp[0][7] = 0
                    # elif move == 2:
                    #     board_temp[0][2] = 6
                    #     board_temp[0][3] = 2
                    #     board_temp[0][0] = 0
                else:
                    # the move isn't a castle
                    piece_index = board[figure // 10][figure % 10]
                    board_temp[figure // 10][figure % 10] = 0
                    board_temp[move // 10][move % 10] = piece_index
                self.w_threat_map = zeros((8, 8), dtype=int8)
                self.b_threat_map = zeros((8, 8), dtype=int8)
                self.possible_moves_white(board_temp)
                self.possible_moves_black(board_temp)
                if self.b_incheck(board_temp) or self.w_incheck(board_temp):
                    pass
                else:
                    temp_moves.append(move)
                board_temp = board.copy()
            legal_moves.append(temp_moves)
            temp_moves = []

        return legal_moves

    def possible_moves_white(self, board):
        self.w_threat_map = zeros((8, 8), dtype=int8)
        self.b_threat_map = zeros((8, 8), dtype=int8)
        moves = []
        enp = None
        if self.reg.en_passant != "":
            enp = int_enp(self.reg.en_passant)
        for i in range(8):
            for j in range(8):
                sq = board[i][j]
                if sq != 0:
                    if sq == 1:
                        temp = [i*10 + j]
                        if i != 0:
                            if board[i - 1][j] == 0:
                                if i != 1:
                                    temp.append((i-1)*10 + j)
                                else:
                                    temp.append((i-1)*100 + j * 10 + 9)
                            if j != 0:
                                self.w_threat_map[i-1][j-1] += 1
                                if 7 <= board[i - 1][j - 1] <= 11:
                                    if i != 1:
                                        temp.append((i-1)*10 + (j-1))
                                    else:
                                        temp.append((i-1)*100 + (j-1) * 10 + 9)
                            if j != 7:
                                self.w_threat_map[i-1][j+1] += 1
                                if 7 <= board[i - 1][j + 1] <= 11:
                                    if i != 1:
                                        temp.append((i - 1) * 10 + (j + 1))
                                    else:
                                        temp.append((i - 1) * 100 + (j + 1) * 10 + 9)
                            if enp is not None and j != 0 and enp[0] == (i - 1) and enp[1] == (j - 1):
                                temp.append((i-1)*10 + (j-1))
                            if enp is not None and j != 7 and enp[0] == (i - 1) and enp[1] == (j + 1):
                                temp.append((i-1)*10 + (j+1))
                            if i == 6:
                                for start in [60, 61, 62, 63, 64, 65, 66, 67]:
                                    if i*10 + j == start:
                                        if board[i - 1][j] == 0 and board[i - 2][j] == 0:
                                            temp.append((i-2)*10 + j)
                        moves.append(temp)
                    elif sq == 2:
                        temp = [i*10 + j]
                        cont_up = cont_down = cont_left = cont_right = True
                        for shift in range(1, 8):
                            if i + shift <= 7 and cont_down:

                                if 1 <= board[i + shift][j] <= 6:
                                    cont_down = False
                                    self.w_threat_map[i+shift][j] += 1
                                elif 7 <= board[i + shift][j] <= 12:
                                    cont_down = False
                                    temp.append((i+shift)*10 + j)
                                    self.w_threat_map[i+shift][j] += 1
                                else:
                                    temp.append((i+shift)*10 + j)
                                    self.w_threat_map[i+shift][j] += 1

                            if i - shift >= 0 and cont_up:

                                if 1 <= board[i - shift][j] <= 6:
                                    cont_up = False
                                    self.w_threat_map[i - shift][j] += 1
                                elif 7 <= board[i - shift][j] <= 12:
                                    cont_up = False
                                    temp.append((i - shift) * 10 + j)
                                    self.w_threat_map[i - shift][j] += 1
                                else:
                                    temp.append((i - shift) * 10 + j)
                                    self.w_threat_map[i - shift][j] += 1

                            if j + shift <= 7 and cont_right:

                                if 1 <= board[i][j + shift] <= 6:
                                    cont_right = False
                                    self.w_threat_map[i][j + shift] += 1
                                elif 7 <= board[i][j + shift] <= 12:
                                    cont_right = False
                                    temp.append(i*10 + j+shift)
                                    self.w_threat_map[i][j + shift] += 1
                                else:
                                    temp.append(i*10 + j+shift)
                                    self.w_threat_map[i][j + shift] += 1

                            if j - shift >= 0 and cont_left:

                                if 1 <= board[i][j - shift] <= 6:
                                    cont_left = False
                                    self.w_threat_map[i][j - shift] += 1
                                elif 7 <= board[i][j - shift] <= 12:
                                    cont_left = False
                                    temp.append(i*10 + j-shift)
                                    self.w_threat_map[i][j - shift] += 1
                                else:
                                    temp.append(i*10 + j-shift)
                                    self.w_threat_map[i][j - shift] += 1

                        moves.append(temp)
                    elif sq == 3:
                        temp = [i*10 + j]
                        if i-2 >= 0 and j+1 <= 7:
                            self.w_threat_map[i-2][j+1] += 1
                            if board[i-2][j+1] == 0 or 7 <= board[i-2][j+1] <= 12:
                                temp.append((i-2)*10 + j+1)
                        if i-2 >= 0 and j-1 >= 0:
                            self.w_threat_map[i-2][j-1] += 1
                            if board[i-2][j-1] == 0 or 7 <= board[i-2][j-1] <= 12:
                                temp.append((i-2)*10 + j-1)
                        if i+2 <= 7 and j+1 <= 7:
                            self.w_threat_map[i+2][j+1] += 1
                            if board[i+2][j+1] == 0 or 7 <= board[i+2][j+1] <= 12:
                                temp.append((i+2)*10 + j+1)
                        if i+2 <= 7 and j-1 >= 0:
                            self.w_threat_map[i+2][j-1] += 1
                            if board[i+2][j-1] == 0 or 7 <= board[i+2][j-1] <= 12:
                                temp.append((i+2)*10 + j-1)
                        if i-1 >= 0 and j+2 <= 7:
                            self.w_threat_map[i-1][j+2] += 1
                            if board[i-1][j+2] == 0 or 7 <= board[i-1][j+2] <= 12:
                                temp.append((i-1)*10 + j+2)
                        if i-1 >= 0 and j-2 >= 0:
                            self.w_threat_map[i-1][j-2] += 1
                            if board[i-1][j-2] == 0 or 7 <= board[i-1][j-2] <= 12:
                                temp.append((i-1)*10 + j-2)
                        if i+1 <= 7 and j+2 <= 7:
                            self.w_threat_map[i+1][j+2] += 1
                            if board[i+1][j+2] == 0 or 7 <= board[i+1][j+2] <= 12:
                                temp.append((i+1)*10 + j+2)
                        if i+1 <= 7 and j-2 >= 0:
                            self.w_threat_map[i+1][j-2] += 1
                            if board[i+1][j-2] == 0 or 7 <= board[i+1][j-2] <= 12:
                                temp.append((i+1)*10 + j-2)
                        moves.append(temp)
                    elif sq == 4:
                        temp = [10*i + j]
                        cont_up = cont_down = cont_left = cont_right = True
                        for shift in range(1, 8):
                            if i + shift <= 7 and cont_down and j + shift <= 7:

                                if 1 <= board[i + shift][j + shift] <= 6:
                                    cont_down = False
                                    self.w_threat_map[i + shift][j + shift] += 1
                                elif 7 <= board[i + shift][j + shift] <= 12:
                                    cont_down = False
                                    temp.append((i+shift)*10 + (j+shift))
                                    self.w_threat_map[i + shift][j + shift] += 1
                                else:
                                    temp.append((i+shift)*10 + (j+shift))
                                    self.w_threat_map[i + shift][j + shift] += 1

                            if i - shift >= 0 and cont_up and j - shift >= 0:

                                if 1 <= board[i - shift][j - shift] <= 6:
                                    cont_up = False
                                    self.w_threat_map[i - shift][j - shift] += 1
                                elif 7 <= board[i - shift][j - shift] <= 12:
                                    cont_up = False
                                    temp.append((i - shift) * 10 + (j-shift))
                                    self.w_threat_map[i - shift][j - shift] += 1
                                else:
                                    temp.append((i - shift) * 10 + (j-shift))
                                    self.w_threat_map[i - shift][j - shift] += 1

                            if j + shift <= 7 and cont_right and i - shift >= 0:

                                if 1 <= board[i - shift][j + shift] <= 6:
                                    cont_right = False
                                    self.w_threat_map[i - shift][j + shift] += 1
                                elif 7 <= board[i - shift][j + shift] <= 12:
                                    cont_right = False
                                    temp.append((i-shift)*10 + j+shift)
                                    self.w_threat_map[i - shift][j + shift] += 1
                                else:
                                    temp.append((i-shift)*10 + j+shift)
                                    self.w_threat_map[i - shift][j + shift] += 1

                            if j - shift >= 0 and cont_left and i + shift <= 7:

                                if 1 <= board[i + shift][j - shift] <= 6:
                                    cont_left = False
                                    self.w_threat_map[i + shift][j - shift] += 1
                                elif 7 <= board[i + shift][j - shift] <= 12:
                                    cont_left = False
                                    temp.append((i + shift)*10 + j-shift)
                                    self.w_threat_map[i + shift][j - shift] += 1
                                else:
                                    temp.append((i + shift)*10 + j-shift)
                                    self.w_threat_map[i + shift][j - shift] += 1

                        moves.append(temp)
                    elif sq == 5:
                        temp = [i * 10 + j]
                        cont_up = cont_down = cont_left = cont_right = True
                        cont_ne = cont_es = cont_sw = cont_wn = True
                        for shift in range(1, 8):
                            if i + shift <= 7 and cont_down:

                                if 1 <= board[i + shift][j] <= 6:
                                    cont_down = False
                                    self.w_threat_map[i + shift][j] += 1
                                elif 7 <= board[i + shift][j] <= 12:
                                    cont_down = False
                                    temp.append((i + shift) * 10 + j)
                                    self.w_threat_map[i + shift][j] += 1
                                else:
                                    temp.append((i + shift) * 10 + j)
                                    self.w_threat_map[i + shift][j] += 1

                            if i - shift >= 0 and cont_up:

                                if 1 <= board[i - shift][j] <= 6:
                                    cont_up = False
                                    self.w_threat_map[i - shift][j] += 1
                                elif 7 <= board[i - shift][j] <= 12:
                                    cont_up = False
                                    temp.append((i - shift) * 10 + j)
                                    self.w_threat_map[i - shift][j] += 1
                                else:
                                    temp.append((i - shift) * 10 + j)
                                    self.w_threat_map[i - shift][j] += 1

                            if j + shift <= 7 and cont_right:

                                if 1 <= board[i][j + shift] <= 6:
                                    cont_right = False
                                    self.w_threat_map[i][j + shift] += 1
                                elif 7 <= board[i][j + shift] <= 12:
                                    cont_right = False
                                    temp.append(i * 10 + j + shift)
                                    self.w_threat_map[i][j + shift] += 1
                                else:
                                    temp.append(i * 10 + j + shift)
                                    self.w_threat_map[i][j + shift] += 1

                            if j - shift >= 0 and cont_left:

                                if 1 <= board[i][j - shift] <= 6:
                                    cont_left = False
                                    self.w_threat_map[i][j - shift] += 1
                                elif 7 <= board[i][j - shift] <= 12:
                                    cont_left = False
                                    temp.append(i * 10 + j - shift)
                                    self.w_threat_map[i][j - shift] += 1
                                else:
                                    temp.append(i * 10 + j - shift)
                                    self.w_threat_map[i][j - shift] += 1

                            if i + shift <= 7 and cont_es and j + shift <= 7:

                                if 1 <= board[i + shift][j + shift] <= 6:
                                    cont_es = False
                                    self.w_threat_map[i + shift][j + shift] += 1
                                elif 7 <= board[i + shift][j + shift] <= 12:
                                    cont_es = False
                                    temp.append((i+shift)*10 + (j+shift))
                                    self.w_threat_map[i + shift][j + shift] += 1
                                else:
                                    temp.append((i+shift)*10 + (j+shift))
                                    self.w_threat_map[i + shift][j + shift] += 1

                            if i - shift >= 0 and cont_wn and j - shift >= 0:

                                if 1 <= board[i - shift][j - shift] <= 6:
                                    cont_wn = False
                                    self.w_threat_map[i - shift][j - shift] += 1
                                elif 7 <= board[i - shift][j - shift] <= 12:
                                    cont_wn = False
                                    temp.append((i - shift) * 10 + (j-shift))
                                    self.w_threat_map[i - shift][j - shift] += 1
                                else:
                                    temp.append((i - shift) * 10 + (j-shift))
                                    self.w_threat_map[i - shift][j - shift] += 1

                            if j + shift <= 7 and cont_ne and i - shift >= 0:

                                if 1 <= board[i - shift][j + shift] <= 6:
                                    cont_ne = False
                                    self.w_threat_map[i - shift][j + shift] += 1
                                elif 7 <= board[i - shift][j + shift] <= 12:
                                    cont_ne = False
                                    temp.append((i-shift)*10 + j+shift)
                                    self.w_threat_map[i - shift][j + shift] += 1
                                else:
                                    temp.append((i-shift)*10 + j+shift)
                                    self.w_threat_map[i - shift][j + shift] += 1

                            if j - shift >= 0 and cont_sw and i + shift <= 7:

                                if 1 <= board[i + shift][j - shift] <= 6:
                                    cont_sw = False
                                    self.w_threat_map[i + shift][j - shift] += 1
                                elif 7 <= board[i + shift][j - shift] <= 12:
                                    cont_sw = False
                                    temp.append((i + shift)*10 + j-shift)
                                    self.w_threat_map[i + shift][j - shift] += 1
                                else:
                                    temp.append((i + shift)*10 + j-shift)
                                    self.w_threat_map[i + shift][j - shift] += 1

                        moves.append(temp)
                    elif sq == 6:
                        if 0 <= i-1 <= 7:
                            # i-1, j
                            self.w_threat_map[i - 1][j] += 1
                        if 0 <= i-1 <= 7 and 0 <= j-1 <= 7:
                            # i-1, j-1
                            self.w_threat_map[i - 1][j - 1] += 1
                        if 0 <= j-1 <= 7:
                            # i, j-1
                            self.w_threat_map[i][j - 1] += 1
                        if 0 <= i + 1 <= 7 and 0 <= j - 1 <= 7:
                            self.w_threat_map[i + 1][j - 1] += 1
                            # i+1, j-1
                        if 0 <= i + 1 <= 7:
                            # i+1, j
                            self.w_threat_map[i + 1][j] += 1
                        if 0 <= i + 1 <= 7 and 0 <= j + 1 <= 7:
                            # i+1, j+1
                            self.w_threat_map[i + 1][j + 1] += 1
                        if 0 <= j + 1 <= 7:
                            # i, j+1
                            self.w_threat_map[i][j + 1] += 1
                        if 0 <= i - 1 <= 7 and 0 <= j + 1 <= 7:
                            # i-1, j+1
                            self.w_threat_map[i - 1][j + 1] += 1
        return moves

    def possible_moves_black(self, board):
        moves = []
        enp = None
        if self.reg.en_passant != "":
            enp = int_enp(self.reg.en_passant)
        for i in range(8):
            for j in range(8):
                sq = board[i][j]
                if sq != 0:
                    if sq == 7:
                        # black pawn
                        temp = [i*10 + j]
                        if i != 7:
                            if board[i + 1][j] == 0:
                                if i != 6:
                                    temp.append((i + 1) * 10 + j)
                                else:
                                    temp.append((i + 1) * 100 + j * 10 + 9)
                            if j != 0:
                                self.b_threat_map[i + 1][j - 1] += 1
                                if 1 <= board[i + 1][j - 1] <= 6:
                                    if i != 6:
                                        temp.append((i+1)*10 + (j-1))
                                    else:
                                        temp.append((i+1)*100 + (j-1) * 10 + 9)
                            if j != 7:
                                self.b_threat_map[i + 1][j + 1] += 1
                                if 1 <= board[i + 1][j + 1] <= 6:
                                    if i != 6:
                                        temp.append((i+1)*10 + (j+1))
                                    else:
                                        temp.append((i+1)*100 + (j+1) * 10 + 9)
                            if enp is not None and j != 0 and enp[0] == (i + 1) and enp[1] == (j - 1):
                                temp.append((i+1)*10 + (j-1))
                            if enp is not None and j != 7 and enp[0] == (i + 1) and enp[1] == (j + 1):
                                temp.append((i+1)*10 + (j+1))
                            if i == 1:
                                for start in [10, 11, 12, 13, 14, 15, 16, 17]:
                                    if i * 10 + j == start:
                                        if board[i + 1][j] == 0 and board[i + 2][j] == 0:
                                            temp.append((i + 2) * 10 + j)
                        moves.append(temp)
                    elif sq == 8:
                        temp = [i*10 + j]
                        cont_up = cont_down = cont_left = cont_right = True
                        for shift in range(1, 8):
                            if i + shift <= 7 and cont_down:

                                if 7 <= board[i + shift][j] <= 12:
                                    cont_down = False
                                    self.b_threat_map[i + shift][j] += 1
                                elif 1 <= board[i + shift][j] <= 6:
                                    cont_down = False
                                    temp.append((i + shift) * 10 + j)
                                    self.b_threat_map[i + shift][j] += 1
                                else:
                                    temp.append((i + shift) * 10 + j)
                                    self.b_threat_map[i + shift][j] += 1

                            if i - shift >= 0 and cont_up:

                                if 7 <= board[i - shift][j] <= 12:
                                    cont_up = False
                                    self.b_threat_map[i - shift][j] += 1
                                elif 1 <= board[i - shift][j] <= 6:
                                    cont_up = False
                                    temp.append((i - shift) * 10 + j)
                                    self.b_threat_map[i - shift][j] += 1
                                else:
                                    temp.append((i - shift) * 10 + j)
                                    self.b_threat_map[i - shift][j] += 1

                            if j + shift <= 7 and cont_right:

                                if 7 <= board[i][j + shift] <= 12:
                                    cont_right = False
                                    self.b_threat_map[i][j + shift] += 1
                                elif 1 <= board[i][j + shift] <= 6:
                                    cont_right = False
                                    temp.append(i * 10 + j + shift)
                                    self.b_threat_map[i][j + shift] += 1
                                else:
                                    temp.append(i * 10 + j + shift)
                                    self.b_threat_map[i][j + shift] += 1

                            if j - shift >= 0 and cont_left:

                                if 7 <= board[i][j - shift] <= 12:
                                    cont_left = False
                                    self.b_threat_map[i][j - shift] += 1
                                elif 1 <= board[i][j - shift] <= 6:
                                    cont_left = False
                                    temp.append(i * 10 + j - shift)
                                    self.b_threat_map[i][j - shift] += 1
                                else:
                                    temp.append(i * 10 + j - shift)
                                    self.b_threat_map[i][j - shift] += 1

                        moves.append(temp)
                    elif sq == 9:
                        temp = [i * 10 + j]
                        if i - 2 >= 0 and j + 1 <= 7:
                            self.b_threat_map[i - 2][j + 1] += 1
                            if board[i - 2][j + 1] == 0 or 1 <= board[i - 2][j + 1] <= 6:
                                temp.append((i - 2) * 10 + j + 1)
                        if i - 2 >= 0 and j - 1 >= 0:
                            self.b_threat_map[i - 2][j - 1] += 1
                            if board[i - 2][j - 1] == 0 or 1 <= board[i - 2][j - 1] <= 6:
                                temp.append((i - 2) * 10 + j - 1)
                        if i + 2 <= 7 and j + 1 <= 7:
                            self.b_threat_map[i + 2][j + 1] += 1
                            if board[i + 2][j + 1] == 0 or 1 <= board[i + 2][j + 1] <= 6:
                                temp.append((i + 2) * 10 + j + 1)
                        if i + 2 <= 7 and j - 1 >= 0:
                            self.b_threat_map[i + 2][j - 1] += 1
                            if board[i + 2][j - 1] == 0 or 1 <= board[i + 2][j - 1] <= 6:
                                temp.append((i + 2) * 10 + j - 1)
                        if i - 1 >= 0 and j + 2 <= 7:
                            self.b_threat_map[i - 1][j + 2] += 1
                            if board[i - 1][j + 2] == 0 or 1 <= board[i - 1][j + 2] <= 6:
                                temp.append((i - 1) * 10 + j + 2)
                        if i - 1 >= 0 and j - 2 >= 0:
                            self.b_threat_map[i - 1][j - 2] += 1
                            if board[i - 1][j - 2] == 0 or 1 <= board[i - 1][j - 2] <= 6:
                                temp.append((i - 1) * 10 + j - 2)
                        if i + 1 <= 7 and j + 2 <= 7:
                            self.b_threat_map[i + 1][j + 2] += 1
                            if board[i + 1][j + 2] == 0 or 1 <= board[i + 1][j + 2] <= 6:
                                temp.append((i + 1) * 10 + j + 2)
                        if i + 1 <= 7 and j - 2 >= 0:
                            self.b_threat_map[i + 1][j - 2] += 1
                            if board[i + 1][j - 2] == 0 or 1 <= board[i + 1][j - 2] <= 6:
                                temp.append((i + 1) * 10 + j - 2)
                        moves.append(temp)
                    elif sq == 10:
                        temp = [10 * i + j]
                        cont_up = cont_down = cont_left = cont_right = True
                        for shift in range(1, 8):
                            if i + shift <= 7 and cont_down and j + shift <= 7:

                                if 7 <= board[i + shift][j + shift] <= 12:
                                    cont_down = False
                                    self.b_threat_map[i + shift][j + shift] += 1
                                elif 1 <= board[i + shift][j + shift] <= 6:
                                    cont_down = False
                                    temp.append((i + shift) * 10 + (j + shift))
                                    self.b_threat_map[i + shift][j + shift] += 1
                                else:
                                    temp.append((i + shift) * 10 + (j + shift))
                                    self.b_threat_map[i + shift][j + shift] += 1

                            if i - shift >= 0 and cont_up and j - shift >= 0:

                                if 7 <= board[i - shift][j - shift] <= 12:
                                    cont_up = False
                                    self.b_threat_map[i - shift][j - shift] += 1
                                elif 1 <= board[i - shift][j - shift] <= 6:
                                    cont_up = False
                                    temp.append((i - shift) * 10 + (j - shift))
                                    self.b_threat_map[i - shift][j - shift] += 1
                                else:
                                    temp.append((i - shift) * 10 + (j - shift))
                                    self.b_threat_map[i - shift][j - shift] += 1

                            if j + shift <= 7 and cont_right and i - shift >= 0:

                                if 7 <= board[i - shift][j + shift] <= 12:
                                    cont_right = False
                                    self.b_threat_map[i - shift][j + shift] += 1
                                elif 1 <= board[i - shift][j + shift] <= 6:
                                    cont_right = False
                                    temp.append((i - shift) * 10 + j + shift)
                                    self.b_threat_map[i - shift][j + shift] += 1
                                else:
                                    temp.append((i - shift) * 10 + j + shift)
                                    self.b_threat_map[i - shift][j + shift] += 1

                            if j - shift >= 0 and cont_left and i + shift <= 7:

                                if 7 <= board[i + shift][j - shift] <= 12:
                                    cont_left = False
                                    self.b_threat_map[i + shift][j - shift] += 1
                                elif 1 <= board[i + shift][j - shift] <= 6:
                                    cont_left = False
                                    temp.append((i + shift) * 10 + j - shift)
                                    self.b_threat_map[i + shift][j - shift] += 1
                                else:
                                    temp.append((i + shift) * 10 + j - shift)
                                    self.b_threat_map[i + shift][j - shift] += 1

                        moves.append(temp)
                    elif sq == 11:
                        temp = [i * 10 + j]
                        cont_up = cont_down = cont_left = cont_right = True
                        cont_ne = cont_es = cont_sw = cont_wn = True
                        for shift in range(1, 8):
                            if i + shift <= 7 and cont_down:

                                if 7 <= board[i + shift][j] <= 12:
                                    cont_down = False
                                    self.b_threat_map[i + shift][j] += 1
                                elif 1 <= board[i + shift][j] <= 6:
                                    cont_down = False
                                    temp.append((i + shift) * 10 + j)
                                    self.b_threat_map[i + shift][j] += 1
                                else:
                                    temp.append((i + shift) * 10 + j)
                                    self.b_threat_map[i + shift][j] += 1

                            if i - shift >= 0 and cont_up:

                                if 7 <= board[i - shift][j] <= 12:
                                    cont_up = False
                                    self.b_threat_map[i - shift][j] += 1
                                elif 1 <= board[i - shift][j] <= 6:
                                    cont_up = False
                                    temp.append((i - shift) * 10 + j)
                                    self.b_threat_map[i - shift][j] += 1
                                else:
                                    temp.append((i - shift) * 10 + j)
                                    self.b_threat_map[i - shift][j] += 1

                            if j + shift <= 7 and cont_right:

                                if 7 <= board[i][j + shift] <= 12:
                                    cont_right = False
                                    self.b_threat_map[i][j + shift] += 1
                                elif 1 <= board[i][j + shift] <= 6:
                                    cont_right = False
                                    temp.append(i * 10 + j + shift)
                                    self.b_threat_map[i][j + shift] += 1
                                else:
                                    temp.append(i * 10 + j + shift)
                                    self.b_threat_map[i][j + shift] += 1

                            if j - shift >= 0 and cont_left:

                                if 7 <= board[i][j - shift] <= 12:
                                    cont_left = False
                                    self.b_threat_map[i][j - shift] += 1
                                elif 1 <= board[i][j - shift] <= 6:
                                    cont_left = False
                                    temp.append(i * 10 + j - shift)
                                    self.b_threat_map[i][j - shift] += 1
                                else:
                                    temp.append(i * 10 + j - shift)
                                    self.b_threat_map[i][j - shift] += 1

                            if i + shift <= 7 and cont_es and j + shift <= 7:

                                if 7 <= board[i + shift][j + shift] <= 12:
                                    cont_es = False
                                    self.b_threat_map[i + shift][j + shift] += 1
                                elif 1 <= board[i + shift][j + shift] <= 6:
                                    cont_es = False
                                    temp.append((i + shift) * 10 + (j + shift))
                                    self.b_threat_map[i + shift][j + shift] += 1
                                else:
                                    temp.append((i + shift) * 10 + (j + shift))
                                    self.b_threat_map[i + shift][j + shift] += 1

                            if i - shift >= 0 and cont_wn and j - shift >= 0:

                                if 7 <= board[i - shift][j - shift] <= 12:
                                    cont_wn = False
                                    self.b_threat_map[i - shift][j - shift] += 1
                                elif 1 <= board[i - shift][j - shift] <= 6:
                                    cont_wn = False
                                    temp.append((i - shift) * 10 + (j - shift))
                                    self.b_threat_map[i - shift][j - shift] += 1
                                else:
                                    temp.append((i - shift) * 10 + (j - shift))
                                    self.b_threat_map[i - shift][j - shift] += 1

                            if j + shift <= 7 and cont_ne and i - shift >= 0:

                                if 7 <= board[i - shift][j + shift] <= 12:
                                    cont_ne = False
                                    self.b_threat_map[i - shift][j + shift] += 1
                                elif 1 <= board[i - shift][j + shift] <= 6:
                                    cont_ne = False
                                    temp.append((i - shift) * 10 + j + shift)
                                    self.b_threat_map[i - shift][j + shift] += 1
                                else:
                                    temp.append((i - shift) * 10 + j + shift)
                                    self.b_threat_map[i - shift][j + shift] += 1

                            if j - shift >= 0 and cont_sw and i + shift <= 7:

                                if 7 <= board[i + shift][j - shift] <= 12:
                                    cont_sw = False
                                    self.b_threat_map[i + shift][j - shift] += 1
                                elif 1 <= board[i + shift][j - shift] <= 6:
                                    cont_sw = False
                                    temp.append((i + shift) * 10 + j - shift)
                                    self.b_threat_map[i + shift][j - shift] += 1
                                else:
                                    temp.append((i + shift) * 10 + j - shift)
                                    self.b_threat_map[i + shift][j - shift] += 1

                        moves.append(temp)
                    elif sq == 12:
                        if 0 <= i - 1 <= 7:
                            # i-1, j
                            self.b_threat_map[i - 1][j] += 1
                        if 0 <= i - 1 <= 7 and 0 <= j - 1 <= 7:
                            # i-1, j-1
                            self.b_threat_map[i - 1][j - 1] += 1
                        if 0 <= j - 1 <= 7:
                            # i, j-1
                            self.b_threat_map[i][j - 1] += 1
                        if 0 <= i + 1 <= 7 and 0 <= j - 1 <= 7:
                            self.b_threat_map[i + 1][j - 1] += 1
                            # i+1, j-1
                        if 0 <= i + 1 <= 7:
                            # i+1, j
                            self.b_threat_map[i + 1][j] += 1
                        if 0 <= i + 1 <= 7 and 0 <= j + 1 <= 7:
                            # i+1, j+1
                            self.b_threat_map[i + 1][j + 1] += 1
                        if 0 <= j + 1 <= 7:
                            # i, j+1
                            self.b_threat_map[i][j + 1] += 1
                        if 0 <= i - 1 <= 7 and 0 <= j + 1 <= 7:
                            # i-1, j+1
                            self.b_threat_map[i - 1][j + 1] += 1
        return moves

    def kings_moves(self, board):
        moves = []
        for i in range(8):
            for j in range(8):
                if board[i][j] == 6:
                    temp = [i * 10 + j]
                    if 0 <= i - 1 <= 7:
                        if self.b_threat_map[i-1][j] == 0 and (7 <= board[i-1][j] <= 12 or board[i-1][j] == 0):
                            temp.append((i-1)*10 + j)
                    if 0 <= i - 1 <= 7 and 0 <= j - 1 <= 7:
                        if self.b_threat_map[i-1][j-1] == 0 and (7 <= board[i-1][j-1] <= 12 or board[i-1][j-1] == 0):
                            temp.append((i - 1) * 10 + (j - 1))
                    if 0 <= j - 1 <= 7:
                        if self.b_threat_map[i][j-1] == 0 and (7 <= board[i][j-1] <= 12 or board[i][j-1] == 0):
                            temp.append(i * 10 + (j - 1))
                    if 0 <= i + 1 <= 7 and 0 <= j - 1 <= 7:
                        if self.b_threat_map[i+1][j-1] == 0 and (7 <= board[i+1][j-1] <= 12 or board[i+1][j-1] == 0):
                            temp.append((i + 1) * 10 + (j - 1))
                    if 0 <= i + 1 <= 7:
                        if self.b_threat_map[i+1][j] == 0 and (7 <= board[i+1][j] <= 12 or board[i+1][j] == 0):
                            temp.append((i + 1) * 10 + j)
                    if 0 <= i + 1 <= 7 and 0 <= j + 1 <= 7:
                        if self.b_threat_map[i+1][j+1] == 0 and (7 <= board[i+1][j+1] <= 12 or board[i+1][j+1] == 0):
                            temp.append((i + 1) * 10 + (j + 1))
                    if 0 <= j + 1 <= 7:
                        if self.b_threat_map[i][j+1] == 0 and (7 <= board[i][j+1] <= 12 or board[i][j+1] == 0):
                            temp.append(i * 10 + (j + 1))
                    if 0 <= i - 1 <= 7 and 0 <= j + 1 <= 7:
                        if self.b_threat_map[i-1][j+1] == 0 and (7 <= board[i-1][j+1] <= 12 or board[i-1][j+1] == 0):
                            temp.append((i - 1) * 10 + (j + 1))
                    # castle
                    if self.reg.white_castle_king:
                        if board[7][5] == 0 and board[7][6] == 0 and self.b_threat_map[7][5] == 0 and \
                                self.b_threat_map[7][6] == 0 and self.b_threat_map[7][4] == 0:
                            temp.append(768)
                    if self.reg.white_castle_queen:
                        if board[7][3] == 0 and board[7][2] == 0 and self.b_threat_map[7][3] == 0 and \
                                board[7][1] == 0 and self.b_threat_map[7][2] == 0 and self.b_threat_map[7][4] == 0:
                            temp.append(728)
                    moves.append(temp)
                if board[i][j] == 12:
                    temp = [i * 10 + j]
                    if 0 <= i - 1 <= 7:
                        if self.w_threat_map[i-1][j] == 0 and (1 <= board[i-1][j] <= 6 or board[i-1][j] == 0):
                            temp.append((i - 1) * 10 + j)
                    if 0 <= i - 1 <= 7 and 0 <= j - 1 <= 7:
                        if self.w_threat_map[i-1][j-1] == 0 and (1 <= board[i-1][j-1] <= 6 or board[i-1][j-1] == 0):
                            temp.append((i - 1) * 10 + (j - 1))
                    if 0 <= j - 1 <= 7:
                        if self.w_threat_map[i][j-1] == 0 and (1 <= board[i][j-1] <= 6 or board[i][j-1] == 0):
                            temp.append(i * 10 + (j - 1))
                    if 0 <= i + 1 <= 7 and 0 <= j - 1 <= 7:
                        if self.w_threat_map[i+1][j-1] == 0 and (1 <= board[i+1][j-1] <= 6 or board[i+1][j-1] == 0):
                            temp.append((i + 1) * 10 + (j - 1))
                    if 0 <= i + 1 <= 7:
                        if self.w_threat_map[i+1][j] == 0 and (1 <= board[i+1][j] <= 6 or board[i+1][j] == 0):
                            temp.append((i + 1) * 10 + j)
                    if 0 <= i + 1 <= 7 and 0 <= j + 1 <= 7:
                        if self.w_threat_map[i+1][j+1] == 0 and (1 <= board[i+1][j+1] <= 6 or board[i+1][j+1] == 0):
                            temp.append((i + 1) * 10 + (j + 1))
                    if 0 <= j + 1 <= 7:
                        if self.w_threat_map[i][j+1] == 0 and (1 <= board[i][j+1] <= 6 or board[i][j+1] == 0):
                            temp.append(i * 10 + (j + 1))
                    if 0 <= i - 1 <= 7 and 0 <= j + 1 <= 7:
                        if self.w_threat_map[i-1][j+1] == 0 and (1 <= board[i-1][j+1] <= 6 or board[i-1][j+1] == 0):
                            temp.append((i - 1) * 10 + (j + 1))
                    # castle
                    if self.reg.black_castle_king:
                        if board[0][5] == 0 and board[0][6] == 0 and self.w_threat_map[0][5] == 0 and \
                                self.w_threat_map[0][6] == 0 and self.w_threat_map[0][4] == 0:
                            temp.append(68)
                    if self.reg.black_castle_queen:
                        if board[0][3] == 0 and board[0][2] == 0 and self.w_threat_map[0][3] == 0 and \
                                board[0][1] == 0 and self.w_threat_map[0][2] == 0 and self.w_threat_map[0][4] == 0:
                            temp.append(28)
                    moves.append(temp)
        return moves

    def w_incheck(self, board):
        self.b_threat_map = zeros((8, 8), dtype=int8)
        self.possible_moves_black(board)
        for i in range(8):
            for j in range(8):
                if board[i][j] == 6 and self.b_threat_map[i][j] > 0:
                    return True
        return False

    def b_incheck(self, board):
        self.w_threat_map = zeros((8, 8), dtype=int8)
        self.possible_moves_white(board)
        for i in range(8):
            for j in range(8):
                if board[i][j] == 12 and self.w_threat_map[i][j] > 0:
                    return True
        return False

    def evaluate(self, board):
        # Evaluator of position
        # -----------------------
        # material
        # activity of figures (smh like development, checks how many squares a piece defends or attacs in percentage)
        # returns a value + if white have advantage or - if black have advantage
        # value can rise up to 100 if 100 or -100 the there is a forced mate
        # --------------material values --------------
        # pawn - 120
        # rook - 700
        # knight - 410
        # bishop - 420
        # queen - 1270
        # --------- values are multiplied by 140 and changed a little
        value = 0

        # material evaluation
        for i in range(8):
            for j in range(8):
                if board[i][j] == 1:
                    value += 120
                elif board[i][j] == 2:
                    value += 700
                elif board[i][j] == 3:
                    value += 410
                elif board[i][j] == 4:
                    value += 420
                elif board[i][j] == 5:
                    value += 1270
                elif board[i][j] == 7:
                    value -= 120
                elif board[i][j] == 8:
                    value -= 700
                elif board[i][j] == 9:
                    value -= 410
                elif board[i][j] == 10:
                    value -= 420
                elif board[i][j] == 11:
                    value -= 1270

        # activity evaluation
        # pawn

        return value

    def get_moves(self, board, white_turn):
        # returns all moves as a list of tuples
        all_moves = []

        if white_turn:
            for piece in self.white_moves(board):
                figure = piece.pop(0)
                for move in piece:
                    if move % 10 != 9:
                        all_moves.append((figure, move))
                    else:
                        move //= 10
                        for i in range(1, 5):
                            all_moves.append((figure, (move * 10 + i) * 10 + 9))
        else:
            for piece in self.black_moves(board):
                figure = piece.pop(0)
                for move in piece:
                    if move % 10 != 9:
                        all_moves.append((figure, move))
                    else:
                        move //= 10
                        for i in range(1, 5):
                            all_moves.append((figure, (move * 10 + i) * 10 + 9))

        if len(all_moves) == 0:
            # there are no possible moves -> its a checkmate or stalemate
            return [False]

        return all_moves

    def copy_with_move(self, board, move, reg_copy):
        # make the move
        piece_index = board[move[0] // 10][move[0] % 10]

        if move[1] % 10 == 8:
            # its a castle

            if move[1] == 768:
                # white kingside
                board[7][6] = 6
                board[7][5] = 2
                board[7][7] = 0
            elif move[1] == 728:
                # white queenside
                board[7][2] = 6
                board[7][3] = 2
                board[7][0] = 0
            elif move[1] == 68:
                # black kingside
                board[0][6] = 12
                board[0][5] = 8
                board[0][7] = 0
            else:
                # black queenside
                board[0][2] = 12
                board[0][3] = 8
                board[0][0] = 0
            # update reg
            reg_copy[4] += 1

        elif move[1] % 10 == 9:
            # is a promotion
            piece_index = (move[1] % 100) // 10

            board[move[0] // 10][move[0] % 10] = 0
            if board[move[1] // 100][(move[1] // 10) % 10] != 0:
                # it's a capture
                reg_copy[4] = 0
            else:
                # it's a normal promotion
                reg_copy[4] += 1
            board[move[1] // 1000][(move[1] // 100) % 10] = piece_index

        else:
            # its normal move(can be enpassant, or move generateing enpassant)

            if piece_index == 1:
                # its a white pawn move

                if move[0] - move[1] == 20:
                    # its a first move(double up)
                    # add enpassant here

                    board[move[0] // 10][move[0] % 10] = 0
                    board[move[1] // 10][move[1] % 10] = piece_index
                    # reg change
                    reg_copy[5] = move[1] + 10
                    reg_copy[4] += 1

                elif move[1] == reg_copy[6]:
                    # its and en passant

                    board[move[0] // 10][move[0] % 10] = 0
                    board[move[1] // 10][move[1] % 10] = piece_index
                    board[(move[1] + 10) // 10][(move[1] + 10) % 10] = 0
                    # reg change
                    reg_copy[4] = 0

                else:
                    # its a normal move

                    if board[move[1] // 10][move[1] % 10] != 0:
                        reg_copy[4] = 0
                    else:
                        reg_copy[4] += 1
                    board[move[0] // 10][move[0] % 10] = 0
                    board[move[1] // 10][move[1] % 10] = piece_index

            elif piece_index == 7:
                # its a black pawn move
                if move[1] - move[0] == 20:
                    # its a first move(double up)
                    # add enpassant here

                    board[move[0] // 10][move[0] % 10] = 0
                    board[move[1] // 10][move[1] % 10] = piece_index
                    # reg change
                    reg_copy[5] = move[1] - 10
                    reg_copy[4] += 1

                elif move[1] == reg_copy[6]:
                    # its and en passant

                    board[move[0] // 10][move[0] % 10] = 0
                    board[move[1] // 10][move[1] % 10] = piece_index
                    board[(move[1] - 10) // 10][(move[1] - 10) % 10] = 0
                    # reg change
                    reg_copy[4] = 0

                else:
                    # its a normal move
                    if board[move[1] // 10][move[1] % 10] != 0:
                        reg_copy[4] = 0
                    else:
                        reg_copy[4] += 1
                    board[move[0] // 10][move[0] % 10] = 0
                    board[move[1] // 10][move[1] % 10] = piece_index

            else:
                # its a normal move

                if board[move[1] // 10][move[1] % 10] != 0:
                    # its a capture
                    reg_copy[4] = 0
                else:
                    # its not a capture
                    reg_copy[4] += 1
                board[move[0] // 10][move[0] % 10] = 0
                board[move[1] // 10][move[1] % 10] = piece_index

        # update castle rights
        if move[0] == 74:
            reg_copy[0] = reg_copy[1] = False
        elif move[0] == 4:
            reg_copy[2] = reg_copy[3] = False

        return board, reg_copy

    def cord_to_int(self, cord):

        for i in range(64):
            if cord % 10 == i % 8 and cord // 10 == i // 8:
                return i
        return None

    def convert_to_bitarray(self, board, reg, white_turn):

        seq = "0b"

        if white_turn:
            seq += "1"
        else:
            seq += "0"

        if reg[0]:
            seq += "1"
        else:
            seq += "0"

        if reg[1]:
            seq += "1"
        else:
            seq += "0"

        if reg[2]:
            seq += "1"
        else:
            seq += "0"

        if reg[3]:
            seq += "1"
        else:
            seq += "0"

        temp = self.cord_to_int(reg[5])
        if temp is not None:
            seq += bin(temp)[2:]

        temp = self.cord_to_int(reg[6])
        if temp is not None:
            seq += bin(temp)[2:]

        for row in board:
            for piece in row:
                seq += bin(piece)[2:]

        bit_seq = Bits(seq)

        return bit_seq

    def backtrack_check(self, array, position):
        if array.count(position):
            return True
        else:
            array.append(position)
            return False

    def minmax(self, board, depth, white_turn, reg_copy, depth_origin, backtracking_array, completion, expo):

        # ----------------------------------------------------
        # The minimax search algorithm v1.0
        # futures: minimaxing, backtracking
        #
        # info:
        # - board format is a standard gui numpy board
        # - reg format: list as presented [w_kingside, w_queenside, b_kingside, b_queenside, half_moves, en_passant, enp_temp]
        # - backtracking format: bit string ->f
        #   first bit - 1 = white turn
        #                  0 = black turn
        #   next 4 bits determining the castle rights(
        #           bit1 - white kingside (1, 0 = True, False)
        #           bit2 - white queenside
        #           bit3 - black kingside
        #           bit4 - black queenside)
        #   next 5 bits determine the en_passant
        #   next 5 bits determine the enp_temp
        #   next bits represent the board
        #       if the field is empty there is one bit = 0
        #       if the field is full there is 4 bits representing the figure index
        #       (worst case = 160 bits)(best case = 8 bits)
        #
        # ----------------------------------------------------

        best_move = None

        # depth counts down from the original one to 0
        if depth == 0:
            return self.evaluate(board)

        tab = self.get_moves(board, white_turn)
        expo *= 1/len(tab)
        for move in tab:
            if move is False:
                if self.w_incheck(board):
                    return -100000
                elif self.b_incheck(board):
                    return 100000
                else:
                    return 0
            # for every move run self then chose from the returned values which move is the best
            else:
                reg_temp = reg_copy.copy()
                board_temp, reg_temp = self.copy_with_move(board.copy(), move, reg_temp)
                bitarray_temp = self.convert_to_bitarray(board_temp, reg_temp, rev(white_turn))
                if self.backtrack_check(backtracking_array, bitarray_temp):
                    current_move = None
                else:
                    current_move = (move, self.minmax(board_temp, depth - 1, rev(white_turn), reg_temp, depth_origin, backtracking_array, completion, expo))

            if best_move is None:
                best_move = current_move
            elif current_move is not None:
                if white_turn:
                    if current_move[1] >= best_move[1]:
                        best_move = current_move
                else:
                    if current_move[1] <= best_move[1]:
                        best_move = current_move

            completion += expo
            print(completion)

        if depth_origin == depth:
            return best_move[0]
        else:
            return best_move[1]
