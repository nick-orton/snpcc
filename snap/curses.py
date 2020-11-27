import curses
from snap.state import State
from snap.screen import MainScreen, HelpScreen, ClientScreen
import logging

_LOGGER = logging.getLogger(__name__)

def initColors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

def update_state_from_keypress(key, state):
    if key in [curses.KEY_DOWN, ord('j')]:
        state.next_client()
    if key in [curses.KEY_UP, ord('k')]:
        state.prev_client()
    if key == ord('m'):
        state.toggle_mute()
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
    _LOGGER.info("Starting ncsnpcc")
    initColors()
    stdscr.clear()
    stdscr.refresh()

    key = 0

    state = State(MainScreen())

    while (key != ord('q')):
        stdscr.clear()

        update_state_from_keypress(key, state)

        state.screen.draw(state, stdscr)
        stdscr.refresh()

        key = stdscr.getch()

def main():
    curses.wrapper(draw_screen)
