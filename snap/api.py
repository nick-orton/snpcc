""" Client for Snapcast API

This implementation assumes that there is only one group defined
"""
import asyncio
import snapcast.control

class Api:
    """ Client for Snapcast server """
    def __init__(self, addr):
        self.loop = asyncio.get_event_loop()
        self.server = self.loop.run_until_complete(snapcast.control.create_server(self.loop, addr))
        self.active_stream = self._get_active_stream()

    @staticmethod
    def _run(action):
        """ run the async rpc call """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(action)

    def _get_active_stream(self):
        """ Get the active stream for the group """
        group = self.server.groups[0]
        stream_id = group.stream
        return self.server.stream(stream_id)

    def set_stream(self, stream):
        """ Set the stream for the group """
        group_id = self.server.groups[0].identifier
        Api._run(self.server.group_stream(group_id,
            stream.identifier))
        self.active_stream = stream

    def refresh(self, client):
        """ No Op that refreshes the server state """
        # HACK - didn't see a better way to do a no-op that refreshes state
        # FIXME: This functionality is no longer needed
        i = client.volume
        self.loop.run_until_complete(client.set_volume(i))
