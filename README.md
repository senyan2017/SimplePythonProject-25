# SimplePythonProject
Example of Python for GSM Students

## Usage

```bash
python main.py                 # -> Let's Python Project
python main.py --name World    # -> Hello, World! Welcome to Let's Python Project
python main.py -n Alice        # short flag, identical to --name
```

An empty/whitespace name or an unknown flag exits with a non-zero status and a
clear `Error:`/usage message (input is never silently ignored).

Run the tests with `pytest`.

## Docker

```bash
docker build -t simple-python-project .
docker run --rm simple-python-project --name World   # same flags as the local command
```
