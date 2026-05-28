import os
import shutil
import subprocess


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_npx_available():
    assert shutil.which("npx") is not None, "npx binary not found in PATH."


def test_node_version_supports_sveltekit():
    # SvelteKit requires Node.js 18+ (recommended 20+). Verify at least 18.
    result = subprocess.run(
        ["node", "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    version_string = result.stdout.strip().lstrip("v")
    major = int(version_string.split(".")[0])
    assert major >= 18, (
        f"Node.js major version {major} is too old; SvelteKit requires Node.js 18+."
    )


def test_home_user_directory_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."


def test_project_directory_not_yet_created():
    # The executor is expected to create the project. It must not already exist.
    project_dir = "/home/user/svelte-table-snippets"
    assert not os.path.exists(project_dir), (
        f"Project directory {project_dir} should not exist before the task begins."
    )
