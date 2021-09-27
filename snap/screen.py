""" Module for drawing the applicaiton screens """
import abc
import curses
from string import Template

class Screen(metaclass=abc.ABCMeta):
    """ Superclass for all screens"""
    def __init__(self, name):
        self.name = name

    def draw(self, state, stdscr):
        """ Draws the screen in three parts, title, content, status-bar."""
        self.draw_title(stdscr)
        self.content(state, stdscr)
        Screen.draw_status_bar(stdscr)

    @abc.abstractmethod
    def content(self, state, stdscr):
        """ Draw the content for the screen. """

    def draw_title(self, stdscr):
        """ Draw the screen title """
        _, width = stdscr.getmaxyx()
        stdscr.addstr(0, 0, "{}".format(self.name), curses.A_BOLD)
        stdscr.hline(1,0, curses.ACS_HLINE, width)

    @staticmethod
    def draw_status_bar(stdscr):
        """ Draw the screen footer """
        height, width = stdscr.getmaxyx()
        statusbarstr = "Press 'q' to exit, '1' for help "
        stdscr.hline(height-2,0, curses.ACS_HLINE, width)
        stdscr.addstr(height-1, 0, statusbarstr)

def _volume_string(value):
    stars = int(value / 2)
    spaces = 50 - stars
    return "|" + u'\u2588'*stars + " "*spaces + "|"

def _status_string(client, max_len, selected):
    name = client.friendly_name
    if selected:
        name = "[{}]".format(name)
    if client.muted:
        name = "{} (m)".format(name)
    name = name.ljust(max_len + 8, ' ')
    return "{}{}".format(name, _volume_string(client.volume))

class MainScreen(Screen):
    """ Displays the streams, clients, and their volume """
    def __init__(self):
        super().__init__("Main")

    def content(self, state, stdscr):
        max_client_name_len = max([len(client.friendly_name) for client in
            state.clients])
        out = "Streams".ljust(max_client_name_len + 8, ' ')
        for stream in state.streams:
            if stream == state.active_stream:
                out += "[{}] ".format(stream.name)
            else:
                out += "{} ".format(stream.name)
        stdscr.addstr(3, 0, out)

        for idx, client in enumerate(state.clients):
            selected = False
            if state.client == client:
                color = curses.color_pair(1)
                selected = True
            elif client.muted:
                color = curses.color_pair(2)
            else:
                color = curses.color_pair(4)

            client_display = _status_string(client, max_client_name_len,
                    selected)
            stdscr.addstr(5 + idx, 0, client_display, color)

HELP_SCREEN_TEXT = """
Navigation
----------

  1     Help Screen (this screen)
  2     Main Screen
  3     Client Screen
  q     quit application

Commands
--------

  j,k     change selected client
  s       change selected stream
  h       lower volume on selected client
  l       raise volume on selected client
  H       lower volume on all clients
  L       raise volume on all clients
  m       mute/unmute selected client
  a       mute/unmute all clients
  space   refresh the screen"""


class HelpScreen(Screen):
    """ Instructions for how to use snpcc """
    def __init__(self):
        super().__init__("Help")

    def content(self, state, stdscr):
        for idx,line in enumerate(HELP_SCREEN_TEXT.splitlines()):
            stdscr.addstr(2+idx, 0, line)

CLIENT_SCREEN = """
Name          $name
Identifier    $identifier
Volume        $volume
Muted         $muted
Latency       $latency
Stream        $active_stream
Version       $version"""

class ClientScreen(Screen):
    """ Display details about the currently selected client"""
    def __init__(self):
        super().__init__("Client")

    def content(self, state, stdscr):
        template = Template(CLIENT_SCREEN)
        vals = template.substitute(name=state.client.name,
                                   identifier=state.client.identifier,
                                   volume=state.client.volume,
                                   muted=state.client.muted,
                                   latency=state.client.latency,
                                   active_stream=state.active_stream.name,
                                   version=state.client.version)

        for idx,line in enumerate(vals.splitlines()):
            stdscr.addstr(2+idx, 0, line)

class Screens():
    main_screen = MainScreen()
    help_screen = HelpScreen()
    client_screen = ClientScreen()
