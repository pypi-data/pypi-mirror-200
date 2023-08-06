# (generated with --quick)

import collections
import gym
import hsuanwu.common.typing
import numpy
import numpy as np
import omegaconf
import pathlib
import torch
from typing import Any, Tuple, Type

Batch: Type[hsuanwu.common.typing.Batch]
DataLoader: Any
DictConfig: Any
Distribution: Any
Env: Any
Path: Type[pathlib.Path]
Space: Any
Tensor: Any
deque: Type[collections.deque]
ndarray: Type[numpy.ndarray]
register: Any

class FrameStack(Any):
    _frames: collections.deque
    _k: Any
    _max_episode_steps: Any
    observation_space: Any
    def __init__(self, env, k) -> None: ...
    def _get_obs(self) -> Any: ...
    def reset(self) -> Any: ...
    def step(self, action) -> Tuple[Any, Any, Any, Any]: ...

def make_dmc_env(env_id: str = ..., resource_files: str = ..., img_source: str = ..., total_frames: int = ..., seed: int = ..., visualize_reward: bool = ..., from_pixels: bool = ..., height: int = ..., width: int = ..., camera_id: int = ..., frame_stack: int = ..., frame_skip: int = ..., episode_length: int = ..., environment_kwargs = ...) -> Any: ...
