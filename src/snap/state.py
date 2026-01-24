""" Stateful controll of the snapcast server """
import logging
from snap.screen import Screens
from snap.api import Api
from snap.client import Client

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
        """ Return all clients registered with the server ordered alphabetically
            by identifier """
        clients = self._api().server.clients
        clients.sort(key=lambda c: c.identifier)
        return [Client(client) for client in clients]

    def get_client(self, idx):
        """ Return the client with the specified index
            note: this will not work unless clients() is well ordered """
        clients = self.clients()
        return clients[idx]

    def find_by_name(self, name):
        """ Return the first client with the friendly name that matches """
        clients = self.clients()
        for client in clients:
            if client.friendly_name == name:
                return client
        return -1 #FIXME Error

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
                client.mute(True)
        else:
            for client in self.clients():
                client.mute(False)

    def lower_volume_all(self):
        """ Reduce the volume for all clients """
        for client in self.clients():
            client.lower_volume()

    def raise_volume_all(self):
        """ Increase the volume for all clients """
        for client in self.clients():
            client.raise_volume()

