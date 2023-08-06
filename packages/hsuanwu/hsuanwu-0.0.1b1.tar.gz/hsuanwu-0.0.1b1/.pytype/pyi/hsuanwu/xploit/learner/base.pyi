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

class BaseLearner:
    __doc__: str
    _action_space: Any
    _action_type: str
    _aug: Any
    _device: Any
    _dist: Any
    _encoder: Any
    _encoder_opt: Any
    _eps: float
    _feature_dim: int
    _irs: Any
    _lr: float
    _obs_space: Any
    training: bool
    def __init__(self, observation_space, action_space, action_type: str, device = ..., feature_dim: int = ..., lr: float = ..., eps: float = ...) -> None: ...
    def act(self, obs, training: bool = ..., *args) -> Any: ...
    def set_aug(self, aug) -> None: ...
    def set_dist(self, dist) -> None: ...
    def set_encoder(self, encoder) -> None: ...
    def set_irs(self, irs) -> None: ...
    def train(self, training: bool = ...) -> None: ...
    def update(self, *args) -> Any: ...
