from snap.snap import Api
import snap
import click

def _volume_string(value):
    stars = int(value / 2)
    bars = 50 - stars
    return "|" + u'\u2588'*stars + " "*bars + "|"

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
       status()

@cli.command()
def status():
    """ Show the volume levels for every client """
    for client in Api().clients():
        muted_status = "red" if client.muted else "green"
        click.secho(snap.status_string(client), fg=muted_status)

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
    api = Api()
    sc_client = api.client(client)
    api.set_volume(sc_client, volume)

def _set_mute(value, name):
    api = Api()
    client = api.client(name)
    api.mute(client, value)

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
