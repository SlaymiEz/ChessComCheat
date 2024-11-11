from Browser import Browser
import threading

from Engine import Engine
from Parser import Parser

browser = Browser()

def run_browser():
    browser.open_browser()

browser_thread = threading.Thread(target=run_browser)
browser_thread.start()

while True:
    userInput = input("'start', 'exit' : ")
    if userInput == "start":
        browser.clear_squares()
        color = input("b or w ? : ")
        while userInput != "quit":
            browser.clear_squares()
            move = Engine.get_move(color, browser.driver.page_source)
            first_square = Parser.move_to_square(1, move) # Ex : 42
            second_square = Parser.move_to_square(2, move) # Ex : 44
            browser.color_square(first_square)
            browser.color_square(second_square)
            userInput = input("quit to exit, enter to continue playing : ")
    if userInput == "exit":
        exit(0)