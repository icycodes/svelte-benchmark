import os
import re
import socket
import subprocess
import time

import pytest
import requests
from xprocess import ProcessStarter

from pochi_verifier import PochiVerifier


PROJECT_DIR = "/home/user/myproject"
BASE_URL = "http://localhost:3000"


def _port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0


@pytest.fixture(scope="session")
def start_app(xprocess):
    # Ensure the project is built before starting (idempotent: skip if already built).
    build_dir = os.path.join(PROJECT_DIR, "build")
    if not os.path.isdir(build_dir):
        install = subprocess.run(
            ["npm", "install", "--no-audit", "--no-fund"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
        )
        assert install.returncode == 0, (
            f"`npm install` failed before running tests:\nstdout:\n{install.stdout}\nstderr:\n{install.stderr}"
        )
        build = subprocess.run(
            ["npm", "run", "build"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
        )
        assert build.returncode == 0, (
            f"`npm run build` failed before running tests:\nstdout:\n{build.stdout}\nstderr:\n{build.stderr}"
        )

    class Starter(ProcessStarter):
        name = "sveltekit_app"
        args = ["node", "build"]
        env = {**os.environ, "PORT": "3000", "HOST": "0.0.0.0", "NODE_ENV": "production"}
        popen_kwargs = {"cwd": PROJECT_DIR, "text": True}
        timeout = 60
        terminate_on_interrupt = True

        def startup_check(self):
            try:
                r = requests.get(BASE_URL + "/", timeout=2)
                return r.status_code == 200
            except Exception:
                return False

    xprocess.ensure(Starter.name, Starter)

    # Extra safety: wait for port to be open before yielding.
    deadline = time.time() + 30
    while time.time() < deadline and not _port_open("localhost", 3000):
        time.sleep(0.5)
    assert _port_open("localhost", 3000), "SvelteKit server did not start on port 3000."

    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()


@pytest.fixture(scope="session")
def browser_verifier():
    yield PochiVerifier()


# -----------------------------------------------------------------------------
# Order is important here: the initial render test must run BEFORE any test
# that mutates the in-memory like counts on the server.
# -----------------------------------------------------------------------------


def test_01_initial_render(start_app):
    """The home page must render every post with its initial like count and a Like button."""
    response = requests.get(BASE_URL + "/", timeout=10)
    assert response.status_code == 200, (
        f"GET / expected 200, got {response.status_code}; body: {response.text[:500]}"
    )
    html = response.text

    expected_posts = [
        ("1", "First Post", "0"),
        ("2", "Second Post", "5"),
        ("3", "Third Post", "10"),
        ("broken", "Broken Post", "0"),
    ]

    for post_id, title, likes in expected_posts:
        # Container element
        container_re = re.compile(
            rf'data-testid=["\']post-{re.escape(post_id)}["\']'
        )
        assert container_re.search(html), (
            f'Expected container with data-testid="post-{post_id}" in /. '
            f"Page snippet: {html[:500]}"
        )

        # Title element with exact title text content
        title_re = re.compile(
            rf'data-testid=["\']title-{re.escape(post_id)}["\'][^>]*>\s*'
            rf"{re.escape(title)}\s*<",
        )
        assert title_re.search(html), (
            f'Expected element with data-testid="title-{post_id}" and text '
            f'"{title}" in /. Page snippet: {html[:500]}'
        )

        # Likes element whose visible text is the integer (no extra non-digit chars surrounding the number)
        likes_re = re.compile(
            rf'data-testid=["\']likes-{re.escape(post_id)}["\'][^>]*>\s*'
            rf"{re.escape(likes)}\s*<",
        )
        assert likes_re.search(html), (
            f'Expected element with data-testid="likes-{post_id}" and exact '
            f'text "{likes}" in /. Page snippet: {html[:500]}'
        )

        # Like button
        button_re = re.compile(
            rf'<button[^>]*data-testid=["\']like-{re.escape(post_id)}["\'][^>]*>'
            rf"[^<]*like[^<]*</button>",
            re.IGNORECASE,
        )
        assert button_re.search(html), (
            f'Expected <button data-testid="like-{post_id}"> containing text '
            f'"Like" in /. Page snippet: {html[:500]}'
        )


def test_02_like_post_1_increments_twice(start_app):
    """POST /api/posts/1/like must return JSON {id, likes} and increment the count."""
    r1 = requests.post(
        BASE_URL + "/api/posts/1/like",
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    assert r1.status_code == 200, (
        f"First POST /api/posts/1/like expected 200, got {r1.status_code}; body: {r1.text}"
    )
    body1 = r1.json()
    assert body1.get("id") == "1", f"Expected id '1' in response, got {body1}"
    assert body1.get("likes") == 1, (
        f"Expected likes==1 after first like of post 1, got {body1}"
    )

    r2 = requests.post(
        BASE_URL + "/api/posts/1/like",
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    assert r2.status_code == 200, (
        f"Second POST /api/posts/1/like expected 200, got {r2.status_code}; body: {r2.text}"
    )
    body2 = r2.json()
    assert body2.get("id") == "1", f"Expected id '1' in response, got {body2}"
    assert body2.get("likes") == 2, (
        f"Expected likes==2 after second like of post 1, got {body2}"
    )


def test_03_like_post_2(start_app):
    """POST /api/posts/2/like must increment from 5 to 6."""
    r = requests.post(
        BASE_URL + "/api/posts/2/like",
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    assert r.status_code == 200, (
        f"POST /api/posts/2/like expected 200, got {r.status_code}; body: {r.text}"
    )
    body = r.json()
    assert body.get("id") == "2", f"Expected id '2' in response, got {body}"
    assert body.get("likes") == 6, (
        f"Expected likes==6 after first like of post 2 (initial 5), got {body}"
    )


def test_04_like_unknown_post_returns_404(start_app):
    """An unknown post id must respond with HTTP 404."""
    r = requests.post(
        BASE_URL + "/api/posts/does-not-exist/like",
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    assert r.status_code == 404, (
        f"POST /api/posts/does-not-exist/like expected 404, got {r.status_code}; body: {r.text}"
    )


def test_05_like_broken_returns_500_and_does_not_mutate(start_app):
    """The 'broken' id always returns 500 and never mutates server state."""
    r1 = requests.post(
        BASE_URL + "/api/posts/broken/like",
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    assert r1.status_code == 500, (
        f"First POST /api/posts/broken/like expected 500, got {r1.status_code}; body: {r1.text}"
    )
    r2 = requests.post(
        BASE_URL + "/api/posts/broken/like",
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    assert r2.status_code == 500, (
        f"Second POST /api/posts/broken/like expected 500, got {r2.status_code}; body: {r2.text}"
    )

    # The server-side like count for 'broken' must still be 0.
    page = requests.get(BASE_URL + "/", timeout=10)
    assert page.status_code == 200, (
        f"GET / expected 200, got {page.status_code}"
    )
    likes_re = re.compile(
        r'data-testid=["\']likes-broken["\'][^>]*>\s*0\s*<'
    )
    assert likes_re.search(page.text), (
        "Expected data-testid=\"likes-broken\" to still show 0 after two failing likes. "
        f"Page snippet: {page.text[:500]}"
    )


def test_06_endpoint_has_artificial_delay(start_app):
    """A successful POST must take at least 250 ms due to the artificial server delay."""
    start = time.perf_counter()
    r = requests.post(
        BASE_URL + "/api/posts/3/like",
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    elapsed = time.perf_counter() - start
    assert r.status_code == 200, (
        f"POST /api/posts/3/like expected 200, got {r.status_code}; body: {r.text}"
    )
    body = r.json()
    assert body.get("id") == "3", f"Expected id '3' in response, got {body}"
    assert body.get("likes") == 11, (
        f"Expected likes==11 after first like of post 3 (initial 10), got {body}"
    )
    assert elapsed >= 0.25, (
        f"Expected at least 250 ms of artificial server delay on /api/posts/3/like, "
        f"but the response took only {elapsed*1000:.0f} ms."
    )


def test_07_browser_optimistic_update(start_app, browser_verifier):
    reason = (
        "The Like button on the SvelteKit page must use an optimistic UI pattern: "
        "clicking it has to update the displayed like count immediately, before the "
        "server response arrives."
    )
    truth = (
        "Open http://localhost:3000/ in the browser and wait until the page is "
        "fully loaded and hydrated (the element with data-testid='like-1' must be "
        "present and clickable). "
        "Read the current text content of the element with data-testid='likes-1' "
        "and remember it as `before` (it is a non-negative integer). "
        "Click the button with data-testid='like-1' exactly once. "
        "Within 150 ms of the click, while the server endpoint is still sleeping "
        "for its artificial ~300 ms delay, check the text content of the element "
        "with data-testid='likes-1'. It MUST equal String(Number(before) + 1). If "
        "it has not changed yet, the optimistic update is missing and the test fails. "
        "Then wait ~800 ms so the server response settles, and check again that the "
        "text content of data-testid='likes-1' is still String(Number(before) + 1) "
        "(i.e. the optimistic value was kept, not reverted). "
        "Pass only if both checks succeed."
    )
    result = browser_verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_07_browser_optimistic_update",
    )
    assert result.status == "pass", (
        f"Browser optimistic-update verification failed: {result.reason}"
    )


def test_08_browser_optimistic_rollback(start_app, browser_verifier):
    reason = (
        "When the Like button is clicked for a post whose server endpoint fails, the "
        "optimistic UI update must be rolled back so the displayed like count "
        "matches the previous value again."
    )
    truth = (
        "Open http://localhost:3000/ in the browser and wait until the page is "
        "fully loaded and hydrated (the element with data-testid='like-broken' "
        "must be present and clickable). "
        "Check that the text content of the element with data-testid='likes-broken' "
        "is exactly '0'. "
        "Click the button with data-testid='like-broken' exactly once. "
        "Within 150 ms of the click, while the server endpoint is still sleeping "
        "for its artificial ~300 ms delay, check that the text content of the "
        "element with data-testid='likes-broken' is exactly '1' (the optimistic "
        "update is visible). "
        "Then wait ~1000 ms so the server's HTTP 500 response settles, and check "
        "that the text content of data-testid='likes-broken' is back to exactly "
        "'0' (the optimistic change has been rolled back). "
        "Pass only if both the intermediate optimistic value AND the final "
        "rolled-back value are observed."
    )
    result = browser_verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_08_browser_optimistic_rollback",
    )
    assert result.status == "pass", (
        f"Browser optimistic-rollback verification failed: {result.reason}"
    )
