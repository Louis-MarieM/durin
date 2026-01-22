from enum import Enum

class PipelineState(Enum):
    FAILED = "Failed"
    QUEUED = "Queued"
    RUNNING = "Running"
    SUCCESS = "Success"
