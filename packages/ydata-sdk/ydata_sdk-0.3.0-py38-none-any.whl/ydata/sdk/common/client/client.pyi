from _typeshed import Incomplete
from httpx import Response as Response, codes as http_codes
from typing import Dict, Optional, Union
from ydata.sdk.common.client.singleton import SingletonClient
from ydata.sdk.common.types import Project

codes = http_codes
HELP_TEXT: Incomplete

class Client(metaclass=SingletonClient):
    codes = codes
    project: Incomplete
    def __init__(self, credentials: Optional[Union[str, Dict]] = ..., project: Optional[Project] = ..., set_as_global: bool = ...) -> None: ...
    def post(self, endpoint: str, data: Optional[Dict] = ..., json: Optional[Dict] = ..., files: Optional[Dict] = ..., raise_for_status: bool = ...) -> Response: ...
    def get(self, endpoint: str, params: Optional[Dict] = ..., cookies: Optional[Dict] = ..., raise_for_status: bool = ...) -> Response: ...
    def get_static_file(self, endpoint: str, raise_for_status: bool = ...) -> Response: ...
