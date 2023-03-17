#!/usr/bin/python

import curses
import time

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
screen.nodelay(True)
screen.leaveok(True)

x = 0
y = 0

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_RIGHT:
            x += 1
        elif char == curses.KEY_LEFT:
            x -= 1
        elif char == curses.KEY_UP:
            y += 1
        elif char == curses.KEY_DOWN:
            y -= 1
        else:
            screen.addstr(0, 0, f'x:{x:4} y:{y:4}')
        time.sleep(0.1)
finally:
    # shut down cleanly
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()