
from snap import snap
import logging

_LOGGER = logging.getLogger(__name__)

class State():
    """ Representation of the application state. Methods for modifying state.  """
    def __init__(self, screen):
        self.clients = snap.server.clients
        self.client = self.clients[0]
        self.active_stream = snap.get_active_stream()
        self.streams = snap.server.streams
        self.screen = screen


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
        if(y >= len(self.clients)):
            y = 0
        self.client = self.clients[y]

    def prev_client(self):
        y = self.clients.index(self.client)
        y = y - 1
        if(y < 0):
            y = len(self.clients)-1
        self.client = self.clients[y]

    def toggle_mute(self):
       if(self.client.muted):
           snap.mute(self.client, False)
       else:
           snap.mute(self.client, True)

    def mute_all(self):
        all_muted = True
        for client in snap.server.clients:
            if not client.muted:
                all_muted = False
        if not all_muted:
            for client in snap.server.clients:
                snap.mute(client, True)
        else:
            for client in snap.server.clients:
                snap.mute(client, False)

    def lower_volume(self):
       volume = max(0, self.client.volume - 5)
       snap.set_volume(self.client, volume)

    def raise_volume(self):
       volume = min(100, self.client.volume + 5)
       snap.set_volume(self.client, volume)


