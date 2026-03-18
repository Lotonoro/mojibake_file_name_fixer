from __future__ import annotations

import argparse
import logging
import os
import sys

from fix_dir import fix_dir

logger = logging.getLogger(__name__)

def fix_dir_recursive(target_dir: str, dry_run: bool) -> None:
    if not os.path.exists(target_dir):
        logger.error(f"Error: Directory '{target_dir}' does not exist.")
        sys.exit(1)

    # We walk bottom-up (topdown=False) so that if we rename a parent directory, 
    # it doesn't break the paths of the files/directories inside it that we haven't visited yet.
    for root, dirs, files in os.walk(target_dir, topdown=False):
        logger.debug("Walking directory: %s", root)

        # 1. Fix files in this directory (non-recursive)
        fix_dir(root, dry_run)

def main() -> None:
    parser = argparse.ArgumentParser(description="Walk directories and fix file/directory names.")
    parser.add_argument("directory", help="The root directory to walk.")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without actually renaming files.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")
        logger.debug("Debug logging enabled")

    fix_dir_recursive(args.directory, args.dry_run)

if __name__ == "__main__":
    main()
