# Copyright 2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Implementation of MLPActorActor."""

from __future__ import annotations

import torch
from torch.distributions import Distribution

from omnisafe.models.base import Actor
from omnisafe.typing import Activation, InitFunction, OmnisafeSpace
from omnisafe.utils.model import build_mlp_network


# pylint: disable-next=too-many-instance-attributes
class MLPActor(Actor):
    """Implementation of MLPActor."""

    def __init__(
        self,
        obs_space: OmnisafeSpace,
        act_space: OmnisafeSpace,
        hidden_sizes: list[int],
        activation: Activation = 'relu',
        output_activation: Activation = 'identity',
        weight_initialization_mode: InitFunction = 'kaiming_uniform',
    ) -> None:
        """Initialize MLPActor.

        Args:
            obs_space (OmnisafeSpace): Observation space.
            act_space (OmnisafeSpace): Action space.
            hidden_sizes (list): List of hidden layer sizes.
            activation (Activation): Activation function.
            output_activation (Activation): Output activation function.
            weight_initialization_mode (InitFunction): Weight initialization mode.
        """
        super().__init__(obs_space, act_space, hidden_sizes, activation, weight_initialization_mode)
        self.net = build_mlp_network(
            sizes=[self._obs_dim, *self._hidden_sizes, self._act_dim],
            activation=activation,
            output_activation=output_activation,
            weight_initialization_mode=weight_initialization_mode,
        )
        self._noise = 0.2
        self._noise_clip = 100
        self.register_buffer('_act_min', torch.tensor(self._act_space.low, dtype=torch.float32))
        self.register_buffer('_act_max', torch.tensor(self._act_space.high, dtype=torch.float32))

    def predict(
        self,
        obs: torch.Tensor,
        deterministic: bool = True,
    ) -> torch.Tensor:
        """Predict the action given observation.

        The predicted action depends on the ``deterministic`` flag.

        - If ``deterministic`` is ``True``, the predicted action is the mean of the distribution.
        - If ``deterministic`` is ``False``, the predicted action is sampled from the distribution.

        Args:
            obs (torch.Tensor): Observation.
            deterministic (bool): Whether to use deterministic policy.
        """
        action = torch.tanh(self.net(obs))
        if deterministic:
            return action

        noise = torch.normal(0, self._noise * torch.ones_like(action))
        noise = torch.clamp(noise, -self._noise_clip, self._noise_clip)
        return torch.clamp(action + noise, self._act_min, self._act_max)

    @property
    def noise(self) -> float:
        """Get the action noise."""
        return self._noise

    @noise.setter
    def noise(self, noise: float) -> None:
        """Set the action noise."""
        assert noise >= 0, 'Noise should be non-negative.'
        self._noise = noise

    @property
    def noise_clip(self) -> float:
        """Get the action noise bound."""
        return self._noise_clip

    @noise_clip.setter
    def noise_clip(self, noise_clip: float) -> None:
        assert noise_clip >= 0, 'Noise clip should be non-negative.'
        self._noise_clip = noise_clip

    def _distribution(self, obs: torch.Tensor) -> Distribution:
        raise NotImplementedError

    def forward(self, obs: torch.Tensor) -> Distribution:
        raise NotImplementedError

    def log_prob(self, act: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError
