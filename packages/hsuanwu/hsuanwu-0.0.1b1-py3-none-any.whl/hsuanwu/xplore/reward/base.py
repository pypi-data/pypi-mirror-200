import torch

from hsuanwu.common.typing import *


class BaseIntrinsicRewardModule(object):
    """Base class of intrinsic reward module.

    Args:
        obs_shape: Data shape of observation.
        action_space: Data shape of action.
        action_type: Continuous or discrete action. "cont" or "dis".
        device: Device (cpu, cuda, ...) on which the code should be run.
        beta: The initial weighting coefficient of the intrinsic rewards.
        kappa: The decay rate.

    Returns:
        Instance of the base intrinsic reward module.
    """

    def __init__(
        self,
        obs_shape: Tuple,
        action_shape: Tuple,
        action_type: str,
        device: torch.device,
        beta: float,
        kappa: float,
    ) -> None:
        self._obs_shape = obs_shape
        self._action_shape = action_shape
        self._action_type = action_type

        self._device = torch.device(device)
        self._beta = beta
        self._kappa = kappa

    def compute_irs(self, rollouts: Dict, step: int) -> ndarray:
        """Compute the intrinsic rewards using the collected observations.

        Args:
            rollouts: The collected experiences. A python dict like
                {observations (n_steps, n_envs, *obs_shape) <class 'numpy.ndarray'>,
                actions (n_steps, n_envs, action_shape) <class 'numpy.ndarray'>,
                rewards (n_steps, n_envs, 1) <class 'numpy.ndarray'>}.
            step: The current time step.

        Returns:
            The intrinsic rewards.
        """
        pass

    def update(
        self,
        rollouts: Dict,
    ) -> None:
        """Update the intrinsic reward module if necessary.

        Args:
            rollouts: The collected experiences. A python dict like
                {observations (n_steps, n_envs, *obs_shape) <class 'numpy.ndarray'>,
                actions (n_steps, n_envs, action_shape) <class 'numpy.ndarray'>,
                rewards (n_steps, n_envs, 1) <class 'numpy.ndarray'>}.

        Returns:
            None
        """
        pass
