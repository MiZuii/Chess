from Display import View
from Game import update, setup
from Engines import MChessEngine
from numpy import zeros, int8


def main():

    # 8| 00  01  02  03  04  05  06  07
    # 7| 10  11  12  13  14  15  16  17
    # 6| 20  21  22  23  24  25  26  27
    # 5| 30  31  32  33  34  35  36  37
    # 4| 40  41  42  43  44  45  46  47
    # 3| 50  51  52  53  54  55  56  57
    # 2| 60  61  62  63  64  65  66  67
    # 1| 70  71  72  73  74  75  76  77
    #  |-a---b---c---d---e--f---g---h--
    #
    # array board representation - ex. 35 = [3][5] = f5
    #
    # WHITE PIECES:   \         BLACK PIECES:
    # 1 - pawn             \         7 - pawn
    # 2 - rook               \        8 - rook
    # 3 - knight            \        9 - knight
    # 4 - bishop            \       10 - bishop
    # 5 - queen            \        11 - queen
    # 6 - king               \         12 - king

    board = zeros((8, 8), dtype=int8)
    mchess = MChessEngine("MChess", board)
    root = View(720, "Test", 80, update, setup, board, mchess)


if __name__ == "__main__":
    main()
