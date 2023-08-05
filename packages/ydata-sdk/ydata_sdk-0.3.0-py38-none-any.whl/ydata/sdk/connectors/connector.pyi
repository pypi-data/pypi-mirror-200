from pathlib import Path
from typing import Dict, Optional, Union
from ydata.sdk.common.client import Client
from ydata.sdk.common.types import UID
from ydata.sdk.connectors._models.connector_list import ConnectorsList
from ydata.sdk.connectors._models.connector_type import ConnectorType
from ydata.sdk.connectors._models.credentials.credentials import Credentials
from ydata.sdk.utils.model_mixin import ModelFactoryMixin

class Connector(ModelFactoryMixin):
    def __init__(self, connector_type: Union[ConnectorType, str] = ..., credentials: Optional[Dict] = ..., name: Optional[str] = ..., client: Optional[Client] = ...) -> None: ...
    @property
    def uid(self) -> UID: ...
    @property
    def type(self) -> str: ...
    @staticmethod
    def get(uid: UID, client: Optional[Client] = ...) -> Connector: ...
    @staticmethod
    def create(connector_type: Union[ConnectorType, str], credentials: Union[str, Path, Dict, Credentials], name: Optional[str] = ..., client: Optional[Client] = ...) -> Connector: ...
    @staticmethod
    def list(client: Optional[Client] = ...) -> ConnectorsList: ...
