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

def set_cursor(key, clients, selected):

    y = clients.index(selected)
    if key in [curses.KEY_DOWN, ord('j')]:
        y = y + 1
    elif key in [curses.KEY_UP, ord('k')]:
        y = y - 1

    y = max(0, y)
    y = min(len(clients)-1, y)
    return clients[y]

def initColors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

def change_client(selected, key):
    if key == ord('m'):
       if(selected.muted):
           snap.mute(selected, False)
       else:
           snap.mute(selected, True)
    if key in [curses.KEY_LEFT, ord('h')]:
       volume = max(0, selected.volume - 5)
       snap.set_volume(selected, volume)
    if key in [curses.KEY_RIGHT, ord('l')]:
       volume = min(100, selected.volume + 5)
       snap.set_volume(selected, volume)

def change_stream(key):
    if key == ord('s'):
        idx = snap.streams().index(snap.active_stream) + 1
        if idx >= len(snap.streams()):
            idx = 0
        snap.set_stream(snap.streams()[idx])


def draw_screen(stdscr):
    _LOGGER.info("Starting ncsnpcc")
    initColors()
    stdscr.clear()
    stdscr.refresh()

    key = 0

    clients = snap.clients()
    client = clients[0]

    while (key != ord('q')):
        stdscr.clear()

        client  = set_cursor(key, clients, client)

        change_client(client, key)
        change_stream(key)

        # Draw Screen
        draw_streams(stdscr, 0,  snap.active_stream)
        draw_clients(stdscr, 2, clients, client)
        draw_status_bar(stdscr)
        stdscr.refresh()

        key = stdscr.getch()

def draw_streams(stdscr, y_offset, active_stream):
    out = "Streams: "
    for stream in snap.streams():
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
