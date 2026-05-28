import json
import os
import shutil

PROJECT_DIR = "/home/user/sveltekit-todos"


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Project directory {PROJECT_DIR} does not exist."
    )


def test_package_json_exists():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json), (
        f"package.json not found at {package_json}."
    )


def test_package_json_has_svelte_dependency():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    with open(package_json) as f:
        pkg = json.load(f)
    deps = {}
    deps.update(pkg.get("dependencies", {}) or {})
    deps.update(pkg.get("devDependencies", {}) or {})
    assert "svelte" in deps, (
        "svelte is not listed as a dependency in package.json. "
        "The initial SvelteKit project skeleton is missing."
    )
    assert "@sveltejs/kit" in deps, (
        "@sveltejs/kit is not listed as a dependency in package.json. "
        "The initial SvelteKit project skeleton is missing."
    )


def test_node_modules_installed():
    node_modules = os.path.join(PROJECT_DIR, "node_modules")
    assert os.path.isdir(node_modules), (
        f"node_modules directory not found at {node_modules}. "
        "Dependencies should be pre-installed."
    )


def test_svelte_config_exists():
    candidates = [
        os.path.join(PROJECT_DIR, "svelte.config.js"),
        os.path.join(PROJECT_DIR, "svelte.config.mjs"),
        os.path.join(PROJECT_DIR, "svelte.config.ts"),
    ]
    assert any(os.path.isfile(p) for p in candidates), (
        "Expected a svelte.config.{js,mjs,ts} in the project root."
    )


def test_routes_directory_exists():
    routes_dir = os.path.join(PROJECT_DIR, "src", "routes")
    assert os.path.isdir(routes_dir), (
        f"SvelteKit routes directory not found at {routes_dir}."
    )
