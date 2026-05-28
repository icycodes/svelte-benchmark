import os
import re
import socket
import subprocess

import pytest
import requests
from pochi_verifier import PochiVerifier
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/svelte-table-snippets"
PAGE_FILE = os.path.join(PROJECT_DIR, "src", "routes", "+page.svelte")
TABLE_FILE = os.path.join(PROJECT_DIR, "src", "lib", "Table.svelte")
BUILD_INDEX = os.path.join(PROJECT_DIR, "build", "index.js")
SVELTE_CONFIG_CANDIDATES = [
    os.path.join(PROJECT_DIR, "svelte.config.js"),
    os.path.join(PROJECT_DIR, "svelte.config.ts"),
    os.path.join(PROJECT_DIR, "svelte.config.mjs"),
]


# ----------------------------------------------------------------------------
# Source-level / build-output checks (run before starting the server)
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


def test_build_output_index_exists():
    # The agent is expected to have run `npm run build` so the start command
    # `npm run build && node build` will produce build/index.js. Even if the
    # start fixture rebuilds, we expect the artifact to be present.
    # Allow the start fixture to build it before this assertion runs by ordering
    # this test to depend on the server fixture (see below).
    pass


# ----------------------------------------------------------------------------
# Reusable Table component source checks
# ----------------------------------------------------------------------------


def test_table_component_file_exists():
    assert os.path.isfile(TABLE_FILE), (
        f"Reusable Table component not found at {TABLE_FILE}."
    )


def test_table_component_uses_props_rune():
    with open(TABLE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert "$props(" in content, (
        f"Table.svelte must declare props using the $props() rune; not found in {TABLE_FILE}."
    )


def test_table_component_renders_snippets():
    with open(TABLE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    render_count = len(re.findall(r"\{@render\b", content))
    assert render_count >= 2, (
        "Table.svelte must use {@render ...} at least twice (header + per-row); "
        f"found {render_count} occurrence(s)."
    )


def test_table_component_has_no_hardcoded_data():
    with open(TABLE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    forbidden = ["Apple", "Banana", "Cherry", "Date", "alice@example.com"]
    leaked = [t for t in forbidden if t in content]
    assert not leaked, (
        "Table.svelte must be generic and must not contain hard-coded dataset "
        f"values; found: {leaked}."
    )


# ----------------------------------------------------------------------------
# Page-level source checks (snippets + runes)
# ----------------------------------------------------------------------------


def test_page_uses_snippet_blocks():
    assert os.path.isfile(PAGE_FILE), f"Page file not found at {PAGE_FILE}."
    with open(PAGE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    header_snippets = len(re.findall(r"\{#snippet\s+header\s*\(", content))
    row_snippets = len(re.findall(r"\{#snippet\s+row\s*\(", content))
    assert header_snippets >= 2, (
        f"+page.svelte must define at least two {{#snippet header(...)}} blocks "
        f"(one per table); found {header_snippets}."
    )
    assert row_snippets >= 2, (
        f"+page.svelte must define at least two {{#snippet row(...)}} blocks "
        f"(one per table); found {row_snippets}."
    )


def test_page_uses_runes():
    with open(PAGE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert "$state(" in content, "+page.svelte must use the $state(...) rune."
    assert "$derived(" in content, "+page.svelte must use the $derived(...) rune."


def test_page_imports_table_component():
    with open(PAGE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    # Accept either an alias import from $lib or a relative import.
    pattern = re.compile(
        r"import\s+Table\s+from\s+['\"](\$lib(/[^'\"]*)?|(\.\.?/)+lib/Table\.svelte|(\.\.?/)+[^'\"]*Table\.svelte)['\"]"
    )
    assert pattern.search(content), (
        "+page.svelte must import the Table component from $lib or a relative path."
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
    # Build first so `node build` works.
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
        name = "svelte_table_app"
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
# HTTP / HTML checks
# ----------------------------------------------------------------------------


def test_root_returns_200(start_app):
    r = requests.get("http://localhost:3000/", timeout=15)
    assert r.status_code == 200, (
        f"GET / expected 200, got {r.status_code}. Body:\n{r.text[:500]}"
    )


def test_root_contains_two_tables(start_app):
    r = requests.get("http://localhost:3000/", timeout=15)
    table_open_count = len(re.findall(r"<table\b", r.text, flags=re.IGNORECASE))
    assert table_open_count >= 2, (
        f"Expected at least 2 <table> elements on /, found {table_open_count}."
    )


def test_root_contains_product_rows(start_app):
    r = requests.get("http://localhost:3000/", timeout=15)
    for needle in ("Apple", "Banana", "Cherry", "Date"):
        assert needle in r.text, (
            f"Expected product name {needle!r} to be rendered in the page."
        )


def test_root_contains_user_rows(start_app):
    r = requests.get("http://localhost:3000/", timeout=15)
    needles = [
        "Alice",
        "Bob",
        "Carol",
        "alice@example.com",
        "bob@example.com",
        "carol@example.com",
        "admin",
        "editor",
        "viewer",
    ]
    for needle in needles:
        assert needle in r.text, (
            f"Expected user-table value {needle!r} to be rendered in the page."
        )


def test_root_contains_computed_line_total(start_app):
    # Apple price 2.50 * qty 4 = 10.00 should appear as a line total in the row snippet.
    r = requests.get("http://localhost:3000/", timeout=15)
    assert "10.00" in r.text, (
        "Expected a computed line total (price * qty, e.g. 10.00) to be rendered "
        "by the products row snippet."
    )


def test_root_contains_inventory_total(start_app):
    # Total = 10.00 + 10.00 + 26.00 + 10.00 = 56.00
    r = requests.get("http://localhost:3000/", timeout=15)
    assert "$56.00" in r.text, (
        "Expected the inventory total '$56.00' to be visible on /."
    )


# ----------------------------------------------------------------------------
# Browser verification (interactive filter)
# ----------------------------------------------------------------------------


def test_filter_updates_table_and_total_in_browser(start_app):
    reason = (
        "The Products table on /, rendered by a generic Table component using "
        "Svelte 5 Snippets, must update live as the user types into a filter "
        "input. The inventory-total summary, computed with $derived, must also "
        "update accordingly."
    )
    truth = (
        "Navigate to http://localhost:3000/. Verify that the page shows two "
        "tables, that the Products table contains rows for 'Apple', 'Banana', "
        "'Cherry', and 'Date', and that the inventory-total element shows "
        "'$56.00'. Locate the product filter text input on the page and type "
        "'app' into it. After typing, verify that the Products table still "
        "shows 'Apple' but no longer shows 'Banana', 'Cherry', or 'Date', and "
        "that the inventory-total element now shows '$10.00'. Then clear the "
        "filter input; verify that all four products ('Apple', 'Banana', "
        "'Cherry', 'Date') are visible again and that the inventory-total "
        "element shows '$56.00' once more."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_filter_updates_table_and_total_in_browser",
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
