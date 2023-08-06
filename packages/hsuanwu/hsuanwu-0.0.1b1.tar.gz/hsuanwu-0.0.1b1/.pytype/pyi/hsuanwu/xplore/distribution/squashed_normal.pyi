# (generated with --quick)

import collections
import hsuanwu.common.typing
import math
import numpy
import omegaconf
import pathlib
import torch
from torch import distributions as pyd
from torch.nn import functional as F
from typing import Annotated, Any, Type

Batch: Type[hsuanwu.common.typing.Batch]
DataLoader: Any
DictConfig: Any
Distribution: Any
Env: Any
Path: Type[pathlib.Path]
Space: Any
Tensor: Any
ndarray: Type[numpy.ndarray]

class SquashedNormal(Any):
    __doc__: str
    _base_dist: Any
    _eps: float
    _high: float
    _low: float
    _mu: Any
    _sigma: Any
    mean: Annotated[Any, 'property']
    def __init__(self, mu, sigma, low: float = ..., high: float = ..., eps: float = ...) -> None: ...
    def _clamp(self, x) -> Any: ...
    def rsample(self, sample_shape = ...) -> Any: ...
    def sample(self, sample_shape = ...) -> Any: ...

class TanhTransform(Any):
    __doc__: str
    bijective: bool
    codomain: Any
    domain: Any
    sign: int
    def __eq__(self, other) -> bool: ...
    def __init__(self, cache_size = ...) -> None: ...
    def _call(self, x) -> Any: ...
    def _inverse(self, y) -> Any: ...
    @staticmethod
    def atanh(x) -> Any: ...
    def log_abs_det_jacobian(self, x, y) -> Any: ...
