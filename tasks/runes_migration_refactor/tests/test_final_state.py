import os
import re
import socket
import subprocess
import pytest
from xprocess import ProcessStarter
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/tip-calculator"
SRC_DIR = os.path.join(PROJECT_DIR, "src")
PORT = 3000

SVELTE_EXTS = (".svelte", ".svelte.js", ".svelte.ts")


def _iter_source_files():
    matched = []
    for root, _dirs, files in os.walk(SRC_DIR):
        for name in files:
            if name.endswith(SVELTE_EXTS):
                matched.append(os.path.join(root, name))
    return matched


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _strip_comments(text):
    """Remove block and line comments to reduce false positives when grepping."""
    # /* ... */ block comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    # // line comments
    text = re.sub(r"//[^\n]*", "", text)
    # <!-- HTML --> comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return text


def test_no_legacy_export_let():
    """`export let` must not appear in any source file."""
    offenders = []
    for path in _iter_source_files():
        content = _strip_comments(_read(path))
        if re.search(r"\bexport\s+let\b", content):
            offenders.append(path)
    assert not offenders, (
        f"Found legacy `export let` declarations in: {offenders}. "
        "Replace them with `let {{ ... }} = $props()`."
    )


def test_no_legacy_event_directives():
    """`on:click`, `on:input`, and `on:change` must not appear."""
    offenders = {}
    patterns = {
        "on:click": re.compile(r"\bon:click\b"),
        "on:input": re.compile(r"\bon:input\b"),
        "on:change": re.compile(r"\bon:change\b"),
    }
    for path in _iter_source_files():
        content = _strip_comments(_read(path))
        hits = [name for name, pat in patterns.items() if pat.search(content)]
        if hits:
            offenders[path] = hits
    assert not offenders, (
        f"Found legacy Svelte 4 event directives: {offenders}. "
        "Use the new attribute syntax (e.g. `onclick={...}`)."
    )


def test_no_create_event_dispatcher():
    """`createEventDispatcher` must not be used anywhere under src/."""
    offenders = []
    for path in _iter_source_files():
        content = _strip_comments(_read(path))
        if "createEventDispatcher" in content:
            offenders.append(path)
    assert not offenders, (
        f"`createEventDispatcher` must not appear in: {offenders}. "
        "Use callback props instead."
    )


def test_no_top_level_reactive_statements():
    """No top-level `$:` reactive statements inside <script> blocks."""
    script_block_re = re.compile(
        r"<script[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE
    )
    offenders = []
    for path in _iter_source_files():
        raw = _read(path)
        if path.endswith(".svelte"):
            blocks = script_block_re.findall(raw)
        else:
            blocks = [raw]
        for block in blocks:
            block_no_comments = _strip_comments(block)
            for line in block_no_comments.splitlines():
                stripped = line.lstrip()
                if stripped.startswith("$:"):
                    offenders.append(path)
                    break
    assert not offenders, (
        f"Found Svelte 4 `$:` reactive statements in: {offenders}. "
        "Use `$derived(...)` or `$effect(...)` instead."
    )


def test_runes_are_used():
    """Each of $props(, $state(, $derived( must appear at least once."""
    seen = set()
    for path in _iter_source_files():
        content = _strip_comments(_read(path))
        for rune in ("$props(", "$state(", "$derived("):
            if rune in content:
                seen.add(rune)
    missing = {"$props(", "$state(", "$derived("} - seen
    assert not missing, (
        f"Migrated code does not use the expected Svelte 5 runes: "
        f"missing {sorted(missing)}."
    )


@pytest.fixture(scope="session")
def start_app(xprocess):
    """Start the SvelteKit dev server in the background."""

    class Starter(ProcessStarter):
        name = "tip_calculator_dev"
        args = [
            "npm",
            "run",
            "dev",
            "--",
            "--host",
            "0.0.0.0",
            "--port",
            str(PORT),
        ]
        env = os.environ.copy()
        popen_kwargs = {"cwd": PROJECT_DIR, "text": True}
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", PORT)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()


@pytest.fixture(scope="session")
def browser_verifier():
    yield PochiVerifier()


def test_required_test_ids_present(start_app):
    """Sanity check the rendered HTML has the data-testid hooks the UI test
    will rely on, even before JS executes (SSR output)."""
    import urllib.request

    with urllib.request.urlopen(f"http://localhost:{PORT}/") as resp:
        html = resp.read().decode("utf-8", errors="replace")

    required_testids = [
        'data-testid="bill-input"',
        'data-testid="people-input"',
        'data-testid="tip-amount"',
        'data-testid="total-amount"',
        'data-testid="per-person"',
        'data-testid="tip-5"',
        'data-testid="tip-10"',
        'data-testid="tip-15"',
    ]
    missing = [tid for tid in required_testids if tid not in html]
    assert not missing, (
        f"Server-rendered HTML is missing required test IDs: {missing}. "
        f"First 500 chars of response: {html[:500]!r}"
    )


def test_tip_calculator_reactivity(start_app, browser_verifier):
    reason = (
        "After migrating the Svelte 4 components to Svelte 5 runes, the "
        "Tip Calculator UI must remain fully reactive: changing the bill, "
        "the number of people, or the selected tip percentage must update "
        "the tip amount, total amount, and per-person amount on screen "
        "without a full page reload."
    )
    truth = (
        "Navigate to http://localhost:3000/. "
        "Locate the input with data-testid='bill-input' and replace its "
        "value with 100. Locate the input with data-testid='people-input' "
        "and replace its value with 2. Click the button with "
        "data-testid='tip-10'. Verify that the element with "
        "data-testid='tip-amount' shows '10.00', the element with "
        "data-testid='total-amount' shows '110.00', and the element with "
        "data-testid='per-person' shows '55.00'. Verify that the button "
        "with data-testid='tip-10' has the CSS class 'selected' while the "
        "buttons with data-testid='tip-5' and data-testid='tip-15' do not "
        "have the 'selected' class. "
        "Now click the button with data-testid='tip-15'. Verify that "
        "data-testid='tip-amount' shows '15.00', data-testid='total-amount' "
        "shows '115.00', and data-testid='per-person' shows '57.50'. Verify "
        "that only the button with data-testid='tip-15' has the CSS class "
        "'selected'. "
        "Finally, change data-testid='bill-input' to 200 and "
        "data-testid='people-input' to 4. Verify that data-testid='tip-amount' "
        "shows '30.00', data-testid='total-amount' shows '230.00', and "
        "data-testid='per-person' shows '57.50'."
    )
    result = browser_verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_tip_calculator_reactivity",
    )
    assert result.status == "pass", (
        f"Browser verification failed: {result.reason}"
    )
