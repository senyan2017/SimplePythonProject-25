"""Tests for the Docker packaging.

Static checks on the Dockerfile always run and are fast. The live build/run
checks actually start a container and are therefore opt-in: set the environment
variable ``RUN_DOCKER_TESTS=1`` (and have docker installed) to enable them.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCKERFILE = ROOT / "Dockerfile"
IMAGE_TAG = "greeter-test:pytest"


def test_dockerfile_exists():
    assert DOCKERFILE.is_file()


def test_dockerfile_entrypoint_forwards_args():
    content = DOCKERFILE.read_text(encoding="utf-8")
    # The entry point must invoke main.py so that arguments appended to
    # ``docker run <image> ...`` are forwarded to the CLI.
    assert "ENTRYPOINT" in content
    assert "main.py" in content


def test_dockerfile_installs_requirements():
    content = DOCKERFILE.read_text(encoding="utf-8")
    assert "requirements.txt" in content


_docker_available = shutil.which("docker") is not None
_run_docker = _docker_available and os.environ.get("RUN_DOCKER_TESTS") == "1"
_DOCKER_REASON = (
    "container tests are opt-in: set RUN_DOCKER_TESTS=1 and install docker"
)


@pytest.fixture(scope="module")
def docker_image():
    build = subprocess.run(
        ["docker", "build", "-t", IMAGE_TAG, "."],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stderr
    yield IMAGE_TAG
    subprocess.run(
        ["docker", "rmi", "-f", IMAGE_TAG], capture_output=True, text=True
    )


@pytest.mark.skipif(not _run_docker, reason=_DOCKER_REASON)
def test_container_default_output(docker_image):
    res = subprocess.run(
        ["docker", "run", "--rm", docker_image],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert res.stdout.strip() == "Hello, World!"


@pytest.mark.skipif(not _run_docker, reason=_DOCKER_REASON)
def test_container_with_args(docker_image):
    res = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            docker_image,
            "--name",
            "Bob",
            "-l",
            "ko",
            "-s",
            "morning",
        ],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert res.stdout.strip() == "좋은 아침이에요, Bob!"


@pytest.mark.skipif(not _run_docker, reason=_DOCKER_REASON)
def test_container_env_var(docker_image):
    res = subprocess.run(
        ["docker", "run", "--rm", "-e", "GREETER_NAME=Eve", docker_image],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert res.stdout.strip() == "Hello, Eve!"


@pytest.mark.skipif(not _run_docker, reason=_DOCKER_REASON)
def test_container_invalid_input_exit_code(docker_image):
    res = subprocess.run(
        ["docker", "run", "--rm", docker_image, "--language", "xx"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 2
    assert "UNSUPPORTED_LANGUAGE" in res.stderr
