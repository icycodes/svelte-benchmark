import * as universal from '../entries/pages/products/_page.js';

export const index = 3;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/products/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/products/+page.js";
export const imports = ["_app/immutable/nodes/3.DVy1w0g7.js","_app/immutable/chunks/yXMt-SqZ.js","_app/immutable/chunks/hUH6J2zQ.js","_app/immutable/chunks/BXFSO2fk.js","_app/immutable/chunks/CeZEYOPG.js","_app/immutable/chunks/BxXlE9cE.js"];
export const stylesheets = ["_app/immutable/assets/3.u6WYfMf2.css"];
export const fonts = [];
