""" Stateful controll of the snapcast server """
import logging
from snap import snap

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
        """ Get the next stream from available streams """
        if self.active_stream:
            idx = self.streams.index(self.active_stream) + 1
            if idx >= len(self.streams):
                idx = 0
            stream = self.streams[idx]
            snap.set_stream(stream)
            self.active_stream = stream

    def next_client(self):
        """ Get the next client from available clients relative to the
        currently selected client """
        idx = self.clients.index(self.client)
        idx = idx + 1
        if idx >= len(self.clients):
            idx = 0
        self.client = self.clients[idx]

    def prev_client(self):
        """ Get the previous client from the available clients relative to the
        currently selected client """
        idx = self.clients.index(self.client)
        idx = idx - 1
        if idx < 0:
            idx = len(self.clients)-1
        self.client = self.clients[idx]

    def toggle_mute(self):
        """ Mute if unmuted or vice-versa """
        if self.client.muted:
            snap.mute(self.client, False)
        else:
            snap.mute(self.client, True)

    def mute_all(self):
        """ Mute all the clients if any are unmuted.  Unmute all the clients if
        all are muted. """
        all_muted = True
        for client in self.clients:
            if not client.muted:
                all_muted = False
        if not all_muted:
            for client in snap.server.clients:
                snap.mute(client, True)
        else:
            for client in snap.server.clients:
                snap.mute(client, False)

    def lower_volume(self):
        """ Reduce the volume by 5% """
        volume = max(0, self.client.volume - 5)
        snap.set_volume(self.client, volume)

    def raise_volume(self):
        """ Increase the volume by 5% """
        volume = min(100, self.client.volume + 5)
        snap.set_volume(self.client, volume)
