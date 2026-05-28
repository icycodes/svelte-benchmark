import json
import os
import shutil

PROJECT_DIR = "/home/user/sveltekit-i18n"


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_npx_available():
    assert shutil.which("npx") is not None, "npx binary not found in PATH."


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_package_json_exists():
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_path), f"package.json not found at {pkg_path}."


def test_package_json_has_sveltekit_and_node_adapter():
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    with open(pkg_path) as f:
        pkg = json.load(f)
    deps = {}
    for key in ("dependencies", "devDependencies"):
        if isinstance(pkg.get(key), dict):
            deps.update(pkg[key])
    assert "@sveltejs/kit" in deps, "@sveltejs/kit is not listed in package.json dependencies/devDependencies."
    assert "@sveltejs/adapter-node" in deps, "@sveltejs/adapter-node is not listed in package.json dependencies/devDependencies."
    assert "svelte" in deps, "svelte is not listed in package.json dependencies/devDependencies."


def test_svelte_config_uses_node_adapter():
    cfg_path = os.path.join(PROJECT_DIR, "svelte.config.js")
    assert os.path.isfile(cfg_path), f"svelte.config.js not found at {cfg_path}."
    with open(cfg_path) as f:
        content = f.read()
    assert "@sveltejs/adapter-node" in content, "svelte.config.js does not reference @sveltejs/adapter-node."


def test_app_html_exists():
    app_html = os.path.join(PROJECT_DIR, "src", "app.html")
    assert os.path.isfile(app_html), f"src/app.html not found at {app_html}."


def test_routes_dir_exists():
    routes_dir = os.path.join(PROJECT_DIR, "src", "routes")
    assert os.path.isdir(routes_dir), f"Routes directory not found at {routes_dir}."


def test_node_modules_installed():
    nm_dir = os.path.join(PROJECT_DIR, "node_modules")
    assert os.path.isdir(nm_dir), "node_modules directory is missing; dependencies are not installed."
    kit_dir = os.path.join(nm_dir, "@sveltejs", "kit")
    assert os.path.isdir(kit_dir), "@sveltejs/kit is not installed under node_modules."
    adapter_dir = os.path.join(nm_dir, "@sveltejs", "adapter-node")
    assert os.path.isdir(adapter_dir), "@sveltejs/adapter-node is not installed under node_modules."
