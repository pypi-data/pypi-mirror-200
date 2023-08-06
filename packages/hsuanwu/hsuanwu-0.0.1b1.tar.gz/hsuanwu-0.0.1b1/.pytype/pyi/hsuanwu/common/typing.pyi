# (generated with --quick)

import collections
import numpy
import omegaconf
import pathlib
import torch
from typing import Any, NamedTuple, Type

DataLoader: Any
DictConfig: Any
Distribution: Any
Env: Any
Path: Type[pathlib.Path]
Space: Any
Tensor: Any
ndarray: Type[numpy.ndarray]

class Batch(NamedTuple):
    observations: Any
    actions: Any
    rewards: Any
    dones: Any
    next_observations: Any
