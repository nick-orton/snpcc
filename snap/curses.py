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
    if key == ord('1'):
        state.screen = HelpScreen()
    if key == ord('2'):
        state.screen = MainScreen()
    if key == ord('3'):
        state.screen = ClientScreen()

class Screen():
    def __init__(self, name):
        self.name = name

    def drawS(self, state, stdscr):
        self.draw_title(stdscr)
        self.draw(state, stdscr)
        self.draw_status_bar(stdscr)

    def draw_title(self, stdscr):
        stdscr.addstr(0, 0, "{}".format(self.name))

    def draw_status_bar(self, stdscr):
        height, width = stdscr.getmaxyx()
        statusbarstr = "Press 'q' to exit, '1' for help "
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))


class MainScreen(Screen):
    def __init__(self):
        super().__init__("Main")

    def draw(self, state, stdscr):
        out = "Streams         "
        for stream in state.streams:
            if stream == state.active_stream:
                out += "[ {} ] ".format(stream.name)
            else:
                out += "{} ".format(stream.name)
        stdscr.addstr(3, 0, out)

        for idx, client in enumerate(state.clients):
            if state.client == client:
                color = curses.color_pair(1)
            elif client.muted:
                color = curses.color_pair(2)
            else:
                color = curses.color_pair(4)

            client_display = status_string(client)
            stdscr.addstr(5 + idx, 0, client_display, color)

class HelpScreen(Screen):
    def __init__(self):
        super().__init__("Help")

    def draw(self, state, stdscr):
        stdscr.addstr(3, 0, "Navigation")
        stdscr.addstr(4, 0, "----------")
        stdscr.addstr(5, 0, "       ")
        stdscr.addstr(6, 0, "1     Help Screen (this screen)")
        stdscr.addstr(7, 0, "2     Main Screen")
        stdscr.addstr(8, 0, "3     Client Screen")
        stdscr.addstr(9, 0, "q     quit application")
        stdscr.addstr(10, 0, "       ")
        stdscr.addstr(11, 0, "Commands")
        stdscr.addstr(12, 0, "--------")
        stdscr.addstr(13, 0, "           ")
        stdscr.addstr(14, 0, "j,k   change selected client")
        stdscr.addstr(15, 0, "s     change selected stream")
        stdscr.addstr(16, 0, "h     lower volume on selected client")
        stdscr.addstr(17, 0, "l     raise volume on selected client")
        stdscr.addstr(18, 0, "l     mute/unmute selected client")

class ClientScreen(Screen):
    def __init__(self):
        super().__init__("Client")

    def draw(self, state, stdscr):
        stdscr.addstr(3, 0, "Client")
        stdscr.addstr(4, 0, "------")
        stdscr.addstr(5, 0, "       ")
        stdscr.addstr(6, 0, "Name          {}".format(state.client.name))
        stdscr.addstr(7, 0, "Identifier    {}".format(state.client.identifier))
        stdscr.addstr(8, 0, "Volume        {}".format(state.client.volume))
        stdscr.addstr(9, 0, "Muted         {}".format(state.client.muted))
        stdscr.addstr(10, 0, "Latency       {}".format(state.client.latency))
        stdscr.addstr(11, 0, "Stream        {}".format(state.client.group.stream))
        stdscr.addstr(12, 0, "Version       {}".format(state.client.version))

def draw_screen(stdscr):
    _LOGGER.info("Starting ncsnpcc")
    initColors()
    stdscr.clear()
    stdscr.refresh()

    key = 0

    screen = MainScreen()
    state = State(screen)

    while (key != ord('q')):
        stdscr.clear()

        handle_keypress(key, state)

        state.screen.drawS(state, stdscr)
        stdscr.refresh()

        key = stdscr.getch()

def main():
    curses.wrapper(draw_screen)
