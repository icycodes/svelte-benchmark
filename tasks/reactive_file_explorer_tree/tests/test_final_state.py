import os
import re
import socket
import subprocess

import pytest
import requests
from pochi_verifier import PochiVerifier
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/svelte-file-explorer"
PAGE_FILE = os.path.join(PROJECT_DIR, "src", "routes", "+page.svelte")
TREE_NODE_FILE = os.path.join(PROJECT_DIR, "src", "lib", "TreeNode.svelte")
BUILD_INDEX = os.path.join(PROJECT_DIR, "build", "index.js")
SVELTE_CONFIG_CANDIDATES = [
    os.path.join(PROJECT_DIR, "svelte.config.js"),
    os.path.join(PROJECT_DIR, "svelte.config.ts"),
    os.path.join(PROJECT_DIR, "svelte.config.mjs"),
]


# ----------------------------------------------------------------------------
# Source-level / project structure checks
# ----------------------------------------------------------------------------


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Expected project directory {PROJECT_DIR} to exist."
    )


def test_package_json_exists():
    pkg = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg), f"package.json not found at {pkg}."


def test_svelte_config_uses_adapter_node():
    found = [p for p in SVELTE_CONFIG_CANDIDATES if os.path.isfile(p)]
    assert found, (
        f"No svelte.config.{{js,ts,mjs}} found in {PROJECT_DIR}; expected one of "
        f"{SVELTE_CONFIG_CANDIDATES}."
    )
    config_text = ""
    for p in found:
        with open(p, "r", encoding="utf-8") as f:
            config_text += f.read() + "\n"
    assert "@sveltejs/adapter-node" in config_text, (
        "svelte.config must import '@sveltejs/adapter-node' to use the Node adapter."
    )


# ----------------------------------------------------------------------------
# Recursive component source checks
# ----------------------------------------------------------------------------


def test_tree_node_component_exists():
    assert os.path.isfile(TREE_NODE_FILE), (
        f"Recursive TreeNode component not found at {TREE_NODE_FILE}."
    )


def test_tree_node_uses_props_rune():
    with open(TREE_NODE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert "$props(" in content, (
        f"TreeNode.svelte must declare props using $props(); not found in {TREE_NODE_FILE}."
    )


def test_tree_node_is_recursive():
    with open(TREE_NODE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    # The component must reference itself by name to recurse.
    assert re.search(r"<\s*TreeNode\b", content), (
        "TreeNode.svelte must reference itself (e.g. <TreeNode ... />) inside its "
        "template to recurse on child folders."
    )


def test_page_file_exists():
    assert os.path.isfile(PAGE_FILE), f"Page file not found at {PAGE_FILE}."


def test_runes_used_in_page_or_component():
    combined = ""
    for path in (PAGE_FILE, TREE_NODE_FILE):
        with open(path, "r", encoding="utf-8") as f:
            combined += f.read() + "\n"
    assert "$state(" in combined, (
        "Expected at least one $state(...) usage in +page.svelte or TreeNode.svelte."
    )
    assert ("$derived(" in combined) or ("$derived.by(" in combined), (
        "Expected at least one $derived(...) (or $derived.by(...)) usage in "
        "+page.svelte or TreeNode.svelte."
    )


# ----------------------------------------------------------------------------
# Runtime / server fixture
# ----------------------------------------------------------------------------


def _port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        return s.connect_ex((host, port)) == 0


@pytest.fixture(scope="session")
def start_app(xprocess):
    # Build the project so `node build` works.
    build = subprocess.run(
        ["npm", "run", "build"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, (
        f"npm run build failed.\nstdout:\n{build.stdout}\nstderr:\n{build.stderr}"
    )
    assert os.path.isfile(BUILD_INDEX), (
        f"Expected build artifact {BUILD_INDEX} to exist after `npm run build`."
    )

    class Starter(ProcessStarter):
        name = "svelte_file_explorer_app"
        args = ["node", "build"]
        env = {**os.environ, "PORT": "3000", "HOST": "0.0.0.0"}
        popen_kwargs = {"cwd": PROJECT_DIR, "text": True}
        timeout = 120
        terminate_on_interrupt = True

        def startup_check(self):
            return _port_open("localhost", 3000)

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()


# ----------------------------------------------------------------------------
# HTTP / SSR HTML checks (initial collapsed state)
# ----------------------------------------------------------------------------


def test_root_returns_200(start_app):
    r = requests.get("http://localhost:3000/", timeout=15)
    assert r.status_code == 200, (
        f"GET / expected 200, got {r.status_code}. Body:\n{r.text[:500]}"
    )


def test_initial_status_bar_zero_counts(start_app):
    r = requests.get("http://localhost:3000/", timeout=15)
    # Open-folder count element with text 0
    open_count_match = re.search(
        r'data-testid=["\']open-folder-count["\'][^>]*>\s*0\s*<',
        r.text,
    )
    assert open_count_match, (
        "Expected an element with data-testid='open-folder-count' and text "
        "content '0' in the initial server-rendered page."
    )
    visible_count_match = re.search(
        r'data-testid=["\']visible-file-count["\'][^>]*>\s*0\s*<',
        r.text,
    )
    assert visible_count_match, (
        "Expected an element with data-testid='visible-file-count' and text "
        "content '0' in the initial server-rendered page."
    )


def test_initial_root_folder_rendered_collapsed(start_app):
    r = requests.get("http://localhost:3000/", timeout=15)
    # A folder row for "root" should be present, with data-open=false and ▶ glyph.
    folder_pattern = re.compile(
        r'<[^>]*data-testid=["\']folder["\'][^>]*data-folder-name=["\']root["\'][^>]*>',
        re.IGNORECASE,
    )
    matches = folder_pattern.findall(r.text)
    assert matches, (
        "Expected a folder row with data-testid='folder' and "
        "data-folder-name='root' on the initial page."
    )
    # Ensure data-open='false' appears in at least one root-folder element.
    root_open_false = re.search(
        r'data-testid=["\']folder["\'][^>]*data-folder-name=["\']root["\'][^>]*data-open=["\']false["\']|'
        r'data-testid=["\']folder["\'][^>]*data-open=["\']false["\'][^>]*data-folder-name=["\']root["\']|'
        r'data-folder-name=["\']root["\'][^>]*data-testid=["\']folder["\'][^>]*data-open=["\']false["\']|'
        r'data-folder-name=["\']root["\'][^>]*data-open=["\']false["\'][^>]*data-testid=["\']folder["\']|'
        r'data-open=["\']false["\'][^>]*data-testid=["\']folder["\'][^>]*data-folder-name=["\']root["\']|'
        r'data-open=["\']false["\'][^>]*data-folder-name=["\']root["\'][^>]*data-testid=["\']folder["\']',
        r.text,
    )
    assert root_open_false, (
        "Expected the root folder to be rendered with data-open='false' on the "
        "initial (collapsed) page."
    )


def test_initial_no_file_rows_rendered(start_app):
    r = requests.get("http://localhost:3000/", timeout=15)
    # No <... data-testid="file" ...> should be present because root is collapsed.
    file_matches = re.findall(r'data-testid=["\']file["\']', r.text)
    assert not file_matches, (
        "Expected no elements with data-testid='file' on the initial page "
        f"(root is collapsed), found {len(file_matches)}."
    )


# ----------------------------------------------------------------------------
# Browser verification (interactive toggling, multi-step)
# ----------------------------------------------------------------------------


def test_recursive_toggle_and_live_counts_in_browser(start_app):
    reason = (
        "The file-explorer page at / must render a recursive folder/file tree "
        "driven by Svelte 5 runes. Toggling a folder must independently expand "
        "or collapse only that folder's subtree, and the always-visible status "
        "bar must reactively show the number of currently open folders and the "
        "number of currently visible files (i.e. files whose entire parent "
        "chain is open)."
    )
    truth = (
        "Navigate to http://localhost:3000/. "
        "Step 1 (initial collapsed state): Verify that the element with "
        "attribute data-testid='open-folder-count' has the text '0', that the "
        "element with attribute data-testid='visible-file-count' has the text "
        "'0', that exactly one folder row is visible with "
        "data-folder-name='root' showing the closed indicator '▶', and that "
        "no element with data-testid='file' is present in the DOM. "
        "Step 2 (expand root): Click the folder row whose "
        "data-folder-name='root'. After the click, verify the root folder row "
        "now shows the open indicator '▼' and has data-open='true'; that "
        "folder rows with data-folder-name='src' and data-folder-name='docs' "
        "are now present in the DOM both showing '▶' and data-open='false'; "
        "that a file row with data-file-name='package.json' is present; that "
        "no file rows with data-file-name equal to 'app.js', 'math.js', "
        "'str.js', 'index.css', or 'readme.md' are present; that the "
        "open-folder-count text is '1'; and that the visible-file-count text "
        "is '1'. "
        "Step 3 (expand src): Click the folder row with data-folder-name='src'. "
        "After the click, verify the src folder row shows '▼' and has "
        "data-open='true'; that the root folder row still has data-open='true' "
        "(toggling src must not collapse root); that a folder row with "
        "data-folder-name='utils' is now present with data-open='false' and "
        "the '▶' indicator; that file rows with data-file-name='app.js' and "
        "data-file-name='index.css' are present; that file rows with "
        "data-file-name='math.js' and data-file-name='str.js' are NOT present "
        "(utils is still closed); that open-folder-count is '2'; and that "
        "visible-file-count is '3'. "
        "Step 4 (expand utils, deep nesting): Click the folder row with "
        "data-folder-name='utils'. After the click, verify that utils has "
        "data-open='true' and shows '▼'; that root and src still have "
        "data-open='true'; that file rows with data-file-name='math.js' and "
        "data-file-name='str.js' are now present; that open-folder-count is "
        "'3'; and that visible-file-count is '5'. "
        "Step 5 (collapse src independently): Click the folder row with "
        "data-folder-name='src' again. After the click, verify that src has "
        "data-open='false' and shows '▶'; that root still has data-open='true'; "
        "that file rows with data-file-name equal to 'app.js', 'index.css', "
        "'math.js', or 'str.js' are NOT present in the DOM; that no folder "
        "row with data-folder-name='utils' is present (it lives under the "
        "collapsed src); that the folder row with data-folder-name='docs' is "
        "still present (sibling of src is not affected); that open-folder-count "
        "is '1'; and that visible-file-count is '1'."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_recursive_toggle_and_live_counts_in_browser",
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
