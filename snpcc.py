#!/usr/local/bin/python3

import sys
import asyncio
import snapcast.control
import click

SERVER = "192.168.86.104"

class Api:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.server = self.loop.run_until_complete(snapcast.control.create_server(self.loop, SERVER))

    def clients(self):
        return self.server.clients

    def client(self, name):
        cache = {}
        for client in self.clients():
            cache[client.friendly_name] = client

        if(not name in cache):
            click.echo("No client named " + name)
            sys.exit()
        return cache[name]

    def set_client_status(self, name, volume, muted):
        client = self.client(name)
        client_volume = client.volume if volume is None else volume
        client_muted = client.muted if muted is None else muted
        self.loop.run_until_complete(self.server.client_volume(client.identifier, {'percent':
            client_volume, 'muted': client_muted}))

@click.group()
def cli():
    pass

@cli.command()
def status():
    for client in Api().clients():
          muted_status = "red" if client.muted else "green"
          click.secho(client.friendly_name + " " + str(client.volume),
                  fg=muted_status)

def _set_mute(value, name):
    api = Api()
    api.set_client_status(name, None, value)

@cli.command()
@click.argument('client')
@click.argument('value')
def volume(client, value):
    Api().set_client_status(client, int(value), None)

@cli.command()
@click.argument('client')
def mute(client):
    _set_mute(True, client)

@cli.command()
@click.argument('client')
def unmute(client):
    _set_mute(False, client)
