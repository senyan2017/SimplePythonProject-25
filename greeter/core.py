"""Core greeting logic, input validation and result types.

This module owns *what* a greeting looks like and *which* inputs are valid. It
deliberately knows nothing about argument parsing or environment variables so it
can be exercised in isolation.

Two complementary APIs are provided:

* :func:`build_greeting` -- Pythonic, raises :class:`GreetingError` on bad input.
* :func:`greet` -- never raises for validation problems; instead it returns a
  structured :class:`GreetingResult` so callers can cleanly distinguish a
  successful greeting from an input-validation failure.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import Config

# Exit codes shared with the CLI layer.
EXIT_OK = 0
EXIT_VALIDATION = 2

# A name longer than this is almost certainly a mistake (or abuse); reject it
# with a clear error rather than printing a wall of text.
MAX_NAME_LENGTH = 100

# Greeting word per (language, scene). Scenes are uniform across languages so a
# scene is valid for every supported language.
GREETINGS = {
    "en": {
        "default": "Hello",
        "morning": "Good morning",
        "evening": "Good evening",
        "formal": "Greetings",
        "casual": "Hey",
    },
    "ko": {
        "default": "안녕하세요",
        "morning": "좋은 아침이에요",
        "evening": "좋은 저녁이에요",
        "formal": "안녕하십니까",
        "casual": "안녕",
    },
    "zh": {
        "default": "你好",
        "morning": "早上好",
        "evening": "晚上好",
        "formal": "您好",
        "casual": "嗨",
    },
    "es": {
        "default": "Hola",
        "morning": "Buenos días",
        "evening": "Buenas noches",
        "formal": "Saludos",
        "casual": "Hey",
    },
    "ja": {
        "default": "こんにちは",
        "morning": "おはようございます",
        "evening": "こんばんは",
        "formal": "ご挨拶申し上げます",
        "casual": "やあ",
    },
    "fr": {
        "default": "Bonjour",
        "morning": "Bonjour",
        "evening": "Bonsoir",
        "formal": "Salutations",
        "casual": "Salut",
    },
}

# Sorted/ordered views used for validation and help text.
SUPPORTED_LANGUAGES = sorted(GREETINGS.keys())
SUPPORTED_SCENES = ["default", "morning", "evening", "formal", "casual"]


class GreetingError(Exception):
    """Raised when the requested greeting cannot be built from the input.

    ``code`` is a short, stable, machine-readable identifier so callers (and
    tests) can branch on the failure type without parsing the message text.
    """

    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code


@dataclass
class GreetingResult:
    """Outcome of a greeting request.

    Using a structured result instead of a bare string lets callers tell a
    successful greeting apart from a validation failure -- which is exactly what
    you want when debugging output coming out of a container.
    """

    ok: bool
    message: str
    code: str = "OK"

    @property
    def exit_code(self) -> int:
        return EXIT_OK if self.ok else EXIT_VALIDATION


def _validate(name: str, language: str, scene: str) -> str:
    """Validate inputs and return the cleaned-up name.

    Raises :class:`GreetingError` with an appropriate ``code`` on failure.
    """

    cleaned = name.strip()
    if not cleaned:
        raise GreetingError("name must not be empty", code="EMPTY_NAME")
    if len(cleaned) > MAX_NAME_LENGTH:
        raise GreetingError(
            "name must be at most {} characters".format(MAX_NAME_LENGTH),
            code="NAME_TOO_LONG",
        )
    if language not in GREETINGS:
        raise GreetingError(
            "unsupported language '{}'; choose from: {}".format(
                language, ", ".join(SUPPORTED_LANGUAGES)
            ),
            code="UNSUPPORTED_LANGUAGE",
        )
    if scene not in SUPPORTED_SCENES:
        raise GreetingError(
            "unsupported scene '{}'; choose from: {}".format(
                scene, ", ".join(SUPPORTED_SCENES)
            ),
            code="UNSUPPORTED_SCENE",
        )
    return cleaned


def build_greeting(name: str, language: str, scene: str) -> str:
    """Return a formatted greeting string or raise :class:`GreetingError`."""

    cleaned = _validate(name, language, scene)
    word = GREETINGS[language][scene]
    return "{}, {}!".format(word, cleaned)


def greet(config: Config) -> GreetingResult:
    """Build a greeting from ``config`` and wrap the outcome in a result.

    Validation problems are reported via the returned :class:`GreetingResult`
    rather than as exceptions, so the CLI flow stays linear.
    """

    try:
        message = build_greeting(config.name, config.language, config.scene)
    except GreetingError as exc:
        return GreetingResult(ok=False, message=str(exc), code=exc.code)
    return GreetingResult(ok=True, message=message, code="OK")
