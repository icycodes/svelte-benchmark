import os
import re
import socket

import pytest
from pochi_verifier import PochiVerifier
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"
TABLE_COMPONENT = os.path.join(PROJECT_DIR, "src", "lib", "Table.svelte")
PAGE_COMPONENT = os.path.join(PROJECT_DIR, "src", "routes", "+page.svelte")
APP_PORT = 4173
APP_URL = f"http://localhost:{APP_PORT}"


# ---------------------------------------------------------------------------
# Static source-code checks
# ---------------------------------------------------------------------------


def test_table_component_exists():
    assert os.path.isfile(TABLE_COMPONENT), (
        f"Expected reusable table component at {TABLE_COMPONENT}, but it was not found."
    )


def test_page_component_exists():
    assert os.path.isfile(PAGE_COMPONENT), (
        f"Expected home page component at {PAGE_COMPONENT}, but it was not found."
    )


def test_table_uses_snippet_render_tag():
    with open(TABLE_COMPONENT, "r", encoding="utf-8") as f:
        content = f.read()
    assert "{@render" in content, (
        f"{TABLE_COMPONENT} must render snippets with the `{{@render ...}}` tag, "
        "but no `{@render` was found."
    )


def test_table_does_not_use_legacy_slot():
    with open(TABLE_COMPONENT, "r", encoding="utf-8") as f:
        content = f.read()
    # `<slot` would also match e.g. `<slot/>` or `<slot name="...">`.
    assert "<slot" not in content, (
        f"{TABLE_COMPONENT} must use Svelte 5 snippets, not the legacy `<slot>` element."
    )


def test_page_imports_table_component():
    with open(PAGE_COMPONENT, "r", encoding="utf-8") as f:
        content = f.read()
    # Allow either the `$lib` alias or a relative path that contains `Table.svelte`.
    import_pattern = re.compile(
        r"import\s+Table\s+from\s+['\"]([^'\"]*Table\.svelte)['\"]"
    )
    assert import_pattern.search(content), (
        f"{PAGE_COMPONENT} must import the `Table` component from a path that resolves "
        "to `src/lib/Table.svelte`."
    )


def test_page_uses_state_rune():
    with open(PAGE_COMPONENT, "r", encoding="utf-8") as f:
        content = f.read()
    assert "$state(" in content, (
        f"{PAGE_COMPONENT} must declare its product list with the `$state` rune."
    )


def test_page_uses_derived_rune():
    with open(PAGE_COMPONENT, "r", encoding="utf-8") as f:
        content = f.read()
    assert "$derived" in content, (
        f"{PAGE_COMPONENT} must compute the grand total with the `$derived` rune."
    )


def test_page_declares_snippets_for_table():
    with open(PAGE_COMPONENT, "r", encoding="utf-8") as f:
        content = f.read()
    assert "{#snippet" in content, (
        f"{PAGE_COMPONENT} must pass `header` and `row` snippets to the Table component "
        "using `{#snippet ...}` blocks."
    )


def test_no_legacy_slots_anywhere_in_src():
    src_dir = os.path.join(PROJECT_DIR, "src")
    assert os.path.isdir(src_dir), f"Expected source directory at {src_dir}."
    offenders: list[str] = []
    for root, _, files in os.walk(src_dir):
        for name in files:
            if not name.endswith(".svelte"):
                continue
            path = os.path.join(root, name)
            with open(path, "r", encoding="utf-8") as f:
                if "<slot" in f.read():
                    offenders.append(path)
    assert not offenders, (
        "Svelte 5 snippets must be used everywhere; the following files still use the "
        f"legacy `<slot>` element: {offenders}"
    )


# ---------------------------------------------------------------------------
# Run-time browser checks
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def start_app(xprocess):
    """Build and start the SvelteKit preview server on port 4173."""

    class Starter(ProcessStarter):
        name = "snippet_data_table_app"
        # Use a login shell so we can chain `npm run build && npm run preview ...`.
        args = [
            "bash",
            "-lc",
            f"npm run build && npm run preview -- --host 0.0.0.0 --port {APP_PORT}",
        ]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 600
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", APP_PORT)) == 0

    xprocess.ensure(Starter.name, Starter)

    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()


@pytest.fixture(scope="session")
def browser_verifier():
    return PochiVerifier()

def test_add_product_updates_table_and_total(start_app, browser_verifier):
    reason = (
        "Adding a new product through the form must append a new row to the table and "
        "update the grand total reactively, without a full page reload."
    )
    truth = (
        f"Navigate to {APP_URL}/. "
        "Read the current text of `[data-testid=\"grand-total\"]` and parse it as a "
        "number, call this value `total_before`. "
        "Count the number of `<tr>` rows inside the `<tbody>` of the page's `<table>` "
        "and call this value `rows_before`. "
        "Fill the form fields as follows: type `Date` into `[data-testid=\"product-name\"]`, "
        "type `2` into `[data-testid=\"product-qty\"]`, and type `5` into "
        "`[data-testid=\"product-price\"]`. Click `[data-testid=\"add-product\"]`. "
        "Wait up to 5 seconds for the DOM to update. Then verify ALL of the following: "
        "(a) the number of `<tr>` rows inside the `<table>`'s `<tbody>` is exactly "
        "`rows_before + 1`; "
        "(b) the newly added `<tr>` contains the visible text `Date`; "
        "(c) the text content of `[data-testid=\"grand-total\"]` parses as a number "
        "equal to `total_before + 10` (because 2 * 5 = 10); "
        f"(d) the current page URL is still `{APP_URL}/` and no full-page reload "
        "occurred between filling the form and observing the update."
    )

    result = browser_verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_add_product_updates_table_and_total",
    )
    assert result.status == "pass", (
        f"Browser verification of the add-product flow failed: {result.reason}"
    )


def test_initial_table_renders(start_app, browser_verifier):
    reason = (
        "The home page must render a real `<table>` produced by a reusable Table "
        "component using Svelte 5 snippets, with a `<thead>` of `<th>` cells and a "
        "`<tbody>` of at least one `<tr>`. It must also display a numeric grand total "
        "inside an element with `data-testid=\"grand-total\"`."
    )
    truth = (
        f"Navigate to {APP_URL}/. Verify that the page contains exactly one `<table>` "
        "element that has a `<thead>` with at least one `<th>` cell and a `<tbody>` "
        "with at least one `<tr>` row. Verify that an element matching the CSS selector "
        "`[data-testid=\"grand-total\"]` exists and that its text content is a number "
        "(parseable as a JavaScript `Number`, i.e. matches `^-?\\d+(\\.\\d+)?$` after "
        "trimming whitespace)."
    )

    result = browser_verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_initial_table_renders",
    )
    assert result.status == "pass", (
        f"Browser verification of the initial table render failed: {result.reason}"
    )

