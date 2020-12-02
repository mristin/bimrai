#!/usr/bin/env python3

"""Generate HTML for all the scenarios in a directory in-place."""
import argparse
import pathlib
import sys

import bimrai


def main() -> int:
    """Execute the main routine."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenarios_dir", help="Path to the directory with the scenarios",
        required=True)

    args = parser.parse_args()

    scenarios_dir = pathlib.Path(args.scenarios_dir)

    for src_pth in scenarios_dir.glob("**/*.md"):
        tgt_pth = src_pth.parent / (src_pth.stem + ".html")
        exit_code = bimrai.process(
            source_path=src_pth, target_path=tgt_pth)

        if exit_code != 0:
            return exit_code


if __name__ == "__main__":
    sys.exit(main())
