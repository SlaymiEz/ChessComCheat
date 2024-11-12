from bs4 import BeautifulSoup
import re

class Parser:
    def __init__(self):
        self.soup = None
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.xfen = ""

    def scan(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")
        chess_board = self.soup.find("wc-chess-board")
        if chess_board:
            formatted_html = chess_board.prettify()
            effects_index = list(re.finditer(r'<!--/Effects-->', formatted_html))
            pieces_index = list(re.finditer(r'<!--/Pieces-->', formatted_html))

            if len(effects_index) >= 2 and len(pieces_index) > 0:
                second_effects_pos = effects_index[1].end()  # End position of the second <!--/Effects-->
                pieces_pos = pieces_index[0].start()  # Start position of the first <!--/Pieces-->
                content_between = formatted_html[second_effects_pos:pieces_pos]
                self.html_to_X_FEN(content_between)
            else:
                print("Could not find the correct comment markers.")
        else:
            print("wc-chess-board element not found.")

    def html_to_X_FEN(self, html_content):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.soup = BeautifulSoup(html_content, "html.parser")
        divs = self.soup.find_all("div", class_="piece")
        positions = []

        for div in divs:
            classes = div.get("class", [])
            filtered_classes = [cls for cls in classes if cls != 'piece']
            positions.append(" ".join(filtered_classes))

        for position in positions:
            cool_list = position.split()
            normal_list = [cool_list[0], cool_list[1]]
            piece, square = normal_list #piece = wr square = square-51
            square = re.search(r'\d+', square).group()

            piece = self.rename_piece(piece)
            square = self.rename_square(square)
            row = int(square[0])
            column = int(square[1])

            self.board[column-1][row-1] = piece

        xfen = ''
        for row in self.board:
            empty_count = 0
            for cell in row:
                if cell == ' ':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        xfen += str(empty_count)
                        empty_count = 0
                    xfen += cell
            if empty_count > 0:
                xfen += str(empty_count)
            xfen += '/'

        # Remove the trailing '/'
        xfen = xfen[:-1]
        self.xfen = xfen

    @staticmethod
    def rename_piece(piece):
        if piece[0] == 'b':
            piece = piece[1]
        elif piece[0] == 'w':
            piece = piece[1].upper()
        return piece
    @staticmethod
    def rename_square(square):
        first_digit = int(str(square)[0])
        second_digit = int(str(square)[1])

        mapping = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
        second_digit = mapping.get(second_digit)

        return f"{first_digit}{second_digit}"
    @staticmethod
    def move_to_square(square_number, move):
        move = str(move)
        square = ""

        if square_number == 1:
            square = move[:2]
        elif square_number == 2:
            square = move[-2:]

        mapping = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

        mapped_value = mapping.get(square[0], square[0])
        square = str(mapped_value) + square[1]

        return square
