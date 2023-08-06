"""
Sungai.

- Project URL: https://github.com/hugocartwright/sungai
"""
import argparse
import sys
from pathlib import Path

from .sungai import DirectoryRater

__version__ = "0.1.6"


def get_args():  # pragma: no cover
    """Get command line arguments."""
    parser = argparse.ArgumentParser(
        description="Sungai"
    )
    parser.add_argument(
        "target",
        type=str,
        help="The path to the target directory.",
    )
    parser.add_argument(
        "--min_score",
        type=float,
        help="The minimum score to pass.",
        required=False,
        default=None,
    )
    parser.add_argument(
        "--ignore_config",
        type=str,
        help="The ignore config file path. Must follow .gitignore syntax.",
        required=False,
        default=None,
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Add if you want verbose output.",
        required=False,
        default=False,
    )

    return parser.parse_args()


def run_sungai():  # pragma: no cover
    """Run sungai."""
    args = get_args()

    target = Path(args.target)

    if not target.is_dir():
        print("[sungai] Error: Target not found")
        sys.exit(1)

    ignore_config = None
    if args.ignore_config:
        ignore_config = Path(args.ignore_config)
        if not ignore_config.is_file():
            print("[sungai] Error: Could not find ignore_config file")
            sys.exit(1)

    try:
        print(f"Sungai ({__version__})")

        directory_rater = DirectoryRater(
            target,
            ignore_config=ignore_config,
        )
        sys.exit(
            directory_rater.run(
                verbose=args.verbose,
                min_score=args.min_score,
            )
        )
    except KeyboardInterrupt:
        sys.exit(1)
