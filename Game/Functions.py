def fen_to_array(fen, board):

    row = 0
    column = 0

    for char in fen:
        if char == " ":
            break
        elif is_int(char):
            column += int(char)
        elif char == "/":
            row += 1
            column = 0
        elif char == "p":
            board[row][column] = 7
            column += 1
        elif char == "r":
            board[row][column] = 8
            column += 1
        elif char == "n":
            board[row][column] = 9
            column += 1
        elif char == "b":
            board[row][column] = 10
            column += 1
        elif char == "q":
            board[row][column] = 11
            column += 1
        elif char == "k":
            board[row][column] = 12
            column += 1
        elif char == "P":
            board[row][column] = 1
            column += 1
        elif char == "R":
            board[row][column] = 2
            column += 1
        elif char == "N":
            board[row][column] = 3
            column += 1
        elif char == "B":
            board[row][column] = 4
            column += 1
        elif char == "Q":
            board[row][column] = 5
            column += 1
        elif char == "K":
            board[row][column] = 6
            column += 1


def is_int(char):
    try:
        int(char)
        return True
    except ValueError:
        return False


def int_enp(square):
    val = [0, 0]
    if square[0] == "a":
        val[1] = 0
    elif square[0] == "b":
        val[1] = 1
    elif square[0] == "c":
        val[1] = 2
    elif square[0] == "d":
        val[1] = 3
    elif square[0] == "e":
        val[1] = 4
    elif square[0] == "f":
        val[1] = 5
    elif square[0] == "g":
        val[1] = 6
    elif square[0] == "h":
        val[1] = 7
    if square[1] == "1":
        val[0] = 7
    elif square[1] == "2":
        val[0] = 6
    elif square[1] == "3":
        val[0] = 5
    elif square[1] == "4":
        val[0] = 4
    elif square[1] == "5":
        val[0] = 3
    elif square[1] == "6":
        val[0] = 2
    elif square[1] == "7":
        val[0] = 1
    elif square[1] == "8":
        val[0] = 0
    return val


def calc_dist(move):
    move_amount = [0, 0]
    move_amount[1] = (move[1] // 10) * 90 - (move[0] // 10) * 90
    move_amount[0] = (move[1] % 10) * 90 - (move[0] % 10) * 90
    return move_amount


def promotion_image(root):
    temp = root.reg.current_promotion

    if temp == 3:
        return root.image_5
    elif temp == 4:
        return root.image_4
    elif temp == 2:
        return root.image_6
    elif temp == 5:
        return root.image_3
    elif temp == 9:
        return root.image_11
    elif temp == 10:
        return root.image_10
    elif temp == 8:
        return root.image_12
    elif temp == 11:
        return root.image_9


def is_fpm(move):
    fpm_list = [[60, 40],
                [61, 41],
                [62, 42],
                [63, 43],
                [64, 44],
                [65, 45],
                [66, 46],
                [67, 47],
                [10, 30],
                [11, 31],
                [12, 32],
                [13, 33],
                [14, 34],
                [15, 35],
                [16, 36],
                [17, 37]]

    if fpm_list.count(move):
        return True
    else:
        return False


def set_enp(move):
    val = ""
    move = move[1] + 10 if move[1] < move[0] else move[0] + 10

    if move % 10 == 0:
        val += "a"
    elif move % 10 == 1:
        val += "b"
    elif move % 10 == 2:
        val += "c"
    elif move % 10 == 3:
        val += "d"
    elif move % 10 == 4:
        val += "e"
    elif move % 10 == 5:
        val += "f"
    elif move % 10 == 6:
        val += "g"
    elif move % 10 == 7:
        val += "h"

    if move // 10 == 0:
        val += "8"
    elif move // 10 == 1:
        val += "7"
    elif move // 10 == 2:
        val += "6"
    elif move // 10 == 3:
        val += "5"
    elif move // 10 == 4:
        val += "4"
    elif move // 10 == 5:
        val += "3"
    elif move // 10 == 6:
        val += "2"
    elif move // 10 == 7:
        val += "1"

    return val


def win_check(root):
    w_knight = 0
    b_knight = 0
    w_bishop = 0
    b_bishop = 0
    other = 0

    # check for half moves draw, repetition and insufficient material
    # half moves
    if root.reg.half_moves >= 100:
        return 3

    # insufficient material
    for row in root.board:
        for field in row:
            if field == 0:
                pass
            elif field == 3:
                w_knight += 1
            elif field == 4:
                w_bishop += 1
            elif field == 6:
                pass
            elif field == 9:
                b_knight += 1
            elif field == 10:
                b_bishop += 1
            elif field == 12:
                pass
            else:
                other += 1
    if other == 0:
        if (w_bishop == 2 or b_bishop == 2) is False:
            if w_bishop == 0 and b_knight == 0:
                return 3
            if b_bishop == 0 and b_knight == 0:
                return 3

    # repetition

    # check if there are possible moves
    for piece in root.reg.current_moves:
        if len(piece) > 1:
            return 0        # returns if finds a possible move

    # there are no possible moves
    if root.reg.white_turn:
        if root.engine.w_incheck(root.board):
            return 2
        else:
            return 3
    else:
        if root.engine.b_incheck(root.board):
            return 1
        else:
            return 3


def make_reg(reg):
    reg_copy = []
    if reg.en_passant != "":
        enp = int_enp(reg.en_passant)
    if reg.enp_temp != "":
        enp_temp = int_enp(reg.enp_temp)

    reg_copy.append(reg.white_castle_king)
    reg_copy.append(reg.white_castle_queen)
    reg_copy.append(reg.black_castle_king)
    reg_copy.append(reg.black_castle_queen)
    reg_copy.append(reg.half_moves)
    if reg.en_passant != "":
        reg_copy.append(enp[0] * 10 + enp[1])
    else:
        reg_copy.append(-1)
    if reg.enp_temp != "":
        reg_copy.append(enp_temp[0] * 10 + enp_temp[1])
    else:
        reg_copy.append(-1)

    return reg_copy


def rev(val):
    if val:
        val = False
    else:
        val = True
    return val
