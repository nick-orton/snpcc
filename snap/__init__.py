""" Module level exports """

import os
import logging
import logging.handlers
from snap.api import Api


#TODO This sucks
def file_logger():
    """ initialize file logger """
    handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE",
        "/tmp/ncsnpcc.log"))
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "ERROR"))
    root.addHandler(handler)

file_logger()

snap = Api()
