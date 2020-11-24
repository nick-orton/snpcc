import curses
from snap import status_string
from snap.state import State
import logging

_LOGGER = logging.getLogger(__name__)

def initColors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

def handle_keypress(key, state):
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

class MainScreen():
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def draw(self, state):
        out = "Streams:        "
        for stream in state.streams:
            if stream == state.active_stream:
                out += "[ {} ] ".format(stream.name)
            else:
                out += "{} ".format(stream.name)
        self.stdscr.addstr(0, 0, out)

        for idx, client in enumerate(state.clients):
        #_LOGGER.info("%s :: %s", type(client), client.muted)
            if state.client == client:
                color = curses.color_pair(1)
            elif client.muted:
                color = curses.color_pair(2)
            else:
                color = curses.color_pair(4)

            client_display = status_string(client)
            self.stdscr.addstr(2 + idx, 0, client_display, color)


    def draw_status_bar(self):
        height, width = self.stdscr.getmaxyx()
        statusbarstr = "Press 'q' to exit , '1' for help, 'hjkl' for volume , or 's' to change stream"
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(height-1, 0, statusbarstr)
        self.stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        self.stdscr.attroff(curses.color_pair(3))

class HelpScreen():
    def __init__(self, stdscr):
        self.stdscr = stdscr
    def draw(self, state):
        self.stdscr.addstr(0, 0, "Navigation")
        self.stdscr.addstr(1, 0, "-------")
        self.stdscr.addstr(2, 0, "       ")
        self.stdscr.addstr(3, 0, "1     Help Screen (this screen)")
        self.stdscr.addstr(4, 0, "2     Main Screen")
        self.stdscr.addstr(5, 0, "3     Client Screen")
        self.stdscr.addstr(6, 0, "q     quit application")
        self.stdscr.addstr(7, 0, "       ")
        self.stdscr.addstr(8, 0, "Main Screen")
        self.stdscr.addstr(9, 0, "-----------")
        self.stdscr.addstr(10, 0, "           ")
        self.stdscr.addstr(11, 0, "j,k   change active client")
        self.stdscr.addstr(12, 0, "s     change active stream")
        self.stdscr.addstr(13, 0, "h     lower volume on selected client")
        self.stdscr.addstr(14, 0, "l     raise volume on selected client")

    def draw_status_bar(self):
        height, width = self.stdscr.getmaxyx()
        statusbarstr = "Press 'q' to exit "
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(height-1, 0, statusbarstr)
        self.stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        self.stdscr.attroff(curses.color_pair(3))

def draw_screen(stdscr):
    _LOGGER.info("Starting ncsnpcc")
    initColors()
    stdscr.clear()
    stdscr.refresh()

    key = 0

    state = State()
    screen = MainScreen(stdscr)

    while (key != ord('q')):
        stdscr.clear()

        handle_keypress(key, state)

        if key == ord('1'):
            screen = HelpScreen(stdscr)
        if key == ord('2'):
            screen = MainScreen(stdscr)

        screen.draw(state)
        screen.draw_status_bar()
        stdscr.refresh()

        key = stdscr.getch()

def main():
    curses.wrapper(draw_screen)
