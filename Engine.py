from Parser import Parser
import chess
import chess.engine

class Engine:
    #def __init__(self, color, html):


    @staticmethod
    def get_move(color, html):
        engine = chess.engine.SimpleEngine.popen_uci("Resources/stockfish-engine.exe")
        engine.configure({"Threads": 24})

        parser = Parser()
        parser.scan(html)
        xfen = parser.xfen
        board = chess.Board()
        board.set_board_fen(xfen)
        if color == "w":
            board.turn = chess.WHITE
        elif color == "b":
            board.turn = chess.BLACK
        board.castling_rights = 0

        result = engine.play(board, chess.engine.Limit(depth=20))

        best_move = result.move
        print(f"Best move: {best_move}")
        engine.quit()
        return best_move



