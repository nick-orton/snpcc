""" Application base module.  Defines CLI commands"""
import click
import os
import yaml
from snap.state import State
from snap.api import Api
from snap import tui

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

def init_state():
  """ initialize the singletons """
  state = State(server_address())
  return state


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
    state = init_state()
    tui.main(state)

@cli.command()
@click.argument('client_num', required=False)
def mute(client_num=None):
    """ Toggle muting/unmuting.  Specify index of client to by toggled or
        mute/unmute all"""
    state = init_state()
    if(client_num == None):
        state.mute_all()
    else:
        idx = int(client_num) - 1 # convert from 1-based to 0-based index
        client = state.get_client(idx)
        client.toggle_mute()
        print("Muted: {}".format(client.friendly_name))

@cli.command()
@click.argument('client_num', required=False)
def up(client_num=None):
    """ Raise volume by 5% """
    state = init_state()
    if(client_num == None):
        state.raise_volume_all()
    else:
        idx = int(client_num) - 1 # convert from 1-based to 0-based index
        client = state.get_client(idx)
        state.raise_volume(client)
        vol = "MUTE" if client.muted else client.volume
        print("{} {}".format(client.friendly_name, vol))

@cli.command()
@click.argument('client_num', required=False)
def down(client_num=None):
    """ Lower volume by 5% """
    state = init_state()
    if(client_num == None):
        state.lower_volume_all()
    else:
        idx = int(client_num) - 1 # convert from 1-based to 0-based index
        client = state.get_client(idx)
        client.lower_volume()
        vol = "MUTE" if client.muted else client.volume
        print("{} {}".format(client.friendly_name, vol))



@cli.command("list")
def list_clients():
    """ List all clients and volumes """
    state = init_state()
    maximum = max([len(client.friendly_name) for client in state.clients()])
    for idx, client in enumerate(state.clients()):
        vol = "--" if client.muted else client.volume
        padding = maximum - len(client.friendly_name)
        display_name = client.friendly_name + " "*padding
        print("{} {} {}".format(idx+1, display_name, vol))
