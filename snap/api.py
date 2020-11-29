""" Client for Snapcast API

This implementation assumes that there is only one group defined
"""
import os
import asyncio
import snapcast.control
import yaml

def server_address():
    """ get the server address from the config file """
    if 'APPDATA' in os.environ:
        confighome = os.environ['APPDATA']
    elif 'XDG_CONFIG_HOME' in os.environ:
        confighome = os.environ['XDG_CONFIG_HOME']
    else:
        confighome = os.path.join(os.environ['HOME'], '.config')
    configpath = os.path.join(confighome, 'snpcc.yml')
    try:
        config = yaml.safe_load(open(configpath))
        return config["server"]
    except FileNotFoundError:
        return "localhost"

class Api:
    """ Client for Snapcast server """
    def __init__(self):
        addr = server_address()
        self.loop = asyncio.get_event_loop()
        self.server = self.loop.run_until_complete(snapcast.control.create_server(self.loop, addr))

    def set_stream(self, stream):
        """ Set the stream for the group """
        group_id = self.server.groups[0].identifier
        self.loop.run_until_complete(self.server.group_stream(group_id,
            stream.identifier))

    def get_active_stream(self):
        """ Get the active stream for the group """
        group = self.server.groups[0]
        stream_id = group.stream
        return self.server.stream(stream_id)

    def mute(self, client, status):
        """ Mute a client """
        self.loop.run_until_complete(client.set_muted(status))

    def set_volume(self, client, percent):
        """ Set volume for a client """
        self.loop.run_until_complete(client.set_volume(percent))
