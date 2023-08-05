import jsonschema
import os
from typing import Optional
_cloud_server_ip: Optional[str] = os.environ.get("CLOUD_SERVER_IP")
_cloud_server_port: Optional[str] = os.environ.get("CLOUD_SERVER_PORT")
assert isinstance(_cloud_server_ip, str)
assert isinstance(_cloud_server_port, str)
assert isinstance(int(_cloud_server_port), int)
cloud_server_ip = _cloud_server_ip
cloud_server_port = int(_cloud_server_port)
cloud_server_protocol: str = "https"

add_schema = {
    "type": "object",
    "required": ["message", "channel"],
    "properties": {
        "message": {"type": "string"},
        "channel": {"type": "string"}
    }
}

result_schema = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {"type": "string"},
    }
}