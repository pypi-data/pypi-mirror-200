from typing import Callable, Optional, Tuple

import jax
import jax.numpy as jnp
from gymnasium import Env
from jaxtyping import Array, Float


def get_trajectory(
    env: Env,
    key: jax.random.PRNGKeyArray,
    act_fn: Callable[..., int],
    act_fn_kwargs: dict,
    obs_preprocessing_fn: Optional[Callable] = None,
    obs_preprocessing_fn_kwargs: Optional[dict] = None,
    render=False,
) -> Tuple[Float[Array, "n_env_steps 1"], jnp.ndarray, jnp.ndarray]:
    if obs_preprocessing_fn is None:

        def obs_preprocessing_fn(x):
            return x

    if obs_preprocessing_fn_kwargs is None:
        obs_preprocessing_fn_kwargs = {}

    obs, _ = env.reset()
    rewards = []
    eps_obs = []
    eps_actions = []

    while True:
        key, subkey = jax.random.split(key)

        obs = obs_preprocessing_fn(obs, **obs_preprocessing_fn_kwargs)
        eps_obs.append(obs)
        action = act_fn(obs, **act_fn_kwargs, key=subkey)
        obs, reward, terminated, truncated, _ = env.step(int(action))

        if render:
            env.render()

        rewards.append(reward)
        eps_actions.append(action)
        if terminated or truncated:
            break
    eps_obs = jnp.stack(eps_obs)
    eps_actions = jnp.array(eps_actions)

    return rewards, eps_obs, eps_actions
