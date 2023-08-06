import time
from typing import TYPE_CHECKING

from deci_lab_client.models import (
    KPI,
    AccuracyMetric,
    AccuracyMetricKey,
    AccuracyMetricType,
    DeepLearningTask,
    FrameworkType,
    GruRequestForm,
    Metric,
    ModelMetadata,
)
from tqdm import tqdm

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Optional


def wait_until(predicate, timeout, period=15, *args, **kwargs):
    must_end = time.time() + timeout
    while time.time() < must_end:
        return_value = predicate(*args, **kwargs)
        if return_value:
            return return_value
        time.sleep(period)
    return False


class TqdmUpTo(tqdm):
    DOWNLOAD_PARAMS = {
        "unit": "B",
        "unit_scale": True,
        "unit_divisor": 1024,
        "miniters": 1,
        "bar_format": "{l_bar}{bar:20}{r_bar}",
    }

    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        return self.update(b * bsize - self.n)  # also sets self.n = b * bsize


_DL_TASK_TO_LABEL = {
    DeepLearningTask.CLASSIFICATION: AccuracyMetricKey.MAP,
    DeepLearningTask.SEMANTIC_SEGMENTATION: AccuracyMetricKey.MIOU,
}


def get_accuracy_metric_key(dl_task: str) -> str:
    return _DL_TASK_TO_LABEL.get(dl_task, AccuracyMetricKey.TOP_1)


def build_model_metadata(
    *,
    name: str,
    dl_task: str,
    input_dimensions: "Sequence[int]",
    hardware_types: "list[str]",
    channel_first: bool = True,
    accuracy: "Optional[float]" = None,
    description: "Optional[str]" = None,
    dataset_name: "Optional[str]" = None,
    target_metric: "Optional[str]" = None,
    target_metric_value: "Optional[float]" = None,
    model_size: "Optional[float]" = None,
    memory_footprint: "Optional[float]" = None,
) -> "ModelMetadata":
    accuracy_metrics = []
    if accuracy is not None:
        accuracy_metrics.append(
            AccuracyMetric(
                key=get_accuracy_metric_key(dl_task),
                is_primary=True,
                value=accuracy,
                type=AccuracyMetricType.PERCENTAGE,
            )
        )
    kpis = []
    if target_metric is not None and target_metric_value is not None:
        kpis.append(KPI(metric=target_metric, value=target_metric_value))
    if model_size is not None:
        kpis.append(KPI(metric=Metric.MODEL_SIZE, value=model_size))
    if memory_footprint is not None:
        kpis.append(KPI(metric=Metric.MEMORY_FOOTPRINT, value=memory_footprint))

    return ModelMetadata(
        name=name,
        framework=FrameworkType.PYTORCH,
        dl_task=dl_task,
        input_dimensions=input_dimensions,
        channel_first=channel_first,
        primary_hardware=hardware_types[0],
        description=description,
        accuracy_metrics=accuracy_metrics,
        dataset_name=dataset_name,
        kpis=kpis,
    )


def build_gru_request_form(
    *,
    batch_size: int,
    quantization_level: str,
    target_hardware_types: "list[str]",
    raw_format: bool,
    target_metric=Metric.THROUGHPUT,
) -> GruRequestForm:
    return GruRequestForm(
        optimize_autonac=False,
        optimize_model_size=False,
        quantization_levels=[quantization_level],
        target_batch_sizes=[batch_size],
        target_hardwares=target_hardware_types,
        target_metric=target_metric,
        raw_format=raw_format,
    )
