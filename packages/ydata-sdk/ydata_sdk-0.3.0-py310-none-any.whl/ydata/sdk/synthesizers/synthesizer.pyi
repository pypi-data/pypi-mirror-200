import abc
from abc import ABC, abstractmethod
from pandas import DataFrame as pdDataFrame
from typing import Dict, List, Optional, Union
from ydata.datascience.common import PrivacyLevel
from ydata.sdk.common.client import Client
from ydata.sdk.common.types import UID
from ydata.sdk.datasources import DataSource
from ydata.sdk.datasources._models.datatype import DataSourceType
from ydata.sdk.datasources._models.metadata.data_types import DataType
from ydata.sdk.synthesizers._models.status import Status
from ydata.sdk.synthesizers._models.synthesizers_list import SynthesizersList
from ydata.sdk.utils.model_mixin import ModelFactoryMixin

class BaseSynthesizer(ABC, ModelFactoryMixin, metaclass=abc.ABCMeta):
    def __init__(self, client: Optional[Client] = ...) -> None: ...
    def fit(self, X: Union[DataSource, pdDataFrame], privacy_level: PrivacyLevel = ..., datatype: Optional[Union[DataSourceType, str]] = ..., sortbykey: Optional[Union[str, List[str]]] = ..., entity_id_cols: Optional[Union[str, List[str]]] = ..., generate_cols: Optional[List[str]] = ..., exclude_cols: Optional[List[str]] = ..., dtypes: Optional[Dict[str, Union[str, DataType]]] = ..., target: Optional[str] = ..., name: Optional[str] = ..., anonymize: Optional[dict] = ...) -> None: ...
    @abstractmethod
    def sample(self) -> pdDataFrame: ...
    @property
    def uid(self) -> UID: ...
    @property
    def status(self) -> Status: ...
    @staticmethod
    def get(uid: str, client: Optional[Client] = ...) -> BaseSynthesizer: ...
    @staticmethod
    def list(client: Optional[Client] = ...) -> SynthesizersList: ...
