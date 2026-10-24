"""Flask server: exposes the Python engine as a small JSON API."""
import time
from flask import Flask, jsonify, render_template, request
import engine

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/new")
def new():
    b = engine.new_board()
    return jsonify(board=b, legal=engine.get_moves(b, 1))


@app.post("/api/play")
def play():
    """Validate + apply the human's move, return new board."""
    d = request.get_json()
    legal = engine.get_moves(d["board"], 1)
    if d["move"] not in legal:
        return jsonify(error="illegal move"), 400
    b = engine.apply_move(d["board"], d["move"])
    return jsonify(board=b, ai_has_moves=bool(engine.get_moves(b, -1)))


@app.post("/api/ai")
def ai():
    """AI picks a move with minimax (+ optional alpha-beta) and applies it."""
    d = request.get_json()
    s = engine.Searcher(prune=bool(d.get("prune", True)))
    t0 = time.perf_counter()
    move, score = s.best_move(d["board"], int(d.get("depth", 6)))
    ms = round((time.perf_counter() - t0) * 1000)
    if move is None:
        return jsonify(move=None)
    b = engine.apply_move(d["board"], move)
    return jsonify(move=move, board=b, score=score, nodes=s.nodes, ms=ms,
                   legal=engine.get_moves(b, 1))


if __name__ == "__main__":
    app.run(debug=True)
