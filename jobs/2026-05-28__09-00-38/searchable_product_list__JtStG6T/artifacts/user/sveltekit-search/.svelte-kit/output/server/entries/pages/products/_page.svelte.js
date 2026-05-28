import { a as attr, b as escape_html, e as ensure_array_like } from "../../../chunks/root.js";
import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { data } = $$props;
    let searchQuery = data.q;
    data.q;
    $$renderer2.push(`<h1>Products</h1> <form method="get" action="/products"><input type="text" name="q"${attr(
      "value",
      // Anticipate the change to avoid overwrite
      searchQuery
    )} placeholder="Search products..." data-testid="search-input"/> <button type="submit" class="sr-only svelte-1dj9mz1">Search</button></form> <p>Showing ${escape_html(data.products.length)} products</p> <ul><!--[-->`);
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
