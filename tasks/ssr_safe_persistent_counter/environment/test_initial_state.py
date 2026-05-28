import os
import shutil
import subprocess


def test_home_user_directory_exists():
    assert os.path.isdir("/home/user"), "/home/user directory must exist before the task begins."


def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_npx_binary_available():
    assert shutil.which("npx") is not None, "npx binary not found in PATH."


def test_node_version_supports_sveltekit():
    result = subprocess.run(
        ["node", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"`node --version` failed: {result.stderr}"
    version = result.stdout.strip().lstrip("v")
    major = int(version.split(".")[0])
    assert major >= 18, (
        f"Node.js >= 18 is required for SvelteKit, but found v{version}."
    )


def test_curl_binary_available():
    assert shutil.which("curl") is not None, (
        "curl binary not found in PATH; the verifier uses curl to check SSR output."
    )


def test_project_directory_not_yet_created():
    project_dir = "/home/user/myproject"
    assert not os.path.exists(project_dir), (
        f"{project_dir} should not exist before the task begins; the executor must scaffold it."
    )
