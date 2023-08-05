from pydantic import BaseModel
from typing import TypeVar
from ydata.core.enum import StringEnum

T = TypeVar('T')

class GenericStateErrorStatus(BaseModel):
    state: T

class PrepareState(StringEnum):
    PREPARING: str
    DISCOVERING: str
    FINISHED: str
    FAILED: str
    UNKNOWN: str

class TrainingState(StringEnum):
    PREPARING: str
    RUNNING: str
    FINISHED: str
    FAILED: str

class ReportState(StringEnum):
    UNKNOWN: str
    DISCOVERING: str
    FINISHED: str
    FAILED: str
PrepareStatus = GenericStateErrorStatus[PrepareState]
TrainingStatus = GenericStateErrorStatus[TrainingState]
ReportStatus = GenericStateErrorStatus[ReportState]

class Status(StringEnum):
    NOT_INITIALIZED: str
    FAILED: str
    PREPARE: str
    TRAIN: str
    REPORT: str
    READY: str
    UNKNOWN: str
