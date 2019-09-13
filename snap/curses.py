import curses
from snap import status_string
from snap import snap
import logging

_LOGGER = logging.getLogger(__name__)

def draw_clients(stdscr, clients, selected):
    for idx, client in enumerate(clients):
        #_LOGGER.info("%s :: %s", type(client), client.muted)
        if selected == client:
            color = curses.color_pair(1)
        elif client.muted:
            color = curses.color_pair(2)
            print(client.muted)
        else:
            color = curses.color_pair(4)

        client_display = status_string(client)
        stdscr.addstr(idx, 0, client_display, color)

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

def draw_screen(stdscr):
    _LOGGER.info("Starting ncsnpcc")
    initColors()
    stdscr.clear()
    stdscr.refresh()

    key = 0

    clients = snap.clients()
    selected = clients[0]

    while (key != ord('q')):
        stdscr.clear()

        selected  = set_cursor(key, clients, selected)

        change_client(selected, key)

        # Draw Screen
        draw_clients(stdscr, clients, selected)
        draw_status_bar(stdscr, selected.friendly_name)
        stdscr.refresh()

        key = stdscr.getch()

def draw_status_bar(stdscr, cursor_y):
    height, width = stdscr.getmaxyx()
    statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}".format(cursor_y)
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height-1, 0, statusbarstr)
    stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    stdscr.attroff(curses.color_pair(3))

def main():
    curses.wrapper(draw_screen)
