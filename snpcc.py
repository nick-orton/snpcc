from snap import snap
from snap import curses as app
from snap import status_string
import click

def _volume_string(value):
    stars = int(value / 2)
    bars = 50 - stars
    return "|" + u'\u2588'*stars + " "*bars + "|"

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
       curses()

@cli.command()
def status():
    """ Show the volume levels for every client """
    for client in snap.clients():
        muted_status = "red" if client.muted else "green"
        click.secho(status_string(client), fg=muted_status)

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
    sc_client = snap.client(client)
    snap.set_volume(sc_client, volume)

def _set_mute(value, name):
    client = snap.client(name)
    snap.mute(client, value)

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

@cli.command()
def curses():
    app.main()



