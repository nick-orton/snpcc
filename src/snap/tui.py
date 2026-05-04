""" Encapsulates ncurses logic and runs the primary event loop """

import curses
import logging
import os
import subprocess
from snap.state import State
from snap.screen import Screens

_LOGGER = logging.getLogger(__name__)

def _set_terminal_title(title):
    try:
        with open('/dev/tty', 'w') as tty:
            tty.write(f"\x1b]2;{title}\x07")
    except OSError:
        pass

def _tmux_rename(title):
    """Rename the current tmux window and disable automatic-rename.
    Returns the prior automatic-rename value so it can be restored."""
    try:
        result = subprocess.run(
            ['tmux', 'show-window-options', '-v', 'automatic-rename'],
            capture_output=True, text=True
        )
        prior = result.stdout.strip() or 'on'
        subprocess.run(['tmux', 'set-window-option', 'automatic-rename', 'off'], check=False)
        subprocess.run(['tmux', 'rename-window', title], check=False)
    except OSError:
        prior = None
    return prior

def _tmux_restore(prior):
    """Restore automatic-rename to its previous value."""
    try:
        subprocess.run(['tmux', 'set-window-option', 'automatic-rename', prior], check=False)
    except OSError:
        pass

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
        state.client.toggle_mute()
    if key in [ord('a'), ord('M')]:
        state.mute_all()
    if key in [curses.KEY_LEFT, ord('h')]:
        state.client.lower_volume()
    if key == ord('H'):
        state.lower_volume_all()
    if key in [curses.KEY_RIGHT, ord('l')]:
        state.client.raise_volume()
    if key == ord('L'):
        state.raise_volume_all()
    if key == ord('s'):
        state.next_stream()
    if key in [ord('1'), ord('?')]:
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
          state.clear_cache()

          update_state_from_keypress(key, state)

          state.screen.draw(state, stdscr)
          stdscr.refresh()

          key = stdscr.getch()
  return event_loop

def main(state):
    """ Wraps the main event loop in curses wrapper. """
    if os.environ.get('TMUX'):
        prior = _tmux_rename("snpcc")
        try:
            curses.wrapper(build_loop(state))
        finally:
            if prior is not None:
                _tmux_restore(prior)
    else:
        _set_terminal_title("snpcc")
        curses.wrapper(build_loop(state))
