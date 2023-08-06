# (generated with --quick)

import collections
import gym
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

class EpisodicLifeEnv(Any):
    __doc__: str
    lives: Any
    was_real_done: Any
    def __init__(self, env) -> None: ...
    def reset(self, **kwargs) -> numpy.ndarray: ...
    def step(self, action: int) -> Any: ...

class FireResetEnv(Any):
    __doc__: str
    def __init__(self, env) -> None: ...
    def reset(self, **kwargs) -> numpy.ndarray: ...

class MaxAndSkipEnv(Any):
    __doc__: str
    _obs_buffer: Any
    _skip: int
    def __init__(self, env, skip: int = ...) -> None: ...
    def step(self, action: int) -> Any: ...

class NoopResetEnv(Any):
    __doc__: str
    noop_action: int
    noop_max: int
    override_num_noops: None
    def __init__(self, env, noop_max: int = ...) -> None: ...
    def reset(self, **kwargs) -> numpy.ndarray: ...
