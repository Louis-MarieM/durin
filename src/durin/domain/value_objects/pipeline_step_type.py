from enum import Enum

class PipelineStepType(Enum):
    EXTRACTOR = "Extractor"
    TRANSFORMER = "Transformer"
    LOADER = "Loader"
