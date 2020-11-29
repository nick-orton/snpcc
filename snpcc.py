""" Application base module.  Defines CLI commands"""
import click
from snap.state import State
from snap import curses as app

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    Command line client for controlling a Snapcast server

    If invoked without commands, snpcc launches the TUI
    see: https://github.com/badaix/snapcast for more details

    """
    if ctx.invoked_subcommand is None:
        curses()

@cli.command()
def curses():
    """Launch the TUI (default command)"""
    app.main()

@cli.command()
def mute():
    """ Toggle muting/unmuting"""
    state = State(None)
    state.mute_all()

@cli.command("list")
def list_clients():
    """ List all clients and volumes """
    state = State(None)
    for client in state.clients:
        vol = "muted" if client.muted else client.volume
        print("{} {}".format(client.friendly_name, vol))
