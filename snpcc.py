#!/usr/local/bin/python3

import sys
import asyncio
import snapcast.control
import click

SERVER = "192.168.86.104"

@click.group()
def cli():
    pass

def get_client(name, clients):
    cache = {}
    for client in clients:
        cache[client.friendly_name] = client

    if(not name in cache):
        click.echo("No client named " + name)
        sys.exit()
    return cache[name]


@cli.command()
def status():
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(snapcast.control.create_server(loop, SERVER))
    for client in server.clients:
          muted_status = "M" if client.muted else "*"
          click.echo(client.friendly_name + " " + muted_status + " " +
                  str(client.volume))
    sys.exit()

def _set_mute(value, name):
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(snapcast.control.create_server(loop, SERVER))
    client = get_client(name, server.clients)
    loop.run_until_complete(server.client_volume(client.identifier, {'percent':
        client.volume, 'muted': value}))
    sys.exit()

@cli.command()
@click.argument('client')
@click.argument('value')
def volume(client, value):
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(snapcast.control.create_server(loop, SERVER))
    sp_client = get_client(client, server.clients)
    loop.run_until_complete(server.client_volume(sp_client.identifier, {'percent':
        int(value)}))
    sys.exit()

@cli.command()
@click.argument('client')
def mute(client):
    _set_mute(True, client)

@cli.command()
@click.argument('client')
def unmute(client):
    _set_mute(False, client)


cli.add_command(status)


if  __name__ =='__main__':main()
