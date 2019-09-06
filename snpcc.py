#!/usr/local/bin/python3

import sys
import asyncio
import snapcast.control

port = 1705

def clients():
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(snapcast.control.create_server(loop,
        '192.168.86.104'))

def get_client(name, clients):
    cache = {}
    for client in clients:
        cache[client.friendly_name] = client

    if(not name in cache):
        print("No client named " + name)
        sys.exit()
    return cache[name]


def status(loop, server):
    for client in server.clients:
          muted_status = "M" if client.muted else "*"
          print(client.friendly_name + " " + muted_status + " " +
                  str(client.volume))
    sys.exit()

def _set_mute(loop, server, value):
    if(len(sys.argv) < 3):
        help()
        sys.exit()
    name = sys.argv[2]
    client = get_client(name, server.clients)
    loop.run_until_complete(server.client_volume(client.identifier, {'percent':
        client.volume, 'muted': value}))
    sys.exit()

def volume(loop, server):
    if(len(sys.argv) < 4):
        help()
        sys.exit()
    name = sys.argv[2]
    value = sys.argv[3]
    client = get_client(name, server.clients)
    loop.run_until_complete(server.client_volume(client.identifier, {'percent':
        int(value)}))
    sys.exit()

def mute(loop, server):
    _set_mute(loop, server, True)

def unmute(loop, server):
    _set_mute(loop, server, False)

def help():
    print("help!")
    sys.exit()

commands = {"status" : status,
        "mute" : mute,
        "unmute" : unmute,
        "volume" : volume }

def main():
  if(len(sys.argv) < 2):
    help()
  if(sys.argv[1] in commands):
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(snapcast.control.create_server(loop,
        '192.168.86.104'))
    commands[sys.argv[1]](loop, server)
  else:
    help()



if  __name__ =='__main__':main()
