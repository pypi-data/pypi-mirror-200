from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from vectice.api.json.metric import MetricInput
from vectice.utils.deprecation import deprecate

if TYPE_CHECKING:
    from vectice.api.json.model_version import ModelVersionOutput, ModelVersionStatus
    from vectice.models.property import Property


class ModelType(Enum):
    """Enumeration of the different model types."""

    ANOMALY_DETECTION = "ANOMALY_DETECTION"
    CLASSIFICATION = "CLASSIFICATION"
    CLUSTERING = "CLUSTERING"
    OTHER = "OTHER"
    RECOMMENDATION_MODELS = "RECOMMENDATION_MODELS"
    REGRESSION = "REGRESSION"
    TIME_SERIES = "TIME_SERIES"


class ModelRegisterOutput(dict):
    @property
    def model_version(self) -> ModelVersionOutput:
        from vectice.api.json.model_version import ModelVersionOutput

        return ModelVersionOutput(**self["modelVersion"])

    @property
    def use_existing_model(self) -> bool:
        return bool(self["useExistingModel"])

    # TODO: complete the jobrun property
    @property
    def job_run(self) -> str:
        return str(self["jobRun"])


class ModelRegisterInput(dict):
    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def model_type(self) -> ModelType:
        return ModelType(**self["modelType"])

    @property
    def properties(self) -> Property:
        from vectice.models.property import Property

        return Property(**self["properties"])

    @property
    def metrics(self) -> list[MetricInput]:
        return [MetricInput(**metric) for metric in self["metrics"]]

    @property
    def status(self) -> ModelVersionStatus:
        from vectice.api.json.model_version import ModelVersionStatus

        return ModelVersionStatus(self["status"])

    @property
    def framework(self) -> str:
        return str(self["framework"])

    @property
    def type(self) -> str:
        return str(self["type"])

    @property
    def algorithm_name(self) -> str:
        return str(self["algorithmName"])

    @property
    def uri(self) -> str:
        return str(self["uri"])

    @property
    @deprecate(
        warn_at="23.1",
        fail_at="23.2",
        remove_at="23.3",
        reason="The 'inputs' property is renamed 'derived_from'. "
        "Using 'inputs' will raise an error in v{fail_at}. "
        "The property will be removed in v{remove_at}.",
    )
    def inputs(self) -> list[int]:
        return self.derived_from

    @property
    def derived_from(self) -> list[int]:
        return [(self["inputs"])]
