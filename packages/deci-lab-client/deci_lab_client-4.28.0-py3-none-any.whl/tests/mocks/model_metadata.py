import random

import factory
from deci_lab_client.models import (
    DeepLearningTask,
    FrameworkType,
    HardwareType,
    ModelMetadata,
)


class ModelMetadataFactory(factory.Factory):
    class Meta:
        model = ModelMetadata

    name = factory.Faker("name")
    framework = factory.LazyFunction(
        lambda: random.choice(list(filter(lambda v: v != "pytorch", FrameworkType.allowable_values)))
    )
    dl_task = factory.LazyFunction(lambda: random.choice(DeepLearningTask.allowable_values))
    primary_hardware = factory.LazyFunction(lambda: random.choice(HardwareType.allowable_values))
    input_dimensions = factory.Faker("name")
    primary_batch_size = factory.Faker("pyint", min_value=1, max_value=64)
