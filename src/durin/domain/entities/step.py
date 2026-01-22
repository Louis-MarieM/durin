from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Callable, get_type_hints, Optional

from ..exceptions.domain_exceptions import DomainException, InvalidOHLCVException, ValidationException

@dataclass
class Step:
    """
    Entity representing a declaration of runnable pipeline step.
    """
    step_id: str
    step_runner: Callable
    params: dict[str, Any]
    parent_steps: set[Step]
    child_steps: set[Step]
    _inputs: dict[str, type]
    _outputs: dict[str, type]
    _binding_map : dict[str, list[tuple[str, str]]]
    description: Optional[str] = None

    
    @property
    def inputs(self) -> dict[str, Any]:
        return self._inputs
    
    @property
    def outputs(self) -> dict[str, Any]:
        return self._outputs

    @property
    def binding_map(self) -> dict[str, list[tuple[str, str]]]:
        return self._binding_map
    
    def __post_init__(self):
        self._validate_types()
        self._validate_business_rules()

        # Computed properties
        self._compute_inputs()
        self._compute_outputs()
        self._compute_binding_map()
    
    def _validate_types(self):
        raise ValidationException()
    
    def _validate_business_rules(self):
        self._validate_step_runner()
        raise InvalidOHLCVException()
    
    def _validate_step_runner(self):
        raise InvalidOHLCVException()
    
    def _compute_inputs(self) -> None:
        signature = inspect.signature(self.step_runner)
        params = list(signature.parameters.items())

        # There is a unique complex object
        param_name, param = params[0]

        try:
            type_hints = get_type_hints(self.step_runner)
            input_type = type_hints.get(param_name)
        except Exception:
            input_type = param.annotation if param.annotation != inspect.Parameter.empty else None
        
        # Extract attributes from input type of step runner
        self._inputs = self._extract_attributes(input_type)
    
    
    def _compute_outputs(self):
        signature = inspect.signature(self.step_runner)

        try:
            type_hints = get_type_hints(self.step_runner)
            output_type = type_hints.get('return')
        except Exception:
            output_type = signature.return_annotation if signature.return_annotation != inspect.Parameter.empty else None
        
        # Extract attributes from output type of step runner
        self._outputs = self._extract_attributes(output_type)
    
    def _extract_attributes(self, obj_type: type) -> dict[str, type]:
        attributes = {}
        
        # Case 1: Type defined as dataclass
        if hasattr(obj_type, '__dataclass_fields__'):
            for field_name, field_info in obj_type.__dataclass_fields__.items():
                attributes[field_name] = field_info.type
            return attributes
        
        # Case 2: Type defined as TypedDict, or NamedTuple, or standard class
        if hasattr(obj_type, '__annotations__') and obj_type.__annotations__:
            return dict(obj_type.__annotations__)
        
        # else :
        raise DomainException(f"Impossible to extract attributes from type {obj_type}.")
    
    def _compute_binding_map(self) -> None:
        # Initiate map

        ...

# Dans le post_init, on valide le Callable, de sorte à ce que sont mapping soit non ambigüe.