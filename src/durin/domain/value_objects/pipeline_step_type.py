from enum import Enum

class PipelineStepType(Enum):
    EXTRACTOR = "Extractor"
    TRASNFORMER = "Transformer"
    LOADER = "Loader"
