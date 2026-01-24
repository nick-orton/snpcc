""" Module level exports """

import os
import logging
import logging.handlers

def file_logger():
    """ initialize file logger """
    handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE",
        "/tmp/snpcc.log"))
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "ERROR"))
    root.addHandler(handler)

file_logger()
