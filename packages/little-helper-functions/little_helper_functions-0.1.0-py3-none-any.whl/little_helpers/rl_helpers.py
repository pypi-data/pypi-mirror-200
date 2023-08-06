import logging
from typing import assert_type

import jax.numpy as jnp
import numpy as np
from jaxtyping import Array

_logger = logging.getLogger(__name__)

__author__ = "Artur A. Galstyan"
__copyright__ = "Artur A. Galstyan"
__license__ = "MIT"


def get_future_rewards(rewards: Array, gamma=0.99) -> Array:
    """Calculate the future rewards for a given set of rewards.
    Args:
        rewards: The rewards to calculate the future rewards for.
        gamma: The discount factor.

    Returns:
        The future rewards.
    """
    
    assert_type(rewards, Array)
    assert_type(gamma, float)



    T = len(rewards)
    returns = np.empty(T)
    future_returns = 0.0
    for t in reversed(range(T)):
        future_returns = rewards[t] + gamma * future_returns
        returns[t] = future_returns
    return jnp.array(returns)


if __name__ == "__main__":
    pass
