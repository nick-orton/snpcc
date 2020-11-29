""" Application base module.  Defines CLI commands"""
import click
from snap import snap
from snap import curses as app

def _volume_string(value):
    stars = int(value / 2)
    bars = 50 - stars
    return "|" + u'\u2588'*stars + " "*bars + "|"

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Application entry point."""
    if ctx.invoked_subcommand is None:
        curses()

def _set_mute(value, name):
    client = snap.client(name)
    snap.mute(client, value)

@cli.command()
@click.argument('client')
def mute(client):
    """ Mute the CLIENT """
    snap.mute(snap.client(client), True)

@cli.command()
@click.argument('client')
def unmute(client):
    """ Unmute the CLIENT """
    snap.mute(snap.client(client), False)

@cli.command()
def curses():
    """Launch the TUI"""
    app.main()
