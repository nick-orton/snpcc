Shell interfaces for [Snapcast](https://github.com/badaix/snapcast)

inspired by mpc and ncmpc

## snpcc

a cli based interface

#### Commands
  - curses
    - opens a curses based interface
  - status
    - styles muted clients as red, unmuted as green
    - default if no command given
    - volumes all lined up no matter what volume level
  - mute
  - unmute
  - volume <value>
    - Error checking for out of bounds volume
  - running without any commands executes curses

#### Curses Commands

q: quit
UP/DOWN: select a client
m: toggle mute
LEFT/Right: change volume
curses - open curse-based interface


## Configuration

- $XDG_CONFIG_HOME/snpcc.yml

## Development Instructions

Virtualenv: 

    $ . ./venv/bin/activate

#### Build

    $ pip install --editable .
    $ snpcc

#### Dependencies

[snapcast](https://github.com/happyleavesaoc/python-snapcast)
[click](https://click.palletsprojects.com)
[pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation)

## TODOs

- choose stream
- help screen for curses
- toggle for snpcc
- man page
- publish
- get log file from config

### Notes

https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df

curses tutorial
https://gist.github.com/claymcleod/b670285f334acd56ad1c


