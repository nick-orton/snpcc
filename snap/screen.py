import curses
from string import Template

class Screen():
    def __init__(self, name):
        self.name = name

    def draw(self, state, stdscr):
        self.draw_title(stdscr)
        self.content(state, stdscr)
        self.draw_status_bar(stdscr)

    #TODO: The title looks bad now, fix
    def draw_title(self, stdscr):
        stdscr.addstr(0, 0, "{}".format(self.name))

    def draw_status_bar(self, stdscr):
        height, width = stdscr.getmaxyx()
        statusbarstr = "Press 'q' to exit, '1' for help "
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))


def _volume_string(value):
    stars = int(value / 2)
    spaces = 50 - stars
    return "|" + u'\u2588'*stars + " "*spaces + "|"

#TODO: make this a margin on the longest client name
def _status_string(client):
    name = client.friendly_name
    if(client.muted):
        name = "{} (m)".format(name)
    name = name.ljust(15, ' ')
    return "{}{}".format(name, _volume_string(client.volume))


class MainScreen(Screen):
    def __init__(self):
        super().__init__("Main")

    def content(self, state, stdscr):
        out = "Streams".ljust(15, ' ')
        for stream in state.streams:
            if stream == state.active_stream:
                out += "[ {} ] ".format(stream.name)
            else:
                out += "{} ".format(stream.name)
        stdscr.addstr(3, 0, out)

        for idx, client in enumerate(state.clients):
            #TODO: add non-color representation of mutedness and selectedness
            if state.client == client:
                color = curses.color_pair(1)
            elif client.muted:
                color = curses.color_pair(2)
            else:
                color = curses.color_pair(4)

            client_display = _status_string(client)
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

  j,k   change selected client
  s     change selected stream
  h     lower volume on selected client
  l     raise volume on selected client
  m     mute/unmute selected client
  a     mute/unmute all clients"""


class HelpScreen(Screen):
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
