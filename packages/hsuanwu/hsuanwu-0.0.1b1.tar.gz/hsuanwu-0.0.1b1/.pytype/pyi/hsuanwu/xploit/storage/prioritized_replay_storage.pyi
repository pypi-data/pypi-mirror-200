# (generated with --quick)

import numpy as np
import random
import torch
from typing import Any, List, Tuple

class PrioritizedReplayStorage:
    alpha: Any
    beta: Any
    beta_schedule: Any
    buffer: List[Tuple[Any, Any, Any, Any, Any]]
    buffer_size: Any
    epsilon: Any
    position: Any
    priorities: Any
    size: Any
    def __init__(self, buffer_size, alpha = ..., beta = ..., beta_schedule = ..., epsilon = ...) -> None: ...
    def add(self, state, action, reward, next_state, done) -> None: ...
    def sample(self, batch_size) -> Tuple[Any, Any, Any, Any, Any, Any, Any]: ...
    def update_priorities(self, indices, priorities) -> None: ...
