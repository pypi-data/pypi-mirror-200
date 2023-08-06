# (generated with --quick)

import collections
import hsuanwu.common.typing
import numpy
import omegaconf
import pathlib
import torch
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

class BaseIntrinsicRewardModule:
    __doc__: str
    _action_shape: Any
    _action_type: str
    _beta: float
    _device: Any
    _kappa: float
    _obs_shape: Any
    def __init__(self, obs_shape, action_shape, action_type: str, device, beta: float, kappa: float) -> None: ...
    def compute_irs(self, rollouts, step: int) -> numpy.ndarray: ...
    def update(self, rollouts) -> None: ...
