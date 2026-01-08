import typing as tp
from argparse import ArgumentParser, Namespace

if tp.TYPE_CHECKING:
    from collections.abc import Callable

import matplotlib.axes as mpl_ax
import matplotlib.pyplot as plt
import numpy as np

from ..defs import VEC_DERIVATIVE, vec_derivative


def runge_kutta_4(x: float, y: float, h: float, f: VEC_DERIVATIVE) -> tuple[float, float]:
    v = np.array((x, y))
    h2 = h * 0.5

    k1 = f(*v)
    k2 = f(*(v + k1 * h2))
    k3 = f(*(v + k2 * h2))
    k4 = f(*(v + k3 * h))

    return tuple(v + (k1 + k2 * 2 + k3 * 2 + k4) * (1.0 / 6.0) * h)


type LIMITER_FUNC = Callable[[float, float], bool]


def iterate(
    x: float,
    y: float,
    dist: float,
    count: int,
    f: VEC_DERIVATIVE,
    limiter: LIMITER_FUNC = lambda _, __: True,
) -> list[tuple[float, float]]:
    result = [(x, y)]
    for _ in range(count):
        x, y = runge_kutta_4(x, y, dist / count, f)

        if not limiter(x, y):
            break

        result.append((x, y))

    return result


def fill_parser(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("left", type=np.float64, metavar="x_min")
    parser.add_argument("bottom", type=np.float64, metavar="y_min")
    parser.add_argument("right", type=np.float64, metavar="x_max")
    parser.add_argument("top", type=np.float64, metavar="y_max")
    parser.add_argument("resolution", type=int, metavar="N", help="number of initial points along largest axis")
    parser.add_argument("len", type=np.float64, metavar="line_len")
    parser.add_argument("precision", type=int, metavar="N", help="number of initial points per line")

    return parser


def render(args: Namespace, axes: mpl_ax.Axes) -> None:
    width: np.float64 = args.top - args.bottom
    height: np.float64 = args.right - args.left

    x_res = round(args.resolution * max(1.0, width / height))
    y_res = round(args.resolution * max(1.0, height / width))

    x_vals = np.linspace(args.bottom, args.top, num=x_res)
    y_vals = np.linspace(args.left, args.right, num=y_res)

    def limiter(x: float, y: float) -> bool:
        return (
            args.left - width / 2 <= x <= args.right + width / 2
            and args.bottom - height / 2 <= y <= args.top + height / 2
        )

    for y in y_vals:
        for x in x_vals:
            forward = iterate(x, y, args.len, args.precision, vec_derivative, limiter)
            backward = iterate(x, y, -args.len, args.precision, vec_derivative, limiter)

            (line,) = axes.plot(*zip(*forward, strict=True))
            axes.plot(*zip(*backward, strict=True), color=line.get_color())


def main() -> None:
    args = fill_parser(ArgumentParser()).parse_args()

    fig, ax = plt.subplots(1, 1, layout="constrained")
    render(args, ax)

    fig.show()
    plt.show()


if __name__ == "__main__":
    main()
