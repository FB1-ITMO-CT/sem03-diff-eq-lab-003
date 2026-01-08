import typing as tp

import numpy as np


def x_derivative(_: tp.Any, y: tp.Any) -> tp.Any:
    return -y * np.log(2 * y**2 - 1)


def y_derivative(x: tp.Any, y: tp.Any) -> tp.Any:
    return x - y - 2 * y**2


def vec_derivative(x: tp.Any, y: tp.Any) -> np.ndarray:
    return np.array([x_derivative(x, y), y_derivative(x, y)])
