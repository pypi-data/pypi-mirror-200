# (generated with --quick)

import collections
import hsuanwu.common.typing
import numpy
import numpy as np
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

class VanillaReplayStorage:
    __doc__: str
    _action_shape: Any
    _batch_size: int
    _buffer_size: int
    _device: Any
    _full: bool
    _global_step: int
    _obs_shape: Any
    actions: Any
    dones: Any
    obs: Any
    rewards: Any
    def __init__(self, device, obs_shape, action_shape, action_type: str, buffer_size: int = ..., batch_size: int = ...) -> None: ...
    def __len__(self) -> int: ...
    def add(self, obs, action, reward, done, info, next_obs) -> None: ...
    def sample(self) -> hsuanwu.common.typing.Batch: ...
