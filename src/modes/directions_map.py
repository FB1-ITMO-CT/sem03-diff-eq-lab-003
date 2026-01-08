from argparse import ArgumentParser, Namespace

import matplotlib.axes as mpl_ax
import matplotlib.pyplot as plt
import numpy as np

from ..defs import vec_derivative


def fill_parser(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("left", type=np.float64, metavar="x_min")
    parser.add_argument("bottom", type=np.float64, metavar="y_min")
    parser.add_argument("right", type=np.float64, metavar="x_max")
    parser.add_argument("top", type=np.float64, metavar="y_max")
    parser.add_argument("resolution", type=int, metavar="N", help="number of dots along largest axis")

    return parser


def length(v: np.ndarray) -> np.float64:
    return np.sqrt(np.sum(v**2))


def render(args: Namespace, axes: mpl_ax.Axes) -> None:
    width: np.float64 = args.top - args.bottom
    height: np.float64 = args.right - args.left

    x_res = round(args.resolution * max(1.0, width / height))
    y_res = round(args.resolution * max(1.0, height / width))

    cell_size: float = min(width, height) / args.resolution * 0.8

    x_vals = np.linspace(args.bottom, args.top, num=x_res)
    y_vals = np.linspace(args.left, args.right, num=y_res)

    plot = [[vec_derivative(x, y) for x in x_vals] for y in y_vals]
    lengths = [[length(v) for v in line] for line in plot]
    max_length = max(map(max, lengths))

    def draw_arrow(x: float, y: float, v: np.ndarray) -> None:
        v_len = length(v)
        size: float = np.sqrt(v_len / max_length)
        dx, dy = v / v_len

        size *= cell_size

        axes.arrow(
            x - dx * size / 2,
            y - dy * size / 2,
            dx * size,
            dy * size,
            head_width=cell_size / 5,
            width=cell_size / 10,
        )

    for y, line in zip(y_vals, plot, strict=True):
        for x, v in zip(x_vals, line, strict=True):
            draw_arrow(x, y, v)


def main() -> None:
    args = fill_parser(ArgumentParser()).parse_args()

    fig, ax = plt.subplots(1, 1, layout="constrained")
    render(args, ax)

    fig.show()
    plt.show()


if __name__ == "__main__":
    main()
