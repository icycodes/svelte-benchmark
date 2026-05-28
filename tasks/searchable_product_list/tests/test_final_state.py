import json
import os
import re
import socket
import subprocess
import time

import pytest
import requests
from pochi_verifier import PochiVerifier
from xprocess import ProcessStarter


PROJECT_DIR = "/home/user/sveltekit-search"
PORT = 3000
BASE_URL = f"http://localhost:{PORT}"

REQUIRED_NAMES = ["Apple iPhone", "Banana Phone", "Cherry Tablet"]


def _port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("localhost", port)) == 0


def _build_project():
    """Run `npm run build` so that `node build` has something to serve."""
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


@pytest.fixture(scope="session")
def start_app(xprocess):
    """Build then start the SvelteKit app on PORT=3000."""
    _build_project()

    class Starter(ProcessStarter):
        name = "sveltekit_search"
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

    # Wait a moment after the port opens for the app to be fully responsive.
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            r = requests.get(BASE_URL + "/products", timeout=5)
            if r.status_code == 200:
                break
        except requests.RequestException:
            pass
        time.sleep(1)

    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()


def _extract_product_items(html: str) -> list[str]:
    """Return the inner-HTML chunks of every element with data-testid=product-item.

    The matcher is intentionally generous so it works regardless of the exact
    element type the executor chooses. It captures the tag's contents up to
    the matching closing tag for that *type* of element.
    """
    items: list[str] = []
    # Match opening tag, capture tag name and attribute string, then non-greedy
    # body up to a closing tag with the same name.
    pattern = re.compile(
        r"<(?P<tag>[a-zA-Z][a-zA-Z0-9-]*)\b[^>]*\bdata-testid=[\"']product-item[\"'][^>]*>"
        r"(?P<body>.*?)</(?P=tag)>",
        re.DOTALL,
    )
    for m in pattern.finditer(html):
        items.append(m.group("body"))
    return items


def test_root_redirects_to_products(start_app):
    response = requests.get(BASE_URL + "/", allow_redirects=False, timeout=30)
    assert 300 <= response.status_code < 400, (
        f"GET / expected a 3xx redirect, got {response.status_code}."
    )
    location = response.headers.get("Location", "")
    # Strip origin if present.
    if location.startswith("http"):
        from urllib.parse import urlparse

        location = urlparse(location).path
    assert location.rstrip("/") == "/products", (
        f"GET / expected redirect to /products, got Location='{location}'."
    )


def test_api_products_returns_required_data(start_app):
    response = requests.get(BASE_URL + "/api/products", timeout=30)
    assert response.status_code == 200, (
        f"GET /api/products expected 200, got {response.status_code}."
    )
    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"GET /api/products must return JSON; failed to parse: {exc}. "
            f"Body: {response.text[:200]}"
        )
    assert isinstance(data, list), (
        f"GET /api/products must return a JSON array, got "
        f"{type(data).__name__}."
    )
    assert len(data) >= 6, (
        f"Expected at least 6 products from /api/products, got {len(data)}."
    )
    for item in data:
        assert isinstance(item, dict), (
            f"Every product entry must be an object, got {type(item).__name__}: {item}."
        )
        assert "id" in item and isinstance(item["id"], (int, float)) and not isinstance(item["id"], bool), (
            f"Each product must have a numeric `id` field. Got: {item}."
        )
        assert "name" in item and isinstance(item["name"], str), (
            f"Each product must have a string `name` field. Got: {item}."
        )
        assert "price" in item and isinstance(item["price"], (int, float)) and not isinstance(item["price"], bool), (
            f"Each product must have a numeric `price` field. Got: {item}."
        )

    names = [item["name"] for item in data]
    assert len(set(names)) == len(names), (
        f"Product names must be unique. Got duplicates in: {names}."
    )
    for required in REQUIRED_NAMES:
        count = sum(1 for n in names if n == required)
        assert count == 1, (
            f"Expected exactly one product named '{required}' in "
            f"/api/products, found {count}. All names: {names}."
        )


def test_products_page_renders_all_when_no_filter(start_app):
    response = requests.get(BASE_URL + "/products", timeout=30)
    assert response.status_code == 200, (
        f"GET /products expected 200, got {response.status_code}."
    )
    html = response.text

    # Search input
    assert re.search(
        r'<input\b[^>]*\bname=["\']q["\'][^>]*\bdata-testid=["\']search-input["\']',
        html,
    ) or re.search(
        r'<input\b[^>]*\bdata-testid=["\']search-input["\'][^>]*\bname=["\']q["\']',
        html,
    ), (
        "Expected an <input> with name='q' AND data-testid='search-input' on "
        "/products."
    )

    items = _extract_product_items(html)
    assert len(items) >= 6, (
        f"Expected at least 6 product-item elements rendered on /products "
        f"with no filter, got {len(items)}."
    )

    flat_html = " ".join(items)
    for required in REQUIRED_NAMES:
        assert required in flat_html, (
            f"Expected the product name '{required}' to appear inside a "
            f"data-testid='product-item' element on /products."
        )


def _names_in_product_items(html: str) -> list[str]:
    """Return the list of REQUIRED product names that appear inside a
    data-testid=product-item element, given the page HTML."""
    items = _extract_product_items(html)
    flat_html = " ".join(items)
    return [name for name in REQUIRED_NAMES if name in flat_html]


def test_products_page_ssr_filter_apple(start_app):
    response = requests.get(BASE_URL + "/products", params={"q": "apple"}, timeout=30)
    assert response.status_code == 200, (
        f"GET /products?q=apple expected 200, got {response.status_code}."
    )
    visible = _names_in_product_items(response.text)
    assert "Apple iPhone" in visible, (
        "GET /products?q=apple must render 'Apple iPhone' inside a "
        "data-testid='product-item' element (case-insensitive match)."
    )
    assert "Banana Phone" not in visible, (
        "GET /products?q=apple must NOT render 'Banana Phone' inside a "
        "data-testid='product-item' element."
    )
    assert "Cherry Tablet" not in visible, (
        "GET /products?q=apple must NOT render 'Cherry Tablet' inside a "
        "data-testid='product-item' element."
    )


def test_products_page_ssr_filter_case_insensitive_uppercase(start_app):
    response = requests.get(BASE_URL + "/products", params={"q": "BAN"}, timeout=30)
    assert response.status_code == 200, (
        f"GET /products?q=BAN expected 200, got {response.status_code}."
    )
    visible = _names_in_product_items(response.text)
    assert "Banana Phone" in visible, (
        "GET /products?q=BAN must render 'Banana Phone' inside a "
        "data-testid='product-item' element (filtering must be "
        "case-insensitive)."
    )
    assert "Apple iPhone" not in visible, (
        "GET /products?q=BAN must NOT render 'Apple iPhone' inside a "
        "data-testid='product-item' element."
    )
    assert "Cherry Tablet" not in visible, (
        "GET /products?q=BAN must NOT render 'Cherry Tablet' inside a "
        "data-testid='product-item' element."
    )


def test_products_page_ssr_filter_no_match(start_app):
    response = requests.get(
        BASE_URL + "/products", params={"q": "zzz_no_match_zzz"}, timeout=30
    )
    assert response.status_code == 200, (
        f"GET /products?q=zzz_no_match_zzz expected 200, got "
        f"{response.status_code}."
    )
    items = _extract_product_items(response.text)
    assert items == [], (
        f"GET /products?q=zzz_no_match_zzz must render zero "
        f"data-testid='product-item' elements, got {len(items)}."
    )


def test_products_page_form_is_get_to_products(start_app):
    response = requests.get(BASE_URL + "/products", timeout=30)
    assert response.status_code == 200
    html = response.text

    # Find the form that wraps the search input. We allow attributes in any order.
    form_pattern = re.compile(
        r"<form\b[^>]*>.*?<input\b[^>]*\bdata-testid=[\"']search-input[\"'][^>]*>.*?</form>",
        re.DOTALL,
    )
    m = form_pattern.search(html)
    assert m is not None, (
        "Expected a <form> element to wrap the search input "
        "(data-testid='search-input') on /products."
    )
    form_tag_match = re.search(r"<form\b[^>]*>", m.group(0))
    assert form_tag_match is not None
    form_open = form_tag_match.group(0)
    assert re.search(r'method=["\']get["\']', form_open, re.IGNORECASE), (
        f"Expected the search <form> on /products to have method=\"get\", got: {form_open}"
    )
    assert re.search(r'action=["\']/products["\']', form_open), (
        f"Expected the search <form> on /products to have action=\"/products\", got: {form_open}"
    )

    # And confirm that submitting that form (via a GET) really filters.
    response2 = requests.get(BASE_URL + "/products", params={"q": "cherry"}, timeout=30)
    assert response2.status_code == 200
    visible = _names_in_product_items(response2.text)
    assert "Cherry Tablet" in visible, (
        "GET /products?q=cherry (the no-JS form path) must render "
        "'Cherry Tablet' inside a data-testid='product-item' element."
    )
    assert "Apple iPhone" not in visible, (
        "GET /products?q=cherry must NOT render 'Apple iPhone' inside a "
        "data-testid='product-item' element."
    )
    assert "Banana Phone" not in visible, (
        "GET /products?q=cherry must NOT render 'Banana Phone' inside a "
        "data-testid='product-item' element."
    )


def _find_page_svelte_source() -> str:
    path = os.path.join(PROJECT_DIR, "src", "routes", "products", "+page.svelte")
    assert os.path.isfile(path), (
        f"Expected src/routes/products/+page.svelte to exist at {path}."
    )
    with open(path) as f:
        return f.read()


def test_source_products_page_uses_runes_and_goto():
    src = _find_page_svelte_source()
    assert re.search(r"\$state\(|\$derived\(|\$props\(", src), (
        "Expected src/routes/products/+page.svelte to use at least one Svelte 5 "
        "rune ($state, $derived, or $props)."
    )
    assert re.search(r"from\s+['\"]\$app/navigation['\"]", src) and "goto" in src, (
        "Expected src/routes/products/+page.svelte to import `goto` from "
        "'$app/navigation'."
    )
    assert re.search(r"replaceState\s*:\s*true", src), (
        "Expected src/routes/products/+page.svelte to pass "
        "`replaceState: true` to goto(...)."
    )
    assert re.search(r"keepFocus\s*:\s*true", src), (
        "Expected src/routes/products/+page.svelte to pass "
        "`keepFocus: true` to goto(...)."
    )


def test_source_products_load_uses_searchparams_and_fetch():
    candidates = [
        os.path.join(PROJECT_DIR, "src", "routes", "products", "+page.js"),
        os.path.join(PROJECT_DIR, "src", "routes", "products", "+page.ts"),
    ]
    path = next((p for p in candidates if os.path.isfile(p)), None)
    assert path is not None, (
        "Expected src/routes/products/+page.js or +page.ts to exist "
        "(a universal load function)."
    )
    with open(path) as f:
        src = f.read()
    assert re.search(r"\bexport\b.*\bload\b", src) or re.search(
        r"\bload\b\s*[:=]", src
    ), (
        f"Expected {path} to export a `load` function."
    )
    assert "url.searchParams" in src, (
        f"Expected {path} to read from `url.searchParams`."
    )
    assert re.search(r"fetch\(\s*['\"]/api/products['\"]", src), (
        f"Expected {path} to call `fetch('/api/products')` (relative URL) "
        f"inside the load function."
    )


def test_source_api_products_server_endpoint_exists():
    candidates = [
        os.path.join(PROJECT_DIR, "src", "routes", "api", "products", "+server.js"),
        os.path.join(PROJECT_DIR, "src", "routes", "api", "products", "+server.ts"),
    ]
    path = next((p for p in candidates if os.path.isfile(p)), None)
    assert path is not None, (
        "Expected src/routes/api/products/+server.js or +server.ts to exist."
    )
    with open(path) as f:
        src = f.read()
    assert re.search(r"export\s+(async\s+)?(const|let|function)\s+GET\b", src) or re.search(
        r"export\s*\{\s*GET\b", src
    ), (
        f"Expected {path} to export a `GET` request handler."
    )


def test_browser_interactive_search(start_app):
    """Use pochi-verifier to drive the products page in a real browser."""
    reason = (
        "The /products page of the SvelteKit app at /home/user/sveltekit-search "
        "must filter a product list in real time as the user types into the "
        "search input, with the URL kept in sync via goto(..., {replaceState: "
        "true, keepFocus: true}) from $app/navigation and the SvelteKit load "
        "function re-running to produce the filtered list. Clearing the "
        "input must show all products again."
    )
    truth = (
        "Navigate to http://localhost:3000/products. Verify that the page "
        "shows at least three elements with the attribute "
        "data-testid='product-item', and that those elements include the "
        "texts 'Apple iPhone', 'Banana Phone', and 'Cherry Tablet' (one of "
        "each). Then click the input element with data-testid='search-input' "
        "to focus it and type the literal text 'Apple' into it. Wait up to "
        "2 seconds, then verify that: (a) the current page URL is exactly "
        "'http://localhost:3000/products?q=Apple' (note the exact casing 'Apple') "
        "without a full page reload, (b) the only element with "
        "data-testid='product-item' visible on the page contains the text "
        "'Apple iPhone', and (c) neither 'Banana Phone' nor 'Cherry Tablet' "
        "appears inside any element with data-testid='product-item'. Then "
        "select all the text in the search input and delete it so the input "
        "is empty. Wait up to 2 seconds, then verify that: (d) the current "
        "page URL becomes 'http://localhost:3000/products' (with no '?q=' "
        "query string), and (e) all three of 'Apple iPhone', 'Banana Phone', "
        "and 'Cherry Tablet' appear again, each inside an element with "
        "data-testid='product-item'."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_interactive_search",
    )
    assert result.status == "pass", (
        f"Browser verification failed: {result.reason}"
    )
