# SimplePythonProject

A small, configurable command-line greeting tool.

## Usage

```
python main.py [--name NAME] [--language LANG] [--scene SCENE]
```

- `--name`, `-n`: who to greet (default: `World`)
- `--language`, `-l`: one of `en`, `es`, `fr`, `ja`, `ko`, `zh` (default: `en`)
- `--scene`, `-s`: one of `default`, `morning`, `evening`, `formal`, `casual` (default: `default`)

Values not supplied on the command line fall back to the environment variables
`GREETER_NAME`, `GREETER_LANGUAGE`, `GREETER_SCENE`, then to the built-in defaults.

Examples:

```
python main.py
# Hello, World!

python main.py --name Bob --language ko --scene morning
# 좋은 아침이에요, Bob!

GREETER_NAME=Eve python main.py
# Hello, Eve!
```

Successful greetings are written to stdout (exit code `0`). Invalid input is
written to stderr with an error code (exit code `2`):

```
python main.py --language xx
# error: unsupported language 'xx'; choose from: en, es, fr, ja, ko, zh (code=UNSUPPORTED_LANGUAGE)
```

## Docker

```
docker build -t greeter .
docker run --rm greeter
docker run --rm greeter --name Bob -l ko -s morning
docker run --rm -e GREETER_NAME=Eve greeter
```

## Tests

```
python -m pytest
```

Container tests are opt-in (they build and run the image):

```
RUN_DOCKER_TESTS=1 python -m pytest tests/test_docker.py
```

---

Example of Python for GSM Students
