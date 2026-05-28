import { a as attr, b as escape_html, e as ensure_array_like } from "../../../chunks/root.js";
import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { data } = $$props;
    let initialQ = data.q;
    let q = initialQ;
    $$renderer2.push(`<h1>Products</h1> <form method="get" action="/products"><input type="text" name="q" data-testid="search-input"${attr(
      "value",
      // Skip navigating if the query is exactly what we started with in the URL
      q
    )} placeholder="Search products..."/> <button type="submit">Search</button></form> <p>Showing ${escape_html(data.products.length)} product(s)</p> <ul><!--[-->`);
    const each_array = ensure_array_like(data.products);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let product = each_array[$$index];
      $$renderer2.push(`<li data-testid="product-item">${escape_html(product.name)} - $${escape_html(product.price)}</li>`);
    }
    $$renderer2.push(`<!--]--></ul>`);
  });
}
export {
  _page as default
};
