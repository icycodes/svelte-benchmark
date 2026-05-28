import { e as escape_html, d as derived } from "../../../../chunks/root.js";
import { p as page } from "../../../../chunks/index2.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    const email = derived(() => page.url.searchParams.get("email"));
    $$renderer2.push(`<h1>Signup Complete!</h1> <p>Thank you for signing up, <strong>${escape_html(email())}</strong>.</p> <p>Your account has been successfully created.</p> <a href="/signup/step-1">Start over</a>`);
  });
}
export {
  _page as default
};
