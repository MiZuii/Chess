from tkinter import *
from .Functions import fen_to_array, calc_dist, promotion_image, is_fpm, set_enp, int_enp, win_check, make_reg
from numpy import zeros, int8
from threading import Thread


def input_get(field, possible_moves, root):
    if root.active_piece is not None:
        for piece in possible_moves:
            if piece[0] == root.active_piece:
                for moves in piece:
                    if moves % 10 == 8:
                        if field == moves // 10 and moves // 10 != root.active_piece:
                            root.reg.move = [root.active_piece, field * 10 + 8]
                            break
                    elif moves % 10 == 9:
                        if field == moves // 10 and moves // 10 != root.active_piece:
                            root.reg.move = [root.active_piece, field * 10 + 9]
                            break
                    else:
                        if field == moves and moves != root.active_piece:
                            root.reg.move = [root.active_piece, field]
                            break
                break
        # delete active move and dots
        root.active_piece = None
        root.canvas.delete("active_move")
    else:
        root.active_piece = field
        for piece in possible_moves:
            if piece[0] == root.active_piece:
                for moves in piece:
                    if moves != root.active_piece:
                        if moves % 10 == 8 or moves % 10 == 9:
                            moves //= 10
                            root.canvas.create_image((90 * (moves % 10) + 45), (90 * (moves // 10) + 45),
                                                     anchor=CENTER, image=root.image_16,
                                                     tags=(str(moves), "active_move",))
                        else:
                            root.canvas.create_image((90 * (moves % 10) + 45), (90 * (moves // 10) + 45),
                                                     anchor=CENTER, image=root.image_16,
                                                     tags=(str(moves), "active_move",))


def setup(root):

    # sets the board img
    root.canvas.create_image(0, 0, anchor=NW, image=root.image_1, tags=("board", ))
    root.canvas.create_image(8, 25, anchor=NW, image=root.image_14, tags=("cords",))
    root.canvas.itemconfigure("cords", state=HIDDEN)

    # sets the click detect invisible images
    for i in range(8):
        for j in range(8):
            root.canvas.create_image((90 * j + 45), (90 * i + 45), anchor=CENTER, image=root.image_15,
                                     state=NORMAL, tags=(str(i*10 + j), "clickgrid", ))

    restart(root)


def update(root):
    if root.reg.move_made and root.reg.game_over is False:

        # add the move to the reg.game
        if root.reg.move is not None:
            root.reg.game.append(root.reg.move)

        # update en passant rights
        if root.reg.move is not None:
            root.reg.enp_temp = root.reg.en_passant
            root.reg.en_passant = ""
            if is_fpm(root.reg.move):
                root.reg.en_passant = set_enp(root.reg.move)

        if root.reg.white_turn:
            root.reg.current_moves = root.engine.white_moves(root.board)
        else:
            root.reg.current_moves = root.engine.black_moves(root.board)

        # draw the move

        if root.reg.move is not None:
            if root.reg.move[1] % 10 == 9:
                root.reg.move[1] //= 10

        if root.reg.last_capture and root.reg.move is not None:
            # last move was a capture
            # (it cant be a castle but can be a pawn promotion)
            imgs = root.canvas.find_overlapping((root.reg.move[1] % 10) * 90 + 40,
                                                (root.reg.move[1] // 10) * 90 + 40,
                                                (root.reg.move[1] % 10) * 90 + 50,
                                                (root.reg.move[1] // 10) * 90 + 50)
            for ids in imgs:
                tags = root.canvas.gettags(ids)
                for tag in tags:
                    if tag == "piece":
                        # move the piece
                        root.canvas.delete(ids)

            imgs = root.canvas.find_overlapping((root.reg.move[0] % 10) * 90 + 10,
                                                (root.reg.move[0] // 10) * 90 + 10,
                                                (root.reg.move[0] % 10) * 90 + 80,
                                                (root.reg.move[0] // 10) * 90 + 80)
            for ids in imgs:
                tags = root.canvas.gettags(ids)
                for tag in tags:
                    if tag == "piece":
                        # move the piece
                        if root.reg.current_promotion is not None:
                            root.canvas.itemconfigure(ids, image=promotion_image(root))
                            root.reg.current_promotion = None
                        am = calc_dist(root.reg.move)
                        root.canvas.move(ids, am[0], am[1])

            root.reg.last_capture = False

        elif root.reg.move is not None:
            # last move was normal move
            if root.reg.move[1] % 10 == 8:
                imgs = root.canvas.find_overlapping((root.reg.move[0] % 10) * 90 + 10,
                                                    (root.reg.move[0] // 10) * 90 + 10,
                                                    (root.reg.move[0] % 10) * 90 + 80,
                                                    (root.reg.move[0] // 10) * 90 + 80)
                for ids in imgs:
                    tags = root.canvas.gettags(ids)
                    for tag in tags:
                        if tag == "piece":
                            # move the piece
                            if root.reg.move[1] == 768:
                                root.canvas.move(ids, 180, 0)
                                root.reg.move = [77, 75]
                            elif root.reg.move[1] == 728:
                                root.canvas.move(ids, -180, 0)
                                root.reg.move = [70, 73]
                            elif root.reg.move[1] == 68:
                                root.canvas.move(ids, 180, 0)
                                root.reg.move = [7, 5]
                            else:
                                root.canvas.move(ids, -180, 0)
                                root.reg.move = [0, 3]

                imgs = root.canvas.find_overlapping((root.reg.move[0] % 10) * 90 + 40,
                                                    (root.reg.move[0] // 10) * 90 + 40,
                                                    (root.reg.move[0] % 10) * 90 + 50,
                                                    (root.reg.move[0] // 10) * 90 + 50)
                for ids in imgs:
                    tags = root.canvas.gettags(ids)
                    for tag in tags:
                        if tag == "piece":
                            # move the piece
                            am = calc_dist(root.reg.move)
                            root.canvas.move(ids, am[0], am[1])

            else:
                # its normal move
                imgs = root.canvas.find_overlapping((root.reg.move[0] % 10) * 90 + 40,
                                                    (root.reg.move[0] // 10) * 90 + 40,
                                                    (root.reg.move[0] % 10) * 90 + 50,
                                                    (root.reg.move[0] // 10) * 90 + 50)
                for ids in imgs:
                    tags = root.canvas.gettags(ids)
                    for tag in tags:
                        if tag == "piece":
                            # move the piece
                            if root.reg.current_promotion is not None:
                                root.canvas.itemconfigure(ids, image=promotion_image(root))
                                root.reg.current_promotion = None
                            am = calc_dist(root.reg.move)
                            root.canvas.move(ids, am[0], am[1])

                if root.reg.enp_temp != "":
                    if root.reg.move[1] == int_enp(root.reg.enp_temp)[0] * 10 + int_enp(root.reg.enp_temp)[1]:
                        # its and en passsssssssant
                        temp = root.reg.move
                        root.reg.move = root.reg.move[1] + 10 if root.reg.move[1] < 50 else root.reg.move[1] - 10
                        imgs = root.canvas.find_overlapping((root.reg.move % 10) * 90 + 40,
                                                            (root.reg.move // 10) * 90 + 40,
                                                            (root.reg.move % 10) * 90 + 50,
                                                            (root.reg.move // 10) * 90 + 50)
                        for ids in imgs:
                            tags = root.canvas.gettags(ids)
                            for tag in tags:
                                if tag == "piece":
                                    # move the piece
                                    root.canvas.delete(ids)
                        root.reg.move = temp

        # update castle rights
        if root.reg.move is not None:
            if root.reg.move[0] == 74:
                root.reg.white_castle_queen = False
                root.reg.white_castle_king = False
            if root.reg.move[0] == 4:
                root.reg.black_castle_king = False
                root.reg.black_castle_queen = False

        root.reg.move = None
        root.reg.move_made = False

        # check if game was won, lost or drawn (0 - game continues, 1 - white wins, 2 - black wins, 3 - draw)
        temp = win_check(root)
        if temp == 1:
            root.reg.game_over = True
            root.game_end("White wins!!!")
        elif temp == 2:
            root.reg.game_over = True
            root.game_end("Black wins!!!")
        elif temp == 3:
            root.reg.game_over = True
            root.game_end("Draw...")

    if root.reg.white_turn and root.reg.game_over is False:
        # white turn

        if root.settings.pl_white:
            # player is playing, white to move
            if root.reg.move:
                if (root.reg.move[1] % 10 == 8 or root.reg.move[1] % 10 == 9) is False:
                    root.reg.move_made = True
                    # do normal move
                    # check if its a capture
                    if root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] != 0:
                        # its a capture
                        root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                        root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                        # register update
                        root.reg.half_moves = 0
                        root.reg.last_capture = True
                    elif root.reg.en_passant != "":
                        if root.reg.move[1] == int_enp(root.reg.en_passant)[0] * 10 + int_enp(root.reg.en_passant)[1]:
                            root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                                root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            root.board[root.reg.move[1] // 10 + 1][root.reg.move[1] % 10] = 0
                            # reg update
                            root.reg.half_moves = 0
                        else:
                            # its not a capture
                            root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                                root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves += 1
                    else:
                        # its not a capture
                        root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                        root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                        # register update
                        root.reg.half_moves += 1
                    root.reg.white_turn = False
                elif root.reg.move[1] % 10 == 8:
                    root.reg.move_made = True
                    # its a castle
                    if root.reg.move[1] == 768:
                        # king side castle
                        if root.reg.white_castle_king:
                            root.board[7][4] = 0
                            root.board[7][6] = 6
                            root.board[7][5] = 2
                            root.board[7][7] = 0
                    else:
                        # queen side castle
                        if root.reg.white_castle_queen:
                            root.board[7][4] = 0
                            root.board[7][2] = 6
                            root.board[7][3] = 2
                            root.board[7][0] = 0
                    # register update
                    root.reg.white_castle_queen = False
                    root.reg.white_castle_king = False
                    root.reg.half_moves += 1
                    root.reg.white_turn = False
                else:
                    # pawn promotion
                    if root.sub_alive is False and root.reg.current_promotion is None:
                        root.promotion(True)
                    if root.reg.current_promotion is not None:
                        # make the promotion and clear it
                        if root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] != 0:
                            # its a capture
                            root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] = root.reg.current_promotion
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves = 0
                            root.reg.last_capture = True
                        else:
                            # its not a capture
                            root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] = root.reg.current_promotion
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves += 1

                        root.reg.white_turn = False
                        root.reg.move_made = True
        else:
            # computer is playing, white to move
            if root.reg.engine_working is False:
                x = Thread(target=engine_thread, args=(root, root.settings.depth))
                x.start()
            if root.reg.move:
                root.reg.engine_working = False
                if (root.reg.move[1] % 10 == 8 or root.reg.move[1] % 10 == 9) is False:
                    root.reg.move_made = True
                    # do normal move
                    # check if its a capture
                    if root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] != 0:
                        # its a capture
                        root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                        root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                        # register update
                        root.reg.half_moves = 0
                        root.reg.last_capture = True
                    elif root.reg.en_passant != "":
                        if root.reg.move[1] == int_enp(root.reg.en_passant)[0] * 10 + int_enp(root.reg.en_passant)[1]:
                            root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                                root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            root.board[root.reg.move[1] // 10 + 1][root.reg.move[1] % 10] = 0
                            # reg update
                            root.reg.half_moves = 0
                        else:
                            # its not a capture
                            root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                                root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves += 1
                    else:
                        # its not a capture
                        root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                        root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                        # register update
                        root.reg.half_moves += 1
                    root.reg.white_turn = False
                elif root.reg.move[1] % 10 == 8:
                    root.reg.move_made = True
                    # its a castle
                    if root.reg.move[1] == 768:
                        # king side castle
                        if root.reg.white_castle_king:
                            root.board[7][4] = 0
                            root.board[7][6] = 6
                            root.board[7][5] = 2
                            root.board[7][7] = 0
                    else:
                        # queen side castle
                        if root.reg.white_castle_queen:
                            root.board[7][4] = 0
                            root.board[7][2] = 6
                            root.board[7][3] = 2
                            root.board[7][0] = 0
                    # register update
                    root.reg.white_castle_queen = False
                    root.reg.white_castle_king = False
                    root.reg.half_moves += 1
                    root.reg.white_turn = False
                else:
                    if root.reg.current_promotion is not None:
                        # make the promotion and clear it
                        if root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] != 0:
                            # its a capture
                            root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] = root.reg.current_promotion
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves = 0
                            root.reg.last_capture = True
                        else:
                            # its not a capture
                            root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] = root.reg.current_promotion
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves += 1

                        root.reg.white_turn = False
                        root.reg.move_made = True

    elif root.reg.game_over is False:
        # black turn
        if root.settings.pl_black:
            # player is playing, black to move
            if root.reg.move:
                if (root.reg.move[1] % 10 == 8 or root.reg.move[1] % 10 == 9) is False:
                    root.reg.move_made = True
                    # do normal move
                    # check if its a capture
                    if root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] != 0:
                        # its a capture
                        root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                        root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                        # register update
                        root.reg.half_moves = 0
                        root.reg.last_capture = True
                    elif root.reg.en_passant != "":
                        if root.reg.move[1] == int_enp(root.reg.en_passant)[0] * 10 + int_enp(root.reg.en_passant)[1]:
                            root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                                root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            root.board[root.reg.move[1] // 10 - 1][root.reg.move[1] % 10] = 0
                            # reg update
                            root.reg.half_moves = 0
                        else:
                            # its not a capture
                            root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                                root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves += 1
                    else:
                        # its not a capture
                        root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                        root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                        # register update
                        root.reg.half_moves += 1
                    root.reg.white_turn = True
                    root.reg.full_moves += 1
                elif root.reg.move[1] % 10 == 8:
                    root.reg.move_made = True
                    # its a castle
                    if root.reg.move[1] == 68:
                        # king side castle
                        if root.reg.black_castle_king:
                            root.board[0][4] = 0
                            root.board[0][6] = 12
                            root.board[0][5] = 8
                            root.board[0][7] = 0
                    else:
                        # queen side castle
                        if root.reg.black_castle_queen:
                            root.board[0][4] = 0
                            root.board[0][2] = 12
                            root.board[0][3] = 8
                            root.board[0][0] = 0
                    # register update
                    root.reg.black_castle_king = False
                    root.reg.black_castle_queen = False
                    root.reg.half_moves += 1
                    root.reg.white_turn = True
                    root.reg.full_moves += 1
                else:
                    if root.sub_alive is False and root.reg.current_promotion is None:
                        root.promotion(False)
                    if root.reg.current_promotion is not None:
                        # make the promotion and clear it
                        if root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] != 0:
                            # its a capture
                            root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] = root.reg.current_promotion
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves = 0
                            root.reg.last_capture = True
                        else:
                            # its not a capture
                            root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] = root.reg.current_promotion
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves += 1

                        root.reg.white_turn = True
                        root.reg.full_moves += 1
                        root.reg.move_made = True
        else:
            # computer is playing, black to move
            if root.reg.engine_working is False:
                x = Thread(target=engine_thread, args=(root, root.settings.depth))
                x.start()
            if root.reg.move:
                root.reg.engine_working = False
                if (root.reg.move[1] % 10 == 8 or root.reg.move[1] % 10 == 9) is False:
                    root.reg.move_made = True
                    # do normal move
                    # check if its a capture
                    if root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] != 0:
                        # its a capture
                        root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                        root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                        # register update
                        root.reg.half_moves = 0
                        root.reg.last_capture = True
                    elif root.reg.en_passant != "":
                        if root.reg.move[1] == int_enp(root.reg.en_passant)[0] * 10 + int_enp(root.reg.en_passant)[1]:
                            root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                                root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            root.board[root.reg.move[1] // 10 - 1][root.reg.move[1] % 10] = 0
                            # reg update
                            root.reg.half_moves = 0
                        else:
                            # its not a capture
                            root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                                root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves += 1
                    else:
                        # its not a capture
                        root.board[root.reg.move[1] // 10][root.reg.move[1] % 10] = \
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10]
                        root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                        # register update
                        root.reg.half_moves += 1
                    root.reg.white_turn = True
                    root.reg.full_moves += 1
                elif root.reg.move[1] % 10 == 8:
                    root.reg.move_made = True
                    # its a castle
                    if root.reg.move[1] == 68:
                        # king side castle
                        if root.reg.black_castle_king:
                            root.board[0][4] = 0
                            root.board[0][6] = 12
                            root.board[0][5] = 8
                            root.board[0][7] = 0
                    else:
                        # queen side castle
                        if root.reg.black_castle_queen:
                            root.board[0][4] = 0
                            root.board[0][2] = 12
                            root.board[0][3] = 8
                            root.board[0][0] = 0
                    # register update
                    root.reg.black_castle_king = False
                    root.reg.black_castle_queen = False
                    root.reg.half_moves += 1
                    root.reg.white_turn = True
                    root.reg.full_moves += 1
                else:
                    if root.reg.current_promotion is not None:
                        # make the promotion and clear it
                        if root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] != 0:
                            # its a capture
                            root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] = root.reg.current_promotion
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves = 0
                            root.reg.last_capture = True
                        else:
                            # its not a capture
                            root.board[root.reg.move[1] // 100][
                                (root.reg.move[1] % 100 - root.reg.move[1] % 10) // 10] = root.reg.current_promotion
                            root.board[root.reg.move[0] // 10][root.reg.move[0] % 10] = 0
                            # register update
                            root.reg.half_moves += 1

                        root.reg.white_turn = True
                        root.reg.full_moves += 1
                        root.reg.move_made = True


def board_redraw(root):
    root.canvas.delete("piece")

    x = 0
    y = 0
    for row in root.board:
        for column in row:
            if column == 0:
                pass
            elif column == 1:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_7,
                                         tags=("piece",))
            elif column == 7:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_13,
                                         tags=("piece",))
            elif column == 2:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_6,
                                         tags=("piece",))
            elif column == 3:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_5,
                                         tags=("piece",))
            elif column == 4:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_4,
                                         tags=("piece",))
            elif column == 5:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_3,
                                         tags=("piece",))
            elif column == 6:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_2,
                                         tags=("piece",))
            elif column == 8:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_12,
                                         tags=("piece",))
            elif column == 9:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_11,
                                         tags=("piece",))
            elif column == 10:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_10,
                                         tags=("piece",))
            elif column == 11:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_9,
                                         tags=("piece",))
            elif column == 12:
                root.canvas.create_image(x, y,
                                         anchor=NW,
                                         image=root.image_8,
                                         tags=("piece",))
            x += 90
        y += 90
        x = 0

        root.canvas.tag_raise("cords", "piece")
        root.canvas.tag_raise("clickgrid", "piece")


def engine_thread(root, depth):
    root.reg.engine_working = True
    backtracking_array = []
    completion = 0
    root.reg.move = root.engine.minmax(root.board, depth, root.reg.white_turn, make_reg(root.reg), depth, backtracking_array, completion, 1)
    print(len(backtracking_array))


def restart(root):

    # settings updateh
    root.settings.update()
    root.reg.reset()
    root.reg.print_reg()
    root.reg.game_over = False

    # clears the board
    root.board = zeros((8, 8), dtype=int8)
    fen_to_array(root.starting_pos, root.board)
    print(root.starting_pos)

    board_redraw(root)
