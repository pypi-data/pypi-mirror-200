from pydantic import BaseModel
from ydata.core.enum import StringEnum

class ValidationState(StringEnum):
    UNKNOWN: str
    VALIDATE: str
    VALIDATING: str
    FAILED: str
    AVAILABLE: str

class MetadataState(StringEnum):
    UNKNOWN: str
    GENERATE: str
    GENERATING: str
    FAILED: str
    AVAILABLE: str

class ProfilingState(StringEnum):
    UNKNOWN: str
    GENERATE: str
    GENERATING: str
    FAILED: str
    AVAILABLE: str

class Status(StringEnum):
    AVAILABLE: str
    PREPARING: str
    VALIDATING: str
    FAILED: str
    UNAVAILABLE: str
    DELETED: str
    UNKNOWN: str

class State(BaseModel):
    validation: ValidationState
    metadata: MetadataState
    profiling: ProfilingState
