import os
import socket
import pytest
from xprocess import ProcessStarter
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/rating-app"
PORT = 3000


@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Build and start the SvelteKit production server.
    Uses the start command from the task acceptance criteria:
        npm run build && PORT=3000 HOST=0.0.0.0 node build
    """

    class Starter(ProcessStarter):
        name = "rating_app"
        args = ["bash", "-lc", "npm run build && PORT=3000 HOST=0.0.0.0 node build"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 300
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", PORT)) == 0

    xprocess.ensure(Starter.name, Starter)

    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()


def test_star_rating_component_exists():
    """Truth step 1: Confirm the bindable StarRating component file exists."""
    component_path = os.path.join(PROJECT_DIR, "src", "lib", "StarRating.svelte")
    assert os.path.isfile(component_path), (
        f"Expected reusable StarRating component at {component_path}, "
        "but the file was not found."
    )


def test_star_rating_uses_bindable_rune():
    """Truth step 1: Confirm the component uses the Svelte 5 $bindable() rune."""
    component_path = os.path.join(PROJECT_DIR, "src", "lib", "StarRating.svelte")
    with open(component_path, "r", encoding="utf-8") as fh:
        content = fh.read()
    assert "$bindable(" in content, (
        "StarRating.svelte must declare a bindable prop using the Svelte 5 "
        "`$bindable()` rune (e.g. `let { value = $bindable(0) } = $props();`)."
    )


def test_initial_render(start_app):
    """Truth step 2: Initial render shows Rating: 0, 5 stars, 0 filled, Reset button."""
    reason = (
        "The home page should render the reusable StarRating component bound to a "
        "parent rating state that starts at 0. There must be exactly five interactive "
        "star elements, none of them filled initially, and a Reset button must be "
        "present."
    )
    truth = (
        "Navigate to http://localhost:3000/. "
        "Verify that the page contains the exact text 'Rating: 0'. "
        "Verify that there are exactly 5 interactive star elements (for example, "
        "buttons with a stable class such as 'star' or elements with a `data-star` "
        "attribute). "
        "Verify that zero stars are marked as filled (for example, no element has "
        "class 'filled' or `data-filled=\"true\"`). "
        "Verify that a button labelled 'Reset' is visible on the page."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_initial_render",
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"


def test_click_fourth_star_updates_bound_value(start_app):
    """Truth step 3: Clicking the 4th star updates heading to Rating: 4 and fills 4 stars."""
    reason = (
        "Clicking the fourth star button must update the parent-bound rating value to "
        "4, which is shown via the heading and reflected by exactly four filled stars."
    )
    truth = (
        "Navigate to http://localhost:3000/. "
        "Click the 4th star element (the fourth interactive star from left to right). "
        "Verify that the page heading now displays the exact text 'Rating: 4'. "
        "Verify that exactly 4 stars are marked as filled (e.g. 4 elements have "
        "the 'filled' class or `data-filled=\"true\"`)."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_click_fourth_star",
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"


def test_click_second_star_decreases_rating(start_app):
    """Truth step 4: Clicking the 2nd star sets rating to 2 (decrease via binding)."""
    reason = (
        "After setting the rating to a higher value, clicking the second star must "
        "set the bound value down to 2, demonstrating the child can update the parent "
        "state through the bindable prop in both directions."
    )
    truth = (
        "Navigate to http://localhost:3000/. "
        "Click the 4th star element. Verify the heading reads 'Rating: 4'. "
        "Then click the 2nd star element (the second interactive star from the left). "
        "Verify that the page heading now displays the exact text 'Rating: 2'. "
        "Verify that exactly 2 stars are marked as filled."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_click_second_star",
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"


def test_reset_button_writes_through_binding(start_app):
    """Truth step 5: Reset button writes 0 back through bind:value from parent."""
    reason = (
        "The Reset button lives on the parent page and writes 0 back into the bound "
        "value. This proves the binding is two-way: changes from the parent flow into "
        "the child component and update the star display."
    )
    truth = (
        "Navigate to http://localhost:3000/. "
        "Click the 3rd star element to set a non-zero rating. "
        "Verify the heading reads 'Rating: 3'. "
        "Then click the button labelled 'Reset'. "
        "Verify that the heading reads 'Rating: 0' and that zero stars are marked "
        "as filled."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_reset_button",
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
