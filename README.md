Shell interfaces for [Snapcast](https://github.com/badaix/snapcast)

inspired by mpc and ncmpc

## snpcc

a cli based interface

#### Commands
  - curses
    - opens a curses based interface
    - default if no command is chosen
  - mute
    - toggles the mute state of all clients

#### TUI Commands

##### Navigation

  1,?   Help Screen 
  2     Main Screen - clients and volumes
  3     Client Screen - client details
  q     quit application

##### Commands

  j,k      change selected client
  s        change selected stream
  h        lower volume on selected client
  l        raise volume on selected client
  H        lower volume on all clients
  L        raise volume on all clients
  m        mute/unmute selected client
  a        mute/unmute all clients"""
  space    refreshes the state

## Configuration

- $XDG_CONFIG_HOME/snpcc.yml

## Development Instructions

Virtualenv: 
    
    $ pip install --user virtualenv
    $ ~/.local/bin/virtualenv venv
    $ . ./venv/bin/activate

#### Build

    $ pip install --editable .
    $ snpcc

#### Dependencies

[snapcast](https://github.com/happyleavesaoc/python-snapcast)
[click](https://click.palletsprojects.com)
[pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation)

## TODOs

- Make 'M' do all clients for symmetry with H,L
- Refactoring
  - better use of asyncio. (use run)  Does API need to be an object?
  - better initializations of Singletons.
- color the streams
- publish
- get log file from config
- man page

### Notes

https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df

(curses tutorial)[https://gist.github.com/claymcleod/b670285f334acd56ad1c]


