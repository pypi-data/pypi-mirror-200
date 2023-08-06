# (generated with --quick)

import collections
import hsuanwu.common.typing
import numpy
import omegaconf
import pathlib
import torch
from torch import nn
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

class BaseEncoder(Any):
    __doc__: str
    _feature_dim: int
    _observation_space: Any
    feature_dim: Annotated[int, 'property']
    def __init__(self, observation_space, feature_dim: int = ...) -> None: ...
