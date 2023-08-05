import requests
import time
import pyttsx3
import os
import yaml
import logging
import jsonschema

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

from .simple_http_notification_conf import result_schema, cloud_server_ip, cloud_server_port, cloud_server_protocol
from .logging_lib import setup_logging
from .authentication import AuthenticationClient, handshake_info

import platform
import hashlib

class SimpleHttpNotificationReceiver:
    def __init__(self, _cloud_server_protocol: str, _cloud_server_ip: str, _cloud_server_port: int,
                 logger: logging.Logger):
        self.logger = logger
        self.cloud_server_protocol = _cloud_server_protocol
        self.cloud_server_ip = _cloud_server_ip
        self.cloud_server_port = _cloud_server_port
        authentication_client = AuthenticationClient(os.path.expanduser("~/.ssh/id_ed25519"), self.logger)
        self.signature = authentication_client.sign_request(handshake_info)
        # use the sha256 hash of hostname as client_id
        self.client_id = int(hashlib.md5(platform.node().encode()).hexdigest(), 16)

    def receive(self, channel: str) -> str:
        try:
            response = requests.get(
                f"{self.cloud_server_protocol}://{self.cloud_server_ip}:{self.cloud_server_port}/notification?channel={channel}&client_id={self.client_id}&sig={self.signature}")
            self.logger.debug(f"Receive notification: {response.status_code}, {response.json()}")
            notification = response.json()
            if notification:
                jsonschema.validate(notification, result_schema)
                message: str = notification["message"]
                return message
            else:
                return ""
        except Exception:
            return ""


if __name__ == '__main__':

    engine = pyttsx3.init()
    logger = setup_logging()
    receiver = SimpleHttpNotificationReceiver(cloud_server_protocol, cloud_server_ip, cloud_server_port, logger)
    while True:
        msg = receiver.receive("test")
        if msg:
            print(msg)
            # engine.setProperty('rate', 120)
            # engine.say(notification)
            # engine.runAndWait()
        time.sleep(1)
