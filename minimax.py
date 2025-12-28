import copy

# ========================
# AI Parameters
# ========================
AI1_PLAYER = -1
AI2_PLAYER = 1
AI1_DEPTH = 3
AI2_DEPTH = 3  # adjust depths

# ========================
# Evaluation function
# ========================
def evaluate(board_state, player):
    opponent = -player
    disc_diff = sum(row.count(player) for row in board_state) - sum(row.count(opponent) for row in board_state)
    corners = [(0,0),(0,3),(3,0),(3,3)]
    corner_score = sum(1 for r,c in corners if board_state[r][c]==player) - sum(1 for r,c in corners if board_state[r][c]==opponent)
    return disc_diff + 10*corner_score

# ========================
# Board helpers
# ========================
def legal_moves(board_obj, board_state, player):
    return board_obj.findAvailableMoves(board_state, player)

def apply_move(board_obj, board_state, player, move):
    new_board = copy.deepcopy(board_state)
    y, x = move
    board_obj.insertDisc(new_board, player, y, x)
    flips = board_obj.flankableDiscs(y, x, new_board, player)
    for r,c in flips:
        new_board[r][c] *= -1
    return new_board

# ========================
# Minimax algorithm
# ========================
def minimax_score(board_obj, board_state, player, depth, perspective):
    moves = legal_moves(board_obj, board_state, player)
    if not moves or depth == 0:
        return evaluate(board_state, perspective)
    if player == perspective:
        best = -float('inf')
        for m in moves:
            nb = apply_move(board_obj, board_state, player, m)
            score = minimax_score(board_obj, nb, -player, depth-1, perspective)
            best = max(best, score)
        return best
    else:
        best = float('inf')
        for m in moves:
            nb = apply_move(board_obj, board_state, player, m)
            score = minimax_score(board_obj, nb, -player, depth-1, perspective)
            best = min(best, score)
        return best

def ai_best_move(board_obj, board_state, player):
    moves = legal_moves(board_obj, board_state, player)
    if not moves:
        return None

    best_move = None
    if player == AI1_PLAYER:
        best_score = -float('inf')
        for m in moves:
            nb = apply_move(board_obj, board_state, player, m)
            score = minimax_score(board_obj, nb, -player, AI1_DEPTH, AI1_PLAYER)
            if score > best_score:
                best_score = score
                best_move = m
    else:
        best_score = float('inf')
        for m in moves:
            nb = apply_move(board_obj, board_state, player, m)
            score = minimax_score(board_obj, nb, -player, AI1_DEPTH, AI1_PLAYER)
            if score < best_score:
                best_score = score
                best_move = m
    return best_move

# ========================
# AI vs AI initializer
# ========================
def init_ai_vs_ai(game_obj):
    """
    Prepare the game object for AI vs AI play.
    This adds a new attribute that the main loop can call each frame.
    """
    game_obj.ai_vs_ai = True
    game_obj.ai_current_player = AI1_PLAYER

    # Patch the original update() method to include AI move
    orig_update = game_obj.update

    def new_update():
        orig_update()  # keep normal game updates (checks for game over)

        if getattr(game_obj, 'ai_vs_ai', False) and not game_obj.gameOver:
            player = game_obj.ai_current_player
            move = ai_best_move(game_obj.grid, game_obj.grid.gridLogic, player)
            if move:
                y, x = move
                game_obj.grid.insertDisc(game_obj.grid.gridLogic, player, y, x)
                flips = game_obj.grid.flankableDiscs(y, x, game_obj.grid.gridLogic, player)
                for r,c in flips:
                    game_obj.grid.gridLogic[r][c] *= -1
                    game_obj.grid.animateTransitions((r,c), player)

                # Record history for previous/next buttons
                alpha = 'ABCDEFGH'
                moveNotation = f"{alpha[x]}{y+1}"
                if player == -1:
                    game_obj.moveHistory.append([moveNotation, None])
                else:
                    if game_obj.moveHistory:
                        game_obj.moveHistory[-1][1] = moveNotation
                    else:
                        game_obj.moveHistory.append([None, moveNotation])
                game_obj.gridHistory.append([row[:] for row in game_obj.grid.gridLogic])
                game_obj.playerHistory.append(-player)
                game_obj.currentHistoryIndex = len(game_obj.gridHistory)-1

            # Switch player for next AI move
            game_obj.ai_current_player *= -1

    game_obj.update = new_update
