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

class TorchVecEnvWrapper:
    __doc__: str
    _device: Any
    _venv: Any
    action_space: Any
    observation_space: Any
    def __init__(self, env, device) -> None: ...
    def reset(self) -> Any: ...
    def step(self, actions) -> Any: ...
