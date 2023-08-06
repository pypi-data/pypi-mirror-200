# (generated with --quick)

import collections
import hsuanwu.common.typing
import numpy
import omegaconf
import pathlib
import torch
from torch import distributions as pyd
from typing import Any, Type

Batch: Type[hsuanwu.common.typing.Batch]
DataLoader: Any
DictConfig: Any
Distribution: Any
Env: Any
Path: Type[pathlib.Path]
Space: Any
Tensor: Any
ndarray: Type[numpy.ndarray]

class BaseDistribution(Any):
    __doc__: str
    _eps: float
    _high: float
    _low: float
    _mu: Any
    _sigma: Any
    def __init__(self, mu, sigma, low: float = ..., high: float = ..., eps: float = ...) -> None: ...
    def _clamp(self, x) -> Any: ...
    def sample(self, clip: float = ..., sample_shape = ...) -> None: ...
