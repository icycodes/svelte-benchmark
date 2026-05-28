import os
import re
import socket
import subprocess

import pytest
import requests
from xprocess import ProcessStarter
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/myproject"
PORT = 5173
BASE_URL = f"http://localhost:{PORT}"


@pytest.fixture(scope="session")
def start_app(xprocess):
    """Start the SvelteKit dev server in the background and wait until port 5173 is open."""

    class Starter(ProcessStarter):
        name = "ssr_safe_persistent_counter_app"
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
        env["BROWSER"] = "none"
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 300
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                return s.connect_ex(("127.0.0.1", PORT)) == 0

    xprocess.ensure(Starter.name, Starter)

    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()


def _fetch_index_html():
    response = requests.get(BASE_URL + "/", timeout=30)
    return response


def test_ssr_returns_200(start_app):
    response = _fetch_index_html()
    assert response.status_code == 200, (
        f"GET / returned status {response.status_code}; expected 200. Body: {response.text[:500]}"
    )


def test_ssr_html_contains_heading(start_app):
    html = _fetch_index_html().text
    assert "Persistent Counter" in html, (
        "Server-rendered HTML must contain the heading text 'Persistent Counter'."
    )


def test_ssr_html_initial_count_is_zero(start_app):
    html = _fetch_index_html().text
    # Look for an element with data-testid="count" whose text is 0.
    pattern = re.compile(
        r"data-testid\s*=\s*[\"']count[\"'][^>]*>\s*0\s*<",
        re.IGNORECASE | re.DOTALL,
    )
    assert pattern.search(html), (
        "Server-rendered HTML must contain an element with data-testid=\"count\" "
        "whose text content is '0'."
    )


def test_ssr_html_hydration_status_is_loading(start_app):
    html = _fetch_index_html().text
    pattern = re.compile(
        r"data-testid\s*=\s*[\"']hydration-status[\"'][^>]*>\s*([A-Za-z]+)\s*<",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(html)
    assert match, (
        "Server-rendered HTML must contain an element with data-testid=\"hydration-status\"."
    )
    text = match.group(1).strip().lower()
    assert text == "loading", (
        f"Server-rendered hydration-status text must be 'loading' (case-insensitive); got '{text}'."
    )


def test_ssr_does_not_leak_window_errors(start_app):
    """A naive `localStorage.getItem(...)` outside `$effect` would crash SSR; ensure no error
    page or 5xx is served."""
    response = _fetch_index_html()
    assert response.status_code == 200, (
        f"Expected 200 from SSR, got {response.status_code}. "
        "This usually means client-only globals (window/localStorage) were touched outside $effect."
    )
    lowered = response.text.lower()
    forbidden_markers = [
        "internal error",
        "referenceerror: window is not defined",
        "referenceerror: localstorage is not defined",
        "referenceerror: document is not defined",
    ]
    for marker in forbidden_markers:
        assert marker not in lowered, (
            f"Server-rendered HTML must not contain the error marker '{marker}'. "
            "Move browser-only access inside a $effect."
        )


def test_browser_initial_hydration_and_counter(start_app):
    reason = (
        "The home page must render a Persistent Counter heading, an initial count of 0, "
        "and a hydration-status element that switches from 'loading' (SSR) to 'ready' "
        "after Svelte hydration."
    )
    truth = (
        f"Navigate to {BASE_URL}/. "
        "Verify the page contains an <h1> with the text 'Persistent Counter'. "
        "Verify the element with attribute data-testid=\"count\" shows the text '0'. "
        "Wait up to 5 seconds for hydration, then verify the element with attribute "
        "data-testid=\"hydration-status\" shows the text 'ready' (case-insensitive)."
    )
    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_initial_hydration_and_counter",
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"


def test_browser_increment_and_persistence(start_app):
    reason = (
        "Clicking the increment button must increase the displayed counter, "
        "the value must be saved to localStorage under the key persistent_counter_value, "
        "and the value must survive a full page reload."
    )
    truth = (
        f"Navigate to {BASE_URL}/. "
        "Before clicking anything, run the following JavaScript in the page context to "
        "clear any previous state: localStorage.removeItem('persistent_counter_value'); "
        "location.reload();. "
        "After the page reloads, wait for hydration (the element with "
        "data-testid=\"hydration-status\" should show 'ready'). "
        "Then click the button with attribute data-testid=\"increment\" exactly three times. "
        "Verify that the element with data-testid=\"count\" now shows the text '3'. "
        "Run this JavaScript in the page context: "
        "JSON.parse(localStorage.getItem('persistent_counter_value')). "
        "Verify the returned value equals the number 3. "
        "Then reload the page. After the page is fully loaded and hydrated, verify that "
        "the element with data-testid=\"count\" again shows '3'."
    )
    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_increment_and_persistence",
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"


def test_browser_reset_clears_counter(start_app):
    reason = (
        "Clicking the reset button must set the counter back to 0 and also update "
        "the value stored under persistent_counter_value in localStorage to 0."
    )
    truth = (
        f"Navigate to {BASE_URL}/. "
        "Run this JavaScript in the page context to seed a non-zero value: "
        "localStorage.setItem('persistent_counter_value', JSON.stringify(7)); location.reload();. "
        "After the page reloads and hydrates (data-testid=\"hydration-status\" shows 'ready'), "
        "verify that the element with data-testid=\"count\" shows '7'. "
        "Then click the button with data-testid=\"reset\" once. "
        "Verify that the element with data-testid=\"count\" now shows '0'. "
        "Run: JSON.parse(localStorage.getItem('persistent_counter_value')). "
        "Verify the returned value equals the number 0."
    )
    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_reset_clears_counter",
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"


def test_package_json_uses_svelte_5(start_app):
    """Sanity check that the project actually uses Svelte 5 runes (per the task's hint)."""
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_path), f"package.json must exist at {pkg_path}."
    with open(pkg_path) as f:
        content = f.read()
    # Look for a svelte dependency that is at least version 5.x.
    match = re.search(r'"svelte"\s*:\s*"([^"]+)"', content)
    assert match, "package.json must declare a 'svelte' dependency."
    version_spec = match.group(1)
    # Extract the first digit group from the spec (handles ^5, ~5.0, 5.0.0, etc.).
    digit_match = re.search(r"(\d+)", version_spec)
    assert digit_match, f"Could not parse svelte version from spec '{version_spec}'."
    major = int(digit_match.group(1))
    assert major >= 5, (
        f"The project must use Svelte 5 (which provides the runes API). Found svelte@{version_spec}."
    )
