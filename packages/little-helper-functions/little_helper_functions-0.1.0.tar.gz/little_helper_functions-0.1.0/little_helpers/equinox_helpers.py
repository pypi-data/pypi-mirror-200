import logging

import equinox as eqx
from jaxtyping import PyTree
from optax import GradientTransformation

_logger = logging.getLogger(__name__)


def eqx_init_optimiser(optim: GradientTransformation, params: PyTree) -> PyTree:
    """Initialise an optax optimiser with a given set of parameters.
        Filters out non-array parameters (e.g. functions) using `eqx.is_array`.
    Args:
        optim: The optax optimiser to initialise.
        params: The parameters to initialise the optimiser with.

    Returns:
        The initialised optimiser state.
    """
    return optim.init(eqx.filter(params, eqx.is_array))


def get_flatten_shape(
    width,
    height,
    kernel_size,
    stride=1,
    padding=0,
    out_channels=1,
    pool_kernel_size=2,
    pool_stride=1,
):

    if kernel_size > width or kernel_size > height:
        raise ValueError("Kernel size cannot be larger than image size.")

    out_height_conv = (height - kernel_size + 2 * padding) / stride + 1
    out_width_conv = (width - kernel_size + 2 * padding) / stride + 1
    out_height_pool = (out_height_conv - pool_kernel_size) / pool_stride + 1
    out_width_pool = (out_width_conv - pool_kernel_size) / pool_stride + 1
    flattened_size = out_height_pool * out_width_pool * out_channels
    return int(flattened_size)
