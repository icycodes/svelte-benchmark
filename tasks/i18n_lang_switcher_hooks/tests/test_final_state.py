import os
import re
import socket
import subprocess
import time

import pytest
import requests
from xprocess import ProcessStarter

from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/sveltekit-i18n"
APP_URL = "http://localhost:3000"
COOKIE_JAR = "/tmp/i18n_cookies.txt"


def _wait_for_port(host: str, port: int, timeout: float = 180.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            if s.connect_ex((host, port)) == 0:
                return True
        time.sleep(1.0)
    return False


@pytest.fixture(scope="session")
def start_app(xprocess):
    # Clean up any leftover cookie jar
    if os.path.isfile(COOKIE_JAR):
        os.remove(COOKIE_JAR)

    # Ensure the build exists; if not, build it.
    build_dir = os.path.join(PROJECT_DIR, "build")
    if not os.path.isdir(build_dir):
        subprocess.run(
            ["npm", "run", "build"],
            cwd=PROJECT_DIR,
            check=True,
            env={**os.environ, "CI": "1"},
        )

    class Starter(ProcessStarter):
        name = "sveltekit_i18n_app"
        args = ["node", "build"]
        env = {**os.environ, "PORT": "3000", "HOST": "0.0.0.0", "NODE_ENV": "production"}
        popen_kwargs = {"cwd": PROJECT_DIR, "text": True}
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                return s.connect_ex(("127.0.0.1", 3000)) == 0

    xprocess.ensure(Starter.name, Starter)
    assert _wait_for_port("127.0.0.1", 3000, timeout=60), "App did not become ready on port 3000"

    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()


@pytest.fixture(scope="session")
def browser_verifier():
    yield PochiVerifier()


def _html_lang(html: str) -> str:
    m = re.search(r"<html\b[^>]*\blang\s*=\s*[\"']([^\"']+)[\"']", html, re.IGNORECASE)
    assert m, "Could not find <html ... lang=...> in response body."
    return m.group(1)


def _has_form_button(html: str, testid: str) -> bool:
    pattern = re.compile(
        r"<button\b[^>]*data-testid\s*=\s*[\"']" + re.escape(testid) + r"[\"'][^>]*>",
        re.IGNORECASE,
    )
    return bool(pattern.search(html))


def _current_locale_text(html: str) -> str:
    m = re.search(
        r"<[^>]+data-testid\s*=\s*[\"']current-locale[\"'][^>]*>\s*([a-zA-Z-]+)\s*<",
        html,
    )
    assert m, "Could not find an element with data-testid='current-locale' in the page."
    return m.group(1).strip()


def test_get_default_locale_is_en(start_app):
    r = requests.get(APP_URL + "/", timeout=15)
    assert r.status_code == 200, f"Expected 200 at GET /, got {r.status_code}: {r.text[:200]}"
    body = r.text
    assert _html_lang(body) == "en", "Default <html lang> should be 'en' when no locale cookie is set."
    assert "Hello, world!" in body, "Default English greeting 'Hello, world!' not found in the response body."
    assert _current_locale_text(body) == "en", "data-testid='current-locale' should show 'en' as default."
    for code in ("en", "de", "fr"):
        assert _has_form_button(body, f"locale-btn-{code}"), (
            f"Missing locale switch button with data-testid='locale-btn-{code}'."
        )
    assert re.search(r"<form\b[^>]*method\s*=\s*[\"']POST[\"']", body, re.IGNORECASE), (
        "Page does not contain a <form method=\"POST\"> for the locale switch."
    )


def test_switch_to_german_persists_in_cookie(start_app):
    session = requests.Session()
    # Submit the form action. Allow redirects=False so we can inspect the 303.
    post = session.post(
        APP_URL + "/",
        data={"locale": "de"},
        allow_redirects=False,
        timeout=15,
    )
    # SvelteKit form actions return 303 redirects on success.
    assert post.status_code in (200, 303), (
        f"Expected 303 (or 200) for locale switch POST, got {post.status_code}: {post.text[:200]}"
    )
    # The cookie must be set on the response (either through a redirect or a 200 with Set-Cookie).
    assert "locale" in session.cookies.get_dict(), (
        f"Expected 'locale' cookie to be set after POST, got cookies: {session.cookies.get_dict()}"
    )
    assert session.cookies.get("locale") == "de", (
        f"Expected locale cookie to equal 'de', got {session.cookies.get('locale')!r}"
    )

    # Now GET / with the cookie and verify the page reflects German.
    get = session.get(APP_URL + "/", timeout=15)
    assert get.status_code == 200, f"GET / after switch returned {get.status_code}"
    body = get.text
    assert _html_lang(body) == "de", "<html lang> should be 'de' after switching."
    assert "Hallo, Welt!" in body, "German greeting 'Hallo, Welt!' not found in response after switch."
    assert _current_locale_text(body) == "de", "data-testid='current-locale' should show 'de' after switching."


def test_switch_to_french_persists_in_cookie(start_app):
    session = requests.Session()
    post = session.post(
        APP_URL + "/",
        data={"locale": "fr"},
        allow_redirects=False,
        timeout=15,
    )
    assert post.status_code in (200, 303), (
        f"Expected 303 (or 200) for locale switch POST, got {post.status_code}"
    )
    assert session.cookies.get("locale") == "fr", (
        f"Expected locale cookie to equal 'fr', got {session.cookies.get('locale')!r}"
    )

    get = session.get(APP_URL + "/", timeout=15)
    assert get.status_code == 200, f"GET / after switching to fr returned {get.status_code}"
    body = get.text
    assert _html_lang(body) == "fr", "<html lang> should be 'fr' after switching to French."
    assert "Bonjour, le monde !" in body, "French greeting 'Bonjour, le monde !' not found in response after switch."
    assert _current_locale_text(body) == "fr", "data-testid='current-locale' should show 'fr' after switching."


def test_invalid_locale_cookie_falls_back_to_default(start_app):
    # Send an invalid locale cookie; the server must NOT crash and must render the default locale.
    r = requests.get(
        APP_URL + "/",
        cookies={"locale": "xx"},
        timeout=15,
    )
    assert r.status_code == 200, (
        f"Server should not crash when an invalid locale cookie is provided; got {r.status_code}."
    )
    body = r.text
    assert _html_lang(body) == "en", "Invalid locale cookie must fall back to 'en' for <html lang>."
    assert "Hello, world!" in body, "Invalid locale cookie should render the default English greeting."


def test_server_side_lang_is_set_without_javascript(start_app):
    # curl-equivalent: a single GET with no JS execution must already have the lang attribute set.
    r = requests.get(APP_URL + "/", cookies={"locale": "de"}, timeout=15)
    assert r.status_code == 200
    assert _html_lang(r.text) == "de", (
        "The <html lang> attribute must be set by the server (transformPageChunk) and not by client-side JS."
    )
    assert "Hallo, Welt!" in r.text, "German greeting must be present in the server-rendered HTML."


def test_hooks_server_file_uses_transform_page_chunk():
    hooks_js = os.path.join(PROJECT_DIR, "src", "hooks.server.js")
    hooks_ts = os.path.join(PROJECT_DIR, "src", "hooks.server.ts")
    path = hooks_js if os.path.isfile(hooks_js) else hooks_ts
    assert os.path.isfile(path), (
        "Expected src/hooks.server.js or src/hooks.server.ts to exist for the i18n handle hook."
    )
    with open(path) as f:
        content = f.read()
    assert "transformPageChunk" in content, (
        "src/hooks.server.* must use transformPageChunk to rewrite the <html lang> attribute."
    )


def test_page_uses_enhance_and_actions_exist():
    page_svelte = os.path.join(PROJECT_DIR, "src", "routes", "+page.svelte")
    assert os.path.isfile(page_svelte), "src/routes/+page.svelte must exist."
    with open(page_svelte) as f:
        page = f.read()
    assert "$app/forms" in page, "+page.svelte must import from '$app/forms'."
    assert re.search(r"use\s*:\s*enhance", page), (
        "+page.svelte must use the `use:enhance` action on the locale switch form."
    )

    action_js = os.path.join(PROJECT_DIR, "src", "routes", "+page.server.js")
    action_ts = os.path.join(PROJECT_DIR, "src", "routes", "+page.server.ts")
    assert os.path.isfile(action_js) or os.path.isfile(action_ts), (
        "A +page.server.js or +page.server.ts at src/routes/ exporting an `actions` object is required."
    )
    action_path = action_js if os.path.isfile(action_js) else action_ts
    with open(action_path) as f:
        action_content = f.read()
    assert "actions" in action_content, (
        "src/routes/+page.server.* must export an `actions` object handling the locale switch."
    )


def test_browser_locale_switcher_ui(start_app, browser_verifier):
    reason = (
        "The page at http://localhost:3000/ must let the user switch between English, German, "
        "and French using buttons inside a SvelteKit form action. The <html lang> attribute "
        "must always reflect the selected locale (because it is set by the server inside "
        "hooks.server.js via transformPageChunk), and the greeting text must update accordingly. "
        "The selected locale must persist across page reloads via the `locale` cookie."
    )
    truth = (
        "Open http://localhost:3000/ in a fresh browser session with cookies cleared. "
        "Verify that document.documentElement.lang === 'en' and the page shows the text "
        "'Hello, world!' and an element with data-testid='current-locale' whose text is 'en'. "
        "Click the button with data-testid='locale-btn-de'. After the navigation/update settles, "
        "verify document.documentElement.lang === 'de', the page shows 'Hallo, Welt!', and the "
        "current-locale element shows 'de'. Then click data-testid='locale-btn-fr'; verify "
        "document.documentElement.lang === 'fr', the page shows 'Bonjour, le monde !', and the "
        "current-locale element shows 'fr'. Finally, reload the page (F5) and verify that the "
        "locale remains 'fr' (lang attribute 'fr' and greeting 'Bonjour, le monde !')."
    )
    result = browser_verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_locale_switcher_ui",
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
