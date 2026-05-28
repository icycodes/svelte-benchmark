import { O as escape_html, N as derived } from "../../../../chunks/renderer.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { data } = $$props;
    let displayEmail = derived(() => data.email || "your email address");
    $$renderer2.push(`<div class="success svelte-1va8uji"><div class="icon svelte-1va8uji">✓</div> <h1 class="svelte-1va8uji">Account created!</h1> <p class="svelte-1va8uji">Welcome aboard! We've registered your account for <strong>${escape_html(displayEmail())}</strong>.</p> <a href="/signup/step-1" class="svelte-1va8uji">Start over</a></div>`);
  });
}
export {
  _page as default
};
