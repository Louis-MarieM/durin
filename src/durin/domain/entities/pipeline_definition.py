from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from ..exceptions.domain_exceptions import DomainException, InvalidPipelineException, PipelineOperationNotPermitted, ValidationException
from ..value_objects.pipeline_step_type import PipelineStepType

def _base_meta(id: UUID, name: str) -> dict:
    return {"id": id, "name": name}

@dataclass(frozen=True)
class PipelineDefinition:
    """
    Entity representing the definition of a pipeline.
    It is immutable and versioned.l
    """
    name: str
    version: int
    steps: List[PipelineStep]
    id: UUID = field(default_factory=uuid4)
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self):
        self._validate_types()
        self._validate_timezones()
        self._validate_business_rules()

    @classmethod
    def create(
        cls,
        name: str,
        steps: List[PipelineStep],
        created_by: str = None,
        description: str = None
    ) -> PipelineDefinition:
        """
        Factory method pour créer une nouvelle définition de pipeline avec valeurs par défaut.
        """
        return cls(
            name=name,
            version=1,
            steps=steps,
            id=uuid4(),
            is_active=True,
            created_at=datetime.now(timezone.utc),
            created_by=created_by,
            description=description
        )

    def deactivate(self) -> PipelineDefinition:
        """
        Returns a new instance with is_active=False (immutability respected).
        """
        if not self.is_active:
            raise PipelineOperationNotPermitted("Pipeline already deactivated.", meta={"pipeline_name": self.name})
        return PipelineDefinition(
            name=self.name,
            version=self.version + 1,
            steps=self.steps,
            id=self.id,
            is_active=False,
            created_at=datetime.now(timezone.utc),
            created_by=self.created_by,
            description=self.description
        )

    def activate(self) -> PipelineDefinition:
        """
        Returns a new instance with is_active=True (immutability respected).
        """
        if self.is_active:
            raise PipelineOperationNotPermitted("Pipeline already activated.", meta={"pipeline_name": self.name})
        return PipelineDefinition(
            name=self.name,
            version=self.version + 1,
            steps=self.steps,
            id=self.id,
            is_active=True,
            created_at=datetime.now(timezone.utc),
            created_by=self.created_by,
            description=self.description
        )

    def update_steps(self, new_steps: List[PipelineStep]) -> PipelineDefinition:
        """
        Creates a new version of the pipeline with new steps.
        """
        return PipelineDefinition(
            name=self.name,
            version=self.version + 1,
            steps=new_steps,
            id=self.id,
            is_active=True,
            created_at=datetime.now(timezone.utc),
            created_by=self.created_by,
            description=self.description
        )
    
    def _validate_types(self) -> None:
        base_meta = _base_meta(self.id, self.name)

        if not isinstance(self.name, str):
            raise ValidationException("name must be of type str.", meta={**base_meta, "name_type": type(self.name)})
        if not isinstance(self.version, int):
            raise ValidationException("version must be of type int.", meta={**base_meta, "version_type": type(self.version)})
        if not isinstance(self.steps, list):
            raise ValidationException("steps must be of type list.", meta={**base_meta, "steps_type": type(self.steps)})
        for index, step in enumerate(self.steps):
            if not isinstance(step, PipelineStep):
                raise ValidationException("Each step must be a PipelineStep instance.", meta={**base_meta, "index": index, "step_type": type(step)})
        if not isinstance(self.id, UUID):
            raise ValidationException("id must be of type UUID.", meta={**base_meta, "id_type": type(self.id)})
        if not isinstance(self.is_active, bool):
            raise ValidationException("is_active must be of type bool.", meta={**base_meta, "is_active_type": type(self.is_active)})
        if not isinstance(self.created_at, datetime):
            raise ValidationException("created_at must be of type datetime.", meta={**base_meta, "created_at_type": type(self.created_at)})
        if self.created_by is not None and not isinstance(self.created_by, str):
            raise ValidationException("created_by must be of type str.", meta={**base_meta, "created_by_type": type(self.created_by)})
        if self.description is not None and not isinstance(self.description, str):
            raise ValidationException("description must be of type str.", meta={**base_meta, "description_type": type(self.description)})
        
    def _validate_timezones(self) -> None:
        base_meta = _base_meta(self.id, self.name)
        
        if self.created_at.tzinfo is None:
            raise ValidationException("created_at must be timezone-aware.", meta=base_meta)

    def _validate_business_rules(self):
        base_meta = _base_meta(self.id, self.name)

        if not self.name or not self.name.strip():
            raise InvalidPipelineException("name must be a non-empty string.", meta={**base_meta})
        if self.version < 1:
            raise InvalidPipelineException("version must be >= 1.", meta={**base_meta, "version": self.version})
        if len(self.steps) == 0:
            raise InvalidPipelineException("Pipeline must contain at least one step.", meta={**base_meta})


@dataclass(frozen=True)
class PipelineStep:
    """
    Entity representing a declaration of pipeline step.
    - step_type : the nature/function of the step in the pipeline.
    - step_runner : the chosen logical implementation (ex : "yahoofinance", "ohclvnormalizer", "postgres").
    - params : parameters specific to this runner.
    """
    step_type: PipelineStepType
    step_runner: str
    params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self._validate_types()
        self._validate_business_rules()
    
    def _validate_types(self) -> None:
        if not isinstance(self.step_type, PipelineStepType):
            raise ValidationException("step_type must be of type PipelineStepType.", meta={"step_type_type": type(self.step_type)})
        if not isinstance(self.step_runner, str):
            raise ValidationException("step_runner must be of type str.", meta={"step_type_type": type(self.step_type), "step_runner_type": type(self.step_runner)})
        if not isinstance(self.params, dict):
            raise ValidationException("params from PipelineStep must be of type dict.", meta={"step_type_type": type(self.step_type), "params_type": type(self.params)})

    def _validate_business_rules(self) -> None:
        if not self.step_runner or not self.step_runner.strip():
            raise InvalidPipelineException("step_runner must be a non-empty string.", meta={"step_type_type": type(self.step_type)})
        