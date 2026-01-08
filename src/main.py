import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from src.modes import trajectories

from .modes import dir_map


def main() -> None:
    parser = argparse.ArgumentParser()

    modes = parser.add_subparsers(title="mode", required=True)
    dir_map.fill_parser(modes.add_parser("dir_map")).set_defaults(module=dir_map)
    trajectories.fill_parser(modes.add_parser("traj")).set_defaults(module=trajectories)

    parser.add_argument("-out", type=Path, metavar="img path")
    parser.add_argument("-figsize", type=lambda s: tuple(map(int, s.split(":"))), metavar="h:w", default=(12, 8))

    args = parser.parse_args()

    fig, ax = plt.subplots(1, 1, layout="constrained", figsize=args.figsize)
    args.module.render(args, ax)

    if args.out is not None:
        fig.savefig(args.out)
    else:
        fig.show()
        plt.show()


if __name__ == "__main__":
    main()
