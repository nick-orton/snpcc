import curses

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
    name = client.friendly_name.ljust(15, ' ')
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

#TODO: Move this into some kind of template
class HelpScreen(Screen):
    def __init__(self):
        super().__init__("Help")

    def content(self, state, stdscr):
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

    def content(self, state, stdscr):
        stdscr.addstr(3, 0, "Client")
        stdscr.addstr(4, 0, "------")
        stdscr.addstr(5, 0, "       ")
        stdscr.addstr(6, 0, "Name          {}".format(state.client.name))
        stdscr.addstr(7, 0, "Identifier    {}".format(state.client.identifier))
        stdscr.addstr(8, 0, "Volume        {}".format(state.client.volume))
        stdscr.addstr(9, 0, "Muted         {}".format(state.client.muted))
        stdscr.addstr(10, 0, "Latency       {}".format(state.client.latency))
        stdscr.addstr(11, 0, "Stream        {}".format(state.active_stream.name))
        stdscr.addstr(12, 0, "Version       {}".format(state.client.version))
