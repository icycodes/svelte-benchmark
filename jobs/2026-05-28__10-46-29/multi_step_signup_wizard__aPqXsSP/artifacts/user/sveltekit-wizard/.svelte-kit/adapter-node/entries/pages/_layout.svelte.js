import { X as head } from "../../chunks/renderer.js";
function _layout($$renderer, $$props) {
  let { children } = $$props;
  head("12qhfyh", $$renderer, ($$renderer2) => {
    $$renderer2.title(($$renderer3) => {
      $$renderer3.push(`<title>Sign Up Wizard</title>`);
    });
    $$renderer2.push(`<meta charset="utf-8"/> <meta name="viewport" content="width=device-width, initial-scale=1"/>`);
  });
  $$renderer.push(`<main class="svelte-12qhfyh">`);
  children($$renderer);
  $$renderer.push(`<!----></main>`);
}
export {
  _layout as default
};
