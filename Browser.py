from copyreg import pickle

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

from Parser import Parser


class Browser:
    def __init__(self):
        chromium_path = "Resources/ChromeForTesting/chrome.exe"
        chromedriver_path = "Resources/chromedriver.exe"

        chrome_options = Options()
        chrome_options.binary_location = chromium_path

        service = Service(chromedriver_path)

        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def open_browser(self):
        self.driver.get("https://www.chess.com")
        time.sleep(3)  # Wait for the page to load
        while True:
           time.sleep(1)

    def color_square(self, square):
        script = f"""
        const board = document.querySelector("wc-chess-board");
        if (board) {{
            const highlightDiv = document.createElement("div");
            highlightDiv.className = "highlight square-{square}";
            highlightDiv.style.backgroundColor = "rgb(82, 176, 220)";
            highlightDiv.style.opacity = "0.8";
            highlightDiv.setAttribute("data-test-element", "highlight");
            board.appendChild(highlightDiv);
        }}
        """
        self.driver.execute_script(script)

    def clear_squares(self):
        script = """
        const divs = document.querySelectorAll("wc-chess-board div");
        divs.forEach(div => {
            if (div.style.backgroundColor === "rgb(82, 176, 220)") {
                div.className = "element-pool";
                div.style.backgroundColor = "";
                div.style.opacity = "";
                div.setAttribute("data-test-element", "");
            }
        });
        """
        self.driver.execute_script(script)


    def opponent_has_played(self, color):
        script = """
        const board = document.querySelector("wc-chess-board");
        const highlightedSquares = [];
        if (board) {
            const divs = board.querySelectorAll("div");
            for (let div of divs) {
                if (div.style.backgroundColor === "rgb(255, 255, 51)") {
                    const classes = div.className.split(" ");
                    for (let cls of classes) {
                        if (cls.startsWith("square-")) {
                            highlightedSquares.push(cls.slice(-2));  // Get the last two characters
                        }
                    }
                }
            }
        }
        return highlightedSquares;
        """

        if self.driver.execute_script(script) is None:
            return False

        square_numbers = self.driver.execute_script(script)

        for square_number in square_numbers:
            square_number = Parser.rename_square(square_number)
            parser = Parser()
            parser.scan(self.driver.page_source)

            row = int(square_number[0])
            column = int(square_number[1])

            piece = parser.board[column-1][row-1]

            if color == 'b':
                if piece.isupper():
                    print("Enemy played")
                    return True
            elif color == 'w':
                if piece.islower():
                    print("Enemy played")
                    return True
            else:
                return False