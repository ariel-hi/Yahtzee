"""Yahtzee!!!"""

import random
import time
import sys
import os

from unicurses import *
import curses
import math

circle = '●'

moves = {'1': 'Ones', '2': 'Twos', '3': 'Threes', '4': 'Fours', '5': 'Fives', '6': 'Sixes',
         '7': '3 of a kind', '8': '4 of a kind', '9': 'Full House',
         '10': 'Small Str', '11': 'Large Str', '12': 'YAHTZEE', '13': 'Chance'}

moves_vals = {'Ones': 'count[0]', 'Twos': 'count[1]*2', 'Threes': 'count[2]*3',
              'Fours': 'count[3]*4', 'Fives': 'count[4]*5', 'Sixes': 'count[5]*6',
              '3 of a kind': 'sum_vals if max_count >= 3 else 0', '4 of a kind': 'sum_vals if max_count >= 4 else 0',
              'Full House': '25 if isFullHouse() else 0', 'Small Str': '30 if isSmallStraight() else 0',
              'Large Str': '40 if isLargeStraight() else 0', 'YAHTZEE': '50 if max_count == 5 else 0', 'Chance': 'sum_vals'}

moves_order_full = ['Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes',
                    '3 of a kind', '4 of a kind', 'Full House', 'Small Str',
                    'Large Str', 'YAHTZEE', 'Chance']

moves_order = ['Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes',
               '3Kind', '4Kind', 'Full H', 'S Str', 'L Str', 'YHTZ!', 'Chance']


def printBlank():
    print(" "*8 + '\t', end='')


def printEnd():
    print(" " + "-"*7 + '\t', end='')


def printRow1(roll):
    if roll == 1:
        print("|       |" + '\t', end='')
    elif roll < 4:
        print("| " + circle + "     |" + '\t', end='')
    else:
        print("| " + circle + "   " + circle + " |" + '\t', end='')


def printRow2(roll):
    if roll % 2 == 1:
        print("|   " + circle + "   |" + '\t', end='')
    elif roll == 6:
        print("| " + circle + "   " + circle + " |" + '\t', end='')
    else:
        print("|       |" + '\t', end='')


def printRow3(roll):
    if roll == 1:
        print("|       |" + '\t', end='')
    elif roll < 4:
        print("|     " + circle + " |" + '\t', end='')
    else:
        print("| " + circle + "   " + circle + " |" + '\t', end='')


def printNum1(num, tabs):
    if num == 1:
        print("    _  " + '\t'*tabs, end='')
    elif num == 4:
        print("       " + '\t'*tabs, end='')
    else:
        print("   _ _ " + '\t'*tabs, end='')


def printNum2(num, tabs):
    if num == 1:
        print("     | " + '\t'*tabs, end='')
    elif num == 7:
        print("      |" + '\t'*tabs, end='')
    elif num == 2 or num == 3:
        print("   _ _|" + '\t'*tabs, end='')
    elif num == 4 or num > 7:
        print("  |_ _|" + '\t'*tabs, end='')
    elif num > 4:
        print("  |_ _ " + '\t'*tabs, end='')
    else:
        print("  |   |" + '\t'*tabs, end='')


def printNum3(num, tabs):
    if num == 1:
        print("    _|_" + '\t'*tabs, end='')
    elif num % 3 == 1:
        print("      |" + '\t'*tabs, end='')
    elif num == 2:
        print("  |_ _ " + '\t'*tabs, end='')
    elif num == 3 or num == 5 or num == 9:
        print("   _ _|" + '\t'*tabs, end='')
    else:
        print("  |_ _|" + '\t'*tabs, end='')


def printLet1(let, tabs):
    let = let.lower()
    if let in ['h', 'k', 'l', 'u', 'v', 'w', 'x', 'y', ' ']:
        print("       " + '\t'*tabs, end='')
    else:
        print("   _ _ " + '\t'*tabs, end='')


def printLet2(let, tabs):
    let = let.lower()
    if let == ' ':
        print("       " + '\t'*tabs, end='')
    elif let in ['a', 'b', 'h', 'p', 'r', 'y']:
        print("  |_ _|" + '\t'*tabs, end='')
    elif let in ['c', 'l']:
        print("  |    " + '\t'*tabs, end='')
    elif let == 'd':
        print("  |   \\" + '\t'*tabs, end='')
    elif let in ['e', 'f']:
        print("  |_   " + '\t'*tabs, end='')
    elif let == 'g':
        print("  |  _ " + '\t'*tabs, end='')
    elif let in ['i', 'j', 't']:
        print("    |  " + '\t'*tabs, end='')
    elif let == 'k':
        print("  |_ _/" + '\t'*tabs, end='')
    elif let == 'm':
        print("  | | |" + '\t'*tabs, end='')
    elif let in ['n', 'o', 'q', 'u', 'w']:
        print("  |   |" + '\t'*tabs, end='')
    elif let == 's':
        print("  |_ _ " + '\t'*tabs, end='')
    elif let == 'v':
        print("  \  / " + '\t'*tabs, end='')
    elif let == 'x':
        print("  \_ / " + '\t'*tabs, end='')
    else:
        print("   _ _|" + '\t'*tabs, end='')


def printLet3(let, tabs):
    let = let.lower()
    if let == ' ':
        print("       " + '\t'*tabs, end='')
    elif let in ['a', 'h', 'm', 'n']:
        print("  |   |" + '\t'*tabs, end='')
    elif let in ['b', 'g', 'o', 'u']:
        print("  |_ _|" + '\t'*tabs, end='')
    elif let in ['c', 'e', 'l', 'z']:
        print("  |_ _ " + '\t'*tabs, end='')
    elif let == 'd':
        print("  |_ _/" + '\t'*tabs, end='')
    elif let in ['f', 'p']:
        print("  |    " + '\t'*tabs, end='')
    elif let == 'i':
        print("   _|_ " + '\t'*tabs, end='')
    elif let == 'j':
        print("  |_|  " + '\t'*tabs, end='')
    elif let in ['k', 'r']:
        print("  |   \\" + '\t'*tabs, end='')
    elif let in ['q', 'w']:
        print("  |_|_|" + '\t'*tabs, end='')
    elif let == 's':
        print("   _ _|" + '\t'*tabs, end='')
    elif let in ['t', 'y']:
        print("    |  " + '\t'*tabs, end='')
    elif let == 'v':
        print("   \/  " + '\t'*tabs, end='')
    else:
        print("  /  \ " + '\t'*tabs, end='')


def printNiceLet1(let, tabs):
    let = let.lower()
    if let == ' ':
        print("       " + '\t'*tabs, end='')
    elif let in ['h', 'k', 'u', 'v', 'y']:
        print("  _   _" + '\t'*tabs, end='')
    elif let in ['i', 't']:
        print("   _  _" + '\t'*tabs, end='')
    elif let in ['c', 'e', 'j', 's']:
        print("    _ _" + '\t'*tabs, end='')
    elif let == 'l':
        print("  _    " + '\t'*tabs, end='')
    elif let == 'w':
        print("  _ _ _" + '\t'*tabs, end='')
    elif let == 'x':
        print("  _  _" + '\t'*tabs, end='')
    else:
        print("   _ _ " + '\t'*tabs, end='')


def printNiceLet2(let, tabs):
    let = let.lower()
    if let == ' ':
        print("       " + '\t'*tabs, end='')
    elif let in ['a', 'b', 'h', 'p', 'r']:
        print("  ||_||" + '\t'*tabs, end='')
    elif let == 'c':
        print("  //   " + '\t'*tabs, end='')
    elif let == 'd':
        print("  || \\\\" + '\t'*tabs, end='')
    elif let in ['e', 's']:
        print("  //_  " + '\t'*tabs, end='')
    elif let == 'f':
        print("  ||_  " + '\t'*tabs, end='')
    elif let == 'g':
        print("  || _ " + '\t'*tabs, end='')
    elif let in ['i', 't']:
        print("    || " + '\t'*tabs, end='')
    elif let == 'j':
        print("  _  ||" + '\t'*tabs, end='')
    elif let == 'k':
        print("  ||_//" + '\t'*tabs, end='')
    elif let == 'l':
        print("  ||   " + '\t'*tabs, end='')
    elif let == 'm':
        print("  |||||" + '\t'*tabs, end='')
    elif let in ['n', 'o', 'u']:
        print("  || ||" + '\t'*tabs, end='')
    elif let == 'q':
        print("  ||  |" + '\t'*tabs, end='')
    elif let == 's':
        print("  //_  " + '\t'*tabs, end='')
    elif let == 'v':
        print("  \\\\ //" + '\t'*tabs, end='')
    elif let == 'w':
        print("  \\\\|//" + '\t'*tabs, end='')
    elif let == 'x':
        print("  \\\\//" + '\t'*tabs, end='')
    elif let == 'y':
        print("  \\\\_//" + '\t'*tabs, end='')
    else:
        print("    //" + '\t'*tabs, end='')


def printNiceLet3(let, tabs):
    let = let.lower()
    if let == ' ':
        print("       " + '\t'*tabs, end='')
    elif let in ['a', 'h', 'm', 'n']:
        print("  || ||" + '\t'*tabs, end='')
    elif let in ['b', 'g', 'o', 'u']:
        print("  ||_||" + '\t'*tabs, end='')
    elif let in ['c', 'e']:
        print("  \\\\_ _" + '\t'*tabs, end='')
    elif let == 'd':
        print("  ||_//" + '\t'*tabs, end='')
    elif let in ['f', 'p']:
        print("  ||   " + '\t'*tabs, end='')
    elif let == 'i':
        print("   _||_" + '\t'*tabs, end='')
    elif let == 'j':
        print("  \\\\_||" + '\t'*tabs, end='')
    elif let in ['k', 'r']:
        print("  || \\\\" + '\t'*tabs, end='')
    elif let == 'l':
        print("  ||_ _" + '\t'*tabs, end='')
    elif let == 'q':
        print("  ||_\|" + '\t'*tabs, end='')
    elif let == 's':
        print("  _ _//" + '\t'*tabs, end='')
    elif let == 't':
        print("    || " + '\t'*tabs, end='')
    elif let in ['v', 'w']:
        print("   \// " + '\t'*tabs, end='')
    elif let == 'x':
        print("  //\\\\" + '\t'*tabs, end='')
    elif let == 'y':
        print("    // " + '\t'*tabs, end='')
    else:
        print("   //_ " + '\t'*tabs, end='')


def printWord(word):
    for i in word:
        printLet1(i, 0)
    print()
    for i in word:
        printLet2(i, 0)
    print()
    for i in word:
        printLet3(i, 0)
    print()


def printNiceWord(word, celeb=False):
    if celeb:
        print("               ", end='')
    for i in word:
        printLet1(i, 0)
    print()
    if celeb:
        print(".~*~.     .~*~.", end='')
    for i in word:
        printLet2(i, 0)
    if celeb:
        print("  .~*~.     .~*~.", end='')
    print()
    if celeb:
        print("     *~.~*     ", end='')
    for i in word:
        printLet3(i, 0)
    if celeb:
        print("       *~.~*     ", end='')
    print()


def diceAction(num_of_dice, roll_num, dice):  # roll a row of num_of_dice dice starting with roll_num
    printBlank()
    for i in range(num_of_dice):
        printEnd()
    print()
    printNum1(roll_num, 2)
    for i in dice:
        printRow1(i)
    print()
    printNum2(roll_num, 2)
    for i in dice:
        printRow2(i)
    print()
    printNum3(roll_num, 2)
    for i in dice:
        printRow3(i)
    print()
    printBlank()
    for i in dice:
        printEnd()
    print()


def movesFunction(dice_vals, player):
    dice_vals = sorted(dice_vals)
    count = [0 for i in range(6)]
    for i in dice_vals:
        count[i - 1] += 1
    max_count = max(count)
    sum_vals = sum(dice_vals)

    def isFullHouse():
        firstCase = dice_vals[0] == dice_vals[1] and dice_vals[2] == dice_vals[4]
        secondCase = dice_vals[0] == dice_vals[2] and dice_vals[3] == dice_vals[4]
        return firstCase != secondCase

    def isSmallStraight():
        return all([i in dice_vals for i in [3, 4]]) and any([i[0] in dice_vals and i[1] in dice_vals for i in [[1, 2], [2, 5], [5, 6]]])

    def isLargeStraight():
        return all([i in dice_vals for i in [2, 3, 4, 5]]) and any([i in dice_vals for i in [1, 6]])

    print("\n~~ POSSIBLE MOVES ~~\n")
    move_count = 1
    for i in moves_order_full:
        if i in player.moves.values():
            print("{0}. {1}: {2}".format(move_count, i, eval(moves_vals[i])))
            move_count += 1
        if i == "Sixes":
            print()
    print()
    while True:
        print("Move? -- ", end='')
        move_num = input()
        move_string = player.moves.get(move_num, -1)
        if move_string != -1:
            break
    print()
    player.move(int(move_num), eval(moves_vals.get(move_string)))


def printBoard(board):
    print('\t', end='')
    for i in range(15):
        if i == 14:
            print("Total\t", end='')
        elif i > 0:
            print(moves_order[i-1], '\t', end='')
        for j in range(len(board)):
            print(board[j][i], '\t', end='')
        print()


def clear_screen(board='', size=90):
    os.system('cls')
    print(" -------     __ __  _____  __ __  ______  ______  _____  _____      ------- ".center(size, ' '))
    print("| ●   ● |   |  |  ||  _  ||  |  ||_    _||__    ||  ___||  ___|    | ●   ● |".center(size, ' '))
    print("| ●   ● |    \_   ||     ||     |  |  |     /  / |  ___||  ___|    | ●   ● |".center(size, ' '))
    print("| ●   ● |     _|__||__|__||__|__|__|__|___ /  /__|_____||_____|    | ●   ● |".center(size, ' '))
    print(" -------     /   ________________________ /  /________________|     ------- ".center(size, ' '))
    print("            |  /  |                      |____________________|             ".center(size, ' '))
    print("             \___/                                                          ".center(size, ' '))
    if board is not '':
        printBoard(board)


class Player(object):
    def __init__(self, name):
        self.name = name
        self.moves = dict(moves)
        self.column = [name] + ['_' for i in range(13)] + [0]

    def move(self, move_num, amount):
        count = 0
        for i in range(1, 14):
            if self.column[i] == '_':
                count += 1
            if count == move_num:
                self.column[i] = amount
                break
        for i in range(move_num, len(self.moves)):
            self.moves[str(i)] = self.moves[str(i + 1)]
        del self.moves[str(len(self.moves))]
        self.column[14] += amount


def stdout(message):
    sys.stdout.write(message)
    sys.stdout.write('\b' * len(message))

NUM_FRAMES = 150
NUM_BLOBS = 800
PERSPECTIVE = 50.0
DELAY = 0.02
M_1_PI = 0.31830988618


class Spaceblob(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


def prng():
    return random.uniform(-1, 1)


def Firework(winner):
    frames = ['_' for i in range(NUM_FRAMES)]
    i = j = x = y = z = v = rows = cols = ith = i0 = 0
    maxx = minx = maxy = miny = 0
    bx = by = bz = br = r = th = t = 0
    blobs = []

    # Initialize ncurses and get window dimensions
    stdscr = initscr()
    rows, cols = getmaxyx(stdscr)
    rows = int(rows)
    cols = int(cols)
    minx = -cols // 2
    maxx = cols+minx-1
    miny = -rows // 2
    maxy = rows+miny-1
    avgx = (maxx + minx) // 2
    avgy = (maxy + miny) // 2

    # Generate random blob coordinates
    blobs = [Spaceblob() for i in range(NUM_BLOBS)]
    for i in range(NUM_BLOBS):
        bx = prng()
        by = prng()
        bz = prng()
        br = math.sqrt(bx*bx + by*by + bz*bz)
        blobs[i].x = (bx / br) * (1.3 + 0.2 * prng())
        blobs[i].y = (0.5 * by / br) * (1.3 + 0.2 * prng())
        blobs[i].z = (bz / br) * (1.3 + 0.2 * prng())

    # Generate animation frames
    for i in range(NUM_FRAMES):
        t = (1. * i) / NUM_FRAMES
        frames[i] = ['_' for i in range(cols * rows + 1)]
        ycount = 0
        for y in range(miny, maxy + 1):
            xcount = -1
            for x in range(minx, maxx + 1):
                xcount += 1
                # Show a single '*' in first frame
                if i == 0:
                    frames[i][xcount+ycount*cols] = '*' if x == 0 and y == 0 else ' '
                    continue

                # Show expanding star in next 7 frames
                if i < 8:
                    r = math.sqrt(x*x + 4*y*y)
                    frames[i][xcount+ycount*cols] = '@' if r < i*2 else ' '
                    continue

                # Otherwise show blast wave */
                r = int(math.sqrt(x*x+4*y*y) * (0.5 + (prng()/3.0)*math.cos(16.*math.atan2(y*2.+0.01, x+0.01))*.3))
                ith = 32 + th * 32. * M_1_PI
                v = i - r - 7
                if v < 0:
                    frames[i][xcount+ycount*cols] = "%@W#H=+~-:."[i-8] if i < 19 else ' '  # initial flash
                elif v < len(winner):
                    frames[i][xcount+ycount*cols] = winner[v]
                else:
                    frames[i][xcount+ycount*cols] = ' '
            ycount += 1
        # Add blobs with perspective effect
        if i > 6:
            i0 = i-6
            for j in range(NUM_BLOBS):
                bx = blobs[j].x * i0
                by = blobs[j].y * i0
                bz = blobs[j].z * i0
                if (bz < 5-PERSPECTIVE or bz > PERSPECTIVE):
                    continue
                x = int(cols / 2 + bx * PERSPECTIVE / (bz+PERSPECTIVE))
                y = int(rows / 2 + by * PERSPECTIVE / (bz+PERSPECTIVE))
                if all([x >= 0, x < cols, y >= 0, y < rows]):
                    frames[i][x+y*cols] = '.' if (bz > 40) else 'o' if (bz > -20) else '@'

    # Now play back the frames in sequence
    curs_set(0)  # hide text cursor (supposedly)
    for i in range(NUM_FRAMES):
        # os.system('cls')
        erase()
        string = ''
        for ch in frames[i]:
            string += ch
        mvaddstr(0, 0, string)
        refresh()
        time.sleep(DELAY)
    curs_set(1)  # unhide cursor
    endwin()  # Exit ncurses


# Game starts
clear_screen()
while True:
    print("How many players? -- ", end='')
    try:
        num_of_players = int(input())
        if num_of_players > 0:
            break
    except Exception:
        pass

players = []
board = []
for i in range(num_of_players):
    print("Player name: ", end='')
    name = input()
    p = Player(name)
    players.append(p)
    board.append(p.column)

for i in range(13):
    for j in range(num_of_players):
        print()
        player = players[j]
        clear_screen(board)
        print("~~ ", player.name.upper(), "'S TURN ~~")
        dice_vals = []
        for k in range(5):
            dice_vals.append(random.randint(1, 6))
        diceAction(5, 1, dice_vals)
        for k in range(2, 4):
            while True:
                print("Reroll how many? -- ", end='')
                try:
                    reroll = int(input())
                    if reroll in range(6):
                        break
                except Exception:
                    pass
            if reroll == 5:
                for l in range(reroll):
                    dice_vals[l] = random.randint(1, 6)
            elif reroll == 0:
                break
            else:
                for l in range(reroll):
                    while True:
                        print("Reroll: ", end='')
                        try:
                            select = int(input())
                            if select in range(1, 6):
                                break
                        except Exception:
                            pass
                    dice_vals[select - 1] = random.randint(1, 6)
            clear_screen(board)
            print("~~ ", player.name.upper(), "'S TURN ~~")
            diceAction(5, k, dice_vals)
        movesFunction(dice_vals, player)
        board[j] = player.column
max_final = -1
winner = ''
for j in range(num_of_players):
    if max_final < sum(board[j][1:14]):
        max_final = sum(board[j][1:14])
        winner = board[j][0]

print()
print("The winner is", end='')
for i in range(3):
    sys.stdout.write('.')
    sys.stdout.flush()
    time.sleep(1)

Firework(winner)
os.system('cls')

printNiceWord(winner, True)
