from typing import Tuple, List

X = "X"
O = "O"
EMPTY = None


def initial_state() -> List[List[str]]:
    """Returns starting state of the board."""
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board: List[List[str]]) -> str:
    """Returns player who has the next turn on a board."""
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board: List[List[str]]) -> List[Tuple[int, int]]:
    """Returns a list of all possible actions (i, j) available on the board."""
    return {(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == EMPTY}


def result(board: List[List[str]], action: Tuple[int, int]) -> List[List[str]]:
    """Returns the board that results from making move (i, j) on the board."""
    i, j = action
    if board[i][j] is not EMPTY or (i, j) not in actions(board):
        raise Exception("Invalid action")
    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board: List[List[str]]) -> str:
    """Returns the winner of the game if there is one."""
    for player in (X, O):
        # Check rows
        for row in board:
            if row.count(player) == 3:
                return player
        # Check columns
        for j in range(3):
            if all(board[i][j] == player for i in range(3)):
                return player
        # Check diagonals
        if all(board[i][i] == player for i in range(3)):
            return player
        if all(board[i][2 - i] == player for i in range(3)):
            return player
    return None


def terminal(board: List[List[str]]) -> bool:
    """Returns True if the game is over, False otherwise."""
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board: List[List[str]]) -> int:
    """Returns 1 if X has won the game, -1 if O has won, 0 otherwise."""
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0


def alphabeta(board: List[List[str]], alpha: float = -float('inf'), beta: float = float('inf'), depth: int = 0,
              maximizing_player: bool = True) -> Tuple[float, Tuple[int, int]]:
    """
    Returns the optimal action for the current player on the board using the minimax algorithm
    with alpha-beta pruning.
    """
    if terminal(board):
        return utility(board), None

    if maximizing_player:
        best_score = -float('inf')
        best_move = None
    else:
        best_score = float('inf')
        best_move = None

    for action in actions(board):
        new_board = result(board, action)
        score, _ = alphabeta(new_board, alpha, beta, depth + 1, not maximizing_player)

        if maximizing_player:
            if score > best_score:
                best_score = score
                best_move = action
            alpha = max(alpha, best_score)
        else:
            if score < best_score:
                best_score = score
                best_move = action
            beta = min(beta, best_score)

        if alpha >= beta:
            break

    return best_score, best_move


def minimax(board: List[List[str]]) -> Tuple[int, int]:
    """
    Returns the optimal action for the current player on the board using the minimax algorithm
    with alpha-beta pruning.
    """
    current_player = player(board)
    maximizing_player = current_player == X
    _, best_move = alphabeta(board, maximizing_player=maximizing_player)
    return best_move
