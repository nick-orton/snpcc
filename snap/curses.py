import curses
from snap import status_string
from snap import snap
import logging

_LOGGER = logging.getLogger(__name__)

def draw_clients(stdscr, y_offset, clients, selected):
    for idx, client in enumerate(clients):
        #_LOGGER.info("%s :: %s", type(client), client.muted)
        if selected == client:
            color = curses.color_pair(1)
        elif client.muted:
            color = curses.color_pair(2)
        else:
            color = curses.color_pair(4)

        client_display = status_string(client)
        stdscr.addstr(y_offset + idx, 0, client_display, color)

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

class State():
    """ Representation of the application state. Methods for modifying state.  """
    def __init__(self):
        self.clients = snap.server.clients
        self.client = self.clients[0]
        self.active_stream = snap.get_active_stream()
        self.streams = snap.server.streams

    def next_stream(self):
        if(self.active_stream):
            idx = self.streams.index(self.active_stream) + 1
            if idx >= len(self.streams):
                idx = 0
            stream = self.streams[idx]
            snap.set_stream(stream)
            self.active_stream = stream

    def next_client(self):
        y = self.clients.index(self.client)
        y = y + 1
        y = min(len(self.clients)-1, y)
        self.client = self.clients[y]

    def prev_client(self):
        y = self.clients.index(self.client)
        y = y - 1
        y = max(0, y)
        self.client = self.clients[y]

    def toggle_mute(self):
       if(self.client.muted):
           snap.mute(self.client, False)
       else:
           snap.mute(self.client, True)

    def lower_volume(self):
       volume = max(0, self.client.volume - 5)
       snap.set_volume(self.client, volume)

    def raise_volume(self):
       volume = min(100, self.client.volume + 5)
       snap.set_volume(self.client, volume)

def draw_screen(stdscr):
    _LOGGER.info("Starting ncsnpcc")
    initColors()
    stdscr.clear()
    stdscr.refresh()

    key = 0

    state = State()

    while (key != ord('q')):
        stdscr.clear()

        handle_keypress(key, state)
        # Draw Screen
        draw_streams(stdscr, 0, state.streams, state.active_stream)
        draw_clients(stdscr, 2, state.clients, state.client)
        draw_status_bar(stdscr)
        stdscr.refresh()

        key = stdscr.getch()

def draw_streams(stdscr, y_offset, streams, active_stream):
    out = "Streams: "
    for stream in streams:
        if stream == active_stream:
            out += "[ {} ] ".format(active_stream.name)
        else:
            out += "{} ".format(stream.name)
    stdscr.addstr(y_offset, 0, out)

def draw_status_bar(stdscr):
    height, width = stdscr.getmaxyx()
    statusbarstr = "Press 'q' to exit , 'hjkl' for volume , or 's' to change stream"
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height-1, 0, statusbarstr)
    stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    stdscr.attroff(curses.color_pair(3))

def main():
    curses.wrapper(draw_screen)
