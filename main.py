import time

from pynput import keyboard

from Browser import Browser
import threading

from Engine import Engine
from Parser import Parser

browser = Browser()

end_pressed = False
arrow_up_pressed = False
space_pressed = False

def on_press(key):
    global end_pressed, arrow_up_pressed, space_pressed
    if key == keyboard.Key.end:
        end_pressed = True
    if key == keyboard.Key.up:
        arrow_up_pressed = True
    if key == keyboard.Key.space:
        space_pressed = True

def on_release(key):
    global end_pressed, arrow_up_pressed, space_pressed
    if key == keyboard.Key.end:
        end_pressed = False
    if key == keyboard.Key.up:
        arrow_up_pressed = False
    if key == keyboard.Key.space:
        space_pressed = False

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

def get_move():
    browser.clear_squares()
    move = engine.get_move(color, browser.driver.page_source)
    first_square = Parser.move_to_square(1, move) # Ex : 42
    second_square = Parser.move_to_square(2, move) # Ex : 44
    browser.color_square(first_square)
    browser.color_square(second_square)

def run_browser():
    browser.open_browser()

browser_thread = threading.Thread(target=run_browser)
browser_thread.start()

engine = Engine()

while True:
    userInput = input("'start', 'exit' : ")
    if userInput == "start":
        browser.clear_squares()
        color = input("b or w ? : ")
        while not end_pressed:
            if browser.opponent_has_played(color):
                get_move()
                while not space_pressed:
                    pass
                print("Played, waiting for move")
            pass
    if userInput == "exit":
        exit(0)

