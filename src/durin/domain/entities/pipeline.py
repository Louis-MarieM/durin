from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from .step import Step
from ..exceptions.domain_exceptions import InvalidPipelineException, ValidationException
from ..value_objects.cron_expression import CronExpression

@dataclass
class Pipeline:
    """
    Entity representing the definition of a pipeline.
    Pipelines can be considered as DAGs. 
    """
    pipeline_id: str
    steps: set[Step]
    # Cron schedule expression
    schedule_interval: CronExpression
    start: datetime
    end: datetime
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    owners: Optional[set[str]] = None
    description: Optional[str] = None

    def __post_init__(self):
        self._validate_types()
        self._validate_timezones()
        self._validate_business_rules()

    def _validate_timezones(self) -> None:
        if self.start.tzinfo is None:
            raise ValidationException("start must be timezone-aware.", meta={"pipeline_id": self.pipeline_id})
        if self.end.tzinfo is None:
            raise ValidationException("end must be timezone-aware.", meta={"pipeline_id": self.pipeline_id})
        if self.created_at.tzinfo is None:
            raise ValidationException("created_at must be timezone-aware.", meta={"pipeline_id": self.pipeline_id})

    def _validate_types(self) -> None:
        raise ValidationException()

    def _validate_business_rules(self) -> None:
        if self.end < self.start:
            raise InvalidPipelineException("End date is earlier than start date.", meta={"pipeline_id": self.pipeline_id, "start": self.start, "end": self.end})
        self._validate_no_cycle()
    
    def _validate_no_cycle(self) -> None:
        """
        Recursive DFS algorithm with node coloration
        """
        class NodeColor(Enum):
            WHITE = "white"  # Not visited
            GRAY = "gray"    # Visiting
            BLACK = "black"  # Fully visited
        
        colors = {step: NodeColor.WHITE for step in self.steps}

        def has_cycle_from(step: Step) -> tuple[bool, list[str]]:
            colors[step] = NodeColor.GRAY
            
            for child in step.child_steps:
                if child not in self.steps:
                    # External node to the pipeline
                    continue
                
                if colors[child] == NodeColor.GRAY:
                    # Cycle detected
                    return True, [step.step_id, child.step_id]
                
                if colors[child] == NodeColor.WHITE:
                    has_cycle, path = has_cycle_from(child)
                    if has_cycle:
                        return True, [step.step_id] + path
            
            colors[step] = NodeColor.BLACK
            return False, []
        

        for step in self.steps:
            if colors[step] == NodeColor.WHITE:
                has_cycle, cycle_path = has_cycle_from(step)
                if has_cycle:
                    cycle_str = " -> ".join(cycle_path)
                    raise InvalidPipelineException(
                        f"Pipeline '{self.pipeline_id}' contains a cycle: {cycle_str}"
                    )
    
    def _validate_steps(self) -> None:
        self._validate_steps_are_in_pipeline()
        for step in self.steps:
            raise InvalidPipelineException()

    def _validate_steps_are_in_pipeline(self) -> None:
        """
        Validates that all parent and child nodes are in pipeline.
        """
        for step in self.steps:
            for parent in step.parent_steps:
                if parent not in self.steps:
                    raise InvalidPipelineException(
                        "A parent node is external to the pipeline", meta={"pipeline_id": self.pipeline_id, "step_id": step.step_id, "parent_id": parent.step_id}
                    )
            for child in step.child_steps:
                if child not in self.steps:
                    raise InvalidPipelineException(
                        "A child node is external to the pipeline", meta={"pipeline_id": self.pipeline_id, "step_id": step.step_id, "child_id": child.step_id}
                    )

"""
Check de la compatibilité entre un noeud et ses noeuds parents.

Par la suite, on assimile les noeuds à leur callable.

Hypothèses :
- Les callables on un seul objet en input et un seul objet en output.
- Dans chaque input et output, les attributs qui peuvent être passés d'un step 
à l'autre, sont les seuls à avoir leur type dans leur classe respective. S'ils sont 
passés en paramètre, alors le nom de l'attribut doit être donné en même temps.
- Si plusieurs noeuds parents retournent des listes d'attributs du même type, alors on peut concaténer ces listes.
- Si dans les paramètres, ou dans les outputs de noeuds parents, on ne peut pas distinguer des attributs non concaténables ni par leur nom ni par leur type, alors on lève une erreur.
Algo :
- Si un paramètre d'entrée du noeud n'est pas typé, la compatibilité ne peut pas être vérifiée, alors lever une erreur.
- Récupérer la liste des paramètres du noeud et leur type.
    (ex : {"input": InputData, "params": dict[str, Any]}, ou {}...)
- Récupérer la liste des paramètres d'entrée du step et leur type.
    (ex : {"source": str, "timeout": int})
- Récupérer la liste des types des outputs des noeuds parents.
    (ex : [OutputData1, OutputData2])
- 
"""