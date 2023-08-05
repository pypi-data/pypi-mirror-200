from pandas import DataFrame as pdDataFrame
from typing import Dict, List, Optional, Union
from ydata.datascience.common import PrivacyLevel
from ydata.sdk.datasources import DataSource
from ydata.sdk.datasources._models.metadata.data_types import DataType
from ydata.sdk.synthesizers.synthesizer import BaseSynthesizer

class TimeSeriesSynthesizer(BaseSynthesizer):
    def sample(self, n_entities: Optional[int] = ...) -> pdDataFrame: ...
    def fit(self, X: Union[DataSource, pdDataFrame], sortbykey: Optional[Union[str, List[str]]], privacy_level: PrivacyLevel = ..., entity_id_cols: Optional[Union[str, List[str]]] = ..., generate_cols: Optional[List[str]] = ..., exclude_cols: Optional[List[str]] = ..., dtypes: Optional[Dict[str, Union[str, DataType]]] = ..., target: Optional[str] = ..., name: Optional[str] = ..., anonymize: Optional[dict] = ...) -> None: ...
