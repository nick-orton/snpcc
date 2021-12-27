""" Stateful controll of the snapcast server """
import logging
from snap.screen import Screens
from snap.api import Api

_LOGGER = logging.getLogger(__name__)

class State():
    """ Representation of the application state. Methods for modifying state.  """
    def __init__(self, address):
        self.address = address
        self.cache = None
        self.client = self.clients()[0]
        self.screen = Screens.main_screen

    def clear_cache(self):
        """ Clear out the cached API.  This should be run once per event loop.
            I'm not happy about leaking that detail out of the state into the
            event loop, but this is a compromise for performance and recency.
        """
        self.cache = None

    def _api(self):
        """ An instance of the API for the snapserver.  Uses the one in the
            cache if available.  The API contains both the server state and
            handles making async RPCs """
        if not self.cache:
            self.cache = Api(self.address)
        return self.cache

    def _find_idx(self, target, items):
        """ Helper function.  Find the index of on item in a list of items that
            all have an 'identifier' property """
        for idx, item in enumerate(items):
            if item.identifier == target.identifier:
                return idx
        return -1 #FIXME Error

    def clients(self):
        """ Return all clients registered with the server """
        #TODO: sort in a consistent order
        return self._api().server.clients

    def streams(self):
        """ All the available streams on the server """
        return self._api().server.streams

    def active_stream(self):
        """ The currently active stream on the server """
        return self._api().active_stream

    def next_stream(self):
        """ Change the stream the server is using """
        if self.active_stream():
            streams = self.streams()
            idx = self._find_idx(self.active_stream(), streams) + 1
            if idx >= len(self.streams()):
                idx = 0
            stream = streams[idx]
            self._api().set_stream(stream)

    def next_client(self):
        """ Get the next client from available clients relative to the
        currently selected client """
        clients = self.clients()
        idx = self._find_idx(self.client, clients)
        idx = idx + 1
        if idx >= len(clients):
            idx = 0
        self.client = clients[idx]

    def prev_client(self):
        """ Get the previous client from the available clients relative to the
        currently selected client """
        clients = self.clients()
        idx = self._find_idx(self.client, clients)
        idx = idx - 1
        if idx < 0:
            idx = len(clients)-1
        self.client = clients[idx]

    def toggle_mute(self):
        """ Mute if unmuted or vice-versa """
        if self.client.muted:
            Api.mute(self.client, False)
        else:
            Api.mute(self.client, True)

    def refresh(self):
        """ refresh the server state in case was changed elsewhere """
        self._api().refresh(self.client)

    def mute_all(self):
        """ Mute all the clients if any are unmuted.  Unmute all the clients if
        all are muted. """
        all_muted = True
        for client in self.clients():
            if not client.muted:
                all_muted = False
        if not all_muted:
            for client in self.clients():
                Api.mute(client, True)
        else:
            for client in self.clients():
                Api.mute(client, False)

    @staticmethod
    def _change_vol(client, api, amt):
        """ Helper function for volume reduction"""
        volume = client.volume + amt
        volume = max(0, volume)
        volume = min(100, volume)
        Api.set_volume(client, volume)

    def lower_volume(self):
        """ Reduce the volume by 5% """
        State._change_vol(self.client, self._api(), -5)

    def lower_volume_all(self):
        """ Reduce the volume for all clients """
        for client in self.clients():
            State._change_vol(client, self._api(), -5)

    def raise_volume(self):
        """ Increase the volume by 5% """
        State._change_vol(self.client, self._api(), 5)

    def raise_volume_all(self):
        """ Increase the volume for all clients """
        for client in self.clients():
            State._change_vol(client, self._api(), 5)

