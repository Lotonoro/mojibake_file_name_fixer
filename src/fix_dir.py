from __future__ import annotations

import argparse
import logging
import os
import sys

from fix_file import fix_file

logger = logging.getLogger(__name__)


def fix_dir(directory: str, dry_run: bool) -> None:
    logger.info(f"  ====== {directory} ======")
    for name in os.listdir(directory):
        old_path = os.path.join(directory, name)
        if not os.path.isfile(old_path):
            continue
        new_path, changed = fix_file(old_path)
        if not changed:
            continue
        fixed_name = os.path.basename(new_path)

        if dry_run:
            logger.info(f"[DRY-RUN] File: {name} -> {fixed_name}")
        else:
            try:
                os.rename(old_path, new_path)
                logger.info(f"Renamed file: {name} -> {fixed_name}")
            except Exception as e:
                logger.error(f"Error renaming file '{old_path}': {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fix file names within a directory (non-recursive).")
    parser.add_argument("directory", help="The directory to process.")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without actually renaming files.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")
        logger.debug("Debug logging enabled")

    target_dir = args.directory
    if not os.path.isdir(target_dir):
        logger.error(f"Error: Directory '{target_dir}' does not exist.")
        sys.exit(1)

    fix_dir(target_dir, args.dry_run)


if __name__ == "__main__":
    main()
