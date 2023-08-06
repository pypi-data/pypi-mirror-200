"""Utility functions for argument types."""

import numbers
from typing import Optional

import numpy as np

from probnum.typing import DTypeLike, ScalarLike, ShapeLike, ShapeType

__all__ = ["as_shape", "as_numpy_scalar"]


def as_shape(x: ShapeLike, ndim: Optional[numbers.Integral] = None) -> ShapeType:
    """Convert a shape representation into a shape defined as a tuple of ints.

    Parameters
    ----------
    x
        Shape representation.
    ndim
        The required number of dimensions in the shape.

    Raises
    ------
    TypeError
        If ``x`` is not a valid :const:`ShapeLike`.
    TypeError
        If ``x`` does not feature the required number of dimensions.
    """
    if isinstance(x, (int, numbers.Integral, np.integer)):
        shape = (int(x),)
    elif isinstance(x, tuple) and all(isinstance(item, int) for item in x):
        shape = x
    else:
        try:
            _ = iter(x)
        except TypeError as e:
            raise TypeError(
                f"The given shape {x} must be an integer or an iterable of integers."
            ) from e

        if not all(isinstance(item, (int, numbers.Integral, np.integer)) for item in x):
            raise TypeError(f"The given shape {x} must only contain integer values.")

        shape = tuple(int(item) for item in x)

    if isinstance(ndim, numbers.Integral):
        if len(shape) != ndim:
            raise TypeError(f"The given shape {shape} must have {ndim} dimensions.")

    return shape


def as_numpy_scalar(x: ScalarLike, dtype: DTypeLike = None) -> np.ndarray:
    """Convert a scalar into a scalar NumPy array.

    Parameters
    ----------
    x
        Scalar value.
    dtype
        Data type of the scalar.

    Raises
    ------
    ValueError
        If :code:`x` can not be interpreted as a scalar.
    """

    if np.ndim(x) != 0:
        raise ValueError("The given input is not a scalar.")

    return np.asarray(x, dtype=dtype)
