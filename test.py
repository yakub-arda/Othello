SIZE = 4
EMPTY = 0
BLACK = 1
WHITE = -1

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1)
]

counter = 0


def index(r, c):
    return r * SIZE + c


def on_board(r, c):
    return 0 <= r < SIZE and 0 <= c < SIZE


def captures(board, r, c, player, dr, dc):
    i, j = r + dr, c + dc
    found_opponent = False

    while on_board(i, j):
        v = board[index(i, j)]
        if v == -player:
            found_opponent = True
        elif v == player:
            return found_opponent
        else:
            return False
        i += dr
        j += dc
    return False


def legal_moves(board, player):
    moves = []
    for r in range(SIZE):
        for c in range(SIZE):
            if board[index(r, c)] != EMPTY:
                continue
            for dr, dc in DIRECTIONS:
                if captures(board, r, c, player, dr, dc):
                    moves.append((r, c))
                    break
    return moves


def apply_move(board, r, c, player):
    board = list(board)
    board[index(r, c)] = player

    for dr, dc in DIRECTIONS:
        if captures(board, r, c, player, dr, dc):
            i, j = r + dr, c + dc
            while board[index(i, j)] == -player:
                board[index(i, j)] = player
                i += dr
                j += dc

    return tuple(board)


def explore(board, player):
    global counter

    moves = legal_moves(board, player)

    if not moves:
        if not legal_moves(board, -player):
            counter += 1
            print(counter)
            return
        explore(board, -player)
        return

    for r, c in moves:
        explore(apply_move(board, r, c, player), -player)


def initial_board():
    board = [EMPTY] * (SIZE * SIZE)
    m = SIZE // 2
    board[index(m - 1, m - 1)] = WHITE
    board[index(m,     m    )] = WHITE
    board[index(m - 1, m    )] = BLACK
    board[index(m,     m - 1)] = BLACK
    return tuple(board)


if __name__ == "__main__":
    explore(initial_board(), BLACK)
    print("Total paths:", counter)
