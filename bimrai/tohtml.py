#!/usr/bin/env python3

"""Visualize a BIMRAI scenario to an HTML page."""
import argparse
import pathlib
import sys

import bimrai


def main() -> int:
    """Execute main method."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="Path to the BIMRAI scenario",
                        required=True)
    parser.add_argument("--output", help="Path to the HTML file",
                        required=True)

    args = parser.parse_args()

    source_path = pathlib.Path(args.input)
    target_path = pathlib.Path(args.output)

    return bimrai.process(source_path, target_path)


if __name__ == __name__:
    sys.exit(main())
