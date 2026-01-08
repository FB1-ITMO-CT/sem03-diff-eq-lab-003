import typing as tp
from argparse import ArgumentParser, Namespace

import matplotlib.axes as mpl_ax
import matplotlib.pyplot as plt
import numpy as np

from ..defs import VEC_DERIVATIVE, vec_derivative, vec_derivative_lin
from .trajectories_map import iterate


def fill_parser(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("len", type=np.float64, metavar="line_len")
    parser.add_argument("precision", type=int, metavar="N", help="number of initial points per line")

    parser.add_argument(
        "points",
        type=lambda s: tuple(map(float, s.split(":"))),
        nargs="+",
        metavar="x:y",
        help="starting points",
    )

    return parser


def render(args: Namespace, axes: mpl_ax.Axes) -> None:
    def draw_line(x: float, y: float, f: VEC_DERIVATIVE):
        forward = iterate(x, y, args.len, args.precision, f)
        backward = iterate(x, y, -args.len, args.precision, f)

        (line,) = axes.plot(*zip(*forward, strict=True))
        (line2,) = axes.plot(*zip(*backward, strict=True), color=line.get_color())

        return (line, line2)

    for x, y in tp.cast("list[tuple[float, float]]", args.points):
        (main, _) = draw_line(x, y, vec_derivative)

        for line in draw_line(x, y, vec_derivative_lin(x, y)):
            line.set_color(main.get_color())
            line.set_linestyle("--")


def main() -> None:
    args = fill_parser(ArgumentParser()).parse_args()

    fig, ax = plt.subplots(1, 1, layout="constrained")
    render(args, ax)

    fig.show()
    plt.show()


if __name__ == "__main__":
    main()
