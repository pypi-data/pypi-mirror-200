# (generated with --quick)

import collections
import hsuanwu.common.typing
import numpy
import omegaconf
import pathlib
import torch
from torch import distributions as pyd
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

class Categorical(Any):
    __doc__: str
    mean: Annotated[Any, 'property']
    def __init__(self, logits = ...) -> None: ...
    def log_probs(self, actions) -> Any: ...
    def sample(self) -> Any: ...
