# Advent of code 2024

<https://adventofcode.com/2024>

Helping Santa with Python.

Tested with Python 3.12.

## Install

1. Make a venv
2. Activate the venv
3. Install requirements

```shell
# Make a venv
$ pyenv virtualenv 3.12.7 aoc2024

# Activate the venv
$ pyenv activate aoc2024

# Install requirements
$ pip install -r requirements.txt
```

## Input data

Expects a directory called `data` in this directory, containing a directory for each day, containing that day's data file. For example:

- `data/day01/input.txt`
- `data/day02/input.txt`
- `data/day03/input.txt`
- ...

## PYTHONPATH

For Python to find the code, the `PYTHONPATH` env var needs to point to the `src` directory. Sourcing `bin/activate.sh` will set it.

## Run

Run all the days with `bin/run.sh`

Run an individual day with `./run.py` in the day's directory.
