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
Box: Any
DataLoader: Any
DictConfig: Any
Distribution: Any
Env: Any
NormalizeReward: Any
Path: Type[pathlib.Path]
ProcgenEnv: Any
RecordEpisodeStatistics: Any
Space: Any
Tensor: Any
TransformObservation: Any
TransformReward: Any
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

def make_procgen_env(env_id: str = ..., num_envs: int = ..., gamma: float = ..., num_levels: int = ..., start_level: int = ..., distribution_mode: str = ..., device = ...) -> Any: ...
