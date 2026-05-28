import json
import os
import re
import socket
import subprocess
import time
from urllib.parse import urlparse

import pytest
import requests
from pochi_verifier import PochiVerifier
from xprocess import ProcessStarter


PROJECT_DIR = "/home/user/sveltekit-wizard"
PORT = 3000
BASE_URL = f"http://localhost:{PORT}"


def _port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("localhost", port)) == 0


def _wait_for_port(port: int, timeout: int = 120) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _port_open(port):
            return True
        time.sleep(1)
    return False


def _build_project():
    """Run npm run build so that `node build` has something to serve."""
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


def _find_users_json() -> str | None:
    """Return the absolute path to the users JSON file if it exists."""
    candidates = [
        os.path.join(PROJECT_DIR, "data", "users.json"),
        os.path.join(PROJECT_DIR, "users.json"),
        os.path.join(PROJECT_DIR, "src", "lib", "server", "users.json"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    # Fallback: walk the project directory looking for a *.json file that
    # looks like a list of user records. Skip node_modules and build output.
    for root, dirs, files in os.walk(PROJECT_DIR):
        dirs[:] = [
            d for d in dirs
            if d not in {"node_modules", ".svelte-kit", "build", ".git"}
        ]
        for fname in files:
            if not fname.endswith(".json"):
                continue
            full = os.path.join(root, fname)
            try:
                with open(full) as f:
                    data = json.load(f)
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(data, list) and any(
                isinstance(x, dict) and "email" in x and "firstName" in x
                for x in data
            ):
                return full
    return None


def _reset_users_file():
    """Remove any pre-existing users JSON file so we start clean."""
    for path in (
        os.path.join(PROJECT_DIR, "data", "users.json"),
        os.path.join(PROJECT_DIR, "users.json"),
        os.path.join(PROJECT_DIR, "src", "lib", "server", "users.json"),
    ):
        try:
            if os.path.isfile(path):
                os.remove(path)
        except OSError:
            pass


@pytest.fixture(scope="session")
def start_app(xprocess):
    """Build then start the SvelteKit wizard on PORT=3000."""
    _reset_users_file()
    _build_project()

    class Starter(ProcessStarter):
        name = "sveltekit_wizard"
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


def _post_form(session: requests.Session, url: str, data: dict) -> requests.Response:
    """POST a form to a SvelteKit form action endpoint with the action header.

    Does NOT follow redirects so we can assert on 303 statuses.
    """
    return session.post(
        url,
        data=data,
        headers={"x-sveltekit-action": "true"},
        allow_redirects=False,
        timeout=30,
    )


def _follow_redirects(
    session: requests.Session, response: requests.Response, max_hops: int = 5
) -> requests.Response:
    """Follow up to max_hops redirects manually, preserving cookies."""
    hops = 0
    while response.is_redirect and hops < max_hops:
        location = response.headers["Location"]
        if location.startswith("/"):
            location = BASE_URL + location
        response = session.get(location, allow_redirects=False, timeout=30)
        hops += 1
    return response


def _redirect_path(response: requests.Response) -> str:
    location = response.headers.get("Location", "")
    if location.startswith("http"):
        return urlparse(location).path
    # Strip query string for path comparisons.
    return location.split("?", 1)[0]


def test_root_redirects_to_step_1(start_app):
    """GET / must redirect (3xx) to /signup/step-1."""
    session = requests.Session()
    response = session.get(BASE_URL + "/", allow_redirects=False, timeout=30)
    assert 300 <= response.status_code < 400, (
        f"GET / expected a 3xx redirect, got {response.status_code}: "
        f"{response.text[:200]}"
    )
    path = _redirect_path(response)
    assert path.rstrip("/") == "/signup/step-1", (
        f"GET / expected redirect to /signup/step-1, got Location='{path}'."
    )


def test_step_1_renders_email_input(start_app):
    """GET /signup/step-1 must render an input with name='email'."""
    response = requests.get(BASE_URL + "/signup/step-1", timeout=30)
    assert response.status_code == 200, (
        f"GET /signup/step-1 expected 200, got {response.status_code}."
    )
    assert re.search(r'name=["\']email["\']', response.text), (
        "Expected an <input name='email'> on /signup/step-1."
    )


def test_step_2_requires_step_1(start_app):
    """GET /signup/step-2 without a session must redirect back to step-1."""
    session = requests.Session()
    response = session.get(
        BASE_URL + "/signup/step-2", allow_redirects=False, timeout=30
    )
    assert 300 <= response.status_code < 400, (
        f"GET /signup/step-2 without session expected a redirect, got "
        f"{response.status_code}."
    )
    path = _redirect_path(response)
    assert path.rstrip("/") == "/signup/step-1", (
        f"Expected /signup/step-2 to redirect to /signup/step-1 when no "
        f"session is present, got Location='{path}'."
    )


def test_review_requires_earlier_steps(start_app):
    """GET /signup/review without earlier steps must redirect back."""
    session = requests.Session()
    response = session.get(
        BASE_URL + "/signup/review", allow_redirects=False, timeout=30
    )
    assert 300 <= response.status_code < 400, (
        f"GET /signup/review without session expected a redirect, got "
        f"{response.status_code}."
    )
    path = _redirect_path(response).rstrip("/")
    assert path in {
        "/signup/step-1",
        "/signup/step-2",
        "/signup/step-3",
    }, (
        f"Expected /signup/review to redirect to an earlier step when no "
        f"session is present, got Location='{path}'."
    )


def test_step_1_validation_error_for_invalid_email(start_app):
    """An invalid email on step-1 must re-render the page with an error."""
    session = requests.Session()
    # Hit step-1 first so the server can set a session cookie if it wants to.
    session.get(BASE_URL + "/signup/step-1", timeout=30)
    response = _post_form(
        session, BASE_URL + "/signup/step-1", {"email": "not-an-email"}
    )
    # Either a 200 with re-rendered HTML or a 400/422 with the same.
    assert response.status_code in {200, 400, 422}, (
        f"POST /signup/step-1 with invalid email expected 200/400/422, got "
        f"{response.status_code}: {response.text[:200]}"
    )
    body = response.text.lower()
    assert "email" in body, (
        "Expected the re-rendered step-1 page to mention 'email'."
    )
    assert re.search(r"invalid|valid|required|error", body), (
        "Expected the re-rendered step-1 page to show an error indicator "
        "for the invalid email."
    )
    assert re.search(r'name=["\']email["\']', response.text), (
        "Expected the email input to still be on the page after a "
        "validation error."
    )


def test_happy_path_through_wizard(start_app):
    """Drive the wizard end-to-end via plain HTTP and verify persistence."""
    _reset_users_file()
    session = requests.Session()

    # Step 1: submit a valid email.
    session.get(BASE_URL + "/signup/step-1", timeout=30)
    resp = _post_form(
        session,
        BASE_URL + "/signup/step-1",
        {"email": "alice@example.com"},
    )
    assert resp.status_code in (302, 303), (
        f"POST /signup/step-1 with valid email expected a 303 redirect, "
        f"got {resp.status_code}: {resp.text[:200]}"
    )
    assert _redirect_path(resp).rstrip("/") == "/signup/step-2", (
        f"Expected redirect to /signup/step-2 after step-1, got "
        f"Location='{_redirect_path(resp)}'."
    )
    page2 = session.get(BASE_URL + "/signup/step-2", timeout=30)
    assert page2.status_code == 200, (
        f"GET /signup/step-2 expected 200, got {page2.status_code}."
    )
    assert re.search(r'name=["\']password["\']', page2.text), (
        "Expected an <input name='password'> on /signup/step-2."
    )
    assert re.search(r'name=["\']confirmPassword["\']', page2.text), (
        "Expected an <input name='confirmPassword'> on /signup/step-2."
    )

    # Step 2: mismatched passwords -> validation error.
    resp = _post_form(
        session,
        BASE_URL + "/signup/step-2",
        {"password": "secret123", "confirmPassword": "wrongpass"},
    )
    assert resp.status_code in {200, 400, 422}, (
        f"POST /signup/step-2 with mismatched passwords expected 200/400/422, "
        f"got {resp.status_code}."
    )
    assert resp.status_code not in (302, 303), (
        "Mismatched passwords on step-2 must not redirect to a later step."
    )
    assert re.search(r"match|same|confirm", resp.text.lower()), (
        "Expected a 'password' mismatch error message on step-2 after "
        "mismatched submission."
    )

    # Step 2: matching passwords -> redirect to step-3.
    resp = _post_form(
        session,
        BASE_URL + "/signup/step-2",
        {"password": "secret123", "confirmPassword": "secret123"},
    )
    assert resp.status_code in (302, 303), (
        f"POST /signup/step-2 with matching passwords expected a 303 "
        f"redirect, got {resp.status_code}: {resp.text[:200]}"
    )
    assert _redirect_path(resp).rstrip("/") == "/signup/step-3", (
        f"Expected redirect to /signup/step-3 after step-2, got "
        f"Location='{_redirect_path(resp)}'."
    )

    page3 = session.get(BASE_URL + "/signup/step-3", timeout=30)
    assert page3.status_code == 200, (
        f"GET /signup/step-3 expected 200, got {page3.status_code}."
    )
    assert re.search(r'name=["\']firstName["\']', page3.text), (
        "Expected an <input name='firstName'> on /signup/step-3."
    )
    assert re.search(r'name=["\']lastName["\']', page3.text), (
        "Expected an <input name='lastName'> on /signup/step-3."
    )

    # Step 3: submit name -> redirect to review.
    resp = _post_form(
        session,
        BASE_URL + "/signup/step-3",
        {"firstName": "Alice", "lastName": "Anderson"},
    )
    assert resp.status_code in (302, 303), (
        f"POST /signup/step-3 expected a 303 redirect to /signup/review, "
        f"got {resp.status_code}: {resp.text[:200]}"
    )
    assert _redirect_path(resp).rstrip("/") == "/signup/review", (
        f"Expected redirect to /signup/review after step-3, got "
        f"Location='{_redirect_path(resp)}'."
    )

    review = session.get(BASE_URL + "/signup/review", timeout=30)
    assert review.status_code == 200, (
        f"GET /signup/review expected 200, got {review.status_code}."
    )
    assert "alice@example.com" in review.text, (
        "Expected the review page to display the submitted email."
    )
    assert "Alice" in review.text, (
        "Expected the review page to display the submitted firstName."
    )
    assert "Anderson" in review.text, (
        "Expected the review page to display the submitted lastName."
    )
    assert "secret123" not in review.text, (
        "The raw password must not appear on /signup/review."
    )

    # Final submission from review.
    resp = _post_form(session, BASE_URL + "/signup/review", {})
    assert resp.status_code in (302, 303), (
        f"POST /signup/review expected a 303 redirect to /signup/done, "
        f"got {resp.status_code}: {resp.text[:200]}"
    )
    location = resp.headers.get("Location", "")
    if location.startswith("http"):
        location_path_query = urlparse(location).path + (
            "?" + urlparse(location).query if urlparse(location).query else ""
        )
    else:
        location_path_query = location
    assert "/signup/done" in location_path_query, (
        f"Expected redirect to /signup/done after final submit, got "
        f"Location='{location}'."
    )
    assert "email=alice@example.com" in location_path_query.replace(
        "%40", "@"
    ), (
        f"Expected /signup/done redirect to include email=alice@example.com, "
        f"got Location='{location}'."
    )

    done = session.get(BASE_URL + location_path_query, timeout=30)
    assert done.status_code == 200, (
        f"GET /signup/done expected 200, got {done.status_code}."
    )
    assert "alice@example.com" in done.text, (
        "Expected the done page to display the submitted email."
    )

    # Persistence to JSON file.
    users_path = _find_users_json()
    assert users_path is not None, (
        "Expected a users JSON file to exist somewhere under "
        f"{PROJECT_DIR} after a successful signup."
    )
    with open(users_path) as f:
        raw = f.read()
    assert "secret123" not in raw, (
        f"The raw password 'secret123' must not appear in {users_path}."
    )
    data = json.loads(raw)
    assert isinstance(data, list), (
        f"Expected {users_path} to contain a JSON array, got "
        f"{type(data).__name__}."
    )
    alice_records = [
        record
        for record in data
        if isinstance(record, dict)
        and record.get("email") == "alice@example.com"
    ]
    assert alice_records, (
        f"Expected a user record for alice@example.com in {users_path}, "
        f"got {data}."
    )
    record = alice_records[-1]
    assert record.get("firstName") == "Alice", (
        f"Expected firstName='Alice' in {record}."
    )
    assert record.get("lastName") == "Anderson", (
        f"Expected lastName='Anderson' in {record}."
    )
    assert record.get("passwordLength") == 9, (
        f"Expected passwordLength=9 in {record}."
    )


def test_source_uses_runes_and_enhance():
    """At least one signup +page.svelte must use runes + use:enhance."""
    signup_dir = os.path.join(PROJECT_DIR, "src", "routes", "signup")
    assert os.path.isdir(signup_dir), (
        f"Expected {signup_dir} to exist (the signup routes directory)."
    )

    page_files = []
    for root, _, files in os.walk(signup_dir):
        for name in files:
            if name == "+page.svelte":
                page_files.append(os.path.join(root, name))
    assert page_files, (
        "Expected at least one +page.svelte under src/routes/signup/."
    )

    saw_rune = False
    saw_enhance = False
    saw_enhance_import = False
    for path in page_files:
        with open(path) as f:
            content = f.read()
        if re.search(r"\$state\(|\$derived\(|\$props\(", content):
            saw_rune = True
        if "use:enhance" in content:
            saw_enhance = True
        if re.search(r"from\s+['\"]\$app/forms['\"]", content):
            saw_enhance_import = True
    assert saw_rune, (
        "Expected at least one of $state(, $derived(, or $props( in a "
        "+page.svelte under src/routes/signup/."
    )
    assert saw_enhance, (
        "Expected use:enhance on at least one signup form."
    )
    assert saw_enhance_import, (
        "Expected an import from '$app/forms' (e.g. `enhance`) in at "
        "least one signup +page.svelte."
    )


def test_step_pages_export_actions():
    """Every step's +page.server.{js,ts} must export an `actions` object."""
    required = [
        "signup/step-1",
        "signup/step-2",
        "signup/step-3",
        "signup/review",
    ]
    for sub in required:
        base = os.path.join(PROJECT_DIR, "src", "routes", sub)
        path = None
        for ext in (".ts", ".js"):
            candidate = os.path.join(base, "+page.server" + ext)
            if os.path.isfile(candidate):
                path = candidate
                break
        assert path is not None, (
            f"Expected src/routes/{sub}/+page.server.(ts|js) to exist."
        )
        with open(path) as f:
            content = f.read()
        assert re.search(
            r"export\s+(const|let|var)?\s*actions", content
        ) or ("export { actions" in content), (
            f"Expected `export const actions` in {path}."
        )


def test_browser_full_flow(start_app):
    """Use pochi-verifier to drive the wizard in a real browser."""
    _reset_users_file()

    reason = (
        "The SvelteKit multi-step signup wizard at /home/user/sveltekit-wizard "
        "must let a user complete a four-page wizard (email, password, name, "
        "review) using forms, with state persisted between steps via a "
        "server-side session, and the final user record stored in a JSON "
        "file on disk without the raw password."
    )
    truth = (
        "Navigate to http://localhost:3000/signup/step-1. Fill the email "
        "input with 'bob@example.com' and submit the form. On the next "
        "page, fill the 'password' input and the 'confirmPassword' input "
        "both with 'password1234' and submit. On the next page, fill the "
        "'firstName' input with 'Bob' and the 'lastName' input with "
        "'Builder' and submit. On the review page, verify that the page "
        "shows 'bob@example.com', 'Bob', and 'Builder' but does NOT show "
        "the string 'password1234'. Click the final submit button. Verify "
        "that the resulting page URL includes '/signup/done' and the page "
        "displays a success message that includes 'bob@example.com'."
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

    # After the browser flow, the users file must include Bob with
    # passwordLength=12, and must not contain the raw password.
    users_path = _find_users_json()
    assert users_path is not None, (
        "Expected a users JSON file to exist after the browser-driven "
        "signup."
    )
    with open(users_path) as f:
        raw = f.read()
    assert "password1234" not in raw, (
        f"The raw password 'password1234' must not appear in {users_path}."
    )
    data = json.loads(raw)
    bob_records = [
        record
        for record in data
        if isinstance(record, dict)
        and record.get("email") == "bob@example.com"
    ]
    assert bob_records, (
        f"Expected a user record for bob@example.com in {users_path}, "
        f"got {data}."
    )
    record = bob_records[-1]
    assert record.get("firstName") == "Bob", (
        f"Expected firstName='Bob' in {record}."
    )
    assert record.get("lastName") == "Builder", (
        f"Expected lastName='Builder' in {record}."
    )
    assert record.get("passwordLength") == 12, (
        f"Expected passwordLength=12 in {record}."
    )
