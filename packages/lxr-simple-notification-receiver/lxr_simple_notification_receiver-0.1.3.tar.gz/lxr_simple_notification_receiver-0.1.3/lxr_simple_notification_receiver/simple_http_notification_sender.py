#! /usr/bin/env python3
import json
import logging
import requests

import sys, importlib
from pathlib import Path


def import_parents(level: int = 1) -> None:
    global __package__
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[level]

    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError:  # already removed
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])
    importlib.import_module(__package__)  # won't be needed after that


if __name__ == '__main__' and __package__ is None:
    import_parents()

from .simple_http_notification_conf import add_schema, cloud_server_ip, cloud_server_port, cloud_server_protocol
from .logging_lib import setup_logging


class SimpleHttpNotificationSender:
    def __init__(self, _cloud_server_protocol: str, _cloud_server_ip: str, _cloud_server_port: int,
                 logger: logging.Logger) -> None:
        self.logger = logger
        self.cloud_server_protocol = _cloud_server_protocol
        self.cloud_server_ip = _cloud_server_ip
        self.cloud_server_port = _cloud_server_port

    def clear(self, channel: str) -> None:
        response = requests.get(
            f'{self.cloud_server_protocol}://{self.cloud_server_ip}:{self.cloud_server_port}/clear?channel={channel}')

    def send(self, channel: str, message: str) -> None:
        data = {"message": message, "channel": channel}
        headers = {'Content-type': 'application/json'}
        response = requests.post(
            f'{self.cloud_server_protocol}://{self.cloud_server_ip}:{self.cloud_server_port}/notification',
            data=json.dumps(data), headers=headers)
        logging.debug(f"Send notification: {message} with response: {response.json()}")


if __name__ == '__main__':
    logger = setup_logging()
    if len(sys.argv) == 2:
        msg = sys.argv[1]
    sender = SimpleHttpNotificationSender(cloud_server_protocol, cloud_server_ip, cloud_server_port, logger)
    sender.send("art_ci", msg)
