# Mojibake File Name Fixer

A collection of Python scripts to automatically detect and fix mojibake or other encoding errors in text files and filenames/directories.

This is particularly useful when dealing with filenames or text content that has been incorrectly encoded (e.g., Japanese/Chinese characters that display as garbled characters due to Shift-JIS / GB18030 / UTF-8 mismatches, or Windows-1252 corruption).

## Dependencies

The core encoding fix logic requires the Python [ftfy](https://ftfy.readthedocs.io/en/latest/) library for robust, statistical-model based repairs.

This project uses `uv` for dependency management (Python >= 3.11). To install dependencies from the lockfile:
```bash
uv sync
```

If you need to add the dependency to a fresh project:
```bash
uv add ftfy
```

To run the scripts with the managed environment:
```bash
uv run python src/main.py
```

## Scripts

### Single Entry Point (`src/main.py`)

Use `main.py` to choose the input mode. If no mode is provided, it auto-detects from `--input`. If the input is a file path, it runs in `file` mode; if it’s a directory, it runs in `dir` mode; otherwise it treats the input as a string. You can pass `--mode` to override the auto-detected mode.

**Usage:**

```bash
# Fix a single string (auto-detect from input)
uv run python src/main.py --input "garbled text here"
```

```bash
# Fix a file path
uv run python src/main.py --input "/path/to/bad_filename.txt"
```

```bash
# Fix files in a directory (non-recursive)
uv run python src/main.py --input "/path/to/dir"
```

```bash
# Fix files recursively (file names only; directory names are not changed)
uv run python src/main.py --input "/path/to/dir" --recursive --dry-run
```

### Standalone Scripts

Each script can also be run directly:

```bash
# Fix a string (reads from prompt)
uv run python src/fix_string.py
```

```bash
# Fix a single file path (reads from prompt)
uv run python src/fix_file.py
```

```bash
# Fix files in a directory (non-recursive)
uv run python src/fix_dir.py /path/to/dir --dry-run
```

```bash
# Walk directories and fix files (file names only)
uv run python src/fix_dir_recursive.py /path/to/dir --dry-run
```

## How the fixing works (`encoding_tools.py`)

All scripts delegate to the `fix_text()` logic located inside `encoding_tools.py`. It uses `ftfy.fix_text()` and accepts a fix only when it improves a generalized “badness” score based on Unicode categories. It also preserves protected tokens (runs of CJK or ASCII alphanumerics) to avoid destructive changes.
