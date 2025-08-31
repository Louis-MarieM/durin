from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from uuid import uuid4
import pytest

from durin.domain import (
    Interval,
    InvalidPipelineException,
    PipelineDefinition,
    PipelineOperationNotPermitted,
    PipelineStep,
    PipelineStepType,
    ValidationException
)

@pytest.fixture
def _valid_pipeline_step_fields() -> dict:
    start_date = datetime(2024, 1, 1, 9, 30, tzinfo=timezone.utc)
    end_date = datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
    return dict(
        step_type=PipelineStepType.EXTRACTOR,
        step_runner="yahoofinance",
        params={"ticker": "AAPL", "interval": Interval.ONE_DAY, "start_date": start_date, "end_date": end_date}
    )

@pytest.fixture
def _valid_pipeline_step(_valid_pipeline_step_fields) -> PipelineStep:
    return PipelineStep(**_valid_pipeline_step_fields)

@pytest.fixture
def _valid_pipeline_definition_fields(_valid_pipeline_step) -> dict:
    created_at = datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
    return dict(
        name="Daily Batch",
        version=1,
        steps=[_valid_pipeline_step],
        created_at=created_at
    )


# ---- Tests PipelineDefinition ----

def test_init__when_valid_fields__then_creates_step_instance(_valid_pipeline_definition_fields):
    obj = PipelineDefinition(**_valid_pipeline_definition_fields)
    assert isinstance(obj, PipelineDefinition)

def test_create__when_valid_fields__then_creates_step_instance(_valid_pipeline_step):
    obj = PipelineDefinition.create(
            name="Daily Batch",
            steps=[_valid_pipeline_step],
            created_by="Heleme",
            description="Batch to run every morning"
        )
    assert isinstance(obj, PipelineDefinition)

@pytest.mark.parametrize("field, bad_value", [
    ("name", 123),
    ("version", "1"),
    ("steps", [dict(
        step_type=PipelineStepType.EXTRACTOR,
        step_runner="yahoofinance",
        params={"ticker": "AAPL"})]),
    ("id", 100),
    ("created_at", "01/01/2025"),
    ("created_by", 123),
    ("description", 123)
])
def test_init__when_type_invalid__then_raises_ValidationException(_valid_pipeline_definition_fields, field, bad_value):
    args = {**_valid_pipeline_definition_fields}
    args[field] = bad_value
    with pytest.raises(ValidationException):
        PipelineDefinition(**args)

def test_init__when_timezone_not_valid__then_raises_ValidationException(_valid_pipeline_definition_fields):
    args = {**_valid_pipeline_definition_fields}
    datetime_without_timezone = datetime(2025, 1, 1, 9, 30)
    args["created_at"] = datetime_without_timezone
    with pytest.raises(ValidationException):
        PipelineDefinition(**args)

def test_init__when_name_empty_string__then_raises_InvalidPipelineException(_valid_pipeline_definition_fields):
    args = {**_valid_pipeline_definition_fields}
    args["name"] = "    "
    with pytest.raises(InvalidPipelineException):
        PipelineDefinition(**args)

def test_init__when_version_inconsistent__then_raises_InvalidPipelineException(_valid_pipeline_definition_fields):
    args = {**_valid_pipeline_definition_fields}
    args["version"] = 0
    with pytest.raises(InvalidPipelineException):
        PipelineDefinition(**args)

def test_init__when_no_step__then_raises_InvalidPipelineException(_valid_pipeline_definition_fields):
    args = {**_valid_pipeline_definition_fields}
    args["steps"] = []
    with pytest.raises(InvalidPipelineException):
        PipelineDefinition(**args) 

def test_deactivate__when_active_pipeline__then_deactivates_it(_valid_pipeline_definition_fields):
    args = {**_valid_pipeline_definition_fields}
    obj = PipelineDefinition(**args)
    new_obj = obj.deactivate()
    assert not new_obj.is_active

def test_deactivate__when_not_active_pipeline__then_raises_PipelineOperationNotPermitted(_valid_pipeline_definition_fields):
    args = {**_valid_pipeline_definition_fields}
    args["is_active"] = False
    obj = PipelineDefinition(**args)
    with pytest.raises(PipelineOperationNotPermitted):
        obj.deactivate()

def test_activate__when_not_active_pipeline__then_deactivates_it(_valid_pipeline_definition_fields):
    args = {**_valid_pipeline_definition_fields}
    args["is_active"] = False
    obj = PipelineDefinition(**args)
    new_obj = obj.activate()
    assert new_obj.is_active

def test_activate__when_active_pipeline__then_raises_PipelineOperationNotPermitted(_valid_pipeline_definition_fields):
    args = {**_valid_pipeline_definition_fields}
    obj = PipelineDefinition(**args)
    with pytest.raises(PipelineOperationNotPermitted):
        obj.activate()

def test_update_steps__when_valid_steps__then_creates_new_pipeline(_valid_pipeline_definition_fields, _valid_pipeline_step_fields):
    pipeline_definition_args = {**_valid_pipeline_definition_fields}
    pipeline_definition = PipelineDefinition(**pipeline_definition_args)
 
    pipeline_step_args = {**_valid_pipeline_step_fields}
    pipeline_step_args["step_runner"] = "New extracter"
    new_pipeline_step = PipelineStep(**pipeline_step_args)

    new_pipeline_definition = pipeline_definition.update_steps([new_pipeline_step])
    assert new_pipeline_definition.steps[0].step_runner == "New extracter"

def test_update_steps__when_invalid_steps__then_raises_an_exception(_valid_pipeline_definition_fields, _valid_pipeline_step_fields):
    pipeline_definition_args = {**_valid_pipeline_definition_fields}
    pipeline_definition = PipelineDefinition(**pipeline_definition_args)

    pipeline_step_args = {**_valid_pipeline_step_fields}
    new_pipeline_step = PipelineStep(**pipeline_step_args)

    with pytest.raises(ValidationException):
        pipeline_definition.update_steps([new_pipeline_step, pipeline_step_args])

def frozen__when_attempt_mutation__then_raises_FrozenInstanceError(_valid_pipeline_definition_fields):
    obj = PipelineDefinition(**_valid_pipeline_definition_fields)
    with pytest.raises(FrozenInstanceError):
        obj.name = "Monthly ETL"

# ---- Tests PipelineStep ----

def test_init__when_valid_fields_then_creates_step_instance(_valid_pipeline_step_fields):
    obj = PipelineStep(**_valid_pipeline_step_fields)
    assert isinstance(obj, PipelineStep)

@pytest.mark.parametrize("field, bad_value", [
    ("step_type", "EXTRACTOR"),
    ("step_runner", 100),
    ("params", []),
])
def test_init__when_type_invalid__then_raises_ValidationException(_valid_pipeline_step_fields, field, bad_value):
    args = _valid_pipeline_step_fields.copy()
    args[field] = bad_value
    with pytest.raises(ValidationException):
        PipelineStep(**args)

def test_init__when_step_runner_empty_string__then_raises_InvalidPipelineException(_valid_pipeline_step_fields):
    args = _valid_pipeline_step_fields.copy()
    args["step_runner"] = "    "
    with pytest.raises(InvalidPipelineException):
        PipelineStep(**args)

def frozen__when_attempt_mutation__then_raises_FrozenInstanceError(_valid_pipeline_step_fields):
    obj = PipelineStep(**_valid_pipeline_step_fields)
    with pytest.raises(FrozenInstanceError):
        obj.step_runner = "web_scrapper"
