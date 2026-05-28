import { Q as ensure_array_like, J as attr_class, G as attr, K as bind_props, V as escape_html } from "../../chunks/renderer.js";
import "clsx";
function StarRating($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { value = 0, max = 5 } = $$props;
    $$renderer2.push(`<div class="star-rating"><!--[-->`);
    const each_array = ensure_array_like(Array(max));
    for (let i = 0, $$length = each_array.length; i < $$length; i++) {
      each_array[i];
      $$renderer2.push(`<button${attr_class("star svelte-hwyvsy", void 0, { "filled": i < value })}${attr("data-filled", i < value ? "true" : "false")}>★</button>`);
    }
    $$renderer2.push(`<!--]--></div>`);
    bind_props($$props, { value });
  });
}
function _page($$renderer) {
  let rating = 0;
  let $$settled = true;
  let $$inner_renderer;
  function $$render_inner($$renderer2) {
    $$renderer2.push(`<h1>Rating: ${escape_html(rating)}</h1> `);
    StarRating($$renderer2, {
      get value() {
        return rating;
      },
      set value($$value) {
        rating = $$value;
        $$settled = false;
      }
    });
    $$renderer2.push(`<!----> <button>Reset</button>`);
  }
  do {
    $$settled = true;
    $$inner_renderer = $$renderer.copy();
    $$render_inner($$inner_renderer);
  } while (!$$settled);
  $$renderer.subsume($$inner_renderer);
}
export {
  _page as default
};
