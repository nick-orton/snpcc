""" Encapsulates ncurses logic and runs the primary event loop """

import curses
import logging
from snap.state import State
from snap.screen import Screens

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
    if key == ord(' '):
        state.refresh()
    if key == ord('m'):
        state.toggle_mute()
    if key == ord('a'):
        state.mute_all()
    if key in [curses.KEY_LEFT, ord('h')]:
        state.lower_volume()
    if key == ord('H'):
        state.lower_volume_all()
    if key in [curses.KEY_RIGHT, ord('l')]:
        state.raise_volume()
    if key == ord('L'):
        state.raise_volume_all()
    if key == ord('s'):
        state.next_stream()
    if key == ord('1'):
        state.screen = Screens.help_screen
    if key == ord('2'):
        state.screen = Screens.main_screen
    if key == ord('3'):
        state.screen = Screens.client_screen

def build_loop(state):

  def event_loop(stdscr):
      """ Main event loop.  Listens for keystrokes and draws the screen. """
      _LOGGER.info("Starting ncsnpcc")
      init_colors()
      stdscr.clear()
      stdscr.refresh()

      key = 0


      while key != ord('q'):
          stdscr.clear()

          update_state_from_keypress(key, state)

          state.screen.draw(state, stdscr)
          stdscr.refresh()

          key = stdscr.getch()
  return event_loop

def main(state):
    """ Wraps the main event loop in curses wrapper. """
    curses.wrapper(build_loop(state))
