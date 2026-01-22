from enum import Enum

class StepState(Enum):
    FAILED = "Failed"
    QUEUED = "Queued"
    RUNNING = "Running"
    SKIPPED = "Skipped"
    SUCCESS = "Success"
