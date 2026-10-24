# Checkers Playing Agent — Minimax / Alpha-Beta Pruning

Play checkers against an AI. Legal moves and captures are highlighted.

## Tech stack
| Layer | Tech | Role |
|---|---|---|
| Game logic + AI | Python 3 (`engine.py`) | Rules, forced captures, multi-jumps, kings, Minimax + Alpha-Beta |
| Server | Flask (`app.py`) | JSON API between browser and engine |
| Frontend | HTML + CSS + vanilla JS (`templates/index.html`) | Draws board, highlights, calls API |
| Testing | plain `assert` (`tests.py`) | Rules + proof that pruning keeps the same result |

## Run
```
pip install -r requirements.txt
python tests.py      # optional sanity check
python app.py        # open http://127.0.0.1:5000
```

## Architecture
Browser (JS) --JSON--> Flask routes --> engine.py
- `GET /api/new`  -> start board + human legal moves
- `POST /api/play` -> validate and apply human move
- `POST /api/ai`  -> AI search, returns move, score, nodes searched, time

All rules and AI are in Python; JS only renders.

## Algorithm
- State: 64-int list. AI = MAX player, human = MIN player.
- Minimax explores moves to a fixed depth; leaves scored by `evaluate()`:
  man = 100 (+3 per row advanced), king = 160.
- Alpha-beta: keep window [alpha, beta]; stop exploring a branch once beta <= alpha,
  because the opponent would never allow that line. Same answer as minimax, fewer nodes.
- Mandatory capture also shrinks the branching factor.
- No/low moves left = loss for the side to move (terminal score +-99999).

## Viva questions to prepare
1. Why does alpha-beta return the same value as minimax?
2. Best/worst case complexity: O(b^(d/2)) vs O(b^d). What decides which you get?
3. How would move ordering improve pruning?
4. Limits of this evaluation function? What would you add (back-row, mobility, center control)?
5. Why depth-limited search instead of full game tree?

## Possible extensions
Iterative deepening, transposition table, better evaluation, draw rule, undo, AI vs AI.
