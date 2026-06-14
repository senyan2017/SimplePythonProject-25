"""Tests for Dockerfile validity and container behavior."""

import os
import subprocess

import pytest

DOCKERFILE = os.path.join(os.path.dirname(__file__), "..", "Dockerfile")


class TestDockerfileStructure:
    """Static analysis of the Dockerfile (no Docker daemon required)."""

    def test_dockerfile_exists(self):
        assert os.path.isfile(DOCKERFILE)

    def test_has_entrypoint(self):
        content = open(DOCKERFILE).read()
        assert "ENTRYPOINT" in content

    def test_entrypoint_runs_main(self):
        content = open(DOCKERFILE).read()
        assert "main.py" in content

    def test_has_cmd_for_arg_override(self):
        """CMD should be present so users can pass args at docker run time."""
        content = open(DOCKERFILE).read()
        assert "CMD" in content

    def test_uses_workdir(self):
        content = open(DOCKERFILE).read()
        assert "WORKDIR" in content

    def test_copies_requirements_first(self):
        """requirements.txt should be copied before app code for layer caching."""
        content = open(DOCKERFILE).read()
        req_pos = content.find("COPY requirements.txt")
        app_pos = content.find("COPY greeter/")
        assert req_pos != -1, "requirements.txt should be COPYed explicitly"
        assert app_pos != -1, "greeter/ should be COPYed explicitly"
        assert req_pos < app_pos, "requirements.txt should be copied before app code"


class TestDockerBuild:
    """Build and run the Docker image (requires Docker daemon)."""

    IMAGE_NAME = "greeter-test"

    @pytest.fixture(autouse=True)
    def _check_docker(self):
        """Skip all tests in this class if Docker is unavailable."""
        try:
            subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pytest.skip("Docker daemon not available")

    def test_build_succeeds(self):
        result = subprocess.run(
            ["docker", "build", "-t", self.IMAGE_NAME, "."],
            capture_output=True,
            timeout=120,
        )
        assert result.returncode == 0, result.stderr.decode()

    def test_run_default(self):
        result = subprocess.run(
            ["docker", "run", "--rm", self.IMAGE_NAME],
            capture_output=True,
            timeout=30,
        )
        assert result.returncode == 0
        assert b"World" in result.stdout or b"world" in result.stdout.lower()

    def test_run_with_args(self):
        result = subprocess.run(
            [
                "docker", "run", "--rm", self.IMAGE_NAME,
                "--name", "Docker",
                "--lang", "ko",
                "--scene", "formal",
            ],
            capture_output=True,
            timeout=30,
        )
        assert result.returncode == 0
        assert "Docker" in result.stdout.decode()

    def test_run_with_env(self):
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-e", "GREETER_NAME=EnvTest",
                "-e", "GREETER_LANG=zh",
                self.IMAGE_NAME,
            ],
            capture_output=True,
            timeout=30,
        )
        assert result.returncode == 0
        assert "EnvTest" in result.stdout.decode()

    def test_run_json_output(self):
        result = subprocess.run(
            [
                "docker", "run", "--rm", self.IMAGE_NAME,
                "--name", "JSON",
                "--json",
            ],
            capture_output=True,
            timeout=30,
        )
        assert result.returncode == 0
        import json
        data = json.loads(result.stdout.decode())
        assert data["status"] == "success"

    def test_run_invalid_input_fails(self):
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-e", "GREETER_NAME=",
                self.IMAGE_NAME,
            ],
            capture_output=True,
            timeout=30,
        )
        assert result.returncode != 0
