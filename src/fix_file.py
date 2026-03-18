from __future__ import annotations

import logging
import os

from fix_string import fix_string

logger = logging.getLogger(__name__)

def fix_file(path: str) -> tuple[str, bool]:
    logger.debug("------------------------------------")
    directory, name = os.path.split(path)
    fixed_name, changed = fix_string(name)
    if not changed:
        return path, False
    new_path = os.path.join(directory, fixed_name) if directory else fixed_name
    return new_path, True


def main() -> None:
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")
    # Read filename directly from console input
    filename = input("Enter file path to fix: ")

    result, changed = fix_file(filename)

    if changed:
        logger.info("SUCCESS: {0} -> {1}".format(filename, result))
    else:
        logger.info("SKIPPED (No change): {0}".format(filename))

    # Output to console
    logger.info("\nFixed output:")
    try:
        logger.info(result)
    except Exception:
        logger.error("(character printing failed)")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
