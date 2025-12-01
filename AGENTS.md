# Agent Guidelines for Advent of Code Repository

## Running Code
- Run Python files directly: `python <year>/dec<day>.py` (e.g., `python 2024/dec01.py`)
- No formal test framework; toggle `runtest = True/False` in each file to switch between test and real input
- Test data in `<year>/dec<day>_test.txt`, real data in `<year>/dec<day>.txt` (auto-downloaded if missing)
- New day setup: `make today` or `python newday.py --year=YYYY --day=DD`

## Code Style & Formatting
- **Formatting**: Uses `black` formatter with `isort` (profile=black). Max line length: 120 chars (flake8)
- **Imports**: Standard library first, then third-party (e.g., `from reader import ...`). Use `# noqa` sparingly
- **Types**: Optional type hints (e.g., `Dict[int, List[int]]`), but not required
- **Naming**: Snake_case for variables/functions. `stardate` for day string, `year` for year string
- **Structure**: Each solution has `star1()` and `star2()` functions decorated with `@timeit`, called at module level
- **Logging**: Use `logging.debug()` for debug output, `logging.info()` for results, `print()` for final answers
- **Data**: Always copy data with `data2 = data[:]` before passing to star2 to avoid mutation issues

## Pre-commit Hooks
- Runs: black, isort, flake8, trailing-whitespace, end-of-file-fixer, check-added-large-files, gitleaks
- Run manually: `pre-commit run --all-files`

## File Conventions
- Solutions: `<year>/dec<day>.py` (e.g., `2024/dec01.py`)
- Input files (*.txt) are gitignored; use reader.py's `get_data()` to auto-download with AOC_SESSION env var
