import os
import shutil
import json

PROJECT_DIR = "/home/user/tip-calculator"


def test_node_available():
    """Node.js must be installed so the SvelteKit dev server can run."""
    assert shutil.which("node") is not None, "Node.js binary not found in PATH."


def test_npm_available():
    """npm must be installed to manage SvelteKit dependencies."""
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_dir_exists():
    """The tip-calculator project directory must already exist."""
    assert os.path.isdir(PROJECT_DIR), (
        f"Project directory {PROJECT_DIR} does not exist."
    )


def test_package_json_exists():
    """The SvelteKit project must contain a package.json."""
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_path), (
        f"package.json not found at {pkg_path}."
    )


def test_package_json_uses_svelte_5():
    """The project should depend on Svelte 5."""
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    with open(pkg_path) as f:
        pkg = json.load(f)
    deps = {}
    deps.update(pkg.get("dependencies") or {})
    deps.update(pkg.get("devDependencies") or {})
    svelte_version = deps.get("svelte", "")
    assert svelte_version, "svelte is not listed as a dependency in package.json."
    # Accept "5.x", "^5.x.y", "~5.x.y", etc.
    assert "5" in svelte_version and "4." not in svelte_version, (
        f"Expected Svelte 5 in package.json, got svelte={svelte_version!r}."
    )


def test_node_modules_installed():
    """Dependencies must be installed already so the dev server can start."""
    nm = os.path.join(PROJECT_DIR, "node_modules")
    assert os.path.isdir(nm), (
        f"node_modules not found at {nm}; dependencies are not installed."
    )
    svelte_pkg = os.path.join(nm, "svelte", "package.json")
    assert os.path.isfile(svelte_pkg), (
        f"svelte package not installed under {nm}."
    )


def test_initial_root_page_uses_svelte4_patterns():
    """The starting +page.svelte must still use Svelte 4 idioms (pre-migration)."""
    page_path = os.path.join(PROJECT_DIR, "src", "routes", "+page.svelte")
    assert os.path.isfile(page_path), (
        f"Expected starter route at {page_path}."
    )
    with open(page_path) as f:
        content = f.read()
    # At least one Svelte 4 pattern should be present at the start.
    legacy_markers = ["export let", "on:click", "on:input", "$:"]
    assert any(marker in content for marker in legacy_markers), (
        f"Starter {page_path} does not appear to contain any Svelte 4 "
        f"patterns (export let / on:click / on:input / $:)."
    )


def test_initial_tip_button_component_uses_svelte4_patterns():
    """A reusable component should also start in Svelte 4 style."""
    comp_path = os.path.join(
        PROJECT_DIR, "src", "lib", "TipButton.svelte"
    )
    assert os.path.isfile(comp_path), (
        f"Expected reusable component at {comp_path}."
    )
    with open(comp_path) as f:
        content = f.read()
    legacy_markers = ["export let", "on:click", "createEventDispatcher"]
    assert any(marker in content for marker in legacy_markers), (
        f"Starter {comp_path} does not contain expected Svelte 4 patterns."
    )
