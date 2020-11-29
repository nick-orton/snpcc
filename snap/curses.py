""" Encapsulates ncurses logic and runs the primary event loop """

import curses
import logging
from snap.state import State
from snap.screen import MainScreen, HelpScreen, ClientScreen

_LOGGER = logging.getLogger(__name__)

def init_colors():
    """ Initialize the color scheme for the application """
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

def update_state_from_keypress(key, state):
    """ Handle keyboard input """
    if key in [curses.KEY_DOWN, ord('j')]:
        state.next_client()
    if key in [curses.KEY_UP, ord('k')]:
        state.prev_client()
    if key == ord('m'):
        state.toggle_mute()
    if key == ord('a'):
        state.mute_all()
    if key in [curses.KEY_LEFT, ord('h')]:
        state.lower_volume()
    if key in [curses.KEY_RIGHT, ord('l')]:
        state.raise_volume()
    if key == ord('s'):
        state.next_stream()
    if key == ord('1'):
        state.screen = HelpScreen()
    if key == ord('2'):
        state.screen = MainScreen()
    if key == ord('3'):
        state.screen = ClientScreen()

def draw_screen(stdscr):
    """ Main event loop.  Listens for keystrokes and draws the screen. """
    _LOGGER.info("Starting ncsnpcc")
    init_colors()
    stdscr.clear()
    stdscr.refresh()

    key = 0

    state = State(MainScreen())

    while key != ord('q'):
        stdscr.clear()

        update_state_from_keypress(key, state)

        state.screen.draw(state, stdscr)
        stdscr.refresh()

        key = stdscr.getch()

def main():
    """ Wraps the main event loop in curses wrapper. """
    curses.wrapper(draw_screen)
