import os
import logging
import logging.handlers
from snap.api import Api

def _volume_string(value):
    stars = int(value / 2)
    bars = 50 - stars
    return "|" + u'\u2588'*stars + " "*bars + "|"

def status_string(client):
    name = client.friendly_name.ljust(15, ' ')
    return "{} {}".format(name, _volume_string(client.volume))


#TODO This sucks
def file_logger():
    handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE",
        "/tmp/ncsnpcc.log"))
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "ERROR"))
    root.addHandler(handler)

file_logger()

snap = Api()


