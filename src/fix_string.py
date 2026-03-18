from __future__ import annotations

import logging

from encoding_tools import fix_text

logger = logging.getLogger(__name__)

def fix_string(text: str) -> tuple[str, bool]:
    return fix_text(text)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")
    text = input("Enter string to fix: ")
    result, changed = fix_string(text)
    if not changed:
        logger.info("No fix needed.")
    else:
        logger.info(result)


if __name__ == "__main__":
    main()
