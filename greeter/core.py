"""Core greeting logic and output formatting."""

import json
import sys
from typing import Optional

# Supported languages and scenes
SUPPORTED_LANGS = ("en", "ko", "zh", "ja")
SUPPORTED_SCENES = ("formal", "casual", "birthday", "newyear")

# Greeting templates: GREETINGS[scene][lang]
# Each template contains {name} placeholder.
GREETINGS = {
    "formal": {
        "en": "Good day, {name}. It is a pleasure to meet you.",
        "ko": "{name}님, 안녕하세요. 만나뵙게 되어 영광입니다.",
        "zh": "{name}，您好。很高兴认识您。",
        "ja": "{name}様、はじめまして。お目にかかれて光栄です。",
    },
    "casual": {
        "en": "Hey {name}! What's up?",
        "ko": "안녕 {name}! 잘 지내?",
        "zh": "嗨 {name}！最近怎么样？",
        "ja": "やあ{name}！元気？",
    },
    "birthday": {
        "en": "Happy Birthday, {name}! Wishing you a wonderful year ahead!",
        "ko": "{name}님, 생일 축하합니다! 멋진 한 해 되세요!",
        "zh": "{name}，生日快乐！祝你新的一年精彩纷呈！",
        "ja": "{name}さん、お誕生日おめでとうございます！素晴らしい一年を！",
    },
    "newyear": {
        "en": "Happy New Year, {name}! May this year bring you joy and success!",
        "ko": "{name}님, 새해 복 많이 받으세요!",
        "zh": "{name}，新年快乐！万事如意！",
        "ja": "{name}さん、あけましておめでとうございます！今年もよろしくお願いします！",
    },
}


def validate_inputs(name: str, lang: str, scene: str) -> Optional[str]:
    """Validate inputs. Returns error message if invalid, None if OK."""
    if not name or not name.strip():
        return "Name must not be empty."
    if lang not in SUPPORTED_LANGS:
        return (
            f"Unsupported language '{lang}'. "
            f"Supported: {', '.join(SUPPORTED_LANGS)}"
        )
    if scene not in SUPPORTED_SCENES:
        return (
            f"Unsupported scene '{scene}'. "
            f"Supported: {', '.join(SUPPORTED_SCENES)}"
        )
    return None


def generate_greeting(name: str, lang: str, scene: str) -> str:
    """Generate greeting text. Assumes inputs are already validated."""
    template = GREETINGS[scene][lang]
    return template.format(name=name.strip())


def format_success(
    name: str, lang: str, scene: str, greeting: str, use_json: bool
) -> str:
    """Format a successful greeting output."""
    if use_json:
        payload = {
            "status": "success",
            "data": {
                "name": name.strip(),
                "lang": lang,
                "scene": scene,
                "greeting": greeting,
            },
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
    return greeting


def format_error(code: str, message: str, use_json: bool) -> str:
    """Format an error output."""
    if use_json:
        payload = {
            "status": "error",
            "error": {
                "code": code,
                "message": message,
            },
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
    return f"Error [{code}]: {message}"


def run(
    name: str,
    lang: str,
    scene: str,
    use_json: bool = False,
    out_stream=None,
    err_stream=None,
) -> int:
    """Run the greeter end-to-end.

    Returns exit code: 0 for success, 1 for validation error.
    Writes greeting to out_stream (default stdout) and errors to
    err_stream (default stderr).
    """
    out = out_stream if out_stream is not None else sys.stdout
    err = err_stream if err_stream is not None else sys.stderr

    error = validate_inputs(name, lang, scene)
    if error:
        output = format_error("INVALID_INPUT", error, use_json)
        err.write(output + "\n")
        return 1

    greeting = generate_greeting(name, lang, scene)
    output = format_success(name, lang, scene, greeting, use_json)
    out.write(output + "\n")
    return 0
