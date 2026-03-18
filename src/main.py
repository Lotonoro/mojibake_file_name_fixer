from __future__ import annotations

import argparse
import logging
import os
import sys

from fix_dir import fix_dir
from fix_dir_recursive import fix_dir_recursive
from fix_file import fix_file
from fix_string import fix_string

logger = logging.getLogger(__name__)

def _configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s:%(name)s:%(message)s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fix mojibake in filenames or strings.")
    parser.add_argument(
        "--mode",
        choices=["string", "file", "dir"],
        help="Input mode. If omitted, auto-detect from --input.",
    )
    parser.add_argument(
        "--input",
        help="Input text or path.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print changes without actually renaming files (dir mode only).",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Process directories recursively (dir mode only).",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging.",
    )

    args = parser.parse_args()
    _configure_logging(args.debug)

    prompt = "Enter string or path to fix: "
    if args.mode == "file":
        prompt = "Enter file path to fix: "
    elif args.mode == "dir":
        prompt = "Enter directory path to fix: "

    input_value = args.input if args.input is not None else input(prompt)

    mode = args.mode
    if mode is None:
        if os.path.isfile(input_value):
            mode = "file"
        elif os.path.isdir(input_value):
            mode = "dir"
        else:
            mode = "string"

    if mode == "string":
        fixed, changed = fix_string(input_value)
        if not changed:
            logger.info("No fix needed.")
        else:
            logger.info(fixed)
        return

    if mode == "file":
        if not os.path.exists(input_value):
            logger.error(f"Error: File '{input_value}' does not exist.")
            sys.exit(1)
        fixed, changed = fix_file(input_value)
        if changed:
            logger.info(f"SUCCESS: {input_value} -> {fixed}")
        else:
            logger.info(f"SKIPPED (No change): {input_value}")
        return

    if mode == "dir":
        if args.recursive:
            fix_dir_recursive(input_value, args.dry_run)
        else:
            fix_dir(input_value, args.dry_run)
        return

    logger.error(f"Error: Unsupported mode '{mode}'.")
    sys.exit(1)


if __name__ == "__main__":
    main()
