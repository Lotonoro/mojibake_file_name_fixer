# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import unicodedata
import ftfy

logger = logging.getLogger(__name__)

def fix_text(text: str) -> tuple[str, bool]:
    """
    Single-pass fix with a change flag to avoid double fixing.
    """
    logger.debug("Starting fix_text (ftfy.fix_text). length=%d, text=%s", len(text), text)
    fixed = ftfy.fix_text(text)
    if fixed == text:
        logger.debug("No change after ftfy.fix_text")
        return fixed, False

    # Only accept the fix if it reduces "badness" based on Unicode categories,
    # avoiding brittle character lists.
    original_score = _badness_score(text)
    fixed_score = _badness_score(fixed)
    logger.debug("Badness score original=%d fixed=%d", original_score, fixed_score)
    logger.debug("Original: %s", text)
    logger.debug("  Fixed : %s", fixed)
    if fixed_score <= original_score and _preserves_protected_tokens(text, fixed):
        logger.debug("Accepted fix")
        return fixed, True

    logger.debug("Rejected fix; returning original")
    return text, False


def _badness_score(text: str) -> int:
    """
    Generalized heuristic: count problematic Unicode categories plus replacement chars.
    Lower is better.
    """
    score = 0
    for c in text:
        if c == "\ufffd":
            score += 2
            continue
        cat = unicodedata.category(c)
        if cat in {"Mn", "Me", "Co", "Cn"}:
            score += 1
    return score


def _preserves_protected_tokens(original: str, fixed: str) -> bool:
    original_norm = unicodedata.normalize("NFC", original)
    fixed_norm = unicodedata.normalize("NFC", fixed)
    tokens = _protected_tokens(original_norm)
    for token in tokens:
        if token not in fixed_norm:
            logger.debug("Protected token missing after fix: %s", token)
            return False
    return True


def _protected_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    current: list[str] = []
    current_is_cjk: bool | None = None

    def flush() -> None:
        if len(current) >= 2:
            tokens.append("".join(current))
        current.clear()

    for ch in text:
        is_cjk = _is_cjk(ch)
        is_ascii_alnum = ch.isascii() and ch.isalnum()

        if is_cjk:
            if current_is_cjk is False:
                flush()
            current_is_cjk = True
            current.append(ch)
            continue

        if is_ascii_alnum:
            if current_is_cjk is True:
                flush()
            current_is_cjk = False
            current.append(ch)
            continue

        if current:
            flush()
            current_is_cjk = None

    if current:
        flush()

    return tokens


def _is_cjk(ch: str) -> bool:
    code = ord(ch)
    # Han (CJK Unified Ideographs)
    if 0x4E00 <= code <= 0x9FFF:
        return True
    # Hiragana, Katakana
    if 0x3040 <= code <= 0x30FF:
        return True
    # Hangul
    if 0xAC00 <= code <= 0xD7AF:
        return True
    return False
