# (generated with --quick)

import collections
import hsuanwu.common.typing
import numpy
import omegaconf
import pathlib
import torch
from typing import Any, Type

Batch: Type[hsuanwu.common.typing.Batch]
BatchSampler: Any
DataLoader: Any
DictConfig: Any
Distribution: Any
Env: Any
Path: Type[pathlib.Path]
Space: Any
SubsetRandomSampler: Any
Tensor: Any
ndarray: Type[numpy.ndarray]

class VanillaRolloutStorage:
    __doc__: str
    _action_dim: Any
    _action_shape: Any
    _device: Any
    _discount: float
    _gae_lambda: float
    _global_step: int
    _num_envs: int
    _num_steps: int
    _obs_shape: Any
    actions: Any
    advantages: Any
    dones: Any
    log_probs: Any
    obs: Any
    returns: Any
    rewards: Any
    values: Any
    def __init__(self, device, obs_shape, action_shape, action_type: str, num_steps: int, num_envs: int, discount: float = ..., gae_lambda: float = ...) -> None: ...
    def add(self, obs, actions, rewards, dones, log_probs, values) -> None: ...
    def compute_returns_and_advantages(self, last_values) -> None: ...
    def generator(self, num_mini_batch: int = ...) -> hsuanwu.common.typing.Batch: ...
    def reset(self) -> None: ...
