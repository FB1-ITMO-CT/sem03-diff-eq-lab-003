import typing as tp
from collections.abc import Callable

import numpy as np


def x_derivative(_: tp.Any, y: tp.Any) -> tp.Any:
    return -y * np.log(2 * y**2 - 1)


def y_derivative(x: tp.Any, y: tp.Any) -> tp.Any:
    return x - y - 2 * y**2


type VEC_DERIVATIVE = Callable[[float, float], np.ndarray]


def vec_derivative(x: float, y: float) -> np.ndarray:
    return np.array([x_derivative(x, y), y_derivative(x, y)])


def vec_derivative_lin(_: float, y: float) -> VEC_DERIVATIVE:
    matrix = np.array(
        [
            [0, -np.log(2 * y**2 - 1) - 4 * y**2 / (2 * y**2 - 1)],
            [1, -1 - 4 * y],
        ],
    )

    def impl(x: float, y: float) -> np.ndarray:
        return matrix @ np.array([x, y])

    return impl
