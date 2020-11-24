import asyncio
import snapcast.control
import yaml
import os

def server_address():
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
    def __init__(self):
        addr = server_address()
        self.loop = asyncio.get_event_loop()
        self.server = self.loop.run_until_complete(snapcast.control.create_server(self.loop, addr))

    def set_stream(self, stream):
        group_id = self.server.groups[0].identifier
        self.loop.run_until_complete(self.server.group_stream(group_id,
            stream.identifier))

    def get_active_stream(self):
        group = self.server.groups[0]
        stream_id = group.stream
        return self.server.stream(stream_id)

    #TODO delete me
    def client(self, name):
        cache = {}
        for client in self.clients():
            cache[client.friendly_name] = client

        if(not name in cache):
            raise Exception("No client named " + name)
            sys.exit()
        return cache[name]

    def mute(self, client, status):
        self.loop.run_until_complete(client.set_muted(status))

    def set_volume(self, client, percent):
        self.loop.run_until_complete(client.set_volume(percent))
