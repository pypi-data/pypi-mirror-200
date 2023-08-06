# (generated with --quick)

import collections
import hsuanwu.common.typing
import io
import numpy
import numpy as np
import omegaconf
import pathlib
import random
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

def dump_episode(episode, fn: pathlib.Path) -> None: ...
def episode_len(episode) -> int: ...
def load_episode(fn: pathlib.Path) -> dict: ...
def worker_init_fn(worker_id) -> None: ...
