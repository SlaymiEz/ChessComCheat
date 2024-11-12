from Parser import Parser
import chess
import chess.engine

class Engine:
    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci("Resources/stockfish-engine.exe")
        self.engine.configure({"Threads": 24})
        self.board = chess.Board()


    def get_move(self, color, html):
        parser = Parser()
        parser.scan(html)
        xfen = parser.xfen

        self.board.set_board_fen(xfen)
        if color == "w":
            self.board.turn = chess.WHITE
        elif color == "b":
            self.board.turn = chess.BLACK
        self.board.castling_rights = 0

        result = self.engine.play(self.board, chess.engine.Limit(depth=3))

        best_move = result.move
        print(f"Best move: {best_move}")
        return best_move



