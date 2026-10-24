"""Checkers engine: rules + Minimax with Alpha-Beta pruning.
Board = list of 64 ints (row*8+col). 1/2 = human man/king, -1/-2 = AI man/king, 0 = empty.
Human moves up (row decreases), AI moves down. AI is the MAX player."""
import random

DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
WIN = 99999


def new_board():
    b = [0] * 64
    for i in range(64):
        r, c = divmod(i, 8)
        if (r + c) % 2:
            b[i] = -1 if r < 3 else (1 if r > 4 else 0)
    return b


def sign(x):
    return (x > 0) - (x < 0)


def _in(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def _jumps(b, r, c, piece, done):
    """All capture sequences from (r,c). Returns list of (path, captured)."""
    p, king, out = sign(piece), abs(piece) == 2, []
    for dr, dc in DIRS:
        if not king and dr != -p:
            continue
        lr, lc = r + 2 * dr, c + 2 * dc
        if not _in(lr, lc):
            continue
        mid, land = (r + dr) * 8 + c + dc, lr * 8 + lc
        if sign(b[mid]) != -p or mid in done or b[land] != 0:
            continue
        promoted = not king and lr == (0 if p == 1 else 7)   # jump ends on promotion
        sub = [] if promoted else _jumps(b, lr, lc, piece, done + [mid])
        if not sub:
            out.append(([land], [mid]))
        else:
            out += [([land] + pa, [mid] + ca) for pa, ca in sub]
    return out


def get_moves(b, p):
    """Legal moves for side p. Captures are mandatory (if any exist, only captures)."""
    caps, simple = [], []
    for i in range(64):
        if sign(b[i]) != p:
            continue
        r, c = divmod(i, 8)
        t = b[:]; t[i] = 0                       # vacate start square for loop-jumps
        for path, cs in _jumps(t, r, c, b[i], []):
            caps.append({"from": i, "path": path, "caps": cs})
        for dr, dc in DIRS:
            if abs(b[i]) == 1 and dr != -p:
                continue
            if _in(r + dr, c + dc) and b[(r + dr) * 8 + c + dc] == 0:
                simple.append({"from": i, "path": [(r + dr) * 8 + c + dc], "caps": []})
    return caps or simple


def apply_move(b, m):
    n, piece = b[:], b[m["from"]]
    n[m["from"]] = 0
    for x in m["caps"]:
        n[x] = 0
    d = m["path"][-1]
    if piece == 1 and d // 8 == 0:
        piece = 2
    elif piece == -1 and d // 8 == 7:
        piece = -2
    n[d] = piece
    return n


def evaluate(b):
    """Heuristic from AI's view: material (man 100, king 160) + advancement bonus."""
    s = 0
    for i, v in enumerate(b):
        if not v:
            continue
        r = i // 8
        x = 160 if abs(v) == 2 else 100 + 3 * (r if v < 0 else 7 - r)
        s += x if v < 0 else -x
    return s


class Searcher:
    def __init__(self, prune=True):
        self.prune, self.nodes = prune, 0

    def search(self, b, depth, alpha, beta, p):
        self.nodes += 1
        moves = get_moves(b, p)
        if not moves:                                   # side to move has lost
            return -WIN - depth if p == -1 else WIN + depth
        if depth == 0:
            return evaluate(b)
        if p == -1:                                     # MAX (AI)
            best = float("-inf")
            for m in moves:
                best = max(best, self.search(apply_move(b, m), depth - 1, alpha, beta, 1))
                alpha = max(alpha, best)
                if self.prune and beta <= alpha:        # beta cut-off
                    break
            return best
        best = float("inf")                             # MIN (human)
        for m in moves:
            best = min(best, self.search(apply_move(b, m), depth - 1, alpha, beta, -1))
            beta = min(beta, best)
            if self.prune and beta <= alpha:            # alpha cut-off
                break
        return best

    def best_move(self, b, depth):
        moves = get_moves(b, -1)
        if not moves:
            return None, None
        random.shuffle(moves)                           # vary play among equal moves
        best, bm, alpha = float("-inf"), None, float("-inf")
        for m in moves:
            v = self.search(apply_move(b, m), depth - 1, alpha, float("inf"), 1)
            if v > best:
                best, bm = v, m
            alpha = max(alpha, best)
        return bm, best
