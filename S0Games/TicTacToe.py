import colorama
from os import system, name

board = list(range(1, 10))
# board = [1, 2, 3, 4, 5, 6, 7, "O", "X"]

winners = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
cmove = ((5,), (1, 3, 7, 9), (2, 4, 6, 8))
player, computer = "X", "O"


def print_board():
    j = 1
    for i in board:
        end = " "
        if j % 3 == 0:
            end = "\n\n"
        if i == "X":
            print(colorama.Fore.RED + f"[{i}]" + colorama.Style.RESET_ALL, end=end)
        elif i == "O":
            print(colorama.Fore.BLUE + f"[{i}]" + colorama.Style.RESET_ALL, end=end)
        else:
            print(f"[{i}]", end=end)
        j += 1


def can_move(brd, mve):
    if mve in range(1, 10) and isinstance(brd[mve - 1], int):
        return True
    return False


def make_move(brd, plyr, mve, undo=False):
    if can_move(brd, mve):
        board[mve - 1] = plyr
        win = is_winner(brd, plyr)
        if undo:
            board[mve - 1] = mve
        return True, win
    return False, False



def is_winner(brd, plyr):
    win = True
    for tup in winners:
        win = True
        for j in tup:
            if brd[j] != plyr:
                win = False
                break
        if win:
            break
    return win


def has_empty_spaces():
    return board.count("X") + board.count("O") != 9


def cmp_move():
    mv = -1
    # if computer could win :
    for i in range(1, 10):
        if make_move(board, computer, i, True)[1]:
            mv = i
            break
    # if user could win
    if mv == -1:
        for j in range(1, 10):
            if make_move(board, player, j, True)[1]:
                mv = j
    if mv == -1:
        for tup in cmove:
            for m in tup:
                if mv == -1 and can_move(board, m):
                    mv = m
                    break
    return make_move(board, computer, mv)

draw = 1
while has_empty_spaces():
    print_board()
    move = int(input("Move: "))
    moved, won = make_move(board, player, move)
    if not moved:
        print("Invalid number", "Try again")
        continue
    if won:
        draw = 0
        print_board()
        print(colorama.Fore.LIGHTGREEN_EX + "You won!" + colorama.Style.RESET_ALL)
        break
    elif cmp_move()[-1]:
        draw = 0
        print_board()
        print(colorama.Fore.LIGHTYELLOW_EX + "You lost!" + colorama.Style.RESET_ALL)
        break
    if name == "posix":
        system("clear")

if draw:
    print_board()
    print(colorama.Fore.CYAN + "Draw" + colorama.Style.RESET_ALL)
