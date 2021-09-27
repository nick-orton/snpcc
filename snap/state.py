""" Stateful controll of the snapcast server """
import logging
from snap.screen import Screens

_LOGGER = logging.getLogger(__name__)

class State():
    """ Representation of the application state. Methods for modifying state.  """
    def __init__(self, api):
        self.clients = api.server.clients
        self.api = api
        self.client = self.clients[0]
        self.active_stream = api.get_active_stream()
        self.streams = api.server.streams
        self.screen = Screens.main_screen


    def next_stream(self):
        """ Get the next stream from available streams """
        if self.active_stream:
            idx = self.streams.index(self.active_stream) + 1
            if idx >= len(self.streams):
                idx = 0
            stream = self.streams[idx]
            self.api.set_stream(stream)
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
            self.api.mute(self.client, False)
        else:
            self.api.mute(self.client, True)

    def refresh(self):
        """ refresh the server state in case was changed elsewhere """
        self.api.refresh(self.client)

    def mute_all(self):
        """ Mute all the clients if any are unmuted.  Unmute all the clients if
        all are muted. """
        all_muted = True
        for client in self.clients:
            if not client.muted:
                all_muted = False
        if not all_muted:
            for client in self.api.server.clients:
                self.api.mute(client, True)
        else:
            for client in self.api.server.clients:
                self.api.mute(client, False)

    @staticmethod
    def change_vol(client, api, amt):
        """ Helper method for volume reduction"""
        volume = client.volume + amt
        volume = max(0, volume)
        volume = min(100, volume)
        api.set_volume(client, volume)

    def lower_volume(self):
        """ Reduce the volume by 5% """
        State.change_vol(self.client, self.api, -5)

    def lower_volume_all(self):
        """ Reduce the volume for all clients """
        for client in self.clients:
            State.change_vol(client, self.api, -5)

    def raise_volume(self):
        """ Increase the volume by 5% """
        State.change_vol(self.client, self.api, 5)

    def raise_volume_all(self):
        """ Increase the volume for all clients """
        for client in self.clients:
            State.change_vol(client, self.api, 5)

