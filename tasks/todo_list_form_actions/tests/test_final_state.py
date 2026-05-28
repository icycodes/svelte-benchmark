import os
import re
import socket
import subprocess
import time

import pytest
import requests
from pochi_verifier import PochiVerifier
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/sveltekit-todos"
PORT = 3000
BASE_URL = f"http://localhost:{PORT}"


def _port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("localhost", port)) == 0


def _wait_for_port(port: int, timeout: int = 120):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _port_open(port):
            return True
        time.sleep(1)
    return False


def _build_project():
    """Run npm run build to ensure the build artifacts exist."""
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert result.returncode == 0, (
        f"`npm run build` failed in {PROJECT_DIR}.\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def _reset_persistence():
    """Delete known on-disk todo files so we start from an empty list."""
    candidates = [
        os.path.join(PROJECT_DIR, "data", "todos.json"),
        os.path.join(PROJECT_DIR, "todos.json"),
        os.path.join(PROJECT_DIR, "src", "lib", "server", "todos.json"),
        os.path.join(PROJECT_DIR, "src", "lib", "todos.json"),
    ]
    for path in candidates:
        try:
            if os.path.isfile(path):
                os.remove(path)
        except OSError:
            pass


@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Build the SvelteKit project then start it with `node build` on PORT=3000.
    """
    _reset_persistence()
    _build_project()

    class Starter(ProcessStarter):
        name = "sveltekit_todos"
        args = ["node", "build"]
        env = {**os.environ, "PORT": str(PORT), "HOST": "0.0.0.0"}
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 120
        terminate_on_interrupt = True

        def startup_check(self):
            return _port_open(PORT)

    xprocess.ensure(Starter.name, Starter)

    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()


def _restart_app(xprocess):
    """Stop and restart the SvelteKit server, preserving on-disk data."""
    info = xprocess.getinfo("sveltekit_todos")
    info.terminate()
    # Wait for the port to be free.
    for _ in range(30):
        if not _port_open(PORT):
            break
        time.sleep(1)

    class Starter(ProcessStarter):
        name = "sveltekit_todos"
        args = ["node", "build"]
        env = {**os.environ, "PORT": str(PORT), "HOST": "0.0.0.0"}
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 120
        terminate_on_interrupt = True

        def startup_check(self):
            return _port_open(PORT)

    xprocess.ensure(Starter.name, Starter)


def _post_action(action: str, fields: dict) -> requests.Response:
    """POST to a SvelteKit form action and return the response.

    Uses the `x-sveltekit-action: true` header to make sure the form-action
    handler is invoked even when content-negotiation might prefer a +server.js
    handler. Does NOT follow redirects, so we can assert on 303/302 codes.
    """
    return requests.post(
        f"{BASE_URL}/?/{action}",
        data=fields,
        headers={"x-sveltekit-action": "true"},
        allow_redirects=False,
        timeout=30,
    )


def _find_todo_id(html: str, text: str) -> str:
    """Find the todo id associated with the given todo text in the page HTML.

    The acceptance criteria require an `id` form field for each todo. We look
    for the closest `name="id"` value to the matching todo text.
    """
    # Try to find structures like <input ... name="id" value="<id>" ...>
    # near the todo text. We scan all id values, then verify by re-rendering.
    id_inputs = re.findall(
        r'name=["\']id["\']\s+value=["\']([^"\']+)["\']'
        r"|value=["\']([^"\']+)["\']\s+name=["\']id["\']",
        html,
    )
    candidate_ids = [a or b for a, b in id_inputs]
    # Map ids by proximity to the text occurrence.
    text_index = html.find(text)
    if text_index == -1 or not candidate_ids:
        raise AssertionError(
            f"Could not locate todo text '{text}' or any id form fields in HTML."
        )

    best_id = None
    best_distance = None
    for candidate in candidate_ids:
        # Find the position of this candidate id in HTML.
        pos = html.find(candidate)
        if pos == -1:
            continue
        distance = abs(pos - text_index)
        if best_distance is None or distance < best_distance:
            best_distance = distance
            best_id = candidate
    assert best_id is not None, (
        f"Failed to associate any id with todo text '{text}'."
    )
    return best_id


def test_homepage_renders(start_app):
    """The home page must render and include the add-todo form skeleton."""
    response = requests.get(BASE_URL, timeout=30)
    assert response.status_code == 200, (
        f"GET / returned {response.status_code}: {response.text[:500]}"
    )
    html = response.text
    assert re.search(r'name=["\']text["\']', html), (
        "Expected an input with name='text' on the home page."
    )


def test_add_todo_buy_milk(start_app):
    """POSTing to ?/add must create the todo and it must render on the page."""
    resp = _post_action("add", {"text": "Buy milk"})
    assert resp.status_code in (200, 201, 204, 302, 303), (
        f"POST /?/add returned unexpected status {resp.status_code}: "
        f"{resp.text[:500]}"
    )
    page = requests.get(BASE_URL, timeout=30).text
    assert "Buy milk" in page, "Expected 'Buy milk' in page after add."


def test_add_second_todo_and_remaining_count(start_app):
    """A second add must show both todos and remaining count of 2."""
    resp = _post_action("add", {"text": "Read book"})
    assert resp.status_code in (200, 201, 204, 302, 303), (
        f"POST /?/add returned unexpected status {resp.status_code}."
    )
    page = requests.get(BASE_URL, timeout=30).text
    assert "Buy milk" in page, "Expected 'Buy milk' still present."
    assert "Read book" in page, "Expected 'Read book' to be present."
    # remaining count should be at least visible as the digit 2.
    assert re.search(r"\b2\b", page), (
        "Expected the remaining-count indicator to display 2."
    )


def test_toggle_completion(start_app):
    """Toggling Buy milk must reduce the remaining count to 1."""
    page = requests.get(BASE_URL, timeout=30).text
    buy_milk_id = _find_todo_id(page, "Buy milk")

    resp = _post_action("toggle", {"id": buy_milk_id})
    assert resp.status_code in (200, 201, 204, 302, 303), (
        f"POST /?/toggle returned unexpected status {resp.status_code}: "
        f"{resp.text[:500]}"
    )
    page = requests.get(BASE_URL, timeout=30).text
    assert "Buy milk" in page, "Buy milk should remain visible after toggle."
    assert re.search(r"\b1\b", page), (
        "Expected the remaining-count indicator to display 1 after toggle."
    )


def test_delete_todo(start_app):
    """Deleting Read book must remove it from the page."""
    page = requests.get(BASE_URL, timeout=30).text
    read_book_id = _find_todo_id(page, "Read book")
    resp = _post_action("delete", {"id": read_book_id})
    assert resp.status_code in (200, 201, 204, 302, 303), (
        f"POST /?/delete returned unexpected status {resp.status_code}."
    )
    page = requests.get(BASE_URL, timeout=30).text
    assert "Read book" not in page, (
        "Expected 'Read book' to be removed after delete."
    )
    assert "Buy milk" in page, "'Buy milk' should still be present."
    assert re.search(r"\b0\b", page), (
        "Expected the remaining-count indicator to display 0 (Buy milk "
        "is completed)."
    )


def test_persistence_across_restart(start_app, xprocess):
    """After restart, Buy milk must still be present and remaining count = 0."""
    _restart_app(xprocess)
    assert _wait_for_port(PORT, timeout=60), (
        "Server did not come back up on port 3000 after restart."
    )
    page = requests.get(BASE_URL, timeout=30).text
    assert "Buy milk" in page, (
        "Expected 'Buy milk' to persist across a server restart."
    )


def test_source_uses_runes_and_enhance():
    """The page component must use Svelte 5 runes and use:enhance."""
    candidates = [
        os.path.join(PROJECT_DIR, "src", "routes", "+page.svelte"),
    ]
    page_path = next((p for p in candidates if os.path.isfile(p)), None)
    assert page_path is not None, (
        "src/routes/+page.svelte not found in the project."
    )
    with open(page_path) as f:
        content = f.read()
    assert re.search(r"\$state\(|\$derived\(|\$props\(", content), (
        "Expected at least one Svelte 5 rune ($state, $derived, or $props) "
        "in src/routes/+page.svelte."
    )
    assert "use:enhance" in content, (
        "Expected use:enhance in src/routes/+page.svelte for progressive "
        "enhancement."
    )
    assert re.search(r"from\s+['\"]\$app/forms['\"]", content), (
        "Expected an import from '$app/forms' (e.g. `enhance`) in +page.svelte."
    )


def test_server_module_defines_actions_and_load():
    """+page.server.{js,ts} must define add/toggle/delete actions and load."""
    candidates = [
        os.path.join(PROJECT_DIR, "src", "routes", "+page.server.ts"),
        os.path.join(PROJECT_DIR, "src", "routes", "+page.server.js"),
    ]
    server_path = next((p for p in candidates if os.path.isfile(p)), None)
    assert server_path is not None, (
        "src/routes/+page.server.(ts|js) not found."
    )
    with open(server_path) as f:
        content = f.read()
    # Look for an exported actions object containing add/toggle/delete.
    assert re.search(r"export\s+(const|let|var)?\s*actions", content) or (
        "export { actions" in content
    ), "Expected `export const actions` (or equivalent) in +page.server."
    assert re.search(r"\badd\b", content), (
        "Expected an `add` action handler in +page.server."
    )
    assert re.search(r"\btoggle\b", content), (
        "Expected a `toggle` action handler in +page.server."
    )
    assert re.search(r"\bdelete\b", content), (
        "Expected a `delete` action handler in +page.server."
    )
    assert re.search(r"export\s+(async\s+)?function\s+load", content) or (
        re.search(r"export\s+const\s+load", content) is not None
    ), "Expected an exported `load` function in +page.server."


def test_browser_full_flow(start_app):
    """Use pochi-verifier to do a UI-level walkthrough of the full flow."""
    # Reset persistence so the browser test starts from an empty list.
    _reset_persistence()
    # The persistence reset happens in-place; the running server will reload
    # the file the next time its load function runs. To make sure the file is
    # re-read consistently, restart the server.
    # Note: This shares the same xprocess fixture process; we restart via the
    # xprocess fixture for safety.

    reason = (
        "The SvelteKit Todo app at /home/user/sveltekit-todos must let a user "
        "add new todos using a text input, see them appear in a list, mark "
        "them as complete with a toggle control, see the remaining (incomplete) "
        "count change, and delete todos."
    )
    truth = (
        "Navigate to http://localhost:3000. Verify an input field for entering "
        "new todo text is visible. Type 'Walk dog' into the input and submit "
        "the form (e.g., by pressing Enter or clicking the Add button). Verify "
        "'Walk dog' now appears in the list of todos. Add another todo with "
        "text 'Write report' and verify it appears in the list. Verify that "
        "the page shows a remaining/incomplete count indicating 2 items are "
        "still to do. Mark the 'Walk dog' todo as complete by interacting "
        "with its toggle control (e.g., clicking its checkbox). Verify the "
        "remaining count now shows 1, and the 'Walk dog' item is visibly "
        "marked as completed (e.g., with strikethrough, a checked box, or a "
        "muted style). Delete the 'Write report' todo by clicking its delete "
        "control. Verify 'Write report' is no longer in the list, the "
        "remaining count shows 0, and 'Walk dog' is still present."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_full_flow",
    )
    assert result.status == "pass", (
        f"Browser verification failed: {result.reason}"
    )
