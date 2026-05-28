import { e as escape_html } from "../../../../chunks/root.js";
import "clsx";
import "@sveltejs/kit/internal";
import "../../../../chunks/exports.js";
import "../../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { form } = $$props;
    $$renderer2.push(`<h1>Step 2: Password</h1> <form method="POST"><div><label for="password">Password:</label> <input type="password" id="password" name="password" required=""/></div> <div><label for="confirmPassword">Confirm Password:</label> <input type="password" id="confirmPassword" name="confirmPassword" required=""/></div> `);
    if (form?.message) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<p style="color: red;">${escape_html(form.message)}</p>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> <button type="submit">Next</button></form>`);
  });
}
export {
  _page as default
};
