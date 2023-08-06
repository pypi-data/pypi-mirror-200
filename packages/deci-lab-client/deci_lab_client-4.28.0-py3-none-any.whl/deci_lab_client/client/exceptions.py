class InvalidAuthenticationTokenError(Exception):
    pass


class DownloadModelError(Exception):
    pass


class PyTorchNotInstalledError(Exception):
    def __init__(self):
        super(PyTorchNotInstalledError, self).__init__(
            "Could not `import torch`, please install PyTorch before running this method"
        )


class UnsupportedLoadedModelFramework(Exception):
    def __init__(self):
        super(UnsupportedLoadedModelFramework, self).__init__(
            "local_loaded_model is only supported for Pytorch models at the moment."
            " Please specify a model_local_path instead"
        )


class NotLoggedInError(Exception):
    def __init__(self):
        super(NotLoggedInError, self).__init__("This feature is for premium users only. Please log in first.")


class PremiumOnlyFeatureError(Exception):
    def __init__(self):
        super(PremiumOnlyFeatureError, self).__init__(
            "This feature is for premium users only. Please contact support@deci.ai to become one."
        )


class TimeoutWasReachedBeforeBenchmarkFinishedError(Exception):
    def __init__(self):
        super(TimeoutWasReachedBeforeBenchmarkFinishedError, self).__init__(
            "Add model with async_wait flag was called."
            " Benchmark process was started but waiting for results took too long."
        )
