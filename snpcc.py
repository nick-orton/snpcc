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
        self.loop.run_until_complete(self.server.client_volume(
            client.identifier, {'percent': client_volume,
                                'muted': client_muted}))

def _volume_string(value):
    stars = int(value / 2)
    bars = 50 - stars
    return "|" + u'\u2588'*stars + " "*bars + "|"

@click.group()
def cli():
    pass

@cli.command()
def status():
    """ Show the volume levels for every client """
    for client in Api().clients():
          muted_status = "red" if client.muted else "green"
          click.secho(client.friendly_name.ljust(15, ' ') + " "
                  + _volume_string(client.volume), fg=muted_status)

def _set_mute(value, name):
    api = Api()
    api.set_client_status(name, None, value)

def validate_volume(ctx,param, value):
    volume =  int(value)
    if(int(value) > 100 or int(value) < 0):
        raise click.BadParameter("volume must be between 0 and 100")
    return volume

@cli.command()
@click.argument('client')
@click.argument('volume', callback=validate_volume)
def volume(client, volume):
    """ Set CLIENT level to VOLUME [0-100] """
    Api().set_client_status(client, volume, None)

@cli.command()
@click.argument('client')
def mute(client):
    """ Mute the CLIENT """
    _set_mute(True, client)

@cli.command()
@click.argument('client')
def unmute(client):
    """ Unmute the CLIENT """
    _set_mute(False, client)
