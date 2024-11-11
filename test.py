import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("Resources/stockfish-engine.exe")
board = chess.Board()
board.set_board_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")  # Just piece placement
board.turn = chess.WHITE  # w or b
board.castling_rights = chess.BB_A1 | chess.BB_H1 | chess.BB_A8 | chess.BB_H8  # This sets all castling rights

# Both time (in seconds) and depth constraints
result = engine.play(board, chess.engine.Limit(time=2, depth=20))
best_move = result.move

print(f"Best move: {best_move}")

engine.quit()